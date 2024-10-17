%define major 2
%define modules_major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	A tool for creating Scheme interfaces to C libraries
Name:		g-wrap
Version:	1.9.14
Release:	4
Epoch:		1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.gnucash.org
Source0:	http://download.savannah.gnu.org/releases/g-wrap/%{name}-%{version}.tar.gz
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(guile-2.0)
BuildRequires:	pkgconfig(libffi)
#BuildRequires:	automake1.9
Requires:	guile
Conflicts:	guile-lib

%description
g-wrap is a tool for creating Scheme interfaces to C libraries.  At
the moment it is most heavily focused on providing access to C
libraries from guile, but it also supports RScheme.

%files
%doc AUTHORS ChangeLog INSTALL NEWS README THANKS
%{_datadir}/guile/site/*
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for g-wrap
Group:		System/Libraries

%description -n %{libname}
g-wrap is a tool for specifying types, functions, and constants to
import into a Scheme interpreter, and for generating code (in C) to
interface these to the Guile and RScheme interpreters in particular.

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/%{name}/modules/*.so.%{modules_major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and libraries needed for g-wrap development
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
g-wrap is a tool for creating Scheme interfaces to C libraries.  At
the moment it is most heavily focused on providing access to C
libraries from guile, but it also supports RScheme.

You can provide access to a given C API by creating a specification
file describing the interface you want published at the Scheme level.
g-wrap will handle generating all the lower level library interface
code so that the C library shows up as a set of Scheme functions.

You should install this package if you need to compile programs that
need to use g-wrap C<->Scheme functionality

%files -n %{devname}
%{_bindir}/*
%{_includedir}/g-wrap-wct.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/%{name}/modules/*.so
%{_infodir}/%{name}*
%{_datadir}/aclocal/%{name}.m4
%{_libdir}/pkgconfig/g-wrap-2.0-guile.pc

#----------------------------------------------------------------------------

%prep
%setup -q

touch config.rpath
aclocal -I m4
autoconf
automake --add-missing

%build
# --disable-Werror required for gcc-4.3 & g-wrap-1.9.11:
# core-runtime.c:55: warning: ignoring return value of 'vasprintf', declared with attribute warn_unused_result
%configure2_5x \
	--disable-static \
	--disable-Werror
make

%install
%makeinstall_std

