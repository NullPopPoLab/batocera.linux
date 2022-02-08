################################################################################
#
# DESMUME
#
################################################################################
# Version.: Commits on Aug 16, 2021
LIBRETRO_DESMUME_VERSION = 7929cd39b9fe478cd97bbb61dfbff1cd2924cc05
LIBRETRO_DESMUME_SITE = https://github.com/NullPopPoLab/desmume
LIBRETRO_DESMUME_SITE_METHOD=git
LIBRETRO_DESMUME_LICENSE = GPLv2
LIBRETRO_DESMUME_DEPENDENCIES = libpcap

define LIBRETRO_DESMUME_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/desmume/src/frontend/libretro -f Makefile platform="$(LIBRETRO_PLATFORM)"
endef

define LIBRETRO_DESMUME_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/desmume/src/frontend/libretro/desmume_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/desmume_libretro.so
endef

$(eval $(generic-package))
