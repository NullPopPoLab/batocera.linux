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

        cmd.env['SDL_GAMECONTROLLERCONFIG']=controllersConfig.generateSdlGameControllerConfig(playersControllers)


        return cmd

    def getMouseMode(self, config):
        if "force_mouse" in config and config["force_mouse"] == "0":
            return False
        else:
            return True
