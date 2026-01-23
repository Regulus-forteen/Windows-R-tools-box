# utils.py - 工具函数
import psutil
import platform
import socket
import json
import subprocess
import os
import sys
from pathlib import Path
import webbrowser

def get_system_info():
    """获取详细的系统信息"""
    info = {}
    
    try:
        # 操作系统信息
        system_info = platform.uname()
        info['system'] = {
            '系统': platform.system(),
            '版本': platform.version(),
            '发行版': platform.platform(),
            '架构': platform.architecture()[0],
            '处理器': platform.processor(),
            '机器': platform.machine(),
            '节点': system_info.node,
        }
        
        try:
            hostname = socket.gethostname()
            info['system']['主机名'] = hostname
            
            try:
                ip = socket.gethostbyname(hostname)
                info['system']['IP地址'] = ip
            except:
                info['system']['IP地址'] = '未知'
        except:
            pass
        
        # CPU信息
        cpu_info = {
            '物理核心数': psutil.cpu_count(logical=False),
            '逻辑核心数': psutil.cpu_count(logical=True),
            '使用率': f"{psutil.cpu_percent(interval=1)}%",
        }
        
        try:
            freq = psutil.cpu_freq()
            if freq:
                cpu_info['频率'] = f"{freq.current:.2f} MHz"
        except:
            pass
        
        # 尝试获取CPU型号
        try:
            if platform.system() == "Windows":
                import wmi
                c = wmi.WMI()
                cpu_name = c.Win32_Processor()[0].Name
                cpu_info['型号'] = cpu_name
        except:
            cpu_info['型号'] = platform.processor()
        
        info['cpu'] = cpu_info
        
        # 内存信息
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        info['memory'] = {
            '总内存': f"{mem.total / (1024**3):.2f} GB",
            '可用内存': f"{mem.available / (1024**3):.2f} GB",
            '已用内存': f"{mem.used / (1024**3):.2f} GB",
            '使用率': f"{mem.percent}%",
        }
        
        try:
            info['memory']['交换内存'] = f"{swap.total / (1024**3):.2f} GB"
            info['memory']['交换使用率'] = f"{swap.percent}%"
        except:
            pass
        
        # 磁盘信息
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    '设备': partition.device,
                    '挂载点': partition.mountpoint,
                    '文件系统': partition.fstype,
                    '总空间': f"{usage.total / (1024**3):.2f} GB",
                    '已用空间': f"{usage.used / (1024**3):.2f} GB",
                    '可用空间': f"{usage.free / (1024**3):.2f} GB",
                    '使用率': f"{usage.percent}%"
                }
                disks.append(disk_info)
            except:
                continue
        
        # 只显示主要磁盘
        info['disks'] = disks[:3]  # 只显示前3个磁盘
        
        # 网络信息
        net_info = []
        try:
            for name, addrs in psutil.net_if_addrs().items():
                if name.lower() in ['lo', 'loopback']:
                    continue
                    
                addr_info = {'接口': name, '地址': []}
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        addr_info['地址'].append(f"IPv4: {addr.address}")
                    elif addr.family == socket.AF_INET6:
                        addr_info['地址'].append(f"IPv6: {addr.address}")
                    elif addr.family == psutil.AF_LINK:
                        addr_info['地址'].append(f"MAC: {addr.address}")
                
                if addr_info['地址']:
                    net_info.append(addr_info)
            
            # 限制显示数量
            info['network'] = net_info[:3]
        except:
            info['network'] = []
        
        # 启动时间
        try:
            boot_time = psutil.boot_time()
            from datetime import datetime
            info['boot_time'] = datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
        except:
            info['boot_time'] = "未知"
        
        # 进程数
        try:
            info['process_count'] = len(psutil.pids())
        except:
            info['process_count'] = "未知"
        
        # Python信息
        info['python'] = {
            '版本': platform.python_version(),
            '编译器': platform.python_compiler(),
            '实现': platform.python_implementation(),
        }
        
        # 系统运行时间
        try:
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            info['uptime'] = f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
        except:
            info['uptime'] = "未知"
        
    except Exception as e:
        print(f"⚠️  获取系统信息时出错: {e}")
        info['error'] = f"获取系统信息时出错: {str(e)}"
        info['basic'] = {
            '系统': platform.system(),
            '版本': platform.version(),
            'Python版本': platform.python_version()
        }
    
    return info

def format_system_info_for_display(info):
    """格式化系统信息用于显示"""
    formatted = []
    
    # 基本系统信息
    if 'system' in info:
        formatted.append(("操作系统", info['system']))
    
    # CPU信息
    if 'cpu' in info:
        formatted.append(("CPU信息", info['cpu']))
    
    # 内存信息
    if 'memory' in info:
        formatted.append(("内存信息", info['memory']))
    
    # 磁盘信息
    if 'disks' in info:
        disk_text = []
        for i, disk in enumerate(info['disks'], 1):
            disk_text.append(f"{i}. {disk['设备']}: {disk['总空间']} ({disk['使用率']} 已用)")
        if disk_text:
            formatted.append(("磁盘信息", "\n".join(disk_text)))
    
    # 网络信息
    if 'network' in info and info['network']:
        net_text = []
        for net in info['network'][:3]:  # 只显示前3个网络接口
            addresses = net['地址'][:2]  # 只显示前2个地址
            if addresses:
                net_text.append(f"{net['接口']}: {', '.join(addresses)}")
        if net_text:
            formatted.append(("网络接口", "\n".join(net_text)))
    
    # 系统运行时间
    if 'uptime' in info:
        formatted.append(("系统运行时间", info['uptime']))
    
    # 启动时间
    if 'boot_time' in info:
        formatted.append(("系统启动时间", info['boot_time']))
    
    # 进程数
    if 'process_count' in info:
        formatted.append(("运行进程数", str(info['process_count'])))
    
    # Python信息
    if 'python' in info:
        formatted.append(("Python环境", info['python']))
    
    return formatted

def scan_tools(tools_dir):
    """扫描工具文件夹"""
    tools = []
    
    # 如果工具目录不存在，创建它
    if not tools_dir.exists():
        print(f"⚠️  工具目录不存在: {tools_dir}")
        print("💡 正在创建工具目录结构...")
        tools_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建分类目录
        for category in ["system", "security", "network", "utilities"]:
            category_dir = tools_dir / category
            category_dir.mkdir(exist_ok=True)
    
    # 扫描真实工具
    try:
        for category_dir in tools_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                for tool_file in category_dir.glob("*.json"):
                    try:
                        with open(tool_file, 'r', encoding='utf-8') as f:
                            tool_data = json.load(f)
                            # 确保必要字段存在
                            if 'id' not in tool_data:
                                tool_data['id'] = tool_file.stem
                            if 'category' not in tool_data:
                                tool_data['category'] = category
                            if 'icon' not in tool_data:
                                tool_data['icon'] = 'fas fa-tools'
                            if 'status' not in tool_data:
                                tool_data['status'] = 'on'
                            if 'favorite' not in tool_data:
                                tool_data['favorite'] = False
                            
                            tools.append(tool_data)
                    except Exception as e:
                        print(f"⚠️  加载工具文件失败 {tool_file}: {e}")
                        continue
    except Exception as e:
        print(f"⚠️  扫描工具失败: {e}")
    
    # 如果没有找到工具，返回示例数据
    if not tools:
        print("⚠️  未找到工具文件，使用示例数据")
        tools = [
            {
                "id": "system_cleaner",
                "name": "系统清理工具",
                "description": "清理系统垃圾文件和临时文件",
                "category": "system",
                "icon": "fas fa-broom",
                "status": "on",
                "favorite": True
            },
            {
                "id": "network_speed",
                "name": "网络速度测试",
                "description": "测试网络上传和下载速度",
                "category": "network",
                "icon": "fas fa-tachometer-alt",
                "status": "on",
                "favorite": True
            },
            {
                "id": "file_encrypt",
                "name": "文件加密",
                "description": "使用AES加密保护文件安全",
                "category": "security",
                "icon": "fas fa-lock",
                "status": "on",
                "favorite": False
            },
            {
                "id": "image_converter",
                "name": "图片格式转换",
                "description": "批量转换图片格式",
                "category": "utilities",
                "icon": "fas fa-file-image",
                "status": "on",
                "favorite": True
            }
        ]
    
    return tools

def open_url_in_browser(url):
    """在浏览器中打开URL"""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"⚠️  打开浏览器失败: {e}")
        return False

def launch_tool(tool_id):
    """启动工具"""
    # 这里可以实现具体的工具启动逻辑
    print(f"🔧 启动工具: {tool_id}")
    
    # 模拟工具启动
    try:
        # 在实际应用中，这里会根据工具配置启动相应的程序
        # 例如: subprocess.run([tool_executable, ...])
        
        return True
    except Exception as e:
        print(f"❌ 启动工具失败 {tool_id}: {e}")
        return False
