################################################################################
#
# libretro-bsnes
#
################################################################################
# Version.: Commits on Mar 30, 2021
LIBRETRO_BSNES_VERSION = c7c79f458dcbaef1a0adac6e8ac0426147e69a65
LIBRETRO_BSNES_SITE = https://github.com/NullPopPoLab/bsnes
LIBRETRO_BSNES_SITE_METHOD=git
LIBRETRO_BSNES_LICENSE = GPLv3

define LIBRETRO_BSNES_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/bsnes -f GNUmakefile target="libretro" platform=linux local=false
endef

define LIBRETRO_BSNES_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/bsnes/out/bsnes_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/bsnes_libretro.so
endef

$(eval $(generic-package))
