################################################################################
#
# libretro-desmume
#
################################################################################
# Version: Commits on Sep 26, 2022
LIBRETRO_DESMUME_VERSION = 06d8041e153d3f6cc83e1a75d5abeca9ed0f8441
LIBRETRO_DESMUME_SITE = https://github.com/NullPopPoLab/desmume.git
LIBRETRO_DESMUME_SITE_METHOD = git
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
