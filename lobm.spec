#
# spec file for package lobm
#
Name:           lobm
Version:        4.0
Release:        1.0
License:        Artistic
Summary:        Linux OS Baseline Maker
Url:            https://github.com/Q-Technologies/lobm
Group:          Applications/System
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-build
AutoReqProv:    no
Requires:       perlbrew
Requires:       createrepo
 
%description
This package installs a script that creates OS baselines.  See
https://github.com/Q-Technologies/lobm for more details

%prep
rm -rf *
#cp $RPM_SOURCE_DIR/lobm .
#cp $RPM_SOURCE_DIR/README.md .
#cp $RPM_SOURCE_DIR/LICENSE .

%build

%install
rm -rf $RPM_BUILD_ROOT/*
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 $RPM_SOURCE_DIR/lobm $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/etc/lobm
install -m 644 $RPM_SOURCE_DIR/lobm.yaml $RPM_BUILD_ROOT/etc/lobm
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/lobm/
install -m 644 $RPM_SOURCE_DIR/README.md $RPM_BUILD_ROOT/usr/share/doc/lobm/
install -m 644 $RPM_SOURCE_DIR/LICENSE $RPM_BUILD_ROOT/usr/share/doc/lobm/

%files
%defattr(644,root,root,755)
%attr(755,root,root) /usr/bin/lobm
%config /etc/lobm/lobm.yaml
%docdir /usr/share/doc/lobm/
/usr/share/doc/lobm/

%post
 
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}

%changelog
* Mon Apr 27 2015 matt@Q-Technologies.com.au
- initial RPM version (1.0)

