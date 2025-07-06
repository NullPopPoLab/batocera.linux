################################################################################
#
# libretro-beetle-supergrafx
#
################################################################################
# Version.: Commits on Mar 17, 2023
LIBRETRO_BEETLE_SUPERGRAFX_VERSION = 867b311d4fa3f8676471b6a2d73cc506a0167486
LIBRETRO_BEETLE_SUPERGRAFX_SITE = https://github.com/NullPopPoLab/beetle-supergrafx-libretro.git
LIBRETRO_BEETLE_SUPERGRAFX_SITE_METHOD = git
LIBRETRO_BEETLE_SUPERGRAFX_LICENSE = GPLv2

LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM = $(LIBRETRO_PLATFORM)

ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2835),y)
LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM = rpi1

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2836),y)
LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM = rpi2

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2837),y)
LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM = rpi3_64

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_BCM2711),y)
LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM = rpi4_64
endif

define LIBRETRO_BEETLE_SUPERGRAFX_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/ -f Makefile platform="$(LIBRETRO_BEETLE_SUPERGRAFX_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BEETLE_SUPERGRAFX_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BEETLE_SUPERGRAFX_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_supergrafx_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/mednafen_supergrafx_libretro.so
endef

$(eval $(generic-package))
