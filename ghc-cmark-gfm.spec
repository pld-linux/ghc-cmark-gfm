#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	cmark-gfm
Summary:	Fast, accurate GitHub Flavored Markdown parser and renderer
Summary(pl.UTF-8):	Szybki, dokładny parser i renderer formatu Markdown w wariancie Githuba
Name:		ghc-%{pkgname}
Version:	0.2.1
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/cmark-gfm
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	152d0e1bae76dc1c29ff9edf221dcf4f
URL:		http://hackage.haskell.org/package/cmark-gfm
# for ghc <7.6 also ghc-ghc-prim >= 0.2
BuildRequires:	ghc >= 7.6
BuildRequires:	ghc-base >= 4.5
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-text >= 1.0
BuildRequires:	ghc-text < 1.3
%if %{with prof}
BuildRequires:	ghc-prof >= 7.6
BuildRequires:	ghc-base-prof >= 4.5
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-text-prof >= 1.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.5
Requires:	ghc-bytestring
Requires:	ghc-text >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides Haskell bindings for libcmark-gfm, the reference
parser for GitHub Flavored Markdown, a fully specified variant of
Markdown. It includes sources for libcmark-gfm (0.29.0.gfm.0) and does
not require prior installation of the C library.

%description -l pl.UTF-8
Ten pakiet zawiera wiązania Haskella do libcmark-gfm - referencyjnego
parsera formatu Markdown w wariancie GitHuba (GitHub Flavored
Markdown) - w pełni wyspecyfikowanym wariancie Markdown. Zawiera
źródła libcmark-gfm (0.29.0.gfm.0) i nie wymaga wcześniejszej
instalacji biblioteki C.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.5
Requires:	ghc-bytestring-prof
Requires:	ghc-text-prof >= 1.0

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.md changelog %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%endif
