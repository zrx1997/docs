



```bash
# 动态地址NAT
iptables -t nat -A POSTROUTING -s 10.8.0.0/16 -o em4 -j MASQUERADE
```



