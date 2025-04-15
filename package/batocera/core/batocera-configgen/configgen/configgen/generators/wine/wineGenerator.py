from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from ... import Command
from ...controller import generate_sdl_game_controller_config
from ..Generator import Generator

if TYPE_CHECKING:
    from ...types import HotkeysContext


class WineGenerator(Generator):

    def getHotkeysContext(self) -> HotkeysContext:
        return {
            "name": "wine",
            "keys": { "exit": ["KEY_LEFTALT", "KEY_F4"] }
        }

    def generate(self, system, rom, playersControllers, metadata, guns, wheels, gameResolution):

        environment = {}
        #system.language
        try:
            language = subprocess.check_output("batocera-settings-get system.language", shell=True, text=True).strip()
        except subprocess.CalledProcessError:
            language = 'en_US'
        if language:
            environment.update({
                "LANG": language + ".UTF-8",
                "LC_ALL": language + ".UTF-8"
                }
            )
        # sdl controller option - default is on
        if not system.isOptSet("sdl_config") or system.getOptBoolean("sdl_config"):
            environment.update(
                {
                    "SDL_GAMECONTROLLERCONFIG": generate_sdl_game_controller_config(playersControllers),
                    "SDL_JOYSTICK_HIDAPI": "0"
                }
            )
        # ensure nvidia driver used for vulkan
        if Path('/var/tmp/nvidia.prime').exists():
            variables_to_remove = ['__NV_PRIME_RENDER_OFFLOAD', '__VK_LAYER_NV_optimus', '__GLX_VENDOR_LIBRARY_NAME']
            for variable_name in variables_to_remove:
                if variable_name in os.environ:
                    del os.environ[variable_name]

            environment.update(
                {
                    'VK_ICD_FILENAMES': '/usr/share/vulkan/icd.d/nvidia_icd.x86_64.json:/usr/share/vulkan/icd.d/nvidia_icd.i686.json',
                }
            )

        if 'core' in system.config and system.config['core'] != '':
            environment['WINE_VERSION']=system.config['core']
        if 'esync' in system.config and system.config['esync'] != '':
            environment['ESYNC']=system.config['esync']
        if 'fsync' in system.config and system.config['fsync'] != '':
            environment['FSYNC']=system.config['fsync']
        if 'pba' in system.config and system.config['pba'] != '':
            environment['PBA']=system.config['pba']
        if 'fsr' in system.config and system.config['fsr'] != '':
            environment['FSR']=system.config['fsr']
        if 'fps_limit' in system.config and system.config['fps_limit'] != '':
            environment['FPS_LIMIT']=system.config['fps_limit']
        if 'allow_xim' in system.config and system.config['allow_xim'] != '':
            environment['ALLOW_XIM']=system.config['allow_xim']
        if 'no_write_watch' in system.config and system.config['no_write_watch'] != '':
            environment['NO_WRITE_WATCH']=system.config['no_write_watch']
        if 'force_large_adress' in system.config and system.config['force_large_adress'] != '':
            environment['FORCE_LARGE_ADRESS']=system.config['force_large_adress']
        if 'heap_delay_free' in system.config and system.config['heap_delay_free'] != '':
            environment['HEAP_DELAY_FREE']=system.config['heap_delay_free']
        if 'hide_nvidia_gpu' in system.config and system.config['hide_nvidia_gpu'] != '':
            environment['HIDE_NVIDIA_GPU']=system.config['hide_nvidia_gpu']
        if 'enable_nvapi' in system.config and system.config['enable_nvapi'] != '':
            environment['ENABLE_NVAPI']=system.config['enable_nvapi']
        if 'dxvk_reset_cache' in system.config and system.config['dxvk_reset_cache'] != '':
            environment['DXVK_RESET_CACHE']=system.config['dxvk_reset_cache']
        if 'wine_ntfs' in system.config and system.config['wine_ntfs'] != '':
            environment['WINE_NTFS']=system.config['wine_ntfs']
        if 'wine_debug' in system.config and system.config['wine_debug'] != '':
            environment['WINE_DEBUG']=system.config['wine_debug']
        if 'virtual_desktop' in system.config and system.config['virtual_desktop'] != '':
            environment['VIRTUAL_DESKTOP']=system.config['virtual_desktop']
        if 'videomode' in system.config and system.config['videomode'] != '':
            environment['VIRTUAL_DESKTOP_SIZE']=system.config['videomode']
        if 'mf' in system.config and system.config['mf'] != '':
            environment['MF']=system.config['mf']
        if 'dxvk' in system.config and system.config['dxvk'] != '':
            environment['DXVK']=system.config['dxvk']
        if 'dxvk_hud' in system.config and system.config['dxvk_hud'] != '':
            environment['DXVK_HUD']=system.config['dxvk_hud']

        if 'lang' in system.config and system.config['lang'] != '':
            environment['LANG']=environment['LC_ALL']=system.config['lang']+'.UTF-8'
        if 'enable_rootdrive' in system.config and system.config['enable_rootdrive'] != '':
            environment['BATOCERA_WINE_USE_ROOTDRIVE']=system.config['enable_rootdrive']
        if 'bootup' in system.config and system.config['bootup'] != '':
            environment['BATOCERA_WINE_BOOTUP']=system.config['bootup']
        else:
            environment['BATOCERA_WINE_BOOTUP']=''

        if system.name == "windows_installers":
            commandArray = ["batocera-wine", "windows", "install", rom]
            return Command.Command(array=commandArray, env=environment)
        elif system.name == "windows":
            commandArray = ["batocera-wine", "windows", "play", rom]
            return Command.Command(array=commandArray, env=environment)

        raise Exception("invalid system " + system.name)

    def getMouseMode(self, config, rom):
        if "force_mouse" in config and config["force_mouse"] == "0":
            return False
        else:
            return True
