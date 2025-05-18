# TODO: enable docs (make sphinxcontrib_zopeext compatible with current sphinx-pdg-3)
#
# Conditional build:
%bcond_with	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module		ZODB
Summary:	Python object-oriented database
Summary(pl.UTF-8):	Pythonowa zorientowana obietowo baza danych
Name:		python3-%{module}
Version:	6.0.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zodb/
Source0:	https://files.pythonhosted.org/packages/source/Z/ZODB/zodb-%{version}.tar.gz
# Source0-md5:	2d4d61cc48c56a3234c918d11d454aef
URL:		https://zodb.org/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-BTrees >= 4.2.0
BuildRequires:	python3-ZConfig
BuildRequires:	python3-manuel
BuildRequires:	python3-persistent >= 4.4.0
BuildRequires:	python3-transaction >= 2.4
BuildRequires:	python3-zc.lockfile
BuildRequires:	python3-zodbpickle >= 1.0.1
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.testing
BuildRequires:	python3-zope.testrunner >= 4.4.6
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-j1m.sphinxautozconfig
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-zopeext
BuildRequires:	sphinx-pdg-3 < 7
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZODB provides an object-oriented database for Python that provides a
high-degree of transparency.

- no separate language for database operations
- very little impact on your code to make objects persistent
- no database mapper that partially hides the database.
- almost no seam between code and database.

ZODB is an ACID Transactional database.

%description -l pl.UTF-8
ZODB dostarcza obiektowo zorientowaną bazę danych dla Pythona,
zapewniającą duży stopień przezroczystości.

- brak osobnego języka dla operacji bazodanowych
- bardzo mały wpływ na kod, aby obiekty były trwałe
- brak odwzorowań bazy danych ukrywających częściowo bazę
- prawie bez dodatkowych spojeń między kodem a bazą danych

ZODB to transakcyjna baza danych ACID.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n zodb-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -a 1000 -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

for f in fsdump fsoids fsrefs fstail repozo ; do
%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt HISTORY.rst README.rst
%attr(755,root,root) %{_bindir}/fsdump-3
%attr(755,root,root) %{_bindir}/fsoids-3
%attr(755,root,root) %{_bindir}/fsrefs-3
%attr(755,root,root) %{_bindir}/fstail-3
%attr(755,root,root) %{_bindir}/repozo-3
%attr(755,root,root) %{_bindir}/fsdump
%attr(755,root,root) %{_bindir}/fsoids
%attr(755,root,root) %{_bindir}/fsrefs
%attr(755,root,root) %{_bindir}/fstail
%attr(755,root,root) %{_bindir}/repozo
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/ZODB-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_downloads,_images,_modules,_static,articles,guide,reference,*.html,*.js}
%endif
