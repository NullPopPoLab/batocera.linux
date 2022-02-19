################################################################################
#
# LIBRETRO_SWANSTATION
#
################################################################################
# Version.: Commits on Jan 17, 2022
LIBRETRO_SWANSTATION_VERSION = 23831d0a528380bc30de8eb2d020ac58ec260ece
LIBRETRO_SWANSTATION_SITE = https://github.com/NullPopPoLab/duckstation
LIBRETRO_SWANSTATION_SITE_METHOD=git
LIBRETRO_SWANSTATION_LICENSE = GPLv2
LIBRETRO_SWANSTATION_DEPENDENCIES = fmt boost ffmpeg retroarch

LIBRETRO_SWANSTATION_CONF_OPTS  = -DCMAKE_BUILD_TYPE=Release
LIBRETRO_SWANSTATION_CONF_OPTS += -DBUILD_SHARED_LIBS=FALSE
LIBRETRO_SWANSTATION_CONF_OPTS += -DBUILD_LIBRETRO_CORE=ON
LIBRETRO_SWANSTATION_CONF_OPTS += -DUSE_DRMKMS=ON

LIBRETRO_SWANSTATION_CONF_ENV += LDFLAGS=-lpthread

# Should be set when the package cannot be built inside the source tree but needs a separate build directory.
LIBRETRO_SWANSTATION_SUPPORTS_IN_SOURCE_BUILD = NO

define LIBRETRO_SWANSTATION_INSTALL_TARGET_CMDS
    $(INSTALL) -D $(@D)/buildroot-build/swanstation_libretro.so \
	    $(TARGET_DIR)/usr/lib/libretro/swanstation_libretro.so
endef

$(eval $(cmake-package))
