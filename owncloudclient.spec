
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
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}%{_docdir}/html ${RPM_BUILD_ROOT}%{_docdir}/%{name}
mv ${RPM_BUILD_ROOT}%{_docdir}/latex ${RPM_BUILD_ROOT}%{_docdir}/%{name}
rm ${RPM_BUILD_ROOT}%{_docdir}/%{name}/unthemed/.buildinfo

#%find_lang owncloud

%post
/bin/%update_icon_cache_post hicolor &>/dev/null || :
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    /bin/%update_icon_cache_post hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/sbin/ldconfig

%files
#-n %{name}.lang
%defattr(644,root,root,755)
%doc README.md COPYING
%doc %{_docdir}/%{name}
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/*/*/apps/*.png
#%{_iconsdir}/hicolor
#%config %{_sysconfdir}/ownCloud
#%{_datadir}/owncloud
%{_libdir}/libowncloudsync.so.*
%{_libdir}/owncloud/libocsync.so.*
#%dir %{_libdir}/owncloud
#%{_libdir}/libowncloudsync.so
#%{_libdir}/owncloud/libocsync.so
#%{_includedir}/owncloudsync/
%{_datadir}/nautilus-python/extensions/syncstate.py*
%{_datadir}/nemo-python/extensions/syncstate.py*
%{_mandir}/man1/owncloud*

%clean
rm -rf $RPM_BUILD_ROOT
