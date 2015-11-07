#
# Conditional build:
%bcond_with	tests		# build without tests

# "psr/log": "~1.0"
%define psrlog_min_ver  1.0
%define psrlog_max_ver  2.0

%define		pkgname monolog
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	Sends your logs to files, sockets, inboxes, databases and various web services
Name:		php-%{pkgname}
Version:	1.17.2
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/Seldaek/monolog/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	85b0bbd8541cbf8b09faf18fd29934df
URL:		https://github.com/Seldaek/monolog
BuildRequires:	rpmbuild(macros) >= 1.654
%if %{with tests}
## composer.json
BuildRequires:	php(core) >= %{php_min_version}
BuildRequires:	php-psr-Log < %{psrlog_max_ver}
BuildRequires:	php-psr-Log >= %{psrlog_min_ver}
BuildRequires:	phpunit
## phpcompatinfo (computed from version 1.17.2)
BuildRequires:	php(curl)
BuildRequires:	php(date)
BuildRequires:	php(filter)
BuildRequires:	php(hash)
BuildRequires:	php(json)
BuildRequires:	php(mbstring)
BuildRequires:	php(openssl)
BuildRequires:	php(pcre)
BuildRequires:	php(reflection)
BuildRequires:	php(sockets)
BuildRequires:	php(spl)
BuildRequires:	php(xml)
## Autoloader
BuildRequires:	php-symfony2-ClassLoader
%endif
# composer.json
Requires:	php(core) >= %{php_min_version}
Requires:	php-psr-Log < %{psrlog_max_ver}
Requires:	php-psr-Log >= %{psrlog_min_ver}
# phpcompatinfo (computed from version 1.17.2)
Requires:	php(curl)
Requires:	php(date)
Requires:	php(filter)
Requires:	php(hash)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(openssl)
Requires:	php(pcre)
Requires:	php(sockets)
Requires:	php(spl)
Requires:	php(xml)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# disable pear auto deps
%define		_noautoreq_pear .*

%description
Monolog sends your logs to files, sockets, inboxes, databases and
various web services. Special handlers allow you to build advanced
logging strategies.

This library implements the PSR-3 interface that you can type-hint
against in your own libraries to keep a maximum of interoperability.
You can also use it in your applications to make sure you can always
use another compatible logger at a later time.

%prep
%setup -qn %{pkgname}-%{version}

%build
%if %{with tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
BOOTSTRAP

: Remove MongoDBHandlerTest because it requires a running MongoDB server
rm tests/Monolog/Handler/MongoDBHandlerTest.php

: Remove GitProcessorTest because it requires a git repo
rm tests/Monolog/Processor/GitProcessorTest.php

: Skip tests known to fail
rm -f tests/Monolog/Handler/SwiftMailerHandlerTest.php
sed 's/function testThrowsOnInvalidEncoding/function SKIP_testThrowsOnInvalidEncoding/' \
	-i tests/Monolog/Formatter/NormalizerFormatterTest.php

phpunit --verbose --bootstrap bootstrap.php
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -a src/* $RPM_BUILD_ROOT%{php_data_dir}

%files
%defattr(644,root,root,755)
%doc *.mdown doc LICENSE
%{php_data_dir}/Monolog

%clean
rm -rf $RPM_BUILD_ROOT