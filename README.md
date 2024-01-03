# raspi_information
树莓派启动后自动将`IP, CPU, RAM, DISK`信息通过企业微信、飞书、邮件等方式进行通知。  
格式如下：
```
树莓派启动信息通知
IP: 
	eth0: 192.168.1.11
	lo: 127.0.0.1
	wlan0: 
CPU: 50.1°C - %
RAM: 409MB/1848MB
DISK:
	/home/pi/personal: 477G/477G - 1%
	/boot/firmware: 438M/510M - 15%
	/: 49G/57G - 10%
```

## 配置通知
`notify.py`来自[qinglong](https://github.com/whyour/qinglong)  
在`notify.py`中配置脚本通知方式
## 配置自启动
`sudo nano /etc/rc.local`  
在自启动脚本中添加`/usr/bin/python /your/path/raspi_info.py start`,*注：py脚本后添加任意字符串，可进行通知，如不添加字符串。默认不发送通知*