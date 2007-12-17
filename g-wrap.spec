%define major 0
%define lib_name %mklibname %{name} %{major}

Summary: A tool for creating Scheme interfaces to C libraries
Name: g-wrap
Version: 1.9.6
Release: %mkrel 10
Source0: http://download.savannah.gnu.org/releases/g-wrap/%{name}-%{version}.tar.bz2
# gw fedora patches
Patch: g-wrap-1.9.6-glib2.patch
Patch1: g-wrap-consistent.patch
Patch2: g-wrap-info.patch
# gw the runtime is linked with ffi, so the gw lib needs it too
Patch3: g-wrap-1.9.6-ffilink.patch
Requires: guile >= 1.6
Group: System/Libraries
BuildRequires: guile-devel >= 1.6
BuildRequires: glib2-devel
BuildRequires: libffi-devel
BuildRequires: automake1.9
License: GPL
Epoch: 1
URL: http://www.gnucash.org
Requires: %{lib_name} >= %{epoch}:%{version}-%{release}
Conflicts: guile-lib

%description
g-wrap is a tool for creating Scheme interfaces to C libraries.  At
the moment it is most heavily focused on providing access to C
libraries from guile, but it also supports RScheme.

%package -n %{lib_name}
Epoch: 1
Group:	%{group}
Summary: %{summary}

%description -n %{lib_name}
g-wrap is a tool for specifying types, functions, and constants to
import into a Scheme interpreter, and for generating code (in C) to
interface these to the Guile and RScheme interpreters in particular.

%package -n %{lib_name}-devel
Epoch: 1
Group:	Development/C
Summary: Include files and libraries needed for g-wrap development
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{lib_name} = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-devel
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
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
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
aclocal-1.9 -I m4
autoconf
automake-1.9

%build
%configure2_5x --disable-static

make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall_std 
%multiarch_includes %buildroot%{_includedir}/%name/ffi-support.h

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig -n %{lib_name}

%post -n %{lib_name}-devel
%_install_info %{name}.info

%postun -p /sbin/ldconfig -n %{lib_name}

%postun -n %{lib_name}-devel
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS
%{_datadir}/guile/*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.la

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/g-wrap-wct.h
%{_includedir}/%name
%multiarch %_includedir/multiarch*/%name/ffi-support.h
%{_libdir}/*.so
%{_infodir}/%{name}*
%_libdir/pkgconfig/g-wrap-2.0-guile.pc

