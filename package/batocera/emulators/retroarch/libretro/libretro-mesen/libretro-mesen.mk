################################################################################
#
# libretro-mesen
#
################################################################################
# Version: Commits on Apr 8, 2022
LIBRETRO_MESEN_VERSION = 4d0c252900ae51701f17a3c23d98b608546bec52
LIBRETRO_MESEN_SITE = https://github.com/NullPopPoLab/Mesen
LIBRETRO_MESEN_SITE_METHOD=git
LIBRETRO_MESEN_LICENSE = GPL

define LIBRETRO_MESEN_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" GIT_VERSION="" -C $(@D)/Libretro -f Makefile
endef

define LIBRETRO_MESEN_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/Libretro/mesen_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/mesen_libretro.so
endef

$(eval $(generic-package))
