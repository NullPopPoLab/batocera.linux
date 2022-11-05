################################################################################
#
# VBA-M
#
################################################################################
# Last commit: Oct 20, 2021
LIBRETRO_VBA_M_VERSION = 9f448021afc0d08a765520a7520247656490dedd
LIBRETRO_VBA_M_SITE = https://github.com/NullPopPoLab/visualboyadvance-m
LIBRETRO_VBA_M_SITE_METHOD=git

define LIBRETRO_VBA_M_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)/src/libretro -f Makefile platform="unix"  \
        CURRENT_COMMIT="-$(shell echo $(LIBRETRO_VBA_M_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_VBA_M_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/src/libretro/vbam_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/vba-m_libretro.so
endef

$(eval $(generic-package))
