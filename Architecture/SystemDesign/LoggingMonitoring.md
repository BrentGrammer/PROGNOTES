# Logging and Monitoring

- Monitoring for metrics requires logs showing the things you want to measure.
- Changing logs can break metrics and onitoring - you can use a Time Series DB to store monitoring info.
  - Prometheus
  - InfluxDB
  - Graphite
- Use the time series DB to store send metrics to it from the server.
  - Can use Grafana to go into a db and create a graph of the data.

- Have thresholds for error rates to trigger alarms
  - Can hookup monitoring to Slack or systems like that to send alerts/notifications (i.e. PagerDuty to Slack)
