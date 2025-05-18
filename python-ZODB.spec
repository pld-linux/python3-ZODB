#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		ZODB
Summary:	Python object-oriented database
Summary(pl.UTF-8):	Pythonowa zorientowana obietowo baza danych
Name:		python-%{module}
# keep 5.x here for python2 support
Version:	5.8.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zodb/
Source0:	https://files.pythonhosted.org/packages/source/Z/ZODB/%{module}-%{version}.tar.gz
# Source0-md5:	3d95891e2993d81d4d5b0358c5ce72cb
URL:		https://zodb.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-BTrees >= 4.2.0
BuildRequires:	python-ZConfig
BuildRequires:	python-manuel
BuildRequires:	python-mock
BuildRequires:	python-persistent >= 4.4.0
BuildRequires:	python-six
BuildRequires:	python-transaction > 2.4
BuildRequires:	python-zc.lockfile
BuildRequires:	python-zodbpickle >= 1.0.1
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.testing
BuildRequires:	python-zope.testrunner >= 4.4.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-BTrees
BuildRequires:	python3-ZConfig
BuildRequires:	python3-persistent
BuildRequires:	python3-transaction
BuildRequires:	python3-zc.lockfile
BuildRequires:	python3-zodbpickle
%endif
%endif
%if %{with doc}
BuildRequires:	python-j1m.sphinxautozconfig
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	python-sphinxcontrib-zopeext
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-%{module}
Summary:	Python object-oriented database
Summary(pl.UTF-8):	Pythonowa zorientowana obietowo baza danych
Group:		Documentation
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
ZODB provides an object-oriented database for Python that provides a
high-degree of transparency.

- no separate language for database operations
- very little impact on your code to make objects persistent
- no database mapper that partially hides the database.
- almost no seam between code and database.

ZODB is an ACID Transactional database.

%description -n python3-%{module} -l pl.UTF-8
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
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -a 1000 -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -a 1000 -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

for f in fsdump fsoids fsrefs fstail repozo ; do
%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

for f in fsdump fsoids fsrefs fstail repozo ; do
%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt HISTORY.rst README.rst
%attr(755,root,root) %{_bindir}/fsdump-2
%attr(755,root,root) %{_bindir}/fsoids-2
%attr(755,root,root) %{_bindir}/fsrefs-2
%attr(755,root,root) %{_bindir}/fstail-2
%attr(755,root,root) %{_bindir}/repozo-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/ZODB-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
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
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_downloads,_images,_modules,_static,articles,guide,reference,*.html,*.js}
%endif
