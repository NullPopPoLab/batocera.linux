################################################################################
#
# BEETLE_PCE
#
################################################################################
# Version.: Commits on Nov 24, 2021
LIBRETRO_BEETLE_PCE_VERSION = 5d8989eee422e3f3d2de9db34fb45c736e114b41
LIBRETRO_BEETLE_PCE_SITE = https://github.com/NullPopPoLab/beetle-pce-libretro.git
LIBRETRO_BEETLE_PCE_SITE_METHOD=git
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
