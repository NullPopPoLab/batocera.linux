################################################################################
#
# libretro-pcsx2
#
################################################################################
# Version: Commits on Mar 26, 2022
LIBRETRO_PCSX2_SITE = $(BR2_EXTERNAL_BATOCERA_PATH)/local/libretro-pcsx2
LIBRETRO_PCSX2_SITE_METHOD = local
LIBRETRO_PCSX2_LICENSE = GPLv2
LIBRETRO_PCSX2_DEPENDENCIES = libaio xz host-xxd

LIBRETRO_PCSX2_CONF_OPTS = -DCMAKE_BUILD_TYPE=Release -DSDL2_API=ON \
    -DDISABLE_PCSX2_WRAPPER=ON -DPACKAGE_MODE=OFF -DBUILD_SHARED_LIBS=OFF \
	-DENABLE_TESTS=OFF -DENABLE_QT=OFF -DLIBRETRO=ON -DDISABLE_ADVANCE_SIMD=ON \
	-DEXTRA_PLUGINS=TRUE

define LIBRETRO_PCSX2_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/pcsx2/pcsx2_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/pcsx2_libretro.so
endef

$(eval $(cmake-package))
