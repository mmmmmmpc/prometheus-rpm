Name:           prometheus
Version:        2.0.0
Release:        5%{?dist}
Summary:        Prometheus

License:        ASL 2.0
URL:            http://prometheus.io
Source0:        https://github.com/prometheus/prometheus/releases/download/v2.0.0/prometheus-2.0.0.linux-amd64.tar.gz
Source1:        prometheus.service
Source2:        prometheus.yml

BuildRequires:  systemd

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
Prometheus

%prep
%setup -q -n prometheus-2.0.0.linux-amd64
mkdir rpm-config
cp -av %{SOURCE1} ./rpm-config/
cp -av %{SOURCE2} ./rpm-config/

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT/opt/prometheus

#Create content dirs
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 ./rpm-config/prometheus.service $RPM_BUILD_ROOT%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 ./rpm-config/prometheus.yml $RPM_BUILD_ROOT%{_sysconfdir}/
mkdir -p $RPM_BUILD_ROOT/var/lib/prometheus
cp -parf * $RPM_BUILD_ROOT/opt/prometheus

%pre
# Add the "prometheus" user
getent group prometheus >/dev/null || groupadd -g 371 -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -u 370 -g prometheus -s /bin/sh \
    -d /opt/prometheus -c "Prometheus" prometheus
exit 0

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun

%files
%defattr(-,prometheus,prometheus,755)
%license LICENSE
%doc NOTICE

%attr(644,root,root) %{_unitdir}/prometheus.service
%dir %attr(755,prometheus,prometheus) %{_var}/lib/prometheus
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/prometheus.yml
/opt/prometheus

%changelog
* Sun Nov 19 2017 Miguel Perez Colino <mperez@redhat.com> release 5
- Version 2.0 bump

* Wed Jun 14 2017 Miguel Perez Colino <mperez@redhat.com> release 4
- Fixed service file

* Wed Jun 14 2017 Miguel Perez Colino <mperez@redhat.com> release 3
- Fixed paths

* Wed Jun 14 2017 Miguel Perez Colino <mperez@redhat.com> release 2
- Added data dir
- Added config file

* Wed Jun 14 2017 Miguel Perez Colino <mperez@redhat.com> release 1
- Initial build
