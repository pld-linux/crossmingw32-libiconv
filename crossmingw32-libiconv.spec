%define		realname		libiconv
Summary:	Character set conversion library - mingw32 cross version
Summary(pl):	Biblioteka konwersji zestawów znaków - wersja skro¶na dla mingw32
Name:		crossmingw32-%{realname}
Version:	1.9.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/libiconv/%{realname}-%{version}.tar.gz
# Source0-md5:	0c99a05e0c3c153bac1c960f78711155
Patch0:		%{name}.patch
URL:		http://www.gnu.org/software/libiconv/
#BuildRequires:	autoconf >= 2.57
#BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
#BuildRequires:	libtool
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}

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
%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target=%{target} \
	--host=%{target_platform} \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_bindir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_bindir}/libcharset-1.dll
%{_bindir}/libiconv-2.dll
%{_libdir}/libcharset.dll.a
%{_libdir}/libcharset.la
%{_libdir}/libiconv.dll.a
%{_libdir}/libiconv.la
%{_libdir}/charset.alias
%{_includedir}/*.h
