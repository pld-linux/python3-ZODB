# TODO:
# - fix tests
# - fix docs
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
# - 'module' should match the Python import path (first component?)
# - 'egg_name' should equal to Python egg name
# - 'pypi_name' must match the Python Package Index name
%define		module		ZODB
%define		egg_name	ZODB
%define		pypi_name	ZODB
Summary:	Python object-oriented database
Summary(pl.UTF-8):	Pythonowa zorientowana obietowo baza danych
Name:		python-%{pypi_name}
Version:	5.3.0
Release:	8
License:	ZPL 2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/Z/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	606b51a7a027d5bba2ed4269f3187c67
URL:		http://www.zodb.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-BTrees
BuildRequires:	python-ZConfig
BuildRequires:	python-modules
BuildRequires:	python-persistent
BuildRequires:	python-setuptools
BuildRequires:	python-transaction
BuildRequires:	python-zc.lockfile
BuildRequires:	python-zodbpickle
%endif
%if %{with python3}
BuildRequires:	python3-BTrees
BuildRequires:	python3-ZConfig
BuildRequires:	python3-modules
BuildRequires:	python3-persistent
BuildRequires:	python3-setuptools
BuildRequires:	python3-transaction
BuildRequires:	python3-zc.lockfile
BuildRequires:	python3-zodbpickle
%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-BTrees
Requires:	python-ZConfig
Requires:	python-modules
Requires:	python-persistent
Requires:	python-transaction
Requires:	python-zc.lockfile
Requires:	python-zodbpickle
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of the JSON-RPC v2.0 specification
(backwards-compatible) as a client library.

# %%description -l pl.UTF-8

%package -n python3-%{pypi_name}
Summary:	-
Summary(pl.UTF-8):	-
%description -n python3-%{pypi_name}

%description -n python3-%{pypi_name} -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Group:		Libraries/Python
Requires:	python3-BTrees
Requires:	python3-ZConfig
Requires:	python3-modules
Requires:	python3-persistent
Requires:	python3-transaction
Requires:	python3-zc.lockfile
Requires:	python3-zodbpickle
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst DEVELOPERS.rst HISTORY.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES.rst DEVELOPERS.rst HISTORY.rst
%attr(755,root,root) %{_bindir}/*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
