%define		realname		libiconv
%define		snapshot		2003.02.01-1
Summary:	Character set conversion library - mingw32 cross version
Summary(pl):	Biblioteka konwersji zestawów znaków - wersja skro¶na dla mingw32
Name:		crossmingw32-%{realname}
Version:	1.8
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mingw/%{realname}-%{version}-%{snapshot}-src.tar.bz2
# Source0-md5:	3cda71fd0e14d5f5fa4eca85f053eaea
Patch0:		crossmingw32-libiconv.patch
URL:		http://www.gnu.org/software/libiconv/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	gtk-doc >= 0.9-4
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.1-8.2
BuildRoot:	%{tmpdir}/%{realname}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
The libiconv library provides an iconv() implementation, for use on
systems which don't have one, or whose implementation cannot convert
from/to Unicode.

This package contains the cross version for mingw32.

%description -l pl
Ta biblioteka dostarcza implementacjê iconv() do u¿ywania z systemami,
które takiej funkcji nie posiadaj±, lub na których implementacja nie
potrafi konwertowaæ z/do Unikodu.

Ten pakiet zawiera wersjê skro¶n± dla mingw32.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS

rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}

%configure \
	--target=%{target} \
	--host=%{target_platform} \
	--prefix=%{arch} \
	--disable-static \
	--bindir=%{arch}/bin \
	--libdir=%{arch}/lib \
	--includedir=%{arch}/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}
