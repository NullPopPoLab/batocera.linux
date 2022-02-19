################################################################################
#
# LIBRETRO_DUCKSTATION
#
################################################################################
# libretro cores can be downloaded in binary form,
# but not built from the Github Duckstation sources
# Version.: 0.1-4866-gf799f62a
LIBRETRO_DUCKSTATION_VERSION = add2b1eca73981a7e86547c9daa0259d44bd3508
LIBRETRO_DUCKSTATION_SITE = https://github.com/NullPopPoLab/swanstation
LIBRETRO_DUCKSTATION_SITE_METHOD = git
LIBRETRO_DUCKSTATION_LICENSE = non-commercial

LIBRETRO_DUCKSTATION_PK = unknown
ifeq ($(BR2_x86_64),y)
LIBRETRO_DUCKSTATION_PK = duckstation_libretro_linux_x64.zip
else ifeq ($(BR2_aarch64),y)
LIBRETRO_DUCKSTATION_PK = duckstation_libretro_linux_aarch64.zip
else ifeq ($(BR2_arm),y)
LIBRETRO_DUCKSTATION_PK = duckstation_libretro_linux_armv7.zip
endif

define LIBRETRO_DUCKSTATION_INSTALL_TARGET_CMDS
    cd $(@D) && unzip $(LIBRETRO_DUCKSTATION_PK)

    $(INSTALL) -D $(@D)/duckstation_libretro.so \
        $(TARGET_DIR)/usr/lib/libretro/duckstation_libretro.so
endef

$(eval $(generic-package))
