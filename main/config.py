# config.py - 配置文件
import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.app_name = "Windows R-tools Box"
        self.version = "1.0.0"
        self.author = "Regulus-forteen"
        self.license = "AGPL v3"
        
        # 应用路径
        self.base_dir = Path(__file__).parent
        self.tools_dir = self.base_dir / "tools"
        self.icons_dir = self.base_dir / "icons"
        
        # 确保目录存在
        self.tools_dir.mkdir(exist_ok=True)
        self.icons_dir.mkdir(exist_ok=True)
        
        # 主题颜色 - 克莱因蓝
        self.theme_colors = {
            "primary": "#002FA7",  # 克莱因蓝
            "primary_light": "#4A6FC1",
            "primary_dark": "#001F6E",
            "secondary": "#FF6B35",  # 橙色作为强调色
            "background": "#F8FAFC",
            "card": "#FFFFFF",
            "text": "#1F2937",
            "text_light": "#6B7280",
            "border": "#E5E7EB"
        }
        
        # 搜索引擎配置
        self.search_engines = {
            "百度": {
                "name": "百度",
                "url": "https://www.baidu.com/s?wd={query}",
                "icon": "fas fa-search",
                "color": "#2932E1"
            },
            "必应": {
                "name": "必应",
                "url": "https://www.bing.com/search?q={query}",
                "icon": "fab fa-microsoft",
                "color": "#008373"
            },
            "谷歌": {
                "name": "谷歌",
                "url": "https://www.google.com/search?q={query}",
                "icon": "fab fa-google",
                "color": "#4285F4"
            },
            "搜狗": {
                "name": "搜狗",
                "url": "https://www.sogou.com/web?query={query}",
                "icon": "fas fa-search",
                "color": "#FF5000"
            },
            "360搜索": {
                "name": "360搜索",
                "url": "https://www.so.com/s?q={query}",
                "icon": "fas fa-shield-alt",
                "color": "#19B955"
            }
        }
        
        # 默认收藏网站
        self.favorite_sites = [
            {"name": "GitHub", "url": "https://github.com", "icon": "fab fa-github", "category": "开发"},
            {"name": "Gitee", "url": "https://gitee.com", "icon": "fas fa-code", "category": "开发"},
            {"name": "知乎", "url": "https://www.zhihu.com", "icon": "fas fa-question-circle", "category": "学习"},
            {"name": "B站", "url": "https://www.bilibili.com", "icon": "fas fa-play-circle", "category": "娱乐"},
            {"name": "淘宝", "url": "https://www.taobao.com", "icon": "fas fa-shopping-cart", "category": "购物"},
            {"name": "京东", "url": "https://www.jd.com", "icon": "fas fa-store", "category": "购物"},
            {"name": "微信网页版", "url": "https://wx.qq.com", "icon": "fab fa-weixin", "category": "社交"},
            {"name": "QQ邮箱", "url": "https://mail.qq.com", "icon": "fas fa-envelope", "category": "办公"}
        ]
        
        # 用户设置
        self.settings = {
            "theme": "light",
            "default_search": "百度",
            "show_favorites": True,
            "show_tools": True,
            "check_updates": True,
            "window_position": None,
            "window_size": [1200, 800]
        }
        
        # 加载用户配置
        self.config_file = self.base_dir / "config.json"
        self.load_config()
    
    def load_config(self):
        """加载用户配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 只更新存在的键
                    for key in self.settings:
                        if key in user_config:
                            self.settings[key] = user_config[key]
            except Exception as e:
                print(f"⚠️  加载配置文件失败: {e}")
                print("💡 使用默认配置")
    
    def save_config(self):
        """保存用户配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def get_tool_categories(self):
        """获取工具分类"""
        categories = []
        if self.tools_dir.exists():
            for item in self.tools_dir.iterdir():
                if item.is_dir():
                    categories.append(item.name)
        return categories or ["system", "security", "network", "utilities"]

# 全局配置实例
config = Config()
