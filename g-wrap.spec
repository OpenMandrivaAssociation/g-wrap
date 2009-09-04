%define major 2
%define modules_major 0
%define lib_name %mklibname %{name} %{major}
%define devel_name %mklibname %{name} -d
%define epoch 1

Summary: A tool for creating Scheme interfaces to C libraries
Name: g-wrap
Version: 1.9.11
Release: %mkrel 3
Source0: http://download.savannah.gnu.org/releases/g-wrap/%{name}-%{version}.tar.gz
# gw fedora patches
#Patch: g-wrap-1.9.6-glib2.patch
Patch1: g-wrap-consistent.patch
Patch2: g-wrap-info.patch
Patch3: g-wrap-1.9.11-ffi-pkgconfig.patch
Requires: guile
Requires: %{lib_name} = %{epoch}:%{version}-%{release}
Group: System/Libraries
BuildRequires: guile-devel
BuildRequires: glib2-devel
BuildRequires: ffi5-devel
BuildRequires: automake1.9
License: LGPLv2+
Epoch: %{epoch}
URL: http://www.gnucash.org
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
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
#%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

aclocal -I m4
autoconf
automake

%build
# --disable-Werror required for gcc-4.3 & g-wrap-1.9.11:
# core-runtime.c:55: warning: ignoring return value of 'vasprintf', declared with attribute warn_unused_result
%configure2_5x  --disable-static --disable-Werror
		
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall_std 
#%multiarch_includes %buildroot%{_includedir}/%name/ffi-support.h

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{lib_name}
%endif

%post -n %{devel_name}
%_install_info %{name}.info

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{lib_name}
%endif

%postun -n %{devel_name}
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS
%{_datadir}/guile/site/*

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
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/%{name}/modules/*.so
%{_libdir}/%{name}/modules/*.la
%{_infodir}/%{name}*
%{_datadir}/aclocal/%{name}.m4
%_libdir/pkgconfig/g-wrap-2.0-guile.pc

