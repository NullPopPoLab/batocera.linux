################################################################################
#
# EmulationStation theme "Carbon"
#
################################################################################
# Version.: Commits on Nov 30, 2021
ES_THEME_CARBON_VERSION = e57058c9bfaf09924af012d26ae0b069b52af989
ES_THEME_CARBON_SITE = https://github.com/NullPopPoLab/es-theme-carbon.git
ES_THEME_CARBON_SITE_METHOD = git

define ES_THEME_CARBON_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-carbon
    cp -r $(@D)/* $(TARGET_DIR)/usr/share/emulationstation/themes/es-theme-carbon
endef

$(eval $(generic-package))
