################################################################################
#
# BEETLE-SATURN
#
################################################################################
# Version.: Commits on Dec 05, 2021
LIBRETRO_BEETLE_SATURN_VERSION = 5e04ae5d2dce8c78fc285ee09f22dab4c8cab743
LIBRETRO_BEETLE_SATURN_SITE = https://github.com/NullPopPoLab/beetle-saturn-libretro
LIBRETRO_BEETLE_SATURN_SITE_METHOD=git
LIBRETRO_BEETLE_SATURN_LICENSE = GPLv2

define LIBRETRO_BEETLE_SATURN_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) -f Makefile HAVE_OPENGL=1 platform="$(LIBRETRO_PLATFORM)"
endef

define LIBRETRO_BEETLE_SATURN_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/mednafen_saturn_hw_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/beetle-saturn_libretro.so
endef

$(eval $(generic-package))
