%define name core-testsuite-template
%define version 1.0.0
%define release 3
%define _unpackaged_files_terminate_build 0 


Summary: core test suite for example 
Name: core-testsuite-template
Version: 1.0.0
Release: 1
License: GPLv2
Group: System/Libraries
Source: %{name}-%{version}.tar.gz
Requires:   dbus  
#BuildRequires:	geoclue-devel 
BuildRoot: %{_topdir}/tmp/%{name}-%{version}-buildroot

%description
It's an example for create tts core package.


%prep
%setup -q

%build
./autogen
%configure --prefix=/usr
make %{?jobs:-j%jobs}  

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall TEST_BIN_DIR="$RPM_BUILD_ROOT/opt/%{name}-%{version}" XML_DATA_DIR="$RPM_BUILD_ROOT/usr/share/%{name}"

%post 
cd /opt
ln -s %{name}-%{version} %{name}

%postun
rm -f /opt/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)  
# >> files  
%doc README  
%dir /opt/%{name}-%{version} 
/opt/%{name}-%{version}/core-testsuite-example 
/opt/%{name}-%{version}/*
%{_datadir}/%{name}/*
# << files  

%changelog
