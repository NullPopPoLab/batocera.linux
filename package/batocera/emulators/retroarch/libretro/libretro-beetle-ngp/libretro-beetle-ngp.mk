################################################################################
#
# libretro-beetle-ngp
#
################################################################################
# Version.: Commits on Feb 20, 2023
LIBRETRO_BEETLE_NGP_SITE = $(BR2_EXTERNAL_BATOCERA_PATH)/local/libretro-beetle-ngp
LIBRETRO_BEETLE_NGP_SITE_METHOD = local
LIBRETRO_BEETLE_NGP_LICENSE = GPLv2

LIBRETRO_BEETLE_NGP_PLATFORM = $(LIBRETRO_PLATFORM)

ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2835),y)
LIBRETRO_BEETLE_NGP_PLATFORM = rpi1

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2836),y)
LIBRETRO_BEETLE_NGP_PLATFORM = rpi2

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2837),y)
LIBRETRO_BEETLE_NGP_PLATFORM = rpi3_64

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2711),y)
LIBRETRO_BEETLE_NGP_PLATFORM = rpi4_64
endif

define LIBRETRO_BEETLE_NGP_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/ -f Makefile platform="$(LIBRETRO_BEETLE_NGP_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BEETLE_NGP_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BEETLE_NGP_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_ngp_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/mednafen_ngp_libretro.so
endef

$(eval $(generic-package))
