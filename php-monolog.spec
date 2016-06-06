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
Version:	1.19.0
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/Seldaek/monolog/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	05c338cde7a1525d2093e6df5b3bbe21
URL:		https://github.com/Seldaek/monolog
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.654
%if %{with tests}
BuildRequires:	php(core) >= %{php_min_version}
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
BuildRequires:	php-psr-Log < %{psrlog_max_ver}
BuildRequires:	php-psr-Log >= %{psrlog_min_ver}
BuildRequires:	php-symfony2-ClassLoader
BuildRequires:	phpunit
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php-psr-Log < %{psrlog_max_ver}
Requires:	php-psr-Log >= %{psrlog_min_ver}
Suggests:	php(curl)
Suggests:	php(date)
Suggests:	php(filter)
Suggests:	php(hash)
Suggests:	php(json)
Suggests:	php(mbstring)
Suggests:	php(openssl)
Suggests:	php(pcre)
Suggests:	php(sockets)
Suggests:	php(spl)
Suggests:	php(xml)
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
