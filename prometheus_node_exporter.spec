Name:           prometheus_node_exporter
Version:        0.15.2
Release:        2%{?dist}
Summary:        Prometheus Node Exporter

License:        ASL 2.0
URL:            http://prometheus.io
Source0:        https://github.com/prometheus/node_exporter/releases/download/v0.15.2/node_exporter-0.15.2.linux-amd64.tar.gz
Source1:        prometheus_node_exporter.service

BuildRequires:  systemd

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
Prometheus Node Exporter

%prep
%setup -q -n node_exporter-0.15.2.linux-amd64
mkdir rpm-config
cp -av %{SOURCE1} ./rpm-config/

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT/opt/prometheus/node_exporter

#Create content dirs
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 ./rpm-config/prometheus_node_exporter.service $RPM_BUILD_ROOT%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT/var/lib/prometheus_node_exporter
cp -parf * $RPM_BUILD_ROOT/opt/prometheus/node_exporter

%pre
# Add the "prometheus" user
getent group prometheus >/dev/null || groupadd -g 371 -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -u 370 -g prometheus -s /bin/sh \
    -d /opt/prometheus -c "Prometheus" prometheus
exit 0

%post
%systemd_post prometheus_node_exporter.service

%preun
%systemd_preun prometheus_node_exporter.service

%postun
%systemd_postun

%files
%defattr(-,prometheus,prometheus,755)
%license LICENSE
%doc NOTICE

%attr(644,root,root) %{_unitdir}/prometheus_node_exporter.service
%dir %attr(755,prometheus,prometheus) %{_var}/lib/prometheus_node_exporter
/opt/prometheus/node_exporter

%changelog
* Thu Feb 01 2018 Miguel Perez Colino <mperez@redhat.com> release 2
- Bump version to 0.15.2

* Sun Nov 19 2017 Miguel Perez Colino <mperez@redhat.com> release 1
- Initial build
