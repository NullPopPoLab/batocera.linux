#!/usr/bin/env python

from generators.Generator import Generator
import Command
import os
from os import path
import controllersConfig

class WineGenerator(Generator):

    def generate(self, system, rom, playersControllers, guns, wheels, gameResolution):
        if system.name == "windows_installers":
            commandArray = ["batocera-wine", "windows", "install", rom]
            cmd=Command.Command(array=commandArray)
        elif system.name == "windows":
            commandArray = ["batocera-wine", "windows", "play", rom]
            cmd=Command.Command(array=commandArray)
        else: raise Exception("invalid system " + system.name)

        cmd.env['SDL_GAMECONTROLLERCONFIG']=controllersConfig.generateSdlGameControllerConfig(playersControllers)

        if 'core' in system.config and system.config['core'] != '':
            cmd.env['WINE_VERSION']=system.config['core']
        if 'esync' in system.config and system.config['esync'] != '':
            cmd.env['ESYNC']=system.config['esync']
        if 'fsync' in system.config and system.config['fsync'] != '':
            cmd.env['FSYNC']=system.config['fsync']
        if 'pba' in system.config and system.config['pba'] != '':
            cmd.env['PBA']=system.config['pba']
        if 'fsr' in system.config and system.config['fsr'] != '':
            cmd.env['FSR']=system.config['fsr']
        if 'fps_limit' in system.config and system.config['fps_limit'] != '':
            cmd.env['FPS_LIMIT']=system.config['fps_limit']
        if 'allow_xim' in system.config and system.config['allow_xim'] != '':
            cmd.env['ALLOW_XIM']=system.config['allow_xim']
        if 'no_write_watch' in system.config and system.config['no_write_watch'] != '':
            cmd.env['NO_WRITE_WATCH']=system.config['no_write_watch']
        if 'force_large_adress' in system.config and system.config['force_large_adress'] != '':
            cmd.env['FORCE_LARGE_ADRESS']=system.config['force_large_adress']
        if 'heap_delay_free' in system.config and system.config['heap_delay_free'] != '':
            cmd.env['HEAP_DELAY_FREE']=system.config['heap_delay_free']
        if 'hide_nvidia_gpu' in system.config and system.config['hide_nvidia_gpu'] != '':
            cmd.env['HIDE_NVIDIA_GPU']=system.config['hide_nvidia_gpu']
        if 'enable_nvapi' in system.config and system.config['enable_nvapi'] != '':
            cmd.env['ENABLE_NVAPI']=system.config['enable_nvapi']
        if 'dxvk_reset_cache' in system.config and system.config['dxvk_reset_cache'] != '':
            cmd.env['DXVK_RESET_CACHE']=system.config['dxvk_reset_cache']
        if 'wine_ntfs' in system.config and system.config['wine_ntfs'] != '':
            cmd.env['WINE_NTFS']=system.config['wine_ntfs']
        if 'wine_debug' in system.config and system.config['wine_debug'] != '':
            cmd.env['WINE_DEBUG']=system.config['wine_debug']
        if 'virtual_desktop' in system.config and system.config['virtual_desktop'] != '':
            cmd.env['VIRTUAL_DESKTOP']=system.config['virtual_desktop']
        if 'videomode' in system.config and system.config['videomode'] != '':
            cmd.env['VIRTUAL_DESKTOP_SIZE']=system.config['videomode']
        if 'mf' in system.config and system.config['mf'] != '':
            cmd.env['MF']=system.config['mf']
        if 'dxvk' in system.config and system.config['dxvk'] != '':
            cmd.env['DXVK']=system.config['dxvk']
        if 'dxvk_hud' in system.config and system.config['dxvk_hud'] != '':
            cmd.env['DXVK_HUD']=system.config['dxvk_hud']

        if 'lang' in system.config and system.config['lang'] != '':
            cmd.env['LANG']=cmd.env['LC_ALL']=system.config['lang']+'.UTF-8'

        return cmd

    def getMouseMode(self, config):
        if "force_mouse" in config and config["force_mouse"] == "0":
            return False
        else:
            return True
