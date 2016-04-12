#
# Conditional build:
%bcond_without	nautilus	# build Nautilus extension
%bcond_with	dolphin		# build dolphin extension
%bcond_without	doc		# build docs
%bcond_without	gui		# build only libraries

%if %{without gui}
%undefine	with_nautilus
%undefine	with_dolphin
%undefine	with_doc
%endif

%define		qtver	5.4
Summary:	The ownCloud client
Name:		owncloudclient
Version:	2.1.1
Release:	0.17
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.xz
# Source0-md5:	63a971158201a8dffe96a02c54b86819
Patch0:		syslibs.patch
URL:		https://www.owncloud.com/
BuildRequires:	Qt5Concurrent-devel >= %{qtver}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Keychain-devel
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5WebKit-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sqlite3-devel >= 3.8.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with gui}
BuildRequires:	Qt5LockedFile-devel >= 2.4
BuildRequires:	Qt5SingleApplication-devel >= 2.6
BuildRequires:	Qt5Sql-devel >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
%endif
%if %{with dolphin}
BuildRequires:	kf5-attica-devel >= 5.16
BuildRequires:	kf5-extra-cmake-modules >= 1.2.0
BuildRequires:	kf5-kconfig-devel >= 5.16
BuildRequires:	kf5-ki18n-devel >= 5.16
BuildRequires:	kf5-kio-devel >= 5.16
%endif
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	sphinx-pdg-2
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-makeindex
BuildRequires:	texlive-pdftex
BuildRequires:	texlive-plain
BuildRequires:	texlive-xetex
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	Qt5Gui-platform-xcb
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Suggests:	%{name}-nautilus
Suggests:	%{name}-nemo
Obsoletes:	mirall < 1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ownCloud client enables you to connect to your private ownCloud
Server. With it you can create folders in your home directory, and
keep the contents of those folders synced with your ownCloud server.
Simply copy a file into the directory and the ownCloud Client does the
rest.

ownCloud gives your employees anytime, anywhere access to the files
they need to get the job done, whether through this desktop
application, our mobile apps, the web interface, or other WebDAV
clients. With it, your employees can easily view and share documents
and information critical to the business, in a secure, flexible and
controlled architecture. You can easily extend ownCloud with plug-ins
from the community, or that you build yourself to meet the
requirements of your infrastructure and business.

%package libs
Summary:	Shared ownCloud client libraries
Group:		Libraries
Obsoletes:	mirall-libs < 1.8

%description libs
Shared ownCloud client libraries.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%package nautilus
Summary:	Nautilus overlay icons
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-python

%description nautilus
This package provides overlay icons to visualize the sync state in the
Nautilus file manager.

%prep
%setup -q
%patch0 -p1

rm -r src/3rdparty/qtlockedfile
rm -r src/3rdparty/qtsingleapplication

%build
install -d build
cd build
%cmake \
	-DQTKEYCHAIN_INCLUDE_DIR=/usr/include/qt5keychain \
	-DQTKEYCHAIN_LIBRARY=/usr/%{_lib}/libqt5keychain.so \
	-DQT_LRELEASE_EXECUTABLE=/usr/bin/lrelease-qt5 \
	-DBUILD_WITH_QT4=NO \
%if %{with doc}
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-2 \
	-DPDFLATEX_EXECUTABLE=/usr/bin/pdflatex \
	-DDOXYGEN_EXECUTABLE=/usr/bin/doxygen \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
%else
	-DWITH_DOC=NO \
	-DCMAKE_DISABLE_FIND_PACKAGE_Doxygen=TRUE \
	-DCMAKE_DISABLE_FIND_PACKAGE_PdfLatex=TRUE \
	-DCMAKE_DISABLE_FIND_PACKAGE_Sphinx=TRUE \
%endif
%if %{without dolphin}
	-DCMAKE_DISABLE_FIND_PACKAGE_ECM=TRUE \
	-DCMAKE_DISABLE_FIND_PACKAGE_KF5=TRUE \
%endif
	%{!?with_gui:-DBUILD_LIBRARIES_ONLY=ON} \
	..
%{__make}

%if %{with doc}
%{__make} doc
rm doc/html/unthemed/.buildinfo
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# owncloud client links without rpath
mv $RPM_BUILD_ROOT%{_libdir}/owncloud/libocsync.so* $RPM_BUILD_ROOT%{_libdir}

%if %{with nautilus}
# nemo not in pld
%{__rm} $RPM_BUILD_ROOT%{_datadir}/nemo-python/extensions/syncstate.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with gui}
%files
%defattr(644,root,root,755)
%doc README.md COPYING
%dir %{_sysconfdir}/ownCloud
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ownCloud/*
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/*/*/apps/*.png
%{_datadir}/owncloud
%dir %{_libdir}/owncloud
%if %{with doc}
%{_mandir}/man1/owncloud.1*
%{_mandir}/man1/owncloudcmd.1*
%endif
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libowncloudsync.so.*.*.*
%ghost %{_libdir}/libowncloudsync.so.0
%attr(755,root,root) %{_libdir}/libocsync.so.*.*.*
%ghost %{_libdir}/libocsync.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/owncloudsync
%{_libdir}/libowncloudsync.so
%{_libdir}/libocsync.so

%if %{with nautilus}
%files nautilus
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/syncstate.py*
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}
%endif
