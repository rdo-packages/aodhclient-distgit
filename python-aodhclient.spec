%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%global pypi_name aodhclient

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-aodhclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Aodh

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:        noarch


%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh
%{?python_provide:%python_provide python2-%{library}}


BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr

Requires:         python-babel >= 1.3
Requires:         python-cliff >= 1.14.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneauth1 >= 1.0.0
Requires:         python-six >= 1.9.0
Requires:         python-futurist


%description -n python2-%{pypi_name}
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.


%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Aodh API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx


%description -n python-%{pypi_name}-doc
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

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires:         python3-babel >= 1.3
Requires:         python3-cliff >= 1.14.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-serialization >= 1.4.0
Requires:         python3-oslo-utils >= 2.0.0
Requires:         python3-keystoneauth1 >= 1.0.0
Requires:         python3-six >= 1.9.0
Requires:         python3-futurist

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

%description
This is a client library for Aodh built on the Aodh API. It
provides a Python API (the aodhclient module) and a command-line tool.



%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/aodh %{buildroot}%{_bindir}/python3-aodh
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
install -m 755 -d %{buildroot}/%{_bindir}
pushd %{buildroot}%{_bindir}
#ln -s aodh aodh
for i in aodh-{2,%{?python2_shortver}}; do
    ln -s aodh $i
done
%if 0%{?with_python3}
for i in aodh-{3,%{?python3_shortver}}; do
    ln -s  python3-aodh $i
done
%endif
popd

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/aodh*
%{python2_sitelib}/aodhclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/aodhclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/aodhclient/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/python3-aodh
%{_bindir}/aodh*
%{python3_sitelib}/aodhclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/aodhclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/aodhclient/tests

%endif

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc html

%changelog
