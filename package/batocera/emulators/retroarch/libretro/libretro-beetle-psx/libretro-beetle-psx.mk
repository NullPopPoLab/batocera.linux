################################################################################
#
# LIBRETRO_BEETLE_PSX
#
################################################################################
# Version.: Commits on Dec 10, 2021
LIBRETRO_BEETLE_PSX_VERSION = 634c8e7db755a7c9e8435c878673dbef76211df8
LIBRETRO_BEETLE_PSX_SITE = https://github.com/NullPopPoLab/beetle-psx-libretro
LIBRETRO_BEETLE_PSX_SITE_METHOD=git
LIBRETRO_BEETLE_PSX_LICENSE = GPLv2

LIBRETRO_BEETLE_PSX_EXTRAOPT=
LIBRETRO_BEETLE_PSX_OUTFILE=mednafen_psx_libretro.so

ifeq ($(BR2_PACKAGE_XORG7),y)
LIBRETRO_BEETLE_PSX_EXTRAOPT += HAVE_HW=1
LIBRETRO_BEETLE_PSX_OUTFILE=mednafen_psx_hw_libretro.so
endif

define LIBRETRO_BEETLE_PSX_BUILD_CMDS
    $(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile $(LIBRETRO_BEETLE_PSX_EXTRAOPT) platform="$(LIBRETRO_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BEETLE_PSX_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BEETLE_PSX_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/$(LIBRETRO_BEETLE_PSX_OUTFILE) \
		$(TARGET_DIR)/usr/lib/libretro/mednafen_psx_libretro.so
endef

$(eval $(generic-package))
