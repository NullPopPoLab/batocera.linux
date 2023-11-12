################################################################################
#
# libretro-pocketsnes
#
################################################################################
# Version: Commits on Aug 06, 2022
LIBRETRO_POCKETSNES_VERSION = 74f09ab5ac571646f7ef0bdc631d5257f56a70e4
LIBRETRO_POCKETSNES_SITE = https://github.com/NullPopPoLab/snes9x2002.git
LIBRETRO_POCKETSNES_SITE_METHOD = git
LIBRETRO_POCKETSNES_LICENSE = Non-commercial

LIBRETRO_POCKETSNES_PLATFORM = $(LIBRETRO_PLATFORM)

ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2835),y)
LIBRETRO_POCKETSNES_PLATFORM = unix-rpi1

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2836),y)
LIBRETRO_POCKETSNES_PLATFORM = unix-rpi2
endif

define LIBRETRO_POCKETSNES_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile platform="$(LIBRETRO_POCKETSNES_PLATFORM)"
endef

define LIBRETRO_POCKETSNES_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/snes9x2002_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/pocketsnes_libretro.so
endef

$(eval $(generic-package))
