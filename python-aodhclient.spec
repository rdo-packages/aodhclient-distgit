%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name aodhclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global common_desc \
This is a client library for Aodh built on the Aodh API. It \
provides a Python API (the aodhclient module) and a command-line tool.

Name:             python-aodhclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Aodh

License:          ASL 2.0
URL:              https://launchpad.net/python-aodhclient
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    git-core

Requires:         python3-pbr
Requires:         python3-cliff >= 1.14.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-serialization >= 1.4.0
Requires:         python3-oslo-utils >= 2.0.0
Requires:         python3-osprofiler >= 1.4.0
Requires:         python3-keystoneauth1 >= 1.0.0
Requires:         python3-osc-lib >= 1.0.1
Requires:         python3-pyparsing

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package  doc
Summary:          Documentation for OpenStack Aodh API Client

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-oslo-serialization
BuildRequires:    python3-cliff


%description doc
%{common_desc}
(aodh).

This package contains auto-generated documentation.
%endif

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the requirements
rm -f {,test-}requirements.txt


%build
%{py3_build}

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s aodh %{buildroot}%{_bindir}/aodh-3

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/aodhclient
%{python3_sitelib}/*.egg-info
%{_bindir}/aodh
%{_bindir}/aodh-3
%exclude %{python3_sitelib}/aodhclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/aodhclient/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
