################################################################################
#
# BLUEMSX
#
################################################################################
# Version.: Commits on Oct 07, 2021
LIBRETRO_BLUEMSX_VERSION = 41e088e6019d4492a13dc8be32e4c02519f06e4c
LIBRETRO_BLUEMSX_SITE = https://github.com/NullPopPoLab/blueMSX-libretro
LIBRETRO_BLUEMSX_SITE_METHOD = git
LIBRETRO_BLUEMSX_LICENSE = GPLv2

LIBRETRO_BLUEMSX_PLATFORM = $(LIBRETRO_PLATFORM)

ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_RPI1),y)
LIBRETRO_BLUEMSX_PLATFORM = rpi1

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_RPI2),y)
LIBRETRO_BLUEMSX_PLATFORM = rpi2

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_RPI3)$(BR2_PACKAGE_BATOCERA_TARGET_RPIZERO2),y)
    ifeq ($(BR2_arm),y)
        LIBRETRO_BLUEMSX_PLATFORM = rpi3
    else
        LIBRETRO_BLUEMSX_PLATFORM = rpi3_64
    endif

else ifeq ($(BR2_PACKAGE_BATOCERA_TARGET_RPI4),y)
LIBRETRO_BLUEMSX_PLATFORM = rpi4_64
endif

define LIBRETRO_BLUEMSX_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile.libretro platform="$(LIBRETRO_BLUEMSX_PLATFORM)" \
        GIT_VERSION="-$(shell echo $(LIBRETRO_BLUEMSX_VERSION) | cut -c 1-7)"
endef

define LIBRETRO_BLUEMSX_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/bluemsx_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/bluemsx_libretro.so

	mkdir -p $(TARGET_DIR)/usr/share/batocera/datainit/bios/bluemsx
	cp -pr $(@D)/system/bluemsx/* \
		$(TARGET_DIR)/usr/share/batocera/datainit/bios
endef

$(eval $(generic-package))
