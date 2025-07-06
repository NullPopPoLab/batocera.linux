################################################################################
#
# libretro-beetle-pce
#
################################################################################
# Version.: Commits on Mar 23, 2023
LIBRETRO_BEETLE_PCE_VERSION = cb7e701f7e710c0b527a2dc69969a084a270db4b
LIBRETRO_BEETLE_PCE_SITE = https://github.com/NullPopPoLab/beetle-pce-libretro.git
LIBRETRO_BEETLE_PCE_SITE_METHOD = git
LIBRETRO_BEETLE_PCE_LICENSE = GPLv2

define LIBRETRO_BEETLE_PCE_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) platform="$(LIBRETRO_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BEETLE_PCE_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BEETLE_PCE_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_pce_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/pce_libretro.so
endef

$(eval $(generic-package))
