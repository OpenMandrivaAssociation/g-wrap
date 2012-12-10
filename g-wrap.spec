%define major 2
%define modules_major 0
%define lib_name %mklibname %{name} %{major}
%define devel_name %mklibname %{name} -d
%define epoch 1

Summary: A tool for creating Scheme interfaces to C libraries
Name: g-wrap
Version: 1.9.14
Release: 1
Source0: http://download.savannah.gnu.org/releases/g-wrap/%{name}-%{version}.tar.gz
source1: .abf.yml
# gw fedora patches
Requires: guile
Requires: %{lib_name} = %{epoch}:%{version}-%{release}
Group: System/Libraries
BuildRequires: guile-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: ffi5-devel
BuildRequires: automake1.9
buildrequires: gettext-devel
License: LGPLv2+
Epoch: %{epoch}
URL: http://www.gnucash.org
Conflicts: guile-lib

%description
g-wrap is a tool for creating Scheme interfaces to C libraries.  At
the moment it is most heavily focused on providing access to C
libraries from guile, but it also supports RScheme.

%package -n %{lib_name}
Epoch: %{epoch}
Group:	%{group}
Summary: %{summary}

%description -n %{lib_name}
g-wrap is a tool for specifying types, functions, and constants to
import into a Scheme interpreter, and for generating code (in C) to
interface these to the Guile and RScheme interpreters in particular.

%package -n %{devel_name}
Epoch: %{epoch}
Group:	Development/C
Summary: Include files and libraries needed for g-wrap development
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{lib_name} = %{epoch}:%{version}-%{release}
Obsoletes: %{_lib}g-wrap0-devel
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}

%description -n %{devel_name}
g-wrap is a tool for creating Scheme interfaces to C libraries.  At
the moment it is most heavily focused on providing access to C
libraries from guile, but it also supports RScheme.

You can provide access to a given C API by creating a specification
file describing the interface you want published at the Scheme level.
g-wrap will handle generating all the lower level library interface
code so that the C library shows up as a set of Scheme functions.

You should install this package if you need to compile programs that
need to use g-wrap C<->Scheme functionality

%prep
%setup -q

touch config.rpath
aclocal -I m4
autoconf
automake

%build
# --disable-Werror required for gcc-4.3 & g-wrap-1.9.11:
# core-runtime.c:55: warning: ignoring return value of 'vasprintf', declared with attribute warn_unused_result
%configure2_5x  --disable-static --disable-Werror
		
make

%install

%makeinstall_std 
#%multiarch_includes %buildroot%{_includedir}/%name/ffi-support.h

%post -n %{devel_name}
%_install_info %{name}.info

%postun -n %{devel_name}
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS
%{_datadir}/guile/site/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/%{name}/modules/*.so.%{modules_major}*

%files -n %{devel_name}
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/g-wrap-wct.h
%{_includedir}/%name
#%multiarch %_includedir/multiarch*/%name/ffi-support.h
%{_libdir}/*.so
%{_libdir}/%{name}/modules/*.so
%{_infodir}/%{name}*
%{_datadir}/aclocal/%{name}.m4
%_libdir/pkgconfig/g-wrap-2.0-guile.pc



%changelog
* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 1:1.9.11-2mdv2009.0
+ Revision: 282423
- Fix g-wrap requires, so that it becomes installable

* Fri Sep 05 2008 Emmanuel Andry <eandry@mandriva.org> 1:1.9.11-1mdv2009.0
+ Revision: 281352
- New version
- change major (0 > 2)
- drop patches 0 and 3
- add pkgconfig patch
- check major
- update file list
- BR ffi5-devel

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sun Feb 18 2007 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2007-02-18 18:08:29 (122489)
- rebuild to fix libguile dep for ppc

* Sun Jan 07 2007 Götz Waschk <waschk@mandriva.org> 1.9.6-9mdv2007.1
+ 2007-01-07 13:46:17 (105203)
- Import g-wrap

* Sun Jan 07 2007 Götz Waschk <waschk@mandriva.org> 1.9.6-9mdv2007.1
- unpack patches

* Tue Aug 29 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-8mdv2007.0
- fix buildrequires

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-7mdv2007.0
- rebuild

* Fri Jun 23 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-6mdv2007.0
- use bundled libffi
- add fedora patches for libffi

* Fri Jun 16 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-5mdv2007.0
- conflict with guile-lib

* Thu Jun 15 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-4mdv2007.0
- add missing info entry
- fix build if old version is installed
- patch to build with glib2

* Fri Mar 03 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.9.6-3mdk
- add BuildRequires: guile-lib

* Fri Feb 24 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-2mdk
- fix buildrequires

* Mon Feb 20 2006 Götz Waschk <waschk@mandriva.org> 1.9.6-1mdk
- multiarch
- update file list
- major 0
- reenable libtoolize
- new version

* Fri Jan 07 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.4-12mdk
- libtool 1.4 fixes

* Fri Dec 31 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.3.4-11mdk
- add BuildRequires: libglib-devel libgtk+-devel

* Thu Feb 26 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.4-10mdk
- Fix dependency

