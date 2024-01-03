# raspi_information
send notify when the raspiberry pi startup

## 配置通知
在`notify.py`中配置脚本通知方式
## 配置自启动
`sudo nano /etc/rc.local`  
在自启动脚本中添加`/usr/bin/python /your/path/raspi_info.py start`,*注：py脚本后添加任意字符串，可进行通知，如不添加字符串。默认不发送通知*