################################################################################
#
# libretro-beetle-vb
#
################################################################################
# Version: Commits on Feb 23, 2023
LIBRETRO_BEETLE_VB_VERSION = d7b0556affdc8cc2f36ebac47322a31909e358f9
LIBRETRO_BEETLE_VB_SITE = https://github.com/NullPopPoLab/beetle-vb-libretro.git
LIBRETRO_BEETLE_VB_SITE_METHOD = git
LIBRETRO_BEETLE_VB_LICENSE = GPLv2

LIBRETRO_BEETLE_VB_PLATFORM = $(LIBRETRO_PLATFORM)

ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2835),y)
LIBRETRO_BEETLE_VB_PLATFORM = rpi1

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2836),y)
LIBRETRO_BEETLE_VB_PLATFORM = rpi2

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2837),y)
LIBRETRO_BEETLE_VB_PLATFORM = rpi3_64

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2711),y)
LIBRETRO_BEETLE_VB_PLATFORM = rpi4_64

else ifeq ($(BR2_aarch64),y)
LIBRETRO_BEETLE_VB_PLATFORM = unix
endif

define LIBRETRO_BEETLE_VB_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) platform="$(LIBRETRO_BEETLE_VB_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BEETLE_VB_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BEETLE_VB_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_vb_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/vb_libretro.so
endef

$(eval $(generic-package))
