#!/usr/bin/env python
from PIL import Image, ImageOps
from pathlib import Path
from settings.unixSettings import UnixSettings
from utils.logger import get_logger
from xml.dom import minidom
import Command
import batoceraFiles
import codecs
import configparser
import csv
import os
import shutil
import subprocess
import sys
import zipfile

# Define RetroPad inputs for mapping
retroPad = {
    "joystick1up":      "YAXIS_UP_SWITCH",
    "joystick1down":    "YAXIS_DOWN_SWITCH",
    "joystick1left":    "XAXIS_LEFT_SWITCH",
    "joystick1right":   "XAXIS_RIGHT_SWITCH",
    "up":               "HAT{0}UP",
    "down":             "HAT{0}DOWN",
    "left":             "HAT{0}LEFT",
    "right":            "HAT{0}RIGHT",
    "joystick2up":      "RYAXIS_NEG_SWITCH",
    "joystick2down":    "RYAXIS_POS_SWITCH",
    "joystick2left":    "RXAXIS_NEG_SWITCH",
    "joystick2right":   "RXAXIS_POS_SWITCH",
    "c":                "BUTTON1",
    "b":                "BUTTON2",
    "a":                "BUTTON3",
    "z":                "BUTTON4",
    "y":                "BUTTON5",
    "x":                "BUTTON6",
    "pageup":           "BUTTON7",
    "pagedown":         "BUTTON8",
    "l2":               "BUTTON9",
    "r2":               "BUTTON10",
    "l3":               "CLEAR",
    "r3":               "CANCEL",
    "select":           "COIN",
    "start":            "START",
    "menu":             "MENU",
    "opt":              "HOTKEY"
}

def generateMAMEConfigs(playersControllers, system, rom):
    # Generate command line for MAME/MESS/MAMEVirtual
    commandLine = []
    romBasename = os.path.basename(rom)
    romDirname  = os.path.dirname(rom)
    romDrivername = os.path.splitext(romBasename)[0]
    specialController = 'none'

    if system.config['core'] in [ 'mame', 'mess', 'mamevirtual' ]:
        corePath = 'lr-' + system.config['core']
    else:
        corePath = system.config['core']

    if system.name in [ 'mame', 'neogeo', 'lcdgames', 'plugnplay', 'vis' ]:
        # Set up command line for basic systems
        # ie. no media, softlists, etc.
        if system.getOptBoolean("customcfg"):
            cfgPath = "/userdata/system/configs/{}/custom/".format(corePath)
        else:
            cfgPath = "/userdata/saves/mame/lr-mame/cfg/"
        if not os.path.exists(cfgPath):
            os.makedirs(cfgPath)
        if system.name == 'vis':
            commandLine += [ 'vis', '-cdrom', f'"{rom}"' ]
        else:
            commandLine += [ romDrivername ]
        commandLine += [ '-cfg_directory', cfgPath ]
        commandLine += [ '-rompath', romDirname + ';/userdata/bios/' ]
        pluginsToLoad = []
        if not (system.isOptSet("hiscoreplugin") and system.getOptBoolean("hiscoreplugin") == False):
            pluginsToLoad += [ "hiscore" ]
        if system.isOptSet("coindropplugin") and system.getOptBoolean("coindropplugin"):
            pluginsToLoad += [ "coindrop" ]
        if len(pluginsToLoad) > 0:
            commandLine += [ "-plugins", "-plugin", ",".join(pluginsToLoad) ]
        messMode = -1
        messModel = ''
    else:
        # Set up command line for MESS or MAMEVirtual
        softDir = "/var/run/mame_software/"
        subdirSoftList = [ "mac_hdd", "bbc_hdd", "cdi", "archimedes_hdd", "fmtowns_cd" ]
        if system.isOptSet("softList") and system.config["softList"] != "none":
            softList = system.config["softList"]
        else:
            softList = ""

        # Auto softlist for FM Towns if there is a zip that matches the folder name
        # Used for games that require a CD and floppy to both be inserted
        if system.name == 'fmtowns' and softList == '':
            romParentPath = os.path.basename(romDirname)
            if os.path.exists('/userdata/roms/fmtowns/{}.zip'.format(romParentPath)):
                softList = 'fmtowns_cd'

        # Determine MESS system name (if needed)
        messDataFile = '/usr/share/batocera/configgen/data/mame/messSystems.csv'
        openFile = open(messDataFile, 'r')
        messSystems = []
        messSysName = []
        messRomType = []
        messAutoRun = []
        with openFile:
            messDataList = csv.reader(openFile, delimiter=';', quotechar="'")
            for row in messDataList:
                messSystems.append(row[0])
                messSysName.append(row[1])
                messRomType.append(row[2])
                messAutoRun.append(row[3])
        messMode = messSystems.index(system.name)

        # Alternate system for machines that have different configs (ie computers with different hardware)
        messModel = messSysName[messMode]
        if system.isOptSet("altmodel"):
            messModel = system.config["altmodel"]
        commandLine += [ messModel ]

        if messSysName[messMode] == "":
            # Command line for non-arcade, non-system ROMs (lcdgames, plugnplay)
            if system.getOptBoolean("customcfg"):
                cfgPath = "/userdata/system/configs/{}/custom/".format(corePath)
            else:
                cfgPath = "/userdata/saves/mame/lr-mame/cfg/"
            if not os.path.exists(cfgPath):
                os.makedirs(cfgPath)
            commandLine += [ romDrivername ]
            commandLine += [ '-cfg_directory', cfgPath ]
            commandLine += [ '-rompath', romDirname + ";/userdata/bios/" ]
        else:
            # Command line for MESS consoles/computers
            # TI-99 32k RAM expansion & speech modules
            # Don't enable 32k by default
            if system.name == "ti99":
                commandLine += [ "-ioport", "peb" ]
                if system.isOptSet("ti99_32kram") and system.getOptBoolean("ti99_32kram"):
                    commandLine += ["-ioport:peb:slot2", "32kmem"]
                if not system.isOptSet("ti99_speech") or (system.isOptSet("ti99_speech") and system.getOptBoolean("ti99_speech")):
                    commandLine += ["-ioport:peb:slot3", "speech"]

            #Laser 310 Memory Expansion & joystick
            if system.name == "laser310":
                commandLine += ['-io', 'joystick']
                if not system.isOptSet('memslot'):
                    laser310mem = 'laser_64k'
                else:
                    laser310mem = system.config['memslot']
                commandLine += ["-mem", laser310mem]

            # BBC Joystick
            if system.name == "bbc":
                if system.isOptSet('sticktype') and system.config['sticktype'] != 'none':
                    commandLine += ["-analogue", system.config['sticktype']]
                    specialController = system.config['sticktype']

            # Apple II
            if system.name == "apple2":
                commandLine += ["-sl7", "cffa202"]
                if system.isOptSet('gameio') and system.config['gameio'] != 'none':
                    if system.config['gameio'] == 'joyport' and messModel != 'apple2p':
                        eslog.debug("Joyport is only compatible with Apple II +")
                    else:
                        commandLine += ["-gameio", system.config['gameio']]
                        specialController = system.config['gameio']

            # RAM size (Mac excluded, special handling below)
            if system.name != "macintosh" and system.isOptSet("ramsize"):
                commandLine += [ '-ramsize', str(system.config["ramsize"]) + 'M' ]

            # Mac RAM & Image Reader (if applicable)
            if system.name == "macintosh":
                if system.isOptSet("ramsize"):
                    ramSize = int(system.config["ramsize"])
                    if messModel in [ 'maciix', 'maclc3' ]:
                        if messModel == 'maclc3' and ramSize == 2:
                            ramSize = 4
                        if messModel == 'maclc3' and ramSize > 80:
                            ramSize = 80
                        if messModel == 'maciix' and ramSize == 16:
                            ramSize = 32
                        if messModel == 'maciix' and ramSize == 48:
                            ramSize = 64
                        commandLine += [ '-ramsize', str(ramSize) + 'M' ]
                    if messModel == 'maciix':
                        imageSlot = 'nba'
                        if system.isOptSet('imagereader'):
                            if system.config["imagereader"] == "disabled":
                                imageSlot = ''
                            else:
                                imageSlot = system.config["imagereader"]
                        if imageSlot != "":
                            commandLine += [ "-" + imageSlot, 'image' ]

            if softList != "":
                # Software list ROM commands
                prepSoftwareList(subdirSoftList, softList, softDir, "/userdata/bios/mame/hash", romDirname)
                if softList in subdirSoftList:
                    commandLine += [ os.path.basename(romDirname) ]
                else:
                    commandLine += [ romDrivername ]
                commandLine += [ "-rompath", softDir + ";/userdata/bios/" ]
                commandLine += [ "-swpath", softDir ]
                commandLine += [ "-verbose" ]
            else:
                # Alternate ROM type for systems with mutiple media (ie cassette & floppy)
                # Mac will auto change floppy 1 to 2 if a boot disk is enabled
                if system.name != "macintosh":
                    if system.isOptSet("altromtype"):
                        if system.config["altromtype"] == "flop1" and messModel == "fmtmarty":
                            commandLine += [ "-flop" ]
                        else:
                            commandLine += [ "-" + system.config["altromtype"] ]
                    elif system.name == "adam":
                        # add some logic based on the extension
                        rom_extension = os.path.splitext(rom)[1].lower()
                        if rom_extension == ".ddp":
                            commandLine += [ "-cass1" ]
                        elif rom_extension == ".dsk":
                            commandLine += [ "-flop1" ]
                        else:
                            commandLine += [ "-cart1" ]
                    # try to choose the right floppy for Apple2gs
                    elif system.name == "apple2gs":
                        rom_extension = os.path.splitext(rom)[1].lower()
                        if rom_extension == ".zip":
                            with zipfile.ZipFile(rom, 'r') as zip_file:
                                file_list = zip_file.namelist()
                                # assume only one file in zip
                                if len(file_list) == 1:
                                    filename = file_list[0]
                                    rom_extension = os.path.splitext(filename)[1].lower()
                        if rom_extension in [".2mg", ".2img", ".img", ".image"]:
                            commandLine += [ "-flop3" ]
                        else:
                            commandLine += [ "-flop1" ]
                    else:
                        commandLine += [ "-" + messRomType[messMode] ]
                else:
                    if system.isOptSet("bootdisk"):
                        if ((system.isOptSet("altromtype") and system.config["altromtype"] == "flop1") or not system.isOptSet("altromtype")) and system.config["bootdisk"] in [ "macos30", "macos608", "macos701", "macos75" ]:
                            commandLine += [ "-flop2" ]
                        elif system.isOptSet("altromtype"):
                            commandLine += [ "-" + system.config["altromtype"] ]
                        else:
                            commandLine += [ "-" + messRomType[messMode] ]
                    else:
                        if system.isOptSet("altromtype"):
                            commandLine += [ "-" + system.config["altromtype"] ]
                        else:
                            commandLine += [ "-" + messRomType[messMode] ]
                # Use the full filename for MESS non-softlist ROMs
                commandLine += [ f'"{rom}"' ]
                commandLine += [ "-rompath", romDirname + ";/userdata/bios/" ]

                # Boot disk for Macintosh
                # Will use Floppy 1 or Hard Drive, depending on the disk.
                if system.name == "macintosh" and system.isOptSet("bootdisk"):
                    if system.config["bootdisk"] in [ "macos30", "macos608", "macos701", "macos75" ]:
                        bootType = "-flop1"
                        bootDisk = '"/userdata/bios/' + system.config["bootdisk"] + '.img"'
                    else:
                        bootType = "-hard"
                        bootDisk = '"/userdata/bios/' + system.config["bootdisk"] + '.chd"'
                    commandLine += [ bootType, bootDisk ]

                # Create & add a blank disk if needed, insert into drive 2
                # or drive 1 if drive 2 is selected manually or FM Towns Marty.
                if system.isOptSet('addblankdisk') and system.getOptBoolean('addblankdisk'):
                    if system.name == 'fmtowns':
                        blankDisk = '/usr/share/mame/blank.fmtowns'
                        targetFolder = '/userdata/saves/mame/{}'.format(system.name)
                        targetDisk = '{}/{}.fmtowns'.format(targetFolder, os.path.splitext(romBasename)[0])
                    # Add elif statements here for other systems if enabled
                    if not os.path.exists(targetFolder):
                        os.makedirs(targetFolder)
                    if not os.path.exists(targetDisk):
                        shutil.copy2(blankDisk, targetDisk)
                    # Add other single floppy systems to this if statement
                    if messModel == "fmtmarty":
                        commandLine += [ '-flop', targetDisk ]
                    elif (system.isOptSet('altromtype') and system.config['altromtype'] == 'flop2'):
                        commandLine += [ '-flop1', targetDisk ]
                    else:
                        commandLine += [ '-flop2', targetDisk ]

            # UI enable - for computer systems, the default sends all keys to the emulated system.
            # This will enable hotkeys, but some keys may pass through to MAME and not be usable in the emulated system.
            if not (system.isOptSet("enableui") and not system.getOptBoolean("enableui")):
                commandLine += [ "-ui_active" ]

            # MESS config folder
            if system.getOptBoolean("customcfg"):
                cfgPath = "/userdata/system/configs/{}/{}/custom/".format(corePath, messSysName[messMode])
            else:
                cfgPath = "/userdata/saves/mame/lr-mame/cfg/{}/".format(messSysName[messMode])
            if system.getOptBoolean("pergamecfg"):
                cfgPath = "/userdata/system/configs/{}/{}/{}/".format(corePath, messSysName[messMode], romBasename)
            if not os.path.exists(cfgPath):
                os.makedirs(cfgPath)
            commandLine += [ '-cfg_directory', cfgPath ]

            # Autostart via ini file
            # Init variables, delete old ini if it exists, prepare ini path
            # lr-mame does NOT support multiple ini paths
            # Using computer.ini since autorun only applies to computers, and this would be unlikely to be used otherwise
            autoRunCmd = ""
            autoRunDelay = 0
            if not os.path.exists('/userdata/saves/mame/lr-mame/ini/'):
                     os.makedirs('/userdata/saves/mame/lr-mame/ini/')
            if os.path.exists('/userdata/saves/mame/lr-mame/ini/computer.ini'):
                os.remove('/userdata/saves/mame/lr-mame/ini/computer.ini')
            # bbc has different boots for floppy & cassette, no special boot for carts
            if system.name == "bbc":
                if system.isOptSet("altromtype") or softList != "":
                    if (system.isOptSet("altromtype") and system.config["altromtype"] == "cass") or softList[-4:] == "cass":
                        autoRunCmd = '*tape\\nchain""\\n'
                        autoRunDelay = 2
                    elif (system.isOptSet("altromtype") and left(system.config["altromtype"], 4) == "flop") or softList[-4:] == "flop":
                        autoRunCmd = '*cat\\n\\n\\n\\n*exec !boot\\n'
                        autoRunDelay = 3
                else:
                    autoRunCmd = '*cat\\n\\n\\n\\n*exec !boot\\n'
                    autoRunDelay = 3
            # fm7 boots floppies, needs cassette loading
            elif system.name == "fm7":
                if system.isOptSet("altromtype") or softList != "":
                    if (system.isOptSet("altromtype") and system.config["altromtype"] == "cass") or softList[-4:] == "cass":
                        autoRunCmd = 'LOADM”“,,R\\n'
                        autoRunDelay = 5
            else:
                # Check for an override file, otherwise use generic (if it exists)
                autoRunCmd = messAutoRun[messMode]
                autoRunFile = '/usr/share/batocera/configgen/data/mame/' + softList + '_autoload.csv'
                if os.path.exists(autoRunFile):
                    openARFile = open(autoRunFile, 'r')
                    with openARFile:
                        autoRunList = csv.reader(openARFile, delimiter=';', quotechar="'")
                        for row in autoRunList:
                            if row[0].casefold() == os.path.splitext(romBasename)[0].casefold():
                                autoRunCmd = row[1] + "\\n"
                                autoRunDelay = 3
            commandLine += [ '-inipath', '/userdata/saves/mame/lr-mame/ini/' ]
            if autoRunCmd != "":
                if autoRunCmd.startswith("'"):
                    autoRunCmd.replace("'", "")
                iniFile = open('/userdata/saves/mame/lr-mame/ini/computer.ini', "w")
                iniFile.write('autoboot_command          ' + autoRunCmd + "\n")
                iniFile.write('autoboot_delay            ' + str(autoRunDelay))
                iniFile.close()
            # Create & add a blank disk if needed, insert into drive 2
            # or drive 1 if drive 2 is selected manually.
            if system.isOptSet('addblankdisk') and system.getOptBoolean('addblankdisk'):
                if not os.path.exists('/userdata/saves/lr-mess/{}/{}.dsk'.format(system.name, os.path.splitext(romBasename)[0])):
                    os.makedirs('/userdata/saves/lr-mess/{}/'.format(system.name))
                    shutil.copy2('/usr/share/mame/blank.dsk', '/userdata/saves/lr-mess/{}/{}.dsk'.format(system.name, os.path.splitext(romBasename)[0]))
                if system.isOptSet('altromtype') and system.config['altromtype'] == 'flop2':
                    commandLine += [ '-flop1', '/userdata/saves/lr-mess/{}/{}.dsk'.format(system.name, os.path.splitext(romBasename)[0]) ]
                else:
                    commandLine += [ '-flop2', '/userdata/saves/lr-mess/{}/{}.dsk'.format(system.name, os.path.splitext(romBasename)[0]) ]

    # Lightgun reload option
    if system.isOptSet('offscreenreload') and system.getOptBoolean('offscreenreload'):
        commandArray += [ "-offscreen_reload" ]

    # Art paths - lr-mame displays artwork in the game area and not in the bezel area, so using regular MAME artwork + shaders is not recommended.
    # By default, will ignore standalone MAME's art paths.
    if system.config['core'] != 'same_cdi':
        if not (system.isOptSet("sharemameart") and not system.getOptBoolean('sharemameart')):
            artPath = "/var/run/mame_artwork/;/usr/bin/mame/artwork/;/userdata/bios/lr-mame/artwork/;/userdata/bios/mame/artwork/;/userdata/decorations/"
        else:
            artPath = "/var/run/mame_artwork/;/usr/bin/mame/artwork/;/userdata/bios/lr-mame/artwork/"
        if not system.name == "ti99":
            commandLine += [ '-artpath', artPath ]

    # Artwork crop - default to On for lr-mame
    # Exceptions for PDP-1 (status lights) and VGM Player (indicators)
    if not system.isOptSet("artworkcrop"):
        if not system.name in [ 'pdp1', 'vgmplay', 'ti99' ]:
            commandLine += [ "-artwork_crop" ]
    else:
        if system.getOptBoolean("artworkcrop"):
            commandLine += [ "-artwork_crop" ]

    # Share plugins & samples with standalone MAME (except TI99)
    if not system.name == "ti99":
        commandLine += [ "-pluginspath", "/usr/bin/mame/plugins/;/userdata/saves/mame/plugins" ]
        commandLine += [ "-homepath" , "/userdata/saves/mame/plugins/" ]
        commandLine += [ "-samplepath", "/userdata/bios/mame/samples/" ]
    if not os.path.exists("/userdata/saves/mame/plugins/"):
        os.makedirs("/userdata/saves/mame/plugins/")
    if not os.path.exists("/userdata/bios/mame/samples/"):
        os.makedirs("/userdata/bios/mame/samples/")

    # Delete old cmd files & prepare path
    cmdPath = "/var/run/cmdfiles/"
    if not os.path.exists(cmdPath):
        os.makedirs(cmdPath)
    cmdFileList = os.listdir(cmdPath)
    for file in cmdFileList:
        if file.endswith(".cmd"):
            os.remove(os.path.join(cmdPath, file))

    # Write command line file
    cmdFilename = "{}{}.cmd".format(cmdPath, romDrivername)
    cmdFile = open(cmdFilename, "w")
    cmdFile.write(' '.join(commandLine))
    cmdFile.close()

    # Call Controller Config
    if messMode == -1:
        generateMAMEPadConfig(cfgPath, playersControllers, system, "", romBasename, specialController)
    else:
        generateMAMEPadConfig(cfgPath, playersControllers, system, messModel, romBasename, specialController)

def prepSoftwareList(subdirSoftList, softList, softDir, hashDir, romDirname):
    if not os.path.exists(softDir):
        os.makedirs(softDir)
    # Check for/remove existing symlinks, remove hashfile folder
    for fileName in os.listdir(softDir):
        checkFile = os.path.join(softDir, fileName)
        if os.path.islink(checkFile):
            os.unlink(checkFile)
        if os.path.isdir(checkFile):
            shutil.rmtree(checkFile)
    # Prepare hashfile path
    if not os.path.exists(hashDir):
        os.makedirs(hashDir)
    # Remove existing xml files
    hashFiles = os.listdir(hashDir)
    for file in hashFiles:
        if file.endswith(".xml"):
            os.remove(os.path.join(hashDir, file))
    # Copy hashfile
    shutil.copy2("/usr/share/lr-mame/hash/" + softList + ".xml", hashDir + "/" + softList + ".xml")
    # Link ROM's parent folder if needed, ROM's folder otherwise
    if softList in subdirSoftList:
        romPath = Path(romDirname)
        os.symlink(str(romPath.parents[0]), softDir + softList, True)
    else:
        os.symlink(romDirname, softDir + softList, True)

def getMameControlScheme(system, romBasename):
    # Game list files
    mameCapcom = '/usr/share/batocera/configgen/data/mame/mameCapcom.txt'
    mameKInstinct = '/usr/share/batocera/configgen/data/mame/mameKInstinct.txt'
    mameMKombat = '/usr/share/batocera/configgen/data/mame/mameMKombat.txt'
    mameNeogeo = '/usr/share/batocera/configgen/data/mame/mameNeogeo.txt'
    mameTwinstick = '/usr/share/batocera/configgen/data/mame/mameTwinstick.txt'
    mameRotatedstick = '/usr/share/batocera/configgen/data/mame/mameRotatedstick.txt'

    # Controls for games with 5-6 buttons or other unusual controls
    if system.isOptSet("altlayout"):
        controllerType = system.config["altlayout"] # Option was manually selected
    else:
        controllerType = "auto"

    return "default"

def generateMAMEPadConfig(cfgPath, playersControllers, system, messSysName, romBasename, specialController):
    # config file
    config = minidom.Document()
    configFile = cfgPath + "default.cfg"
    if os.path.exists(configFile):
        try:
            config = minidom.parse(configFile)
        except:
            pass # reinit the file

    if system.isOptSet('customcfg'):
        customCfg = system.getOptBoolean('customcfg')
    else:
        customCfg = False
    # Don't overwrite if using custom configs
    if os.path.exists(configFile) and customCfg:
        overwriteMAME = False
    else:
        overwriteMAME = True

    # Get controller scheme
    altButtons = getMameControlScheme(system, romBasename)
    
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

    # Buttons that change based on game/setting
    if altButtons in controlDict:
        for controlDef in controlDict[altButtons].keys():
            mappings.update({controlDef: controlDict[altButtons][controlDef]})

    xml_mameconfig = getRoot(config, "mameconfig")
    xml_mameconfig.setAttribute("version", "10") # otherwise, config of pad won't work at first run (batocera v33)
    xml_system = getSection(config, xml_mameconfig, "system")
    xml_system.setAttribute("name", "default")

    removeSection(config, xml_system, "input")
    xml_input = config.createElement("input")
    xml_system.appendChild(xml_input)

    messControlDict = {}
    if messSysName in [ "bbcb", "bbcm", "bbcm512", "bbcmc" ]:
        if specialController == 'none':
            useControls = "bbc"
        else:
            useControls = f"bbc-{specialController}"
    elif messSysName in [ "apple2p", "apple2e", "apple2ee" ]:
        if specialController == 'none':
            useControls = "apple2"
        else:
            useControls = f"apple2-{specialController}"
    else:
        useControls = messSysName
    
    # Fill in controls on cfg files
    nplayer = 1
    maxplayers = len(playersControllers)
    for playercontroller, pad in sorted(playersControllers.items()):
        mappings_use = mappings

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

def generatePortElement(pad, config, nplayer, padindex, mapping, key, input, reversed, altButtons):
    # Generic input
    xml_port = config.createElement("port")
    xml_port.setAttribute("type", f"P{nplayer}_{mapping}")
    xml_newseq = config.createElement("newseq")
    xml_newseq.setAttribute("type", "standard")
    xml_port.appendChild(xml_newseq)
    value = config.createTextNode(input2definition(pad, key, input, padindex + 1, reversed, altButtons))
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
    value = config.createTextNode(f"KEYCODE_{kbkey} OR " + input2definition(pad, key, input, padindex + 1, reversed, 0))
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

def input2definition(pad, key, input, joycode, reversed, altButtons, ignoreAxis = False):
    if input.find("BUTTON") != -1 or input.find("HAT") != -1 or input == "START" or input == "SELECT":
        input = input.format(joycode) if "{0}" in input else input
        return f"JOYCODE_{joycode}_{input}"
    elif input.find("AXIS") != -1:
        if altButtons == "qbert": # Q*Bert Joystick
            if key == "joystick1up" or key == "up":
                return f"JOYCODE_{joycode}_{retroPad['joystick1up']}_{joycode}_{retroPad['joystick1right']} OR \
                    JOYCODE_{joycode}_{retroPad['up'].format(joycode)} JOYCODE_{joycode}_{retroPad['right'].format(joycode)}"
            elif key == "joystick1down" or key == "down":
                return f"JOYCODE_{joycode}_{retroPad['joystick1down']} JOYCODE_{joycode}_{retroPad['joystick1left']} OR \
                    JOYCODE_{joycode}_{retroPad['down'].format(joycode)} JOYCODE_{joycode}_{retroPad['left'].format(joycode)}"
            elif key == "joystick1left" or key == "left":
                return f"JOYCODE_{joycode}_{retroPad['joystick1left']} JOYCODE_{joycode}_{retroPad['joystick1up']} OR \
                    JOYCODE_{joycode}_{retroPad['left'].format(joycode)} JOYCODE_{joycode}_{retroPad['up'].format(joycode)}"
            elif key == "joystick1right" or key == "right":
                return f"JOYCODE_{joycode}_{retroPad['joystick1right']} JOYCODE_{joycode}_{retroPad['joystick1down']} OR \
                    JOYCODE_{joycode}_{retroPad['right'].format(joycode)} JOYCODE_{joycode}_{retroPad['down'].format(joycode)}"
            else:
                return f"JOYCODE_{joycode}_{input}"
        elif ignoreAxis:
            if key == "joystick1up" or key == "up":
                return f"JOYCODE_{joycode}_{retroPad['up'].format(joycode)}"
            elif key == "joystick1down" or key == "down":
                return f"JOYCODE_{joycode}_{retroPad['down'].format(joycode)}"
            elif key == "joystick1left" or key == "left":
                return f"JOYCODE_{joycode}_{retroPad['left'].format(joycode)}"
            elif key == "joystick1right" or key == "right":
                return f"JOYCODE_{joycode}_{retroPad['right'].format(joycode)}"
        else:
            if key == "joystick1up" or key == "up":
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['up'].format(joycode)}"
            elif key == "joystick1down" or key == "down":
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['down'].format(joycode)}"
            elif key == "joystick1left" or key == "left":
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['left'].format(joycode)}"
            elif key == "joystick1right" or key == "right":
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['right'].format(joycode)}"
            elif(key == "joystick2up"):
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['x']}"
            elif(key == "joystick2down"):
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['b']}"
            elif(key == "joystick2left"):
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['y']}"
            elif(key == "joystick2right"):
                return f"JOYCODE_{joycode}_{retroPad[key]} OR JOYCODE_{joycode}_{retroPad['a']}"
            else:
                return f"JOYCODE_{joycode}_{input}"
    else:
        return "unknown"

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
