################################################################################
#
# libretro-bsnes-hd
#
################################################################################
# Version: Commits on Jun 29, 2022
LIBRETRO_BSNES_HD_SITE = $(BR2_EXTERNAL_BATOCERA_PATH)/local/libretro-bsnes-hd
LIBRETRO_BSNES_HD_SITE_METHOD = local
LIBRETRO_BSNES_HD_LICENSE = GPLv3

define LIBRETRO_BSNES_HD_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/bsnes -f GNUmakefile target="libretro" platform=linux local=false
endef

define LIBRETRO_BSNES_HD_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/bsnes/out/bsnes_hd_beta_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/bsnes_hd_libretro.so
endef

$(eval $(generic-package))
