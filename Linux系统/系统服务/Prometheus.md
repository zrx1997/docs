

下载prometheus安装包

```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.30.0/prometheus-2.30.0.linux-amd64.tar.gz

tar zxvf prometheus-2.30.0.linux-amd64.tar.gz -C /usr/local/

mv /usr/local/prometheus-2.30.0.linux-amd64/ /usr/local/prometheus

```



创建用户和数据存储目录

```bash
useradd  -s /sbin/nologin -M prometheus
mkdir /usr/local/prometheus/data
chown -R prometheus:prometheus /usr/local/prometheus/
```





创建systemd服务

```bash
vim /usr/lib/systemd/system/prometheus.service

[Unit]
Description=Prometheus
Documentation=https://prometheus.io/
After=network.target

[Service]
Type=simple
User=prometheus
ExecStart=/usr/local/prometheus/prometheus --config.file=/usr/local/prometheus/prometheus.yml --storage.tsdb.path=/usr/local/prometheus/data
Restart=on-failure

[Install]
WantedBy=multi-user.target


systemctl daemon-reload 
systemctl start prometheus
systemctl status prometheus
systemctl enable prometheus


```



grafana安装

```bash
# web ui
wget https://dl.grafana.com/oss/release/grafana-8.1.3.linux-amd64.tar.gz
tar -zxvf grafana-8.1.3.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/grafana-8.1.3/ /usr/local/grafana

```



创建用户与数据目录

```bash
useradd -s /sbin/nologin -M grafana
mkdir /usr/local/grafana/data
chown -R grafana:grafana /usr/local/grafana/

```



创建systemd启动文件

```bash
vim /usr/lib/systemd/system/grafana.service

[Unit]
Description=Grafana
After=network.target
 
[Service]
User=grafana
Group=grafana
Type=notify
ExecStart=/usr/local/grafana/bin/grafana-server -homepath /usr/local/grafana
Restart=on-failure
 
[Install]
WantedBy=multi-user.target

systemctl daemon-reload 
systemctl start grafana
systemctl status grafana
systemctl enable grafana

```



```bash
# 监控硬件信息，资源使用情况
wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz

tar zxvf node_exporter-1.2.2.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/node_exporter-1.2.2.linux-amd64/ /usr/local/node_exporter
nohup /usr/local/node_exporter/node_exporter >/dev/null 2>&1 &

```



```yaml
vim /usr/local/prometheus/prometheus.yml
scrape_configs:

  - job_name: 'prometheus'

    static_configs:
    - targets: ['localhost:9090']
  - job_name: 'www.adcwb.com'
    static_configs:
    - targets: ['106.13.208.193:9100']
```





```bash
# 监控端口，http状态，存活性使用
wget https://github.com/prometheus/blackbox_exporter/releases/download/v0.19.0/blackbox_exporter-0.19.0.linux-amd64.tar.gz

tar zxvf blackbox_exporter-0.19.0.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/blackbox_exporter-0.19.0.linux-amd64 /usr/local/blackbox_exporter

vim /lib/systemd/system/blackbox_exporter.service
[Unit]
Description=blackbox_exporter
After=network.target

[Service]
User=root
Type=simple
ExecStart=/usr/local/blackbox_exporter/blackbox_exporter --config.file=/usr/local/blackbox_exporter/blackbox.yml
Restart=on-failure

[Install]
WantedBy=multi-user.target


systemctl daemon-reload 
systemctl start blackbox_exporter
systemctl stop blackbox_exporter
systemctl status blackbox_exporter
netstat -lnpt|grep 9115

```



```yaml
# ping 检测
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:

  # ping 检测
  - job_name: 'ping_status'
    metrics_path: /probe
    params:
      module: [icmp]
    static_configs:
      - targets: ['43.249.28.50']
        labels:
          instance: 'ping_status'
          group: 'icmp'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: 43.249.28.50:9115

```



```bash
# 发送邮件组件
wget https://github.com/prometheus/alertmanager/releases/download/v0.23.0/alertmanager-0.23.0.linux-amd64.tar.gz

tar zxvf alertmanager-0.23.0.linux-amd64.tar.gz -C /usr/local/
mv /usr/local/alertmanager-0.23.0.linux-amd64 /usr/local/alertmanager

vim /usr/lib/systemd/system/alertmanager.service
[Unit]
Description=alertmanager
Documentation=https://github.com/prometheus/alertmanager
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/alertmanager --config.file=/usr/local/alertmanager/alertmanager.yml --storage.path=/usr/local/alertmanager/data
Restart=on-failure

[Install]
WantedBy=multi-user.target
```



```yaml
global:
  smtp_smarthost: 'smtp.qiye.aliyun.com:465'
  smtp_from: 'devops'
  smtp_auth_username: 'devops@adcwb.com'
  smtp_auth_password: '1a2b3c+D'
  smtp_require_tls: true 

route:
  receiver: mail
  
receivers:
- name: 'mail'
  email_configs:
  - to: 'wh@kf-idc.com'
  
  

  
```



```yaml
groups:

- name: node-up
  rules:
  - alert: node-up
    expr: up{job="43.249.28.50_port_check"} == 0
    for: 15s
    labels:
      severity: 1
      team: node
    annotations:
      summary: "{{ $labels.instance }} 已停止运行超过 15s！"
      
groups:
- name: node-up
  rules:

  - alert: InstanceDown
    expr: up{job="43.249.28.50_port_check"} == 0
    for: 5m
    labels:
      severity: page
    annotations:
      summary: "Instance {{ $labels.instance }} down"
      description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes."

  - alert: APIHighRequestLatency
    expr: api_http_request_latencies_second{quantile="0.5"} > 1
    for: 10m
    annotations:
      summary: "High request latency on {{ $labels.instance }}"
      description: "{{ $labels.instance }} has a median request latency above 1s (current value: {{ $value }}s)"

```



























