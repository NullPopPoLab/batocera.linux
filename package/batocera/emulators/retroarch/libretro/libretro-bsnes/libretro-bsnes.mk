################################################################################
#
# libretro-bsnes
#
################################################################################
# Version.: Commits on Mar 30, 2021
LIBRETRO_BSNES_VERSION = ef7a6920dcedf0c20c72552806ce7477155a997b
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
