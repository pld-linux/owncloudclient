#
# Conditional build:
%bcond_without	nautilus		# build Nautilus extension

Summary:	The ownCloud client
Name:		owncloudclient
Version:	2.1.1
Release:	0.9
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.xz
# Source0-md5:	63a971158201a8dffe96a02c54b86819
URL:		https://www.owncloud.com/
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtKeychain-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXmlPatterns-devel
BuildRequires:	cmake >= 2.8.11
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-Sphinx
BuildRequires:	sphinx-pdg
BuildRequires:	sqlite3-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	texlive-latex-ams
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	Qt5Gui-platform-xcb
Suggests:	%{name}-nautilus
Suggests:	%{name}-nemo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ownCloud sync client - github.com/owncloud/client

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

%build
install -d build
cd build
%cmake \
	-DQTKEYCHAIN_INCLUDE_DIR=/usr/include/qtkeychain \
	-DQTKEYCHAIN_LIBRARY=/usr/%{_lib}/libqtkeychain.so \
	..
%{__make}

# documentation here?
if [ -e conf.py ]; then
	# for old cmake versions we need to move the conf.py.
	mv conf.py doc/
fi

%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# nemo not in pld
%{__rm} $RPM_BUILD_ROOT%{_datadir}/nemo-python/extensions/syncstate.py*

mv $RPM_BUILD_ROOT%{_docdir}/html ${RPM_BUILD_ROOT}%{_docdir}/%{name}
mv $RPM_BUILD_ROOT%{_docdir}/latex ${RPM_BUILD_ROOT}%{_docdir}/%{name}
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/unthemed/.buildinfo

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache_post hicolor

%postun
if [ $1 -eq 0 ] ; then
	%update_icon_cache_post hicolor
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md COPYING
%doc %{_docdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ownCloud/*
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/*/*/apps/*.png
%{_datadir}/owncloud
#%{_libdir}/owncloud/libocsync.so.*
%dir %{_libdir}/owncloud
%{_mandir}/man1/owncloud*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libowncloudsync.so.*.*.*
%ghost %{_libdir}/libowncloudsync.so.0
%attr(755,root,root) %{_libdir}/owncloud/libocsync.so.*.*.*
%ghost %{_libdir}/owncloud/libocsync.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/owncloudsync
%{_libdir}/libowncloudsync.so
%{_libdir}/owncloud/libocsync.so

%if %{with nautilus}
%files nautilus
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/syncstate.py*
%endif
