%global pypi_name aodhclient

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-aodhclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Aodh

License:          ASL 2.0
URL:              https://launchpad.net/python-aodhclient
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch

%description
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.

%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr

Requires:         python-pbr
Requires:         python-cliff >= 1.14.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneauth1 >= 1.0.0
Requires:         python-six >= 1.9.0
Requires:         python-debtcollector
Requires:         python-osc-lib >= 1.0.1
Requires:         pyparsing

%description -n python2-%{pypi_name}
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.


%package  doc
Summary:          Documentation for OpenStack Aodh API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx


%description doc
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool
(aodh).

This package contains auto-generated documentation.

%package -n python2-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh

%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr

Requires:         python3-pbr
Requires:         python3-cliff >= 1.14.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-serialization >= 1.4.0
Requires:         python3-oslo-utils >= 2.0.0
Requires:         python3-keystoneauth1 >= 1.0.0
Requires:         python3-six >= 1.9.0
Requires:         python3-debtcollector
Requires:         python3-osc-lib >= 1.0.1
Requires:         python3-pyparsing

%description -n python3-%{pypi_name}
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.

%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let RPM handle the requirements
rm -f {,test-}requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/aodh %{buildroot}%{_bindir}/aodh-%{python3_version}
ln -s ./aodh-%{python3_version} %{buildroot}%{_bindir}/aodh-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/aodh %{buildroot}%{_bindir}/aodh-%{python2_version}
ln -s ./aodh-%{python2_version} %{buildroot}%{_bindir}/aodh-2

ln -s ./aodh-2 %{buildroot}%{_bindir}/aodh

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/aodhclient
%{python2_sitelib}/*.egg-info
%{_bindir}/aodh
%{_bindir}/aodh-2
%{_bindir}/aodh-%{python2_version}
%exclude %{python2_sitelib}/aodhclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/aodhclient/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.egg-info
%{_bindir}/aodh-3
%{_bindir}/aodh-%{python3_version}
%exclude %{python3_sitelib}/aodhclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/aodhclient/tests
%endif

%files doc
%doc html
%license LICENSE

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-aodhclient/commit/?id=ee17a4cd9a638191217cd9049f50e413e7f5ec70
