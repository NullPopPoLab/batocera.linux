#!/usr/bin/env python
# -*- coding: utf-8 -*-

import batoceraFiles
import Command
import shutil
import os
from utils.logger import get_logger
from os import path
from os import environ
import configparser
from xml.dom import minidom
import codecs
import shutil
import utils.bezels as bezelsUtil
import subprocess
import csv
from xml.dom import minidom
from PIL import Image, ImageOps

eslog = get_logger(__name__)

def generatePadsConfig(cfgPath, playersControllers, sysName, altButtons, customCfg, specialController, decorations, useGuns, guns, useWheels, wheels, useMouse, multiMouse):
    # config file
    config = minidom.Document()
    configFile = cfgPath + "default.cfg"
    if os.path.exists(configFile):
        try:
            config = minidom.parse(configFile)
        except:
            pass # reinit the file
    if os.path.exists(configFile) and customCfg:
        overwriteMAME = False
    else:
        overwriteMAME = True
    
    # Load standard controls from csv
    controlFile = '/usr/share/batocera/configgen/data/mame/mameControls.csv'
    openFile = open(controlFile, 'r')
    controlDict = {}
    with openFile:
        controlList = csv.reader(openFile)
        for row in controlList:
            if not row[0] in controlDict.keys():
                controlDict[row[0]] = {}
            controlDict[row[0]][row[1]] = row[2]

    # Common controls
    mappings = {}
    for controlDef in controlDict['default'].keys():
        mappings[controlDef] = controlDict['default'][controlDef]

    # Only use gun buttons if lightguns are enabled to prevent conflicts with mouse
    gunmappings = {}
    if useGuns:
        for controlDef in controlDict['gunbuttons'].keys():
            gunmappings[controlDef] = controlDict['gunbuttons'][controlDef]

    # Only define mouse buttons if mouse is enabled, to prevent unwanted inputs
    # For a standard mouse, left, right, scroll wheel should be mapped to action buttons, and if side buttons are available, they will be coin & start
    mousemappings = {}
    if useMouse:
        for controlDef in controlDict['mousebuttons'].keys():
            mousemappings[controlDef] = controlDict['mousebuttons'][controlDef]

    # Buttons that change based on game/setting
    if altButtons in controlDict:
        for controlDef in controlDict[altButtons].keys():
            mappings.update({controlDef: controlDict[altButtons][controlDef]})

    xml_mameconfig = getRoot(config, "mameconfig")
    xml_mameconfig.setAttribute("version", "10") # otherwise, config of pad won't work at first run (batocera v33)
    xml_system     = getSection(config, xml_mameconfig, "system")
    xml_system.setAttribute("name", "default")

    removeSection(config, xml_system, "input")
    xml_input = config.createElement("input")
    xml_system.appendChild(xml_input)

    messControlDict = {}
    if sysName in [ "bbcb", "bbcm", "bbcm512", "bbcmc" ]:
        if specialController == 'none':
            useControls = "bbc"
        else:
            useControls = f"bbc-{specialController}"
    elif sysName in [ "apple2p", "apple2e", "apple2ee" ]:
        if specialController == 'none':
            useControls = "apple2"
        else:
            useControls = f"apple2-{specialController}"
    else:
        useControls = sysName
    eslog.debug(f"Using {useControls} for controller config.")
    
    # Fill in controls on cfg files
    nplayer = 1
    maxplayers = len(playersControllers)
    for playercontroller, pad in sorted(playersControllers.items()):
        mappings_use = mappings

    # in case there are more guns than pads, configure them
    if useGuns and len(guns) > len(playersControllers):
        for gunnum in range(len(playersControllers)+1, len(guns)+1):
            addCommonPlayerPorts(config, xml_input, gunnum)
            for mapping in gunmappings:
                xml_input.appendChild(generateGunPortElement(config, gunnum, mapping, gunmappings))

    # save the config file
    #mameXml = open(configFile, "w")
    # TODO: python 3 - workawround to encode files in utf-8
    if overwriteMAME:
        eslog.debug(f"Saving {configFile}")
        mameXml = codecs.open(configFile, "w", "utf-8")
        dom_string = os.linesep.join([s for s in config.toprettyxml().splitlines() if s.strip()]) # remove ugly empty lines while minicom adds them...
        mameXml.write(dom_string)

    # Write alt config (if used, custom config is turned off or file doesn't exist yet)
    if sysName in specialControlList and overwriteSystem:
        eslog.debug(f"Saving {configFile_alt}")
        mameXml_alt = codecs.open(configFile_alt, "w", "utf-8")
        dom_string_alt = os.linesep.join([s for s in config_alt.toprettyxml().splitlines() if s.strip()]) # remove ugly empty lines while minicom adds them...
        mameXml_alt.write(dom_string_alt)

def reverseMapping(key):
    if key == "joystick1down":
        return "joystick1up"
    if key == "joystick1right":
        return "joystick1left"
    if key == "joystick2down":
        return "joystick2up"
    if key == "joystick2right":
        return "joystick2left"
    return None

def generatePortElement(pad, config, nplayer, padindex, mapping, key, input, reversed, altButtons, gunmappings, isWheel, mousemappings, multiMouse):
    # Generic input
    xml_port = config.createElement("port")
    xml_port.setAttribute("type", "P{}_{}".format(nplayer, mapping))
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    keyval = input2definition(pad, key, input, padindex + 1, reversed, altButtons, False, isWheel)
    if mapping in gunmappings:
        keyval = keyval + " OR GUNCODE_{}_{}".format(nplayer, gunmappings[mapping])
    if mapping in mousemappings:
        if multiMouse:
            keyval = keyval + " OR MOUSECODE_{}_{}".format(nplayer, mousemappings[mapping])
        else:
            keyval = keyval + " OR MOUSECODE_1_{}".format(mousemappings[mapping])
    value = config.createTextNode(keyval)
    xml_newseq.appendChild(value)
    return xml_port

def generateGunPortElement(config, nplayer, mapping, gunmappings):
    # Generic input
    xml_port = config.createElement("port")
    if mapping in ["START", "COIN"]:
        xml_port.setAttribute("type", mapping+str(nplayer))
    else:
        xml_port.setAttribute("type", "P{}_{}".format(nplayer, mapping))
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    keyval = None
    if mapping in gunmappings:
        keyval = "GUNCODE_{}_{}".format(nplayer, gunmappings[mapping])
    if keyval is None:
        return None
    value = config.createTextNode(keyval)
    xml_newseq.appendChild(value)
    return xml_port

def generateSpecialPortElementPlayer(pad, config, tag, nplayer, padindex, mapping, key, input, reversed, mask, default, gunmappings, mousemappings, multiMouse):
    # Special button input (ie mouse button to gamepad)
    xml_port = config.createElement("port")
    xml_port.setAttribute("tag", tag)
    xml_port.setAttribute("type", mapping+str(nplayer))
    xml_port.setAttribute("mask", mask)
    xml_port.setAttribute("defvalue", default)
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    keyval = input2definition(pad, key, input, padindex + 1, reversed, 0)
    if mapping in gunmappings:
        keyval = keyval + " OR GUNCODE_{}_{}".format(nplayer, gunmappings[mapping])
    if mapping in mousemappings:
        if multiMouse:
            keyval = keyval + " OR MOUSECODE_{}_{}".format(nplayer, mousemappings[mapping])
        else:
            keyval = keyval + " OR MOUSECODE_1_{}".format(mousemappings[mapping])
    value = config.createTextNode(keyval)
    xml_newseq.appendChild(value)
    return xml_port

def generateSpecialPortElement(pad, config, tag, nplayer, padindex, mapping, key, input, reversed, mask, default):
    # Special button input (ie mouse button to gamepad)
    xml_port = config.createElement("port")
    xml_port.setAttribute("tag", tag)
    xml_port.setAttribute("type", mapping)
    xml_port.setAttribute("mask", mask)
    xml_port.setAttribute("defvalue", default)
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    value = config.createTextNode(input2definition(pad, key, input, padindex + 1, reversed, 0))
    xml_newseq.appendChild(value)
    return xml_port

def generateComboPortElement(pad, config, tag, padindex, mapping, kbkey, key, input, reversed, mask, default):
    # Maps a keycode + button - for important keyboard keys when available
    xml_port = config.createElement("port")
    xml_port.setAttribute("tag", tag)
    xml_port.setAttribute("type", mapping)
    xml_port.setAttribute("mask", mask)
    xml_port.setAttribute("defvalue", default)
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    value = config.createTextNode("KEYCODE_{} OR ".format(kbkey) + input2definition(pad, key, input, padindex + 1, reversed, 0))
    xml_newseq.appendChild(value)
    return xml_port

def generateUIElement(config, tag, padindex, mapping, kbkey, padkey, input, hotkey, hotside, reversed, dpadMode, mask, default):
    # Maps a keycode + button - for important keyboard keys when available
    xml_port = config.createElement("port")
    xml_port.setAttribute("tag", tag)
    xml_port.setAttribute("type", mapping)
    xml_port.setAttribute("mask", mask)
    xml_port.setAttribute("defvalue", default)
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)

    hk = ''
    if hotkey is not None:
        hk = ' '+input2definition('', hotkey, padindex + 1, False, dpadMode, 0)
        if not hotside: hk=' NOT'+hk
    a = []
    if kbkey is not None: a.append("KEYCODE_{}".format(kbkey))
    if input is not None: a.append(input2definition(padkey, input, padindex + 1, reversed, dpadMode, 0)+hk)
    value = config.createTextNode(' OR '.join(a))
    xml_newseq.appendChild(value)
    return xml_port

def generateAnalogPortElement(pad, config, tag, nplayer, padindex, mapping, inckey, deckey, mappedinput, mappedinput2, reversed, mask, default, delta, axis = ''):
    # Mapping analog to digital (mouse, etc)
    xml_port = config.createElement("port")
    xml_port.setAttribute("tag", tag)
    xml_port.setAttribute("type", mapping)
    xml_port.setAttribute("mask", mask)
    xml_port.setAttribute("defvalue", default)
    xml_port.setAttribute("keydelta", delta)
    xml_newseq_inc = config.createElement("newseq")
    xml_newseq_inc.setAttribute("type", "increment")
    xml_port.appendChild(xml_newseq_inc)
    incvalue = config.createTextNode(input2definition(pad, inckey, mappedinput, padindex + 1, reversed, 0, True))
    xml_newseq_inc.appendChild(incvalue)
    xml_newseq_dec = config.createElement("newseq")
    xml_port.appendChild(xml_newseq_dec)
    xml_newseq_dec.setAttribute("type", "decrement")
    decvalue = config.createTextNode(input2definition(pad, deckey, mappedinput2, padindex + 1, reversed, 0, True))
    xml_newseq_dec.appendChild(decvalue)
    xml_newseq_std = config.createElement("newseq")
    xml_port.appendChild(xml_newseq_std)
    xml_newseq_std.setAttribute("type", "standard")
    if axis == '':
        stdvalue = config.createTextNode("NONE")
    else:
        stdvalue = config.createTextNode("JOYCODE_{}_{}".format(padindex + 1, axis))
    xml_newseq_std.appendChild(stdvalue)
    return xml_port

def input2definition(pad, key, input, joycode, reversed, altButtons, ignoreAxis = False, isWheel = False):

    mameAxisMappingNames = {0: "XAXIS", 1: "YAXIS", 2: "ZAXIS", 3: "RXAXIS", 4: "RYAXIS", 5: "RZAXIS"}

    if isWheel:
        if key == "joystick1left" or key == "l2" or key == "r2":
            suffix = ""
            if key == "r2":
                suffix = "_NEG"
            if key == "l2":
                suffix = "_NEG"
            if int(input.id) in mameAxisMappingNames:
                idname = mameAxisMappingNames[int(input.id)]
                return f"JOYCODE_{joycode}_{idname}{suffix}"

    if input.type == "button":
        return f"JOYCODE_{joycode}_BUTTON{int(input.id)+1}"
    elif input.type == "hat":
        if input.value == "1":
            return f"JOYCODE_{joycode}_HAT1UP"
        elif input.value == "2":
            return f"JOYCODE_{joycode}_HAT1RIGHT"
        elif input.value == "4":
            return f"JOYCODE_{joycode}_HAT1DOWN"
        elif input.value == "8":
            return f"JOYCODE_{joycode}_HAT1LEFT"
    elif input.type == "axis":
        # Determine alternate button for D-Pad and right stick as buttons
        dpadInputs = {}
        for direction in ['up', 'down', 'left', 'right']:
            if pad.inputs[direction].type == 'button':
                dpadInputs[direction] = f'JOYCODE_{joycode}_BUTTON{int(pad.inputs[direction].id)+1}'
            elif pad.inputs[direction].type == 'hat':
                if pad.inputs[direction].value == "1":
                    dpadInputs[direction] = f'JOYCODE_{joycode}_HAT1UP'
                if pad.inputs[direction].value == "2":
                    dpadInputs[direction] = f'JOYCODE_{joycode}_HAT1RIGHT'
                if pad.inputs[direction].value == "4":
                    dpadInputs[direction] = f'JOYCODE_{joycode}_HAT1DOWN'
                if pad.inputs[direction].value == "8":
                    dpadInputs[direction] = f'JOYCODE_{joycode}_HAT1LEFT'
            else:
                dpadInputs[direction] = ''
        buttonDirections = {}
        # workarounds for issue #6892
        # Modified because right stick to buttons was not working after the workaround
        # Creates a blank, only modifies if the button exists in the pad.
        # Button assigment modified - blank "OR" gets removed by MAME if the button is undefined.
        for direction in ['a', 'b', 'x', 'y']:
            buttonDirections[direction] = ''
            if direction in pad.inputs.keys():
                if pad.inputs[direction].type == 'button':
                    buttonDirections[direction] = f'JOYCODE_{joycode}_BUTTON{int(pad.inputs[direction].id)+1}'

        if ignoreAxis and dpadInputs['up'] != '' and dpadInputs['down'] != '' \
            and dpadInputs['left'] != '' and dpadInputs['right'] != '':
            if key == "joystick1up" or key == "up":
                return dpadInputs['up']
            if key == "joystick1down" or key == "down":
                return dpadInputs['down']
            if key == "joystick1left" or key == "left":
                return dpadInputs['left']
            if key == "joystick1right" or key == "right":
                return dpadInputs['right']
        if altButtons == "qbert": # Q*Bert Joystick
            if key == "joystick1up" or key == "up":
                return f"JOYCODE_{joycode}_YAXIS_UP_SWITCH JOYCODE_{joycode}_XAXIS_RIGHT_SWITCH OR {dpadInputs['up']} {dpadInputs['right']}"
            if key == "joystick1down" or key == "down":
                return f"JOYCODE_{joycode}_YAXIS_DOWN_SWITCH JOYCODE_{joycode}_XAXIS_LEFT_SWITCH OR {dpadInputs['down']} {dpadInputs['left']}"
            if key == "joystick1left" or key == "left":
                return f"JOYCODE_{joycode}_XAXIS_LEFT_SWITCH JOYCODE_{joycode}_YAXIS_UP_SWITCH OR {dpadInputs['left']} {dpadInputs['up']}"
            if key == "joystick1right" or key == "right":
                return f"JOYCODE_{joycode}_XAXIS_RIGHT_SWITCH JOYCODE_{joycode}_YAXIS_DOWN_SWITCH OR {dpadInputs['right']} {dpadInputs['down']}"
        else:
            if key == "joystick1up" or key == "up":
                return f"JOYCODE_{joycode}_YAXIS_UP_SWITCH OR {dpadInputs['up']}"
            if key == "joystick1down" or key == "down":
                return f"JOYCODE_{joycode}_YAXIS_DOWN_SWITCH OR {dpadInputs['down']}"
            if key == "joystick1left" or key == "left":
                return f"JOYCODE_{joycode}_XAXIS_LEFT_SWITCH OR {dpadInputs['left']}"
            if key == "joystick1right" or key == "right":
                return f"JOYCODE_{joycode}_XAXIS_RIGHT_SWITCH OR {dpadInputs['right']}"
        # Fix for the workaround
        for direction in pad.inputs:
            if(key == "joystick2up"):
                return f"JOYCODE_{joycode}_RYAXIS_NEG_SWITCH OR {buttonDirections['x']}"
            if(key == "joystick2down"):
                return f"JOYCODE_{joycode}_RYAXIS_POS_SWITCH OR {buttonDirections['b']}"
            if(key == "joystick2left"):
                return f"JOYCODE_{joycode}_RXAXIS_NEG_SWITCH OR {buttonDirections['y']}"
            if(key == "joystick2right"):
                return f"JOYCODE_{joycode}_RXAXIS_POS_SWITCH OR {buttonDirections['a']}"
            if int(input.id) in mameAxisMappingNames:
                idname = mameAxisMappingNames[int(input.id)]
                return f"JOYCODE_{joycode}_{idname}_POS_SWITCH"

    return "unknown"

def hasStick(pad):
    if "joystick1up" in pad.inputs:
        return True
    else:
        return False

def getRoot(config, name):
    xml_section = config.getElementsByTagName(name)

    if len(xml_section) == 0:
        xml_section = config.createElement(name)
        config.appendChild(xml_section)
    else:
        xml_section = xml_section[0]

    return xml_section

def getSection(config, xml_root, name):
    xml_section = xml_root.getElementsByTagName(name)

    if len(xml_section) == 0:
        xml_section = config.createElement(name)
        xml_root.appendChild(xml_section)
    else:
        xml_section = xml_section[0]

    return xml_section

def removeSection(config, xml_root, name):
    xml_section = xml_root.getElementsByTagName(name)

    for i in range(0, len(xml_section)):
        old = xml_root.removeChild(xml_section[i])
        old.unlink()

def addCommonPlayerPorts(config, xml_input, nplayer):
    # adstick for guns
    for axis in ["X", "Y"]:
        nanalog = 1 if axis == "X" else 2
        xml_port = config.createElement("port")
        xml_port.setAttribute("tag", ":mainpcb:ANALOG{}".format(nanalog))
        xml_port.setAttribute("type", "P{}_AD_STICK_{}".format(nplayer, axis))
        xml_port.setAttribute("mask", "255")
        xml_port.setAttribute("defvalue", "128")
        xml_newseq = config.createElement("newseq")
        xml_newseq.setAttribute("type", "standard")
        xml_port.appendChild(xml_newseq)
        value = config.createTextNode("GUNCODE_{}_{}AXIS".format(nplayer, axis))
        xml_newseq.appendChild(value)
        xml_input.appendChild(xml_port)
