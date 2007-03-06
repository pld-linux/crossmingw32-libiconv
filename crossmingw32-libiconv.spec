Summary:	Character set conversion library - mingw32 cross version
Summary(pl.UTF-8):	Biblioteka konwersji zestawów znaków - wersja skrośna dla mingw32
%define		_realname   libiconv
Name:		crossmingw32-%{_realname}
Version:	1.11
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	ftp://ftp.gnu.org/gnu/libiconv/%{_realname}-%{version}.tar.gz
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
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch alpha sparc sparc64 sparcv9
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

%package static
Summary:	Static iconv libraries (cross mingw32 version)
Summary(pl.UTF-8):	Statyczne biblioteki iconv (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static iconv libraries (cross mingw32 version).

%description static -l pl.UTF-8
Statyczne biblioteki iconv (wersja skrośna mingw32).

%package dll
Summary:	DLL iconv libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL iconv dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL iconv libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL iconv dla Windows.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub libcharset/autoconf
cp -f /usr/share/automake/config.sub autoconf
%configure \
	--target="%{target}" \
	--host="%{target}" \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_dlldir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# not used on win32
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
# runtime only
rm -f $RPM_BUILD_ROOT%{_bindir}/iconv
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

rm -rf $RPM_BUILD_ROOT%{_datadir}/{doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libcharset.dll.a
%{_libdir}/libiconv.dll.a
%{_libdir}/libcharset.la
%{_libdir}/libiconv.la
%{_includedir}/iconv.h
%{_includedir}/libcharset.h
%{_includedir}/localcharset.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcharset.a
%{_libdir}/libiconv.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libcharset-*.dll
%{_dlldir}/libiconv-*.dll
