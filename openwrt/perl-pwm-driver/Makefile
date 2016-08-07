#
# Copyright (C) 2015 www.emonix.io
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=perl-pwm-driver
PKG_VERSION:=1.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/perl-pwm-driver
  SECTION:=custom
  CATEGORY:=Custom
  DEPENDS:=+perl
  TITLE:=PWM bitbanging emulation using PERL
  VERSION:=$(LINUX_VERSION)-$(PKG_VERSION)
  URL:=http://www.emonix.io
  MAINTAINER:=Ananth Sridhar <ananth.sridhar@wisc.edu>
endef

define Package/perl-pwm-driver/description
  PWM bitbanging emulation using PERL
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/perl-pwm-driver/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/perl-pwm-driver $(1)/usr/bin/
endef

$(eval $(call BuildPackage,perl-pwm-driver))
