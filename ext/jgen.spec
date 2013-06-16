# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           jgen
Version:        0.1.0
Release:        1%{?dist}
Summary:        Generate simple JSON documents from the command line

Group:          Utilities
License:        BSD
URL:            https://github.com/jcmcken/jgen
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python-devel

# requires buildsys-build package to populate RPM macro
%{?el5:Requires: python-simplejson}

# Since YAML support is optional, don't require it by default
%{?require_yaml:Requires: PyYAML}

%description
Generate simple JSON documents from the command line.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%attr(0755,root,root) %{_bindir}/jgen
%doc README.md CHANGELOG.md LICENSE VERSION

%changelog
* Sun Jun 16 2013 Jon McKenzie - 0.1.0
- Initial release.
