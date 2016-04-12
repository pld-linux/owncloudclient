
Summary:	The ownCloud client
Name:		owncloudclient
Version:	2.1.1
Release:	0.2
License:	GPL-2.0+
Group:		X11/Applications
URL:		https://www.owncloud.com
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.xz
# Source0-md5:	63a971158201a8dffe96a02c54b86819
#Source1:	owncloud.sh
#Source2:	owncloudcmd.sh
BuildRequires:	cmake >= 2.8.11
#BuildRequires:	qt4-devel >= 4.7
#BuildRequires:	qtwebkit-devel >= 2.2
BuildRequires:	desktop-file-utils
BuildRequires:	openssl-devel
BuildRequires:	python-Sphinx
BuildRequires:	sphinx-pdg
BuildRequires:	texlive-latex-ams
BuildRequires:	QtKeychain-devel
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
%setup -q
# autostart_use_wrapper.diff
#patch1 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DQTKEYCHAIN_INCLUDE_DIR=/usr/include/qtkeychain \
	-DQTKEYCHAIN_LIBRARY=/usr/%{_lib}/libqtkeychain.so \
	../
%{__make}

# documentation here?
if [ -e conf.py ];
then
  # for old cmake versions we need to move the conf.py.
  mv conf.py doc/
fi

%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

  install -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  mv ${RPM_BUILD_ROOT}%{_docdir}/client/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/client
  rm ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/.buildinfo
  mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed

  install -d ${RPM_BUILD_ROOT}%{_mandir}man1
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloud.1,owncloud.1}
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloudcmd.1,owncloudcmd.1}

%define extdir ${RPM_BUILD_ROOT}%{_datadir}/nautilus-python/extensions
test -f %{extdir}/ownCloud.py  && mv %{extdir}/ownCloud.py  %{extdir}/owncloud.py  || true
test -f %{extdir}/ownCloud.pyo && mv %{extdir}/ownCloud.pyo %{extdir}/owncloud.pyo || true
test -f %{extdir}/ownCloud.pyc && mv %{extdir}/ownCloud.pyc %{extdir}/owncloud.pyc || true

install -d ${RPM_BUILD_ROOT}/%{optdir}/bin
mv ${RPM_BUILD_ROOT}/%{_bindir}/owncloud* ${RPM_BUILD_ROOT}/%{optdir}/bin/

cp -p %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/owncloud
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}/owncloudcmd

%check
## use exit 0 instead of exit 1 to turn this into warnings:
if [ "%{name}" != "testpilotcloud-client" ]; then
  if [ "%{prerelease}" == "" ]; then
    expr match '%{distribution}' '.*:community:\(testing\|nightly\)' && { echo "Error: Need a prerelease here, not %{version}"; exit 1; }
  else
    expr match '%{distribution}' '.*:community:desktop' && { echo "Error: Must not have a prerelease here, not %{version}"; exit 1; }
  fi
fi

%post
/bin/%update_icon_cache_post hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/%update_icon_cache_post hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

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
%doc %{_docdir}/%{name}

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
