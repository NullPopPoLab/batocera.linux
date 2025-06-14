################################################################################
#
# libretro-tgbdual
#
################################################################################
# Version.: Commits on Aug 06, 2022
LIBRETRO_TGBDUAL_VERSION = cf3efc040e531c7362f3da0548cd711084276dde
LIBRETRO_TGBDUAL_SITE = https://github.com/NullPopPoLab/tgbdual-libretro.git
LIBRETRO_TGBDUAL_SITE_METHOD = git
LIBRETRO_TGBDUAL_LICENSE = GPLv2

define LIBRETRO_TGBDUAL_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D)
endef

define LIBRETRO_TGBDUAL_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/tgbdual_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/tgbdual_libretro.so
endef

$(eval $(generic-package))
