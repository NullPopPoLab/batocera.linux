################################################################################
#
# MESEN-S
#
################################################################################
# Version.: 0.4.0
LIBRETRO_MESENS_VERSION = 59be567d783d63c3e1553e38bd67760739c47bcc
LIBRETRO_MESENS_SITE = https://github.com/NullPopPoLab/Mesen-S
LIBRETRO_MESENS_SITE_METHOD=git
LIBRETRO_MESENS_LICENSE = GPL

define LIBRETRO_MESENS_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" GIT_VERSION="" -C $(@D)/Libretro -f Makefile
endef

define LIBRETRO_MESENS_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/Libretro/mesen-s_libretro.so \
		$(TARGET_DIR)/usr/lib/libretro/mesen-s_libretro.so
endef

$(eval $(generic-package))
