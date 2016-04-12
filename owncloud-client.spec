#
# spec file for package owncloud-client
#
# Copyright (c) 2012 ownCloud, inc.; Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes, issues or comments via http://github.com/owncloud/
#

## Caution: This spec file exists in multiple locations. Keep in sync:
##  isv:ownCloud:desktop
##  isv:ownCloud:community:nightly
##  isv:ownCloud:community:testing
##  github.com/owncloud/administration/jenkins/obs_integration/templates/client/v1_8_1/SHORTNAME-client.spec.in
##  -> you can modify it in testing, and play around for a while, but then merge into the copy on
##     github, which is authorative for the branded clients.
##
## created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.1.tar.xz ownCloud.tar.xz

## One specfile to rule them all:
##  versions 1.6.x or 1.7.x, released or prerelease versions. All rpm based platforms.
##  testing, branding, whatever.
##
## Caution: do not change the names of the following three defines.
## prerelease, base_version, tar_version are the interface into buildpackage.pl
## used in rotor.o.c job owncloud-client-linux
## define prerelease as %nil, if this is not a prerelease.
%define prerelease %nil
%define base_version 2.1.1
%define tar_version %{base_version}%{prerelease}

Name:           owncloud-client

%if "%{name}" == "owncloud-client"
%define is_owncloud_client 1
%else
%define is_owncloud_client 0
%endif

# Use translations from an external tarball in the package, or build them
# using the Qt tools? For distros where we do not have the tools, disable.

%if 0%{?centos_version} == 600 || 0%{?rhel_version} == 600 || 0%{?fedora_version} || "%{prerelease}" == ""
# For beta and rc versions we use the ~ notation, as documented in
# http://en.opensuse.org/openSUSE:Package_naming_guidelines
# Some distro's (centos_6) don't allow ~ characters. There we follow the Fedora guidelines,
# which suggests massaging the buildrelease number.
# Otoh: for openSUSE, this technique is discouraged by the package naming guidelines.
Version:       	%{base_version}
%if "%{prerelease}" == ""
Release:        2.5
%else
Release:       	0.2.5.%{prerelease}
%endif
%else
Version:       	%{base_version}~%{prerelease}
Release:        2.5
%endif

License:        GPL-2.0+
Summary:        The ownCloud client
%if %{is_owncloud_client}
Url:            https://www.owncloud.com
%else
Url:            owncloud.com
%endif
Group:          Productivity/Networking/Other
Source0:        owncloudclient-2.1.1.tar.bz2
Source1:        owncloud.sh
Source2:        owncloudcmd.sh

%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?suse_version} == 1110
Patch1:         autostart_use_wrapper.diff
%endif

%if 0%{?rhel_version} >= 600 || 0%{?centos_version} >= 600 || 0%{?suse_version} == 1110
%if 0%{?suse_version} == 1110
# SLES 11 calls make_install makeinstall
%define make_install %{makeinstall}
%endif
# We need a more recent, prefixed Qt for SLE11
%define opt_hack 1
%define qtprefix opt-
%if 0%{?rhel_version} == 600 || 0%{?centos_version} == 600
%define optdir /opt/qt-4.8
%else
%define optdir /opt/qt-5.4
%endif

# Must be all in one line:
%define cmake_args -DCMAKE_INCLUDE_PATH=%{_prefix}/include -DCMAKE_LIBRARY_PATH=%{_prefix}/%{_lib} -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE
%else
%define opt_hack 0
%define qtprefix %{nil}
%define cmake_args -DSYSCONF_INSTALL_DIR=%{_sysconfdir}
%endif

# default to have no docs. Cannot be built with old distros.
%define have_doc 0

# prepare stuff for qt5
# If Qt5 is available, we use it. Also, if the Qt-Version is 5.4 or higher
%define use_qt5 0
%if 0%{?suse_version} > 1310 || 0%{?fedora_version} > 20 || 0%{?rhel_version} >= 700 || 0%{?centos_version} >= 700
  %define use_qt5 1
%endif
# Check for SLE12 -> it does not have qt5 obviously.
%if ! 0%{?is_opensuse} && 0%{?suse_version}==1315
  %define use_qt5 0
%endif

######################################################################### BuildRequires only below here.

BuildRequires:  cmake >= 2.8.11
BuildRequires:  gcc gcc-c++
%if %use_qt5
BuildRequires:  %{qtprefix}libqt5keychain-devel %{qtprefix}libqt5keychain0
%else
BuildRequires:  %{qtprefix}libqtkeychain-devel
%endif

# This is for all modern Fedora and CentOS 7
# These ship Qt in a decent version and do not need the opt-hack
%if 0%{?fedora_version} >= 21 || 0%{?centos_version} >= 700 || 0%{?rhel_version} == 700

%if %use_qt5
BuildRequires:  %{qtprefix}qt5-qttools-devel
BuildRequires:  %{qtprefix}qt5-qtbase
BuildRequires:  %{qtprefix}qt5-qtbase-devel
BuildRequires:  %{qtprefix}qt5-qtbase-gui
BuildRequires:  %{qtprefix}qt5-qtwebkit-devel

%else # no qt5
BuildRequires:  qt4 qt4-devel >= 4.7
BuildRequires:  qtwebkit >= 2.2
BuildRequires:  qtwebkit-devel >= 2.2
%endif

BuildRequires:  openssl-devel
BuildRequires:  inetd desktop-file-utils
%else
# This is for all SUSE and RHEL6 and CentOS 6
%if %use_qt5

BuildRequires:  libQt5Core-devel
BuildRequires:  libQt5Gui-devel
BuildRequires:  libQt5Network-devel
BuildRequires:  libQt5WebKitWidgets-devel
BuildRequires:  libQt5Xml-devel
BuildRequires:  libQt5PrintSupport-devel
BuildRequires:  libQt5DBus-devel
BuildRequires:  libQt5Concurrent-devel
BuildRequires:  libqt5-linguist-devel

%else # no qt5

BuildRequires:  %{qtprefix}libqt4-devel >= 4.7
BuildRequires:  %{qtprefix}libQtWebKit-devel
BuildRequires:  %{qtprefix}libQtWebKit4

%endif

%endif

# SUSE specific stuff
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
BuildRequires:  libopenssl-devel
%endif

# The opt-hack to use the packages installed in /opt on CentOS
%if 0%{?suse_version} || 0%{?fedora_version} || 0%{?rhel_version} > 600 || 0%{?centos_version} > 600
%define have_doc 1
%endif

# no documents on SLE12
%if 0%{?suse_version} == 1315
%define have_doc 0
%endif

# Version independant package name mapping between suse and fedora/centos
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  sqlite-devel
BuildRequires:  inetd desktop-file-utils
%if 0%{?fedora_version} || 0%{?rhel_version} > 600 || 0%{?centos_version} > 600
BuildRequires:  python-sphinx
%endif
%else
%if 0%{have_doc}
BuildRequires:  python-Sphinx
%endif
BuildRequires:  sqlite3-devel
BuildRequires:  update-desktop-files
%endif


######################################################################### Requires only below here.

%if %use_qt5 && 0%{?suse_version} == 0
# suse finds the libs via autoreqprov 
# https://github.com/owncloud/client/issues/4431
Requires:       %{qtprefix}qt5-qtbase
Requires:       %{qtprefix}qt5-qtbase-gui
# libQtWebKit4 is implicitly pulled by libowncloudsync0
Requires:       %{qtprefix}qt5-qtwebkit
# libqt4-sql is implicitly pulled by libqt4-sql-sqlite
%endif

%if 0%{?fedora_version} > 20 || 0%{?centos_version} > 700 || 0%{?suse_version} || 0%{?rhel_version} > 700
# Fedora-19 and -20, CentOS-6, CentOS-7, RHEL_6,7 don't have Suggests.
Suggests:	%{name}-nautilus
Suggests:       %{name}-nemo
%endif

%if 0%{?rhel_version} == 600 || 0%{?centos_version} == 600
# https://github.com/owncloud/client/issues/4400#issuecomment-176686729
Requires:	%{qtprefix}libqt4-sql
%endif

Requires: %{name}-l10n
Requires: libowncloudsync0 = %{version}

######################################################################### Obsoletes only below here.

Obsoletes: libocsync0
Obsoletes: libocsync-devel
Obsoletes: libocsync-plugin-owncloud
Obsoletes: libocsync-plugin-owncloud
Obsoletes: libocsync-devel-doc
Obsoletes: libocsync-doc
Obsoletes: opt-owncloud-client

# Obsolete the experimental Qt5 packages if this is the unbranded client.
%if %{is_owncloud_client}
Obsoletes: libowncloudqt5sync0 libowncloudqt5sync-devel owncloud-client-qt5 owncloud-client-qt5-doc owncloud-client-qt5-l10n
%endif

######################################################################### Package Descriptions start here.

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The ownCloud sync client - github.com/owncloud/client

ownCloud client enables you to connect to your private
ownCloud Server. With it you can create folders in your home
directory, and keep the contents of those folders synced with your
ownCloud server. Simply copy a file into the directory and the
ownCloud Client does the rest.

ownCloud gives your employees anytime, anywhere access to the files
they need to get the job done, whether through this desktop application,
our mobile apps, the web interface, or other WebDAV clients. With it,
your employees can easily view and share documents and information
critical to the business, in a secure, flexible and controlled
architecture. You can easily extend ownCloud with plug-ins from the
community, or that you build yourself to meet the requirements of
your infrastructure and business.

ownCloud - Your Cloud, Your Data, Your Way!  www.owncloud.com

Authors
=======
Duncan Mac-Vicar P. <duncan@kde.org>
Klaas Freitag <freitag@owncloud.com>
Daniel Molkentin <danimo@owncloud.com>



%package -n %{name}-doc
Summary:        Documentation for ownCloud
Group:          Development/Libraries/C and C++
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-%{name}-doc

%description -n %{name}-doc
Documentation about the ownCloud desktop application.

%package -n %{name}-l10n
Summary:        Localization for ownCloud
Group:          Development/Libraries/C and C++
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-%{name}-l10n

%description -n %{name}-l10n
Localization files for the ownCloud desktop application.

%package -n libowncloudsync0
%if %use_qt5
Requires:       %{qtprefix}libqt5keychain0
%else
Requires:       %{qtprefix}libqtkeychain0 >= 0.3
%endif
Obsoletes:      opt-libowncloudsync0
# https://github.com/owncloud/client/issues/4506
Obsoletes:	owncloud-client-libs <= %{version}

Summary:        The ownCloud sync library
Group:          Development/Libraries/C and C++

%description -n libowncloudsync0
The ownCloud sync library.

%package -n libowncloudsync-devel
Summary:        Development files for the ownCloud sync library
Group:          Development/Libraries/C and C++
Requires: libowncloudsync0 = %{version}
Obsoletes:      opt-libowncloudsync-devel

%description -n libowncloudsync-devel
Development files for the ownCloud sync library.

%package -n %{name}-nautilus
Summary:        Nautilus overlay icons
Group:          Productivity/Networking/Other
Requires:       nautilus
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       nautilus-python
%else
Requires:       python-nautilus
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-%{name}-nautilus

%description -n %{name}-nautilus
This package provides overlay icons to visualize the sync state
in the nautilus file manager.

%package -n %{name}-nemo
Summary:        Nemo overlay icons
Group:          Productivity/Networking/Other
Requires:       nemo
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
Requires:       nemo-python
%else
Requires:       python-nemo
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      opt-%{name}-nemo

%description -n %{name}-nemo
This package provides overlay icons to visualize the sync state
in the nemo file manager.

%prep
%setup -q -n owncloudclient-2.1.1
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?suse_version} == 1110
# autostart_use_wrapper.diff
%patch1 -p1
%endif

%if 0%{?rhel_version} == 600 || 0%{?centos_version} == 600
sed -i -e 's/OVERRIDE=override/OVERRIDE=/' cmake/modules/QtVersionAbstraction.cmake
%endif

%build
echo centos_version 0%{?centos_version}
echo rhel_version   0%{?rhel_version}
echo fedora_version 0%{?fedora_version}
echo suse_version   0%{?suse_version}

%if %opt_hack
%endif
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

make doc
popd

%install
pushd build
%make_install

if [ %{have_doc} != 0 ];
then
  mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  mv ${RPM_BUILD_ROOT}/usr/share/doc/client/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  rmdir ${RPM_BUILD_ROOT}/usr/share/doc/client
  rm ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/.buildinfo
  mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed
fi
popd

if [ -d ${RPM_BUILD_ROOT}%{_mandir}/man1 ]; then
%if ! %{is_owncloud_client}
  mkdir -p ${RPM_BUILD_ROOT}%{_mandir}man1
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

install %{SOURCE1} ${RPM_BUILD_ROOT}/usr/bin/owncloud
install %{SOURCE2} ${RPM_BUILD_ROOT}/usr/bin/owncloudcmd
%endif

%if %{?suse_version:1}0
%suse_update_desktop_file -n owncloud
# workaround for https://github.com/owncloud/ownbrander/issues/322
for desktop_icon_dir in $RPM_BUILD_ROOT/usr/share/icons/hicolor/*/apps; do
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
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%post -n libowncloudsync0
/sbin/ldconfig

%postun -n libowncloudsync0
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/owncloud
%{_bindir}/owncloudcmd

%if %{opt_hack}
%{optdir}/bin/owncloud
%{optdir}/bin/owncloudcmd
%endif

%{_datadir}/applications/owncloud.desktop
%{_datadir}/icons/hicolor
%if 0%{have_doc}
%{_mandir}/man1/owncloud*
%endif

%if %opt_hack
/usr/share/icons/hicolor
/usr/share/applications/owncloud.desktop
/usr/bin/owncloud
/usr/bin/owncloudcmd
%endif
%config /etc/ownCloud
%dir /etc

%files -n %{name}-doc
%defattr(-,root,root,-)
%doc README.md COPYING
%if 0%{have_doc}
%doc %{_docdir}/%{name}
%endif

%files -n %{name}-l10n
%defattr(-,root,root,-)
%{_datadir}/owncloud

%files -n libowncloudsync0
%defattr(-,root,root,-)
%{_libdir}/libowncloudsync.so.*
%{_libdir}/owncloud/libocsync.so.*
%dir %{_libdir}/owncloud

%files -n libowncloudsync-devel
%defattr(-,root,root,-)
%{_libdir}/libowncloudsync.so
%{_libdir}/owncloud/libocsync.so
%{_includedir}/owncloudsync/

%files -n %{name}-nautilus
%defattr(-,root,root,-)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nautilus-python/extensions/syncstate.py*
%dir %{_datadir}/nautilus-python
%dir %{_datadir}/nautilus-python/extensions/

%files -n %{name}-nemo
%defattr(-,root,root,-)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nemo-python/extensions/syncstate.py*
%dir %{_datadir}/nemo-python
%dir %{_datadir}/nemo-python/extensions/

%changelog
* Mon Mar 14 2016 jw@owncloud.com
- help with https://github.com/owncloud/client/issues/4506
* Tue Feb  9 2016 jenkins@owncloud.org
  Automatically generated branding added. Version=2.1.1
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.1.tar.xz ownCloud.tar.xz
* Mon Feb  8 2016 jw@owncloud.com
- backported startupscripts to 2.1.0
  https://github.com/owncloud/client/issues/4441
* Fri Jan 29 2016 jw@owncloud.com
- https://github.com/owncloud/client/issues/4400#issuecomment-176686729
  CentOS6:  Requires:       %%{qtprefix}libqt4-sql
* Thu Jan 28 2016 jw@owncloud.com
- CentOS6 fails. It requires opt-qt5-qtbase and friends, although use_qt5 == 0.
  https://github.com/owncloud/client/issues/4400
* Thu Jan 28 2016 jw@owncloud.com
- backported wrapper scripts from 2.1.1
* Wed Dec  9 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.1.0
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.0.tar.xz ownCloud.tar.xz
* Wed Dec  9 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.1.0
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.0.tar.xz ownCloud.tar.xz
* Wed Dec  9 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.1.0
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.0.tar.xz ownCloud.tar.xz
* Thu Dec  3 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.1.0
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.1.0.tar.xz ownCloud.tar.xz
* Wed Nov  4 2015 jw@owncloud.com
- Most hackish solution to https://github.com/owncloud/client/issues/4029
  The -doc package is now always empty. I cannot seem to find a way to create
  a missing directory. Sorry.
* Wed Oct 21 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.0.2
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.0.2.tar.xz ownCloud.tar.xz
* Tue Sep  1 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.0.1
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.0.1.tar.xz ownCloud.tar.xz
* Tue Aug 25 2015 jenkins@owncloud.org
  Automatically generated branding added. Version=2.0.0
  created by: ./genbranding.pl (V1.12) -o -p isv:ownCloud:desktop owncloudclient-2.0.0.tar.xz ownCloud.tar.xz
* Mon Jun 15 2015 freitag@owncloud.com
- Some fixes to make SLE12 build.
* Mon Jun  8 2015 jw@owncloud.com
- version 1.8.2 (release 2015-06-08)
  * Improve reporting of server error messages (#3220)
  * Discovery: Ignore folders with any 503 (#3113)
  * Wizard: Show server error message if possible (#3220)
  * QNAM: Fix handling of mitm cert changes (#3283)
  * Win32: Installer translations added (#3277)
  * Win32: Allow concurrent OEM (un-)installers (#3272)
  * Win32: Make Setup/Update Mutex theme-unique (#3272)
  * HTTP: Add the branding name to the UserAgent string
  * ConnectonValidator: Always run with new credentials (#3266)
  * Recall Feature: Admins can trigger an upload of a file from
  client to server again (#3246)
  * Propagator: Add 'Content-Length: 0' header to MKCOL request (#3256)
  * Switch on checksum verification through branding or config
  * Add ability for checksum verification of up and download
  * Fix opening external links for some labels (#3135)
  * AccountState: Run only a single validator, allow error message
  overriding (#3236, #3153)
  * SyncJournalDB: Minor fixes and simplificatons
  * SyncEngine: Force re-read of folder Etags for upgrades from
  1.8.0 and 1.8.1
  * Propagator: Limit length of temporary file name (#2789)
  * ShareDialog: Password ui fixes (#3189)
  * Fix startup hang by removing QSettings lock file (#3175)
  * Wizard: Allow SSL cert dialog to show twice (#3168)
  * ProtocolWidget: Fix rename message (#3210)
  * Discovery: Test better, treat invalid hrefs as error (#3176)
  * Propagator: Overwrite local data only if unchanged (#3156)
  * ShareDialog: Improve error reporting for share API fails
  * OSX Updater: Only allow updates only if in /Applications (#2931)
  * Wizard: Fix lock icon (#1447)
  * Fix compilation with GCC 5
  * Treat any 503 error as temporary (#3113)
  * Work around for the Qt PUT corruption bug (#2425)
  * OSX Shell integration: Optimizations
  * Windows Shell integration: Optimizations
  .. more than 250 commits since 1.8.1
* Wed May 20 2015 jw@owncloud.com
- https://github.com/owncloud/client/issues/3250
  Added missing wrapper owncloudcmd.sh for CentOS-6
* Thu May  7 2015 jw@owncloud.com
- Release 1.8.1
  * Make "operation canceled" error a soft error
  * Do not throw an error for files that are scheduled to be removed, but can not be found on the server. (#2919)
  * Windows: Reset QNAM to proper function after hibernation. (#2899, #2895, #2973)
  * Fix argument verification of --confdir (#2453)
  * Fix a crash when accessing a dangling UploadDevice pointer (#2984)
  * Add-folder wizard: Make sure there is a scrollbar if folder names are too long (#2962)
  * Add-folder Wizard: Select the newly created folder
  * Activity: Correctly restore column sizes (#3005)
  * SSL Button: do not crash on empty certificate chain
  * SSL Button: Make menu creation lazy (#3007, #2990)
  * Lookup system proxy async to avoid hangs (#2993, #2802)
  * ShareDialog: Some GUI refinements
  * ShareDialog: On creation of a share always retrieve the share. This makes sure that if a default expiration date is set this is reflected in the dialog. (#2889)
  * ShareDialog: Only show share dialog if we are connected.
  * HttpCreds: Fill pw dialog with previous password. (#2848, #2879)
  * HttpCreds: Delete password from old location. (#2186)
  * Do not store Session Cookies in the client cookie storage
  * CookieJar: Don't accidentally overwrite cookies. (#2808)
  * ProtocolWidget: Always add seconds to the DateTime locale. (#2535)
  * Updater: Give context as to which app is about to be updated (#3040)
  * Windows: Add version information for owncloud.exe. This should help us know what version or build number a crash report was generated with.
  * Fix a crash on shutdown in ~SocketApi (#3057)
  * SyncEngine: Show more timing measurements (#3064)
  * Discovery: Add warning if returned etag is 0
  * Fix a crash caused by an invalid DiscoveryDirectoryResult::iterator (#3051)
  * Sync: Fix sync of deletions during 503. (#2894)
  * Handle redirect of auth request. (#3082)
  * Discovery: Fix parsing of broken XML replies, which fixes local file disappearing (#3102)
  * Migration: Silently restore files that were deleted locally by bug (#3102)
  * Sort folder sizes SelectiveSyncTreeView numerically (#3112)
  * Sync: PropagateDownload: Read the mtime from the file system after writing it (#3103)
  * Sync: Propagate download: Fix restoring files for which the conflict file exists (#3106)
  * Use identical User Agents and version for csync and the Qt parts
  * Prevent another crash in ~SocketApi (#3118)
  * Windows: Fix rename of finished file (#3073)
  * AccountWizard: Fix auth error handling (#3155)
  * Documentation fixes
  * Infrastructure/build fixes
  * Win32/OS X: Apply patch from OpenSSL to handle oudated intermediates gracefully (#3087)
- Fixed shell script owncloud.sh to pass parameters correctly.
* Wed May  6 2015 jenkins@owncloud.org
- Automatically generated branding added. Version=1.8.1
  created by: ./genbranding.pl (V1.8) -o -p isv:ownCloud:desktop owncloudclient-1.8.1.tar.xz ownCloud.tar.xz
* Mon Mar 30 2015 jw@owncloud.com
- Added dont_reset_ssl_config.diff from danimo@owncloud.com
  Needed with centos_6 and ubuntu_12.04 -- harmless for others.
* Thu Mar 26 2015 jw@owncloud.com
- CentOS_6: do not require sphinx
* Tue Mar 17 2015 freitag@owncloud.com
- Fix version in spec: Remove rc1
* Mon Mar 16 2015 freitag@owncloud.com
- Update to stable release 1.8.0:
  * Mac OS: HIDPI support
  * Support Sharing from desktop: Added a share dialog that can be
    opened by context menu in the file managers (Win, Mac, Nautilus)
    Supports public links with password enforcement
  * Enhanced usage of parallel HTTP requests for ownCloud 8 servers
  * Renamed github repository from mirall to client.
  * Mac OS: Use native notification support
  * Selective Sync: allow to enforce selective sync in brandings.
  * Added ability to build on Windows utilizing MingGW
  * SQLite database fixes if running on FAT filesystems
  * Improved detection of changing files to upload from local
  * Preparations for the multi-account feature
  * Fixed experience for Window manager without system tray
  * Build with Qt 5.4
  * Dropped libneon dependency if Qt 5.4 is available
  * Keep files open very short, that avoid lock problems on Windows
    especially with office software but also others.
  * Merged some NetBSD patches
  * Selective sync support for owncloudcmd
  * Reorganize the source repository
  * Prepared direct download
  * Added Crashreporter feature to be switched on on demand
  * A huge amount of bug fixes in all areas of the client.
  * almost 700 commits since 1.7.1
* Tue Jan 27 2015 jw@owncloud.com
- potential fix for https://github.com/owncloud/client/issues/1605
* Thu Dec 18 2014 danimo@owncloud.com
- version 1.7.1 (release 2014-12-18)
  * Documentation fixes and updates
  * Nautilus Python plugin fixed for Python 3
  * GUI wording fixes plus improved log messages
  * Fix hidning of the database files in the sync directories
  * Compare http download size with the header value to avoid broken
    downloads, bug #2528
  * Avoid initial ETag fetch job at startup, which is not needed.
  * Add chunk size http header to PUT requests
  * Fixed deteteCookie method of our CookieJar, fix for Shibboleth
  * Added fallback for distros where XDG_RUNTIME_DIR is undefined
  * Fix the setup wizard, bug #1989, #2264
  * Fix scheduling of ETag check jobs, bug #2553
  * Fix to avoid syncing more than one folder at a time, bug #2407
  * Use fife minutes timeout for all network jobs
  * Cleanup for Folderwizard wording
  * Improve journal check: Remove corrupted journal files, bug #2547
  * Fix item count in progress dialog for deletes, bug #1132
  * Display correct file count on deletion (#1132)
  * Fix reinitializing the folder using the wizard in certain cases (#2606)
  * Mac OS: Fixed branding of the pkg file
  * Mac OS: Fix display of overlay icons in certain situations (#1132)
  * Mac OS: Use a bundled version of OpenSSL (#764, #2600, #2510)
  * Win32: improved filesystem watcher
  * Win32: Improve threading with shell integration
  * Win32: Upgraded to OpenSSL 1.0.1j
  * Win32: Improve reliability of Installer, fix removal of Shell Extensions
* Thu Nov 13 2014 freitag@opensuse.org
- Fix nautilus dependency for Fedora
* Thu Nov  6 2014 danimo@owncloud.com
- version 1.7.0 (released 2012-11-06)
  * oC7 Sharing: Handle new sharing options of ownCloud 7 correctly.
  * Added Selective sync: Ability to unselect server folders which are
    excluded from syncing, plus GUI and setup GUI
  * Added overlay icons for Windows Explorer, Mac OS Finder and GNOME Nautilus.
    Information is provided by the client via a local socket / named pipe API
    which provides information about the sync status of files.
  * Improved local change detection: consider file size, detect files
    with ongoing changes and do not upload immediately
  * Improved HTTP request timeout handler: all successful requests reset
    the timeout counter
  * Improvements for syncing command line tool: netrc support, improved
    SSL support, non interactive mode
  * Permission system: ownCloud 7 delivers file and folder permissions,
    added ability to deal with it for shared folders and more.
  * Ignore handling: Do not recurse into ignored or excluded directories
  * Major sync journal database improvements for more stability and performance
  * New library interface to sqlite3
  * Improve "resync handling" if errors occur
  * Blacklist improvements
  * Improved logging: more useful meta info, removed noise
  * Updated to latest Qt5 versions on Windows and OS X
  * Fixed data loss when renaming a download temporary fails and there was
    a conflict at the same time.
  * Fixed missing warnings about reusing a sync folder when the back button
    was used in the advanced folder setup wizard.
  * The 'Retry Sync' button now also restarts all downloads.
  * Clean up temporary downloads and some extra database files when wiping a
    folder.
  * OS X: Sparkle update to provide pkg format properly
  * OS X: Change distribution format from dmg to pkg with new installer.
  * Windows: Fix handling of filenames with trailing dot or space
  * Windows: Don't use the wrong way to get file mtimes in the legacy propagator.
* Fri Oct 24 2014 danimo@owncloud.com
- Update to 1.7.0 rc1
* Tue Oct 21 2014 jw@owncloud.com
- added neon27_ubuntu1204_compat_csync.diff
  to make it build on ancient Ubuntu-12.04
* Tue Oct 21 2014 freitag@owncloud.com
- Added rpath patch, can be removed with next beta as we fixed it
  upstream.
* Tue Oct 21 2014 freitag@owncloud.com
- Update to version 1.7.0 beta4
* Thu Oct  9 2014 jw@owncloud.com
- no Suggests: for CentOS-7
- patching away Q_DECL_OVERRIDE for CentOS-6, too
* Wed Oct  8 2014 jw@owncloud.com
- patching away Q_DECL_OVERRIDE for ubuntu 12.04
* Mon Oct  6 2014 danimo@owncloud.com
- Update to version 1.7.0beta3
* Thu Oct  2 2014 jw@owncloud.com
- CentOS7, go without opthack, but pull qtwebkit from Fedora:19,
- specfiles merged: community:testing, desktop, obs_integration/templates
* Thu Oct  2 2014 freitag@owncloud.com
- Update to version 1.7.0beta2
* Sat Aug 30 2014 freitag@owncloud.com
- Remove the nautilus package for debian, is not part of 1.6.3
* Sat Aug 30 2014 freitag@owncloud.com
- Update to latest tarball of 1.6.3 rc1
* Fri Aug 22 2014 freitag@owncloud.com
- Update to latest tarball of 1.7.0 beta1
* Thu Aug 21 2014 jw@owncloud.com
- added a safeguard against 'binary' directory to debian.rules.
- removed 'binary' directory from tar ball.
  This directory crashes dpkg-genchangelog.
* Thu Aug 21 2014 freitag@owncloud.com
- Update to 1.7.0 beta1
* Mon Aug 18 2014 jw@owncloud.com
- fixed copyright in specfile
* Tue Aug 12 2014 jw@owncloud.com
- added %%check for false prerelease settings to specfile
* Tue Aug 12 2014 jw@owncloud.com
- synced spec, dsc, control with :desktop :community:nightly :community:testing
* Tue Aug 12 2014 jw@owncloud.com
- Proper prerelease setup added to *.spec and *.dsc
* Mon Aug 11 2014 jw@owncloud.com
- Removed debian.owncloud-client.docs and debian.owncloud-client.l10n
  They are redundant with the *.install files.
* Mon Aug 11 2014 freitag@owncloud.com
- Removed the silly file debian.owncloud-client-nautilus from the
  file list which I added before. Reverted Juergens hack.
* Mon Aug 11 2014 jw@owncloud.com
- added rm -f debian/owncloud-client-nautilus to debian.rules
  as a workaround. Debian builds fail if this file exitst.
  Needs investigation why that file is created.
* Fri Aug  8 2014 freitag@owncloud.com
- Added nautilus sub package for rpm based
* Fri Aug  8 2014 freitag@owncloud.com
- Update to 1.7.0alpha1
* Thu Jul 24 2014 freitag@owncloud.com
  version 1.6.2 (release 2014-07-x )
  * Another small mem leak fixed in HTTP Credentials.
  * Fix local file name clash detection for MacOSX.
  * Limit maximum wait time to ten seconds in network limiting.
  * Fix data corruption while trying to resume and the server does
    not support it.
  * HTTP Credentials: Read password from legacy place if not found.
  * Shibboleth: Fix the waiting curser that would not disapear (#1915)
  * Limit memory usage to avoid mem wasting and crashes
  * Propagator: Fix crash when logging out during upload (#1957)
  * Propagator_qnam: Fix signal slot connection (#1963)
  * Use more elaborated way to detect that the server was reconfigured (#1948)
  * Setup Wizard: Reconfigure Server also if local path was changed (#1948)
* Wed Jul 16 2014 freitag@owncloud.com
- New version 1.6.2 rc1
  version 1.6.2 (release 2014-07-x )
  * HTTP Credentials: Read password from legacy place if not found.
  * Shibboleth: Fix the waiting curser that would not disapear (#1915)
  * Limit memory usage to avoid mem wasting and crashes
  * Propagator: Fix crash when logging out during upload (#1957)
  * Propagator_qnam: Fix signal slot connection (#1963)
  * Use more elaborated way to detect that the server was reconfigured (#1948)
  * Setup Wizard: Reconfigure Server also if local path was changed (#1948)
* Mon Jun 23 2014 freitag@owncloud.com
  version 1.6.1 rc1
  * Fix 'precondition failed' bug with broken upload
  * Fix openSSL problems for windows deployment
  * Fix syncing a folder with '#' in the name
  * Fix #1845: do not update parent directory etag before sub
    directories are removed
  * Fix reappearing directories if dirs are removed during its
    upload
  * Fix app version in settings dialog, General tab
  * Fix crash in FolderWizard when going offline
  * Shibboleth fixes
  * More specific error messages (file remove during upload, open
    local sync file)
  * Use QSet rather than QHash in SyncEngine (save memory)
  * Fix some memory leaks
  * Fix some thread race problems, ie. wait for neon thread to finish
    before the propagator is shut down
  * Fix a lot of issues and warnings found by Coverity
  * Fix Mac some settings dialog problems
* Wed May 28 2014 danimo@owncloud.com
  version 1.6.0rc3
  * Avoid data loss when a client file system is not case sensitive
* Fri May 16 2014 danimo@owncloud.com
  version 1.6.0rc2
  * Fix an infinite sync loop
* Thu May 15 2014 freitag@owncloud.com
  version 1.6.0rc1
  * Fix SSL error with previously-expired CAs on Windows
  * Fix incorrect folder pause state after start
  * Fix a couple of actual potential crashes
  * Improve Cookie support (e.g. for cookie-based load-balancers)
  * Introduce a general timeout of 300s for network operations
  * Improve error handling, blacklisting
  * Job-based change propagation, enables faster parallel up/downloads
    (right now only if no bandwidth limit is set and no proxy is used)
  * Significantly reduced CPU load when checking for local and remote changes
  * Speed up file stat code on Windows
  * Enforce Qt5 for Windows and Mac OS X builds
  * Improved owncloudcmd: SSL support, documentation
  * Added advanced logging of operations (file .???.log in sync
    directory)
  * Avoid creating a temporary copy of the sync database (.ctmp)
  * Enable support for TLS 1.2 negotiation on platforms that use
    Qt 5.2 or later
  * Forward server exception messages to client error messages
  * Mac OS X: Support Notification Center in OS X 10.8+
  * Mac OS X: Use native settings dialog
  * Mac OS X: Fix UI inconsistencies on Mavericks
  * Shibboleth: Warn if authenticating with a different user
  * Remove vio abstraction in csync
* Wed Apr 30 2014 freitag@owncloud.com
- Switch SKIP_RPATH OFF for building.
* Tue Apr 29 2014 freitag@owncloud.com
- Fix private install directory.
* Tue Apr 29 2014 freitag@owncloud.com
- Update autostart diff
* Tue Apr 29 2014 freitag@owncloud.com
  version 1.6.0 (release 2014-04- )
  * Minor GUI improvements
  * Qt5 compile issues fixed
  * Ignore sync log file in filewatcher
  * Install libocsync to private library dir and use rpath to localize
  * Fix reconnect after server disconnect
  * Fix crashes
  * Fix "unknown action" display in Activity window
  * Fix memory leaks
  * Respect XDG_CONFIG_HOME environment var
  * Handle empty fileids in the journal correctly
  * Add abilility to compile libowncloudsync without GUI dependendy
* Thu Mar  6 2014 freitag@owncloud.com
- Use proper qtprefix for libqtkeychain dependency
* Wed Mar  5 2014 freitag@owncloud.com
- Update to final RC tarball.
* Wed Mar  5 2014 freitag@owncloud.com
- Update to owncloud client version 1.5.3 rc1
* Thu Feb 13 2014 freitag@owncloud.com
- improve wrapper script, let read neons env file.
* Wed Feb 12 2014 freitag@owncloud.com
- Do more tweaks for CentOS/RHEL
* Wed Feb 12 2014 freitag@owncloud.com
- Adjusted build deps to also build on CentOS
- Detect if documentation can be built and disable if can not.
* Tue Feb  4 2014 freitag@owncloud.com
- Remove build dependency on libocsync-dev for debian.
* Tue Feb  4 2014 freitag@owncloud.com
- Tarball update again.
* Tue Feb  4 2014 freitag@owncloud.com
- Update to version 1.5.1rc1
* Tue Feb  4 2014 freitag@owncloud.com
- Finally make the debian based packages build.
* Sun Feb  2 2014 freitag@owncloud.com
- l10n subpackage for Debian. WIP.
* Fri Jan 31 2014 freitag@owncloud.com
- commit spec file only with l10n subpackage.
* Tue Jan 28 2014 freitag@owncloud.com
- Fix Fedora dependencies, added sqlite3 dep.
* Tue Jan 28 2014 freitag@owncloud.com
- Fixes in debian build files and dependency fixes.
* Sun Dec  8 2013 freitag@owncloud.com
- Another attempt to fix deb control
* Sun Dec  8 2013 freitag@owncloud.com
- Splitted dev package.
* Thu Nov 21 2013 freitag@owncloud.com
- Removed not longer needed dependency on ocsync plugin package.
* Wed Nov 13 2013 freitag@owncloud.com
- Make nightly builds work again.
* Tue Nov 12 2013 freitag@owncloud.com
- Build requires libocsync-plugin-owncloud now because of libhttpbf
  dependency in mirall.
* Wed Jul 31 2013 freitag@owncloud.com
- Removed debug level sub package again.
* Tue Jul 30 2013 danimo@owncloud.com
- Updates for 1.4
* Wed May 22 2013 danimo@owncloud.com
- Remove obsolete dependencies, add qt4-dbus dependency.
* Fri May  3 2013 freitag@owncloud.com
- Added back the build dep to the oxygen icons to have the directories.
* Thu Apr 18 2013 freitag@owncloud.com
- Added explicit requires on libocsync0 for fedora based.
- Removed not longer used Source1 tag.
* Thu Feb 21 2013 freitag@owncloud.com
- fixed project url to github.
* Wed Feb 20 2013 freitag@owncloud.com
- copy over from :devel to :devel:daily.
* Sun Feb  3 2013 freitag@owncloud.com
- Remved extra installed desktop file from deb packages, comes out
  of the source package now.
* Wed Jan 23 2013 freitag@owncloud.com
- Update to version 1.2.0, ocsync 0.70.3 required.
  * [GUI] New status dialog to show a detailed list of synced files.
  * [GUI] New tray notifications about synced files.
  * [GUI] New platform specific icon set.
  * [App] Using cross platform QtKeychain library to store credentials crypted.
  * [App] Use cross platform notification for changes in the local file system rather than regular poll.
  * [Fixes] Improved SSL Certificate handling and SSL fixes troughout syncing.
  * [Fixes] Fixed proxy authentication.
  * [Fixes] Allow brackets in folder name alias.
  * [Fixes] Lots of other minor fixes.
  * [Platform] cmake fixes.
  * [Platform] Improved, more detailed error reporting.
* Thu Jan 17 2013 freitag@owncloud.com
- Fix deb build.
* Thu Jan 17 2013 freitag@owncloud.com
- Fixed building with package desktop file.
* Thu Jan 17 2013 freitag@owncloud.com
- Update to second beta version of 1.2.0
* Fri Dec 21 2012 freitag@owncloud.com
- Update to first beta version of 1.2.0
* Thu Nov 22 2012 freitag@owncloud.com
  version 1.1.2rc (release 2012-11-22), csync 0.60.2 required
  * [Fixes] Allow to properly cancel the password dialog.
  * [Fixes] Share folder name correctly percent encoded with old Qt
    4.6 builds ie. Debian.
  * [Fixes] If local sync dir is not existing, create it.
  * [Fixes] lots of other minor fixes.
  * [GUI] Display error messages in status dialog.
  * [GUI] GUI fixes for the connection wizard.
  * [GUI] Show username for connection in statusdialog.
  * [GUI] Show intro wizard on new connection setup.
  * [APP] Use CredentialStore to better support various credential
    backends.
  * [APP] Handle missing local folder more robust: Create it if
    missing instead of ignoring.
  * [APP] Simplify treewalk code.
  * [Platform] Fix Mac building
* Thu Oct 18 2012 danimo@owncloud.com 
- /etc/owncloud -> /etc/ownCloud
* Thu Oct 18 2012 danimo@owncloud.com 
  version 1.1.1 (release 2012-10-18), csync 0.60.1 required
  * [GUI]   Allow changing folder name in single folder mode
  * [GUI]   Windows: Add license to installer
  * [GUI]   owncloud --logwindow will bring up the log window
    in an already running instance
  * [Fixes] Make sure SSL errors are always handled
  * [Fixes] Allow special characters in folder alias
  * [Fixes] Proper workaround for Menu bug in Ubuntu
  * [Fixes] csync: Fix improper memory cleanup which could
    cause memory leaks and crashes
  * [Fixes] csync: Fix memory leak
  * [Fixes] csync: Allow single quote (') in file names
  * [Fixes] csync: Remove stray temporary files
* Wed Oct 10 2012 freitag@owncloud.com
  version 1.1.0 (release 2012-10-10 ), ocsync 0.60.0 required
  * 
  * [GUI]   Added an about dialog
  * [GUI]   Improved themeing capabilities of the client.
  * [GUI]   Minor fixes in folder assistant.
  * [GUI]   Reworked tray context menu.
  * [GUI]   Users can now sync the server root folder.
  * [Fixes] Proxy support: now supports Proxy Auto-Configuration (PAC)
    on Windows, reliability fixes across all OSes.
  * [Fixes] Url entry field in setup assistant handles http/https correctly.
  * [Fixes] Button enable state in status dialog.
  * [Fixes] Crash fixed on ending the client, tray icon related.
  * [Fixes] Crash through wrong delete operator.
  * [MacOS] behave correctly on retina displays.
  * [MacOS] fix focus policy.
  * [MacOS] Packaging improvements.
  * [MacOS] Packaging improvements.
  * [Platform] Windows: Setup closes client prior to uninstall.
  * [Platform] Windows: ownCloud gets added to autorun by default.
  * [Platform] insert correct version info from cmake.
  * [Platform] csync conf file and database were moved to the users app data
    directory, away from the .csync dir.
  * Renamed exclude.lst to sync-exclude.lst and moved it to
    /etc/appName()/ for more clean packaging. From the user path,
    still exclude.lst is read if sync-exclude.lst is not existing.
  * Placed custom.ini with customization options to /etc/appName()
* Fri Oct  5 2012 freitag@owncloud.com
- Update to v1.1.0beta3 - ocsync 0.50.11 needed
* Thu Sep 20 2012 freitag@owncloud.com
- Update to v1.1.0beta2 - csync 0.50.10 needed
* Fri Aug 31 2012 msrex@owncloud.com
- Update to v1.1.0beta1 - csync 0.50.9 needed
  Required ownCloud v4.5 on the server side
* Tue Aug 14 2012 freitag@owncloud.com
- version 1.0.5 (release 2012-08-14), csync 0.50.8 required
  * [Fixes] Fixed setup dialog: Really use https if checkbox is activated.
* Mon Aug 13 2012 freitag@owncloud.com
- do not remove the unneeded libmirallsync.so to satisfy automatic
  dependency tracking.
* Fri Aug 10 2012 freitag@owncloud.com
- version 1.0.4 (release 2012-08-10), csync 0.50.8 required
  * [APP] ownCloud is now a single instance app, can not start twice any more.
  * [APP] Proxy support
  * [APP] Handle HTTP redirection correctly, note new url.
  * [APP] More relaxed handling of read only directories in the sync paths.
  * [APP] Started to split off a library with sync functionality, eg for KDE
  * [APP] Make ownCloud Info class a singleton, more robust.
  * [GUI] New, simplified connection wizard.
  * [GUI] Added ability for customized theming.
  * [GUI] Improved icon size handling.
  * [GUI] Removed Log Window Button, log available through command line.
  * [GUI] Proxy configuration dialog added.
  * [GUI] Added Translations to languages Slovenian, Polish, Catalan,
    Portuguese (Brazil), German, Greek, Spanish, Czech, Italian, Slovak,
    French, Russian, Japanese, Swedish, Portuguese (Portugal)
    all with translation rate >90%%.
  * [Fixes] Loading of self signed certs into Networkmanager (#oc-843)
  * [Fixes] Win32: Handle SSL dll loading correctly.
  * [Fixes] Many other small fixes and improvements.
* Wed Jul 18 2012 freitag@owncloud.com
- Fixed version in the desktop file
* Fri Jun 22 2012 freitag@owncloud.com
- version 1.0.3 (release 2012-06-19), csync 0.50.7 required
  * [GUI] Added a log window which catches the logging if required and
    allows to save for information.
  * [CMI] Added options --help, --logfile and --logflush
  * [APP] Allow to specify sync frequency in the config file.
  * [Fixes] Do not use csync database files from a sync before.
  * [Fixes] In Connection wizard, write the final config onyl if
    the user really accepted. Also remove the former database.
  * [Fixes] Allow special characters in the sync directory names
  * [Fixes] Win32: Fixed directory removal with special character dirs.
  * [Fixes] MacOS: Do not flood the system log any more
  * [Fixes] MacOS: Put app translations to correct places
  * [Fixes] Win32: Fix loading of csync state db.
  * [Fixes] Improved some english grammar.
  * [Platform] Added krazy2 static code checks.
* Wed May 16 2012 freitag@owncloud.com
- version 1.0.2 (release 18.5.2012), csync 0.50.6 required
  * [GUI] New icon set for ownCloud client
  * [GUI] No splashscreen any more (oC Bug #498)
  * [GUI] Russian translation added
  * [GUI] Added 'open ownCloud' to traymenu
  * [GUI] "Pause" and "Resume" instead of Enable/Disable
  * [Fixes] Long running syncs can be interrupted now.
  * [Fixes] Dialogs comes to front on click
  * [Fixes] Open local sync folder from tray and status for win32
  * [Fixes] Load exclude.lst correctly on MacOSX
* Fri May 11 2012 freitag@owncloud.com
- updated tarball to beta of next release 1.0.2
* Thu May 10 2012 msrex@owncloud.com
- updated debian dependencies around time syncing
* Tue May  1 2012 msrex@owncloud.com
- Correct installation of .desktop file in debian
* Fri Apr 20 2012 msrex@owncloud.com
- change dependencies again on non-SUSE platforms
* Thu Apr 19 2012 msrex@owncloud.com
- fix dependency for libiniparser on non-SUSE platforms
* Wed Apr 18 2012 freitag@opensuse.org
- version 1.0.1 (release 2012-04-18), csync 0.50.5 required
  * [Security] Support SSL Connections
  * [Security] SSL Warning dialog
  * [Security] Do not store password in clear text anymore
  * [Security] Restrict credentials to the configured host
  * [Security] Added ability to forbid local password storage.
  * [Fixes] Various fixes of the startup behaviour.
  * [Fixes] Various fixes in sync status display
  * [GUI] Various error messages for user display improved.
  * [GUI] fixed terms and Translations
  * [GUI] fixed translation loading
  * [Intern] Migrate old credentials to new format
  * [Intern] Some code refactorings, got rid of rotten QWebDav lib
  * [Intern] lots of cmake cleanups
  * [Platform] MacOSX porting efforts
  * [Platform] MacOSX Bundle creation added
  * [Platform] Enabled ranslations on Windows.
* Wed Apr 18 2012 msrex@owncloud.com
- fix typo in debian dependencies
* Wed Apr 18 2012 msrex@owncloud.com
- more debian / ubuntu packaging
* Wed Apr 18 2012 msrex@owncloud.com
- add debian / ubuntu packaging
* Tue Apr  3 2012 freitag@opensuse.org
- removed requirement on rubygem, not needed for this client.
* Mon Apr  2 2012 msrex@suse.de
- change minimum csync version required
* Mon Apr  2 2012 freitag@opensuse.org
- update to version 1.0.0
* Sun Apr  1 2012 msrex@owncloud.com
- renamed package mirall to owncloud-client
- new descriptions
