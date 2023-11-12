################################################################################
#
# libretro-virtualjaguar
#
################################################################################
# Version: Commits on Nov 19, 2022
LIBRETRO_VIRTUALJAGUAR_SITE = $(BR2_EXTERNAL_BATOCERA_PATH)/local/libretro-virtualjaguar
LIBRETRO_VIRTUALJAGUAR_SITE_METHOD = local
LIBRETRO_VIRTUALJAGUAR_LICENSE = GPLv3

define LIBRETRO_VIRTUALJAGUAR_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile \
        platform="unix" GIT_VERSION="-$(shell echo $(LIBRETRO_VIRTUALJAGUAR_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_VIRTUALJAGUAR_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/virtualjaguar_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/virtualjaguar_libretro.so
endef

$(eval $(generic-package))
