################################################################################
#
# EmulationStation theme "Carbon"
#
################################################################################
# Version.: Commits on Nov 30, 2021
ES_THEME_CARBON_VERSION = 371f08ffa0c1b1d5d527af2a3054465b5d66ed1f
ES_THEME_CARBON_SITE = https://github.com/NullPopPoLab/es-theme-carbon.git
ES_THEME_CARBON_SITE_METHOD = git

define ES_THEME_CARBON_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-carbon
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-carbon
endef

$(eval $(generic-package))
