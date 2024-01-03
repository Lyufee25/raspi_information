#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   machine_info.py
@Time   :   2023/12/29 20:37:35
@Author :   lee
@Version:   1.0
@Desc   :   树莓派设备信息自动上报飞书机器人
"""

import os
import sys
import re
import notify
import time
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("test")
log_file_path = os.path.dirname(sys.argv[0])
log_name = "{}.log".format(os.path.basename(sys.argv[0]).replace(".py", ""))
log_max_MB = 3
log_count = 3
log_level = "INFO"
fmt = logging.Formatter(
    '[%(asctime)s %(filename)s:%(lineno)d][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
log_path = os.path.abspath(os.path.join(log_file_path, "logs", log_name)) if os.path.isabs(
    log_file_path) else os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), log_file_path, log_name))
if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))
handler = RotatingFileHandler(filename=log_path, mode='a', maxBytes=log_max_MB *
                              1024 * 1024, backupCount=log_count, encoding="UTF-8")
logger.info_handle = logging.StreamHandler()
handler.setFormatter(fmt)
logger.info_handle.setFormatter(fmt)
logger.setLevel(log_level)
logger.addHandler(handler)
logger.addHandler(logger.info_handle)

logger.info("sevice start...")


class Raspi():

    def __init__(self):
        self.disk_part = self.get_disk_part()
        self.ip = self.get_pi_ip()
        while True:
            if self.ip.strip():
                break
            self.ip = self.get_pi_ip()
            logger.warning(self.ip)
            time.sleep(2)

    def get_cpu_temperature(self):
        """获取树莓派CPU温度
        Returns:
            str: CPU温度（摄氏度）
        """
        res = os.popen('vcgencmd measure_temp').readline()
        return (res.replace("temp=", "").replace("'C\n", "°C"))

    def get_RAM_info(self):
        """获取树莓派内存使用信息
        Returns:
            str: 已用内存/总内存
        """
        cmd = "free -m"
        p = os.popen(cmd)
        ram_info = p.readlines()[1].split()[1:4]  # [total used free]
        return f"{ram_info[1]}MB/{ram_info[0]}MB - {round(int(ram_info[1])/int(ram_info[0]) * 100, 1)}%"

    def get_CPU_usage(self):
        """获取树莓派CPU占用信息
        Returns:
            str: 百分比
        """
        cmd = "top -n1 | awk '/Cpu\(s\):/ {print $2}'"
        return str(os.popen(cmd).readline().strip())+"%"

    def get_disk_part(self):
        """获取树莓派磁盘分区信息
        Returns:
            list: [分区挂载点]
        """
        cmd = "lsblk|grep part"
        p = os.popen(cmd)
        return [x.split()[6] for x in p.readlines()]

    def get_disk_part_space(self):
        """获取各分区磁盘空间
        Returns:
            str: 分区名: 剩余空间/总空间 已用百分比
        """
        disk_space_str = ""
        for part in self.disk_part:
            cmd = f"df -h {part}"
            p = os.popen(cmd)
            info = p.readlines()[1].split()
            prefix = "" if self.disk_part.index(part) == 0 else "\n"
            disk_space_str += f"{prefix}\t{part}: {info[3]}/{info[1]} - {info[4]}"
        return disk_space_str

    def get_pi_ip(self):
        """获取树莓派各网卡IP信息
        Returns:
            str: 网卡名称: IP
        """
        ret = os.popen('ifconfig').readlines()
        ip = ""
        for x in ret:
            net_case = re.search(r"(\w*): flags", x)
            if not net_case:
                ipv4_case = re.search(r"inet (\w.*)  netmask", x)
                if ipv4_case:
                    ip += ipv4_case.group(1)
                continue
            ip += f"\n\t{net_case.group(1)}: " if ip else f"\t{net_case.group(1)}: "
        return ip


if __name__ == '__main__':
    params = sys.argv
    title = "树莓派启动信息通知"
    pi = Raspi()
    content = f"""IP: 
{pi.ip}
CPU: {pi.get_cpu_temperature()} - {pi.get_CPU_usage()}
RAM: {pi.get_RAM_info()}
DISK:
{pi.get_disk_part_space()}"""
    if len(params) > 1:
        logger.info(f"\n{content}")
        notify.send(title=title, content=content)
        logger.info("message send success.")
    else:
        logger.info(f"\n{content}")
