################################################################################
#
# libretro-beetle-saturn
#
################################################################################
# Version.: Commits on Mar 15, 2023
LIBRETRO_BEETLE_SATURN_VERSION = 191d97d86180a7fa3a24b25752959911d10e2fe9
LIBRETRO_BEETLE_SATURN_SITE = https://github.com/NullPopPoLab/beetle-saturn-libretro
LIBRETRO_BEETLE_SATURN_SITE_METHOD = git
LIBRETRO_BEETLE_SATURN_LICENSE = GPLv2

define LIBRETRO_BEETLE_SATURN_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile HAVE_OPENGL=1 platform="$(LIBRETRO_PLATFORM)"
endef

define LIBRETRO_BEETLE_SATURN_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_saturn_hw_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/beetle-saturn_libretro.so
endef

$(eval $(generic-package))
