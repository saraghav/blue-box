#
# Copyright (C) 2015 www.emonix.io
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

# RETAIN BELOW THIS - INCLUDES OPENWRT PACKAGE MANAGER DEFINITIONS
include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk
# RETAIN ABOVE THIS - INCLUDES OPENWRT PACKAGE MANAGER DEFINITIONS

PKG_NAME:=perl-spi-driver
PKG_VERSION:=1.1
PKG_RELEASE:=2

# RETAIN BELOW THIS - INCLUDES OPENWRT PACKAGE MANAGER DEFINITIONS
include $(INCLUDE_DIR)/package.mk
# RETAIN ABOVE THIS - INCLUDES OPENWRT PACKAGE MANAGER DEFINITIONS

define Package/perl-spi-driver
  SECTION:=custom
  CATEGORY:=Custom
  DEPENDS:=+perl
  TITLE:=SPI bitbanging emulation using PERL
  VERSION:=$(LINUX_VERSION)-$(PKG_VERSION)
  URL:=http://www.emonix.io
  MAINTAINER:=Ananth Sridhar <ananth.sridhar@wisc.edu>
endef

define Package/perl-spi-driver/description
  SPI bitbanging emulation using PERL
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/perl-spi-driver/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/perl-spi-driver $(1)/usr/bin/
endef

$(eval $(call BuildPackage,perl-spi-driver))
