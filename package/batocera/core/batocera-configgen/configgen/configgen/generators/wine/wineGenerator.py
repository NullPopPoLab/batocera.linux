#!/usr/bin/env python

from generators.Generator import Generator
import Command
import os
from os import path
import controllersConfig

class WineGenerator(Generator):

    def generate(self, system, rom, playersControllers, guns, gameResolution):
        cmd=None
        if system.name == "windows_installers":
            commandArray = ["batocera-wine", "windows", "install", rom]
            cmd=Command.Command(array=commandArray)
        elif system.name == "windows":
            commandArray = ["batocera-wine", "windows", "play", rom]
            cmd=Command.Command(array=commandArray)
        else: raise Exception("invalid system " + system.name)

        cmd.env['SDL_GAMECONTROLLERCONFIG']=controllersConfig.generateSdlGameControllerConfig(playersControllers,'sdl_config' not in system.config or system.config['sdl_config']=='1')

        if 'lang' in system.config and system.config['lang'] != '':
            cmd.env['LANG']=cmd.env['LC_ALL']=system.config['lang']+'.UTF-8'
        if 'winepoint_each_core' in system.config and system.config['winepoint_each_core'] != '':
            cmd.env['BATCERA_WINE_SAVES_EACH_CORE']=system.config['winepoint_each_core']

        return cmd

    def getMouseMode(self, config):
        if "force_mouse" in config and config["force_mouse"] == "0":
            return False
        else:
            return True
