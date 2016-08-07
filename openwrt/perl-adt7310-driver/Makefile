#
# Copyright (C) 2015 www.emonix.io
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=perl-adt7310-driver
PKG_VERSION:=1.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/perl-adt7310-driver
  SECTION:=custom
  CATEGORY:=Custom
  DEPENDS:=+perl +perl-spi-driver
  TITLE:=Driver for Analog Devices ADT7310 Temperature Sensor
  VERSION:=$(LINUX_VERSION)-$(PKG_VERSION)
  URL:=http://www.emonix.io
  MAINTAINER:=Ananth Sridhar <ananth.sridhar@wisc.edu>
endef

define Package/perl-adt7310-driver/description
  Driver for Analog Devices ADT7310 Temperature Sensor
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/perl-adt7310-driver/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/perl-adt7310-driver $(1)/usr/bin/
endef

$(eval $(call BuildPackage,perl-adt7310-driver))
