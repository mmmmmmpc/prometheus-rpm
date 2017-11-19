# Prometheus-RPM
RPM Packaging Files for Prometheus

rpmckages get build in the [mperezco/prometheus COPR repo](https://copr.fedorainfracloud.org/coprs/mperezco/prometheus/)

## Instructions

You can enable COPR repo in Fedora 26 with:
```
   $ sudo dnf copr enable mperezco/prometheus
```
Install the package
```
   $ sudo dnf install prometheus prometheus_node_exporter -y
```
Start the service
```
   $ sudo systemctl start prometheus
   $ sudo systemctl start prometheus_node_exporter
```
... and access the interface via [http://localhost:9090](http://localhost:9090)


