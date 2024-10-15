################################################################################
#
# libretro-tgbdual
#
################################################################################
# Version.: Commits on Aug 06, 2022
LIBRETRO_TGBDUAL_VERSION = 993ebe21fbccf0bedd78423a24534329fc182dac
LIBRETRO_TGBDUAL_SITE = https://github.com/NullPopPoLab/px68k-libretro.git
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
