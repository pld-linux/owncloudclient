
Summary:	The ownCloud client
Name:		owncloudclient
Version:	2.1.1
Release:	0.1
License:	GPL-2.0+
Group:		X11/Applications
URL:		https://www.owncloud.com
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.xz
# Source0-md5:  ee08ccedccd4c49f1464957146e14d26
Source1:	owncloud.sh
Source2:	owncloudcmd.sh
BuildRequires:	cmake >= 2.8.11
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	qt4
BuildRequires:	qt4-devel >= 4.7
BuildRequires:	qtwebkit >= 2.2
BuildRequires:	qtwebkit-devel >= 2.2
BuildRequires:	inetd
BuildRequires:	desktop-file-utils
BuildRequires:	openssl-devel
BuildRequires:	libQt5Concurrent-devel
BuildRequires:	libQt5Core-devel
BuildRequires:	libQt5DBus-devel
BuildRequires:	libQt5Gui-devel
BuildRequires:	libQt5Network-devel
BuildRequires:	libQt5PrintSupport-devel
BuildRequires:	libQt5WebKitWidgets-devel
BuildRequires:	libQt5Xml-devel
BuildRequires:	libqt5-linguist-devel
BuildRequires:	inetd
BuildRequires:	desktop-file-utils
BuildRequires:	sqlite-devel
BuildRequires:	sphinx-pdg
BuildRequires:	python-Sphinx
BuildRequires:	sqlite3-devel
BuildRequires:	update-desktop-files
Suggests:	%{name}-nautilus
Suggests:	%{name}-nemo
Requires:	%{name}-l10n
Requires:	libowncloudsync0 = %{version}
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

%package -n %{name}-doc
Summary:	Documentation for ownCloud
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	opt-owncloud-client-doc

%description -n %{name}-doc
Documentation about the ownCloud desktop application.

%package -n %{name}-l10n
Summary:	Localization for ownCloud
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	opt-owncloud-client-l10n

%description -n %{name}-l10n
Localization files for the ownCloud desktop application.

%package -n libowncloudsync0
Summary:	The ownCloud sync library
Group:		Development/Libraries

%description -n libowncloudsync0
The ownCloud sync library.

%package -n libowncloudsync-devel
Summary:	Development files for the ownCloud sync library
Group:		Development/Libraries
Requires:	libowncloudsync0 = %{version}

%description -n libowncloudsync-devel
Development files for the ownCloud sync library.

%package -n %{name}-nautilus
Summary:	Nautilus overlay icons
Group:		Productivity/Networking/Other
Requires:	nautilus
Requires:	nautilus-python
Requires:	python-nautilus
Requires:	%{name} = %{version}-%{release}

%description -n %{name}-nautilus
This package provides overlay icons to visualize the sync state in the
nautilus file manager.

%package -n %{name}-nemo
Summary:	Nemo overlay icons
Group:		Productivity/Networking/Other
Requires:	nemo
Requires:	nemo-python
Requires:	python-nemo
Requires:	%{name} = %{version}-%{release}

%description -n %{name}-nemo
This package provides overlay icons to visualize the sync state in the
nemo file manager.

%prep
%setup -q -n owncloudclient-%{version}
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?suse_version} == 1110
# autostart_use_wrapper.diff
%patch1 -p1
%endif

%build
export LD_LIBRARY_PATH=%{optdir}/%{_lib}
export PATH=%{optdir}/bin:$PATH

mkdir build
pushd build
# http://www.cmake.org/Wiki/CMake_RPATH_handling#Default_RPATH_settings
cmake .. -DWITH_DOC=TRUE \
%if "%{prerelease}" != ""
  -DMIRALL_VERSION_SUFFIX="%{prerelease}" \
  -DMIRALL_VERSION_BUILD=0 \
%endif
  -DCMAKE_C_FLAGS:STRING="%{optflags}" \
  -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if %{_lib} == lib64
  -DLIB_SUFFIX=64 \
%endif
%if ! %{is_owncloud_client}
  -DOEM_THEME_DIR=$PWD/../ownCloud/syncclient \
%endif
%if %{opt_hack}
%if 0%{?rhel_version} == 600 || 0%{?centos_version} == 600
  -DQTKEYCHAIN_INCLUDE_DIR=%{optdir}/include/qtkeychain \
  -DQTKEYCHAIN_LIBRARY=%{optdir}/%{_lib}/libqtkeychain.so \
%else
  -DQTKEYCHAIN_INCLUDE_DIR=%{optdir}/include/qt5keychain \
  -DQTKEYCHAIN_LIBRARY=%{optdir}/%{_lib}/libqt5keychain.so \
%endif
%endif
  %cmake_args

# documentation here?
if [ -e conf.py ];
then
  # for old cmake versions we need to move the conf.py.
  mv conf.py doc/
fi

env LD_RUN_PATH=%{_libdir}/owncloud:%{_libdir}/owncloud make %{?_smp_mflags} VERBOSE=1

%{__make} doc
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

if [ %{have_doc} != 0 ];
then
  install -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  mv ${RPM_BUILD_ROOT}%{_docdir}/client/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/client
  rm ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/.buildinfo
  mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed
fi
popd

if [ -d ${RPM_BUILD_ROOT}%{_mandir}/man1 ]; then
%if ! %{is_owncloud_client}
  install -d ${RPM_BUILD_ROOT}%{_mandir}man1
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloud.1,owncloud.1}
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloudcmd.1,owncloudcmd.1}
%endif
  gzip ${RPM_BUILD_ROOT}%{_mandir}/man1/*.1
fi

%define extdir ${RPM_BUILD_ROOT}%{_datadir}/nautilus-python/extensions
test -f %{extdir}/ownCloud.py  && mv %{extdir}/ownCloud.py  %{extdir}/owncloud.py  || true
test -f %{extdir}/ownCloud.pyo && mv %{extdir}/ownCloud.pyo %{extdir}/owncloud.pyo || true
test -f %{extdir}/ownCloud.pyc && mv %{extdir}/ownCloud.pyc %{extdir}/owncloud.pyc || true

%if %opt_hack
install -d ${RPM_BUILD_ROOT}/%{optdir}/bin
mv ${RPM_BUILD_ROOT}/%{_bindir}/owncloud* ${RPM_BUILD_ROOT}/%{optdir}/bin/

cp -p %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/owncloud
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}/owncloudcmd
%endif

%if %{?suse_version:1}0
%suse_update_desktop_file -n owncloud
# workaround for https://github.com/owncloud/ownbrander/issues/322
for desktop_icon_dir in $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/*/apps; do
  # copy shortname to executable name, if missing.
  if [ -f $desktop_icon_dir/owncloud.png -a ! -f $desktop_icon_dir/owncloud.png ]; then
    cp $desktop_icon_dir/owncloud.png $desktop_icon_dir/owncloud.png
  fi
done
%endif

%check
## use exit 0 instead of exit 1 to turn this into warnings:
if [ "%{name}" != "testpilotcloud-client" ]; then
  if [ "%{prerelease}" == "" ]; then
    expr match '%{distribution}' '.*:community:\(testing\|nightly\)' && { echo "Error: Need a prerelease here, not %{version}"; exit 1; }
  else
    expr match '%{distribution}' '.*:community:desktop' && { echo "Error: Must not have a prerelease here, not %{version}"; exit 1; }
  fi
fi

%if 0%{?fedora_version}
%post
/bin/%update_icon_cache_post hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/%update_icon_cache_post hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%post -n libowncloudsync0
/sbin/ldconfig

%postun -n libowncloudsync0
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%{optdir}/bin/owncloud
%{optdir}/bin/owncloudcmd

%{_desktopdir}/owncloud.desktop
%{_iconsdir}/hicolor
%{_mandir}/man1/owncloud*

%{_iconsdir}/hicolor
%{_desktopdir}/owncloud.desktop
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%config %{_sysconfdir}/ownCloud
%dir %{_sysconfdir}

%files -n %{name}-doc
%defattr(644,root,root,755)
%doc README.md COPYING
%if 0%{have_doc}
%doc %{_docdir}/%{name}
%endif

%files -n %{name}-l10n
%defattr(644,root,root,755)
%{_datadir}/owncloud

%files -n libowncloudsync0
%defattr(644,root,root,755)
%{_libdir}/libowncloudsync.so.*
%{_libdir}/owncloud/libocsync.so.*
%dir %{_libdir}/owncloud

%files -n libowncloudsync-devel
%defattr(644,root,root,755)
%{_libdir}/libowncloudsync.so
%{_libdir}/owncloud/libocsync.so
%{_includedir}/owncloudsync/

%files -n %{name}-nautilus
%defattr(644,root,root,755)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nautilus-python/extensions/syncstate.py*
%dir %{_datadir}/nautilus-python
%dir %{_datadir}/nautilus-python/extensions/

%files -n %{name}-nemo
%defattr(644,root,root,755)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nemo-python/extensions/syncstate.py*
%dir %{_datadir}/nemo-python
%dir %{_datadir}/nemo-python/extensions/


%clean
rm -rf $RPM_BUILD_ROOT
