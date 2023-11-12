################################################################################
#
# libretro-bsnes
#
################################################################################
# Version.: Commits on Aug 18, 2023
LIBRETRO_BSNES_SITE = $(BR2_EXTERNAL_BATOCERA_PATH)/local/libretro-bsnes
LIBRETRO_BSNES_SITE_METHOD = local
LIBRETRO_BSNES_LICENSE = GPLv3
LIBRETRO_BSNES_LICENSE_FILE = LICENSE.txt

define LIBRETRO_BSNES_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/ -f Makefile platform="unix"
endef

define LIBRETRO_BSNES_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/bsnes_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/bsnes_libretro.so
endef

$(eval $(generic-package))
