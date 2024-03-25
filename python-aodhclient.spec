%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318
%global pypi_name aodhclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1

%global common_desc \
This is a client library for Aodh built on the Aodh API. It \
provides a Python API (the aodhclient module) and a command-line tool.

Name:             python-aodhclient
Version:          3.5.1
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Aodh

License:          Apache-2.0
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

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    git-core

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package  doc
Summary:          Documentation for OpenStack Aodh API Client


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



sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/\.\[test\]/,+1d' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s aodh %{buildroot}%{_bindir}/aodh-3

%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/aodhclient
%{python3_sitelib}/*.dist-info
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
* Mon Mar 25 2024 RDO <dev@lists.rdoproject.org> 3.5.1-1
- Update to 3.5.1

* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 3.5.0-1
- Update to 3.5.0

