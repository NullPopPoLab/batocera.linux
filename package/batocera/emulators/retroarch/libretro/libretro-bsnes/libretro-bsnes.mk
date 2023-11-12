################################################################################
#
# libretro-bsnes
#
################################################################################
# Version.: Commits on Aug 18, 2023
LIBRETRO_BSNES_VERSION = 9b189919516043b2d9c24d94663f30e7930bd8c7
LIBRETRO_BSNES_SITE = https://github.com/NullPopPoLab/bsnes.git
LIBRETRO_BSNES_SITE_METHOD = git
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
