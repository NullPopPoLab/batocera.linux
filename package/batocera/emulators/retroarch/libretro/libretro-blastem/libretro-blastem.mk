################################################################################
#
# BLASTEM
#
################################################################################
# Version.: Commits on Apr xx, 2020
LIBRETRO_BLASTEM_VERSION = 2ee4fb9bc65c3bcc345ce773e37fc4a409a03447
LIBRETRO_BLASTEM_SITE = https://github.com/NullPopPoLab/blastem
LIBRETRO_BLASTEM_SITE_METHOD=git
LIBRETRO_BLASTEM_LICENSE = Non-commercial

LIBRETRO_BLASTEM_EXTRAOPTS=""

ifeq ($(BR2_x86_64),y)
LIBRETRO_BLASTEM_EXTRAOPTS=CPU=x86_64
else  ifeq ($(BR2_x86_i686),y)
LIBRETRO_BLASTEM_EXTRAOPTS=CPU=i686
endif

define LIBRETRO_BLASTEM_BUILD_CMDS
    $(SED) "s+CPU:=i686+CPU?=i686+g" $(@D)/Makefile
	$(TARGET_CONFIGURE_OPTS) $(MAKE) CXX="$(TARGET_CXX)" CC="$(TARGET_CC)" -C $(@D) libblastem.so $(LIBRETRO_BLASTEM_EXTRAOPTS)
endef

define LIBRETRO_BLASTEM_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/libblastem.so \
		$(TARGET_DIR)/usr/lib/libretro/blastem_libretro.so
endef

$(eval $(generic-package))

