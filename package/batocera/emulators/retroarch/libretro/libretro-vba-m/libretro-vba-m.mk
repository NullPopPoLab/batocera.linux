################################################################################
#
# libretro-vba-m
#
################################################################################
# Version: Commits on Mar 25, 2023
LIBRETRO_VBA_M_VERSION = c8e40fc2bd3bb410c9ddb32c3d882bdd109afd63
LIBRETRO_VBA_M_SITE = https://github.com/NullPopPoLab/visualboyadvance-m.git
LIBRETRO_VBA_M_SITE_METHOD = git

define LIBRETRO_VBA_M_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/src/libretro -f Makefile platform="unix"  \
        CURRENT_COMMIT="-$(shell echo $(LIBRETRO_VBA_M_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_VBA_M_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/src/libretro/vbam_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/vba-m_libretro.so
endef

$(eval $(generic-package))
