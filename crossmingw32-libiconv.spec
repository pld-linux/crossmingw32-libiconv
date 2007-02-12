%define		realname		libiconv
Summary:	Character set conversion library - mingw32 cross version
Summary(pl.UTF-8):	Biblioteka konwersji zestawów znaków - wersja skrośna dla mingw32
Name:		crossmingw32-%{realname}
Version:	1.11
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/libiconv/%{realname}-%{version}.tar.gz
# Source0-md5:	b77a17e4a5a817100ad4b2613935055e
Patch0:		%{name}.patch
URL:		http://www.gnu.org/software/libiconv/
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
# because of broken w32 relink in libtool
BuildConflicts:	crossmingw32-libiconv < 1.10
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}

%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
The libiconv library provides an iconv() implementation, for use on
systems which don't have one, or whose implementation cannot convert
from/to Unicode.

This package contains the cross version for mingw32.

%description -l pl.UTF-8
Ta biblioteka dostarcza implementację iconv() do używania z systemami,
które takiej funkcji nie posiadają, lub na których implementacja nie
potrafi konwertować z/do Unikodu.

Ten pakiet zawiera wersję skrośną dla mingw32.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub libcharset/autoconf
cp -f /usr/share/automake/config.sub autoconf
%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target="%{target}" \
	--host="%{target_platform}" \
	--enable-static

%{__make}

%if 0%{!?debug:1}
%{target}-strip {,libcharset/}lib/.libs/*.dll
%{target}-strip -g -R.comment -R.note {,libcharset/}lib/.libs/*.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install {,libcharset/}lib/.libs/*.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/*
%{_includedir}/*.h

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
