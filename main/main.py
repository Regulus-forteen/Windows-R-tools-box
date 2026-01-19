import tkinter as tk
from tkinter import ttk, messagebox, font
import platform
import psutil
from datetime import datetime
import sys
import os

class ModernRToolsBox:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows R-tools Box")
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 移除默认标题栏
        self.root.overrideredirect(True)
        
        
        # 初始化现代颜色方案
        self.colors = {
            "primary": "#4361ee",
            "primary_dark": "#3a56d4",
            "primary_light": "#eef2ff",
            "secondary": "#7209b7",
            "accent": "#f72585",
            "success": "#4cc9f0",
            "background": "#f8f9fa",
            "card_bg": "#ffffff",
            "sidebar_bg": "#ffffff",
            "text_primary": "#2b2d42",
            "text_secondary": "#8d99ae",
            "text_light": "#ffffff",
            "border": "#e9ecef",
            "hover": "#f1f3f4",
            "shadow": "rgba(0, 0, 0, 0.08)"
        }

        
        # 设置窗口为屏幕3/4大小并居中
        self.setup_window_size()
        
        # 初始化现代字体
        self.setup_fonts()
        
        # 创建自定义标题栏
        self.create_modern_title_bar()
        
        # 创建主容器
        self.create_main_container()
        
        # 创建侧边栏
        self.create_modern_sidebar()
        
        # 创建主工作区
        self.create_modern_workspace()
        
        # 创建状态栏
        self.create_modern_status_bar()
        
        # 创建标题栏拖动功能
        self.setup_drag_functionality()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化内存监控和时间更新
        self.root.after(1000, self.update_memory_usage)
        self.root.after(1000, self.update_time)
        
        # 绑定全局快捷键
        self.bind_shortcuts()
        
    def set_window_icon(self):
        """设置窗口图标"""
        icon_path_32 = os.path.join("main", "R-tools 32x32.ico")
        icon_path_128 = os.path.join("main", "R-tools 128x128.ico")
        
        if os.path.exists(icon_path_32):
            self.root.iconbitmap(icon_path_32)
        elif os.path.exists(icon_path_128):
            self.root.iconbitmap(icon_path_128)
    
    def setup_window_size(self):
        """设置窗口大小为屏幕的3/4并居中"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.window_width = int(screen_width * 0.75)
        self.window_height = int(screen_height * 0.75)
        
        # 计算居中位置
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.configure(bg=self.colors["background"])
    
    def setup_fonts(self):
        """初始化现代字体设置"""
        try:
            self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
            self.heading_font = font.Font(family="Segoe UI", size=13, weight="600")
            self.body_font = font.Font(family="Segoe UI", size=11)
            self.small_font = font.Font(family="Segoe UI", size=10)
            self.mono_font = font.Font(family="Cascadia Code", size=10)
            self.icon_font = font.Font(family="Segoe UI Symbol", size=12)
        except:
            # 备用字体
            self.title_font = font.Font(size=16, weight="bold")
            self.heading_font = font.Font(size=13, weight="bold")
            self.body_font = font.Font(size=11)
            self.small_font = font.Font(size=10)
            self.mono_font = font.Font(family="Courier", size=10)
            self.icon_font = font.Font(size=12)
    
    def create_modern_title_bar(self):
        """创建现代自定义标题栏"""
        title_bar = tk.Frame(
            self.root, 
            bg=self.colors["primary"], 
            height=48
        )
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        
        # 标题栏拖动区域
        self.title_bar = title_bar
        
        # Logo和标题
        logo_frame = tk.Frame(title_bar, bg=self.colors["primary"])
        logo_frame.pack(side="left", padx=(20, 12), pady=0)
        
        # 现代Logo
        logo_canvas = tk.Canvas(
            logo_frame, 
            width=36, 
            height=36, 
            bg=self.colors["primary"], 
            highlightthickness=0
        )
        logo_canvas.pack(side="left")
        # 创建渐变圆形Logo
        logo_canvas.create_oval(2, 2, 34, 34, fill="#ffffff", outline="")
        logo_canvas.create_text(18, 18, text="R", font=("Segoe UI", 16, "bold"), fill=self.colors["primary"])
        
        # 应用名称
        title_label = tk.Label(
            title_bar, 
            text="Windows R-tools Box", 
            bg=self.colors["primary"], 
            fg=self.colors["text_light"],
            font=self.title_font
        )
        title_label.pack(side="left", pady=0)
        
        # 右侧窗口控制按钮
        button_frame = tk.Frame(title_bar, bg=self.colors["primary"])
        button_frame.pack(side="right", padx=0)
        
        # 最小化按钮
        minimize_btn = self.create_modern_button(
            button_frame,
            text="─",
            bg=self.colors["primary"],
            hover_bg="#5a75f0",
            command=self.minimize_window,
            width=46
        )
        minimize_btn.pack(side="left", fill="y")
        
        # 关闭按钮
        close_btn = self.create_modern_button(
            button_frame,
            text="×",
            bg=self.colors["primary"],
            hover_bg="#e81123",
            command=self.on_closing,
            width=46
        )
        close_btn.pack(side="left", fill="y")
    
    def create_modern_button(self, parent, text, bg, hover_bg, command, width=40, height=48):
        """创建现代风格的按钮"""
        btn = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=self.colors["text_light"],
            font=("Segoe UI", 18),
            bd=0,
            width=3,
            height=1,
            activebackground=hover_bg,
            activeforeground=self.colors["text_light"],
            relief="flat",
            cursor="hand2",
            command=command
        )
        
        # 绑定悬停效果
        def on_enter(e):
            btn.config(bg=hover_bg)
        
        def on_leave(e):
            btn.config(bg=bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_main_container(self):
        """创建主容器"""
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill="both", expand=True)
        
        # 侧边栏和主工作区容器
        content_frame = tk.Frame(main_container, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.content_frame = content_frame
    
    def create_modern_sidebar(self):
        """创建现代侧边导航栏"""
        sidebar = tk.Frame(
            self.content_frame, 
            width=260, 
            bg=self.colors["sidebar_bg"],
            relief="flat"
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # 顶部用户区域
        user_frame = tk.Frame(sidebar, bg=self.colors["primary_light"], height=140)
        user_frame.pack(fill="x", pady=(0, 15))
        user_frame.pack_propagate(False)
        
        # 用户头像
        avatar_frame = tk.Frame(user_frame, bg=self.colors["primary_light"])
        avatar_frame.pack(pady=(25, 10))
        
        avatar_canvas = tk.Canvas(
            avatar_frame,
            width=70,
            height=70,
            bg=self.colors["primary_light"],
            highlightthickness=0
        )
        avatar_canvas.pack()
        avatar_canvas.create_oval(5, 5, 65, 65, fill=self.colors["primary"], outline="")
        avatar_canvas.create_text(35, 35, text="R", font=("Segoe UI", 28, "bold"), fill="white")
        
        # 欢迎文本
        welcome_label = tk.Label(
            user_frame,
            text="欢迎使用",
            bg=self.colors["primary_light"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        welcome_label.pack()
        
        username_label = tk.Label(
            user_frame,
            text="R-tools Box",
            bg=self.colors["primary_light"],
            fg=self.colors["primary"],
            font=self.heading_font
        )
        username_label.pack()
        
        # 搜索框
        search_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # 创建现代搜索框
        search_container = tk.Frame(search_frame, bg=self.colors["border"], bd=0)
        search_container.pack(fill="x")
        
        search_icon = tk.Label(
            search_container,
            text="🔍",
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.icon_font
        )
        search_icon.pack(side="left", padx=(12, 8), pady=10)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_container,
            textvariable=search_var,
            font=self.body_font,
            bd=0,
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["primary"],
            relief="flat"
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=8)
        search_entry.insert(0, "搜索工具...")
        
        # 导航菜单
        nav_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        nav_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        categories = [
            ("🏠", "首页概览", self.show_home, True),
            ("⚙️", "系统工具", self.show_system_tools, False),
            ("📁", "文件管理", self.show_file_tools, False),
            ("🌐", "网络工具", self.show_network_tools, False),
            ("🔒", "安全工具", self.show_security_tools, False),
            ("🎨", "个性化", self.show_settings, False),
            ("❓", "帮助中心", self.show_help, False)
        ]
        
        self.nav_buttons = []
        for icon, text, command, is_active in categories:
            nav_item = self.create_nav_item(nav_frame, icon, text, command, is_active)
            nav_item.pack(fill="x", padx=20, pady=2)
            self.nav_buttons.append(nav_item)
        
        # 底部信息区域
        bottom_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"], height=80)
        bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        bottom_frame.pack_propagate(False)
        
        # 版本信息
        version_frame = tk.Frame(bottom_frame, bg=self.colors["sidebar_bg"])
        version_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        version_label = tk.Label(
            version_frame,
            text="版本 v1.0.0",
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        version_label.pack(side="left")
        
        # 底部按钮
        button_frame = tk.Frame(bottom_frame, bg=self.colors["sidebar_bg"])
        button_frame.pack(fill="x", padx=20, pady=5)
        
        # GitHub按钮
        github_btn = self.create_icon_button(
            button_frame,
            "🐙",
            self.colors["text_secondary"],
            self.colors["primary"]
        )
        github_btn.pack(side="left", padx=(0, 10))
        
        # 赞助按钮
        sponsor_btn = self.create_icon_button(
            button_frame,
            "❤️",
            "#ff4081",
            "#f50057"
        )
        sponsor_btn.pack(side="left")
        
        # 设置按钮
        settings_btn = self.create_icon_button(
            button_frame,
            "⚙️",
            self.colors["text_secondary"],
            self.colors["primary"]
        )
        settings_btn.pack(side="right")
    
    def create_nav_item(self, parent, icon, text, command, is_active=False):
        """创建现代导航项"""
        nav_frame = tk.Frame(parent, bg=self.colors["sidebar_bg"])
        
        # 活动状态指示器
        if is_active:
            active_indicator = tk.Frame(nav_frame, bg=self.colors["primary"], width=4)
            active_indicator.pack(side="left", fill="y")
        else:
            # 占位符保持对齐
            tk.Frame(nav_frame, bg=self.colors["sidebar_bg"], width=4).pack(side="left", fill="y")
        
        btn = tk.Button(
            nav_frame,
            text=f"   {icon}  {text}",
            anchor="w",
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_primary"] if not is_active else self.colors["primary"],
            font=self.body_font,
            bd=0,
            padx=16,
            pady=14,
            activebackground=self.colors["hover"],
            activeforeground=self.colors["primary"],
            relief="flat",
            cursor="hand2",
            command=command
        )
        btn.pack(side="left", fill="x", expand=True)
        
        # 悬停效果
        def on_enter(e):
            if not is_active:
                btn.config(bg=self.colors["hover"])
                nav_frame.config(bg=self.colors["hover"])
        
        def on_leave(e):
            if not is_active:
                btn.config(bg=self.colors["sidebar_bg"])
                nav_frame.config(bg=self.colors["sidebar_bg"])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        nav_frame.bind("<Enter>", on_enter)
        nav_frame.bind("<Leave>", on_leave)
        
        return nav_frame
    
    def create_icon_button(self, parent, icon, bg, hover_bg):
        """创建图标按钮"""
        btn = tk.Button(
            parent,
            text=icon,
            bg=bg,
            fg="white",
            font=self.icon_font,
            bd=0,
            width=2,
            pady=4,
            activebackground=hover_bg,
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        
        def on_enter(e):
            btn.config(bg=hover_bg)
        
        def on_leave(e):
            btn.config(bg=bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_modern_workspace(self):
        """创建现代主工作区"""
        workspace = tk.Frame(
            self.content_frame, 
            bg=self.colors["background"],
            relief="flat"
        )
        workspace.pack(side="right", fill="both", expand=True)
        
        # 创建欢迎页面
        self.create_modern_welcome_page(workspace)
        
        self.workspace = workspace
    
    def create_modern_welcome_page(self, parent):
        """创建现代欢迎页面"""
        # 清除现有内容
        for widget in parent.winfo_children():
            widget.destroy()
        
        # 主内容容器
        content_container = tk.Frame(parent, bg=self.colors["background"])
        content_container.pack(fill="both", expand=True)
        
        # 添加滚动条
        canvas = tk.Canvas(content_container, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["background"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 页面内容
        welcome_frame = tk.Frame(scrollable_frame, bg=self.colors["background"])
        welcome_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 欢迎标题
        header_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text="欢迎回来 👋",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(side="left")
        
        date_label = tk.Label(
            header_frame,
            text=datetime.now().strftime("%Y年%m月%d日"),
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.body_font
        )
        date_label.pack(side="right", pady=8)
        
        # 统计卡片行
        stats_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        stats_frame.pack(fill="x", pady=(0, 30))
        
        stats = [
            ("📦", "12", "可用工具", self.colors["primary"]),
            ("⚡", "4", "正在运行", self.colors["success"]),
            ("⭐", "28", "收藏工具", self.colors["secondary"]),
            ("🔄", "3", "最近更新", self.colors["accent"])
        ]
        
        for i, (icon, value, label, color) in enumerate(stats):
            stat_card = self.create_stat_card(stats_frame, icon, value, label, color)
            if i < 3:
                stat_card.pack(side="left", padx=(0, 15))
            else:
                stat_card.pack(side="left")
        
        # 快捷工具区域
        tools_section = tk.Frame(welcome_frame, bg=self.colors["background"])
        tools_section.pack(fill="x", pady=(0, 25))
        
        section_header = tk.Frame(tools_section, bg=self.colors["background"])
        section_header.pack(fill="x", pady=(0, 20))
        
        section_title = tk.Label(
            section_header,
            text="常用工具",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        section_title.pack(side="left")
        
        view_all_btn = tk.Button(
            section_header,
            text="查看全部 →",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=self.small_font,
            bd=0,
            cursor="hand2",
            activebackground=self.colors["background"],
            activeforeground=self.colors["primary_dark"],
            relief="flat"
        )
        view_all_btn.pack(side="right")
        
        # 工具卡片网格
        tools_grid = tk.Frame(tools_section, bg=self.colors["background"])
        tools_grid.pack(fill="x")
        
        tools = [
            ("🗑️", "磁盘清理", "释放磁盘空间，删除临时文件", self.colors["primary"]),
            ("💻", "系统信息", "查看硬件和系统详细信息", self.colors["success"]),
            ("📊", "性能监控", "实时监控系统资源使用", self.colors["secondary"]),
            ("🔍", "文件搜索", "快速查找文件和文件夹", self.colors["accent"]),
            ("🌐", "网络诊断", "检测网络连接和速度", self.colors["primary"]),
            ("🔄", "系统优化", "优化系统性能和启动项", self.colors["success"])
        ]
        
        for i in range(0, len(tools), 3):
            row_frame = tk.Frame(tools_grid, bg=self.colors["background"])
            row_frame.pack(fill="x", pady=(0, 15))
            
            for j in range(3):
                if i + j < len(tools):
                    icon, name, desc, color = tools[i + j]
                    tool_card = self.create_tool_card(row_frame, icon, name, desc, color)
                    tool_card.pack(side="left", padx=(0, 15))
        
        # 最近活动
        activity_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        activity_frame.pack(fill="x", pady=(0, 25))
        
        activity_title = tk.Label(
            activity_frame,
            text="最近活动",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        activity_title.pack(anchor="w", pady=(0, 15))
        
        activities = [
            ("刚刚", "启动了系统信息工具"),
            ("10分钟前", "清理了2.3GB临时文件"),
            ("1小时前", "优化了系统启动项"),
            ("3小时前", "诊断了网络连接")
        ]
        
        for time, action in activities:
            activity_item = self.create_activity_item(activity_frame, time, action)
            activity_item.pack(fill="x", pady=(0, 10))
    
    def create_stat_card(self, parent, icon, value, label, color):
        """创建统计卡片"""
        card = tk.Frame(
            parent,
            width=180,
            height=120,
            bg=self.colors["card_bg"],
            relief="flat"
        )
        card.pack_propagate(False)
        
        # 添加阴影效果
        card.config(highlightbackground=self.colors["border"], highlightthickness=1)
        
        content_frame = tk.Frame(card, bg=self.colors["card_bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 图标
        icon_label = tk.Label(
            content_frame,
            text=icon,
            bg=self.colors["card_bg"],
            font=("Segoe UI", 24)
        )
        icon_label.pack(anchor="w")
        
        # 数值
        value_label = tk.Label(
            content_frame,
            text=value,
            bg=self.colors["card_bg"],
            fg=color,
            font=("Segoe UI", 28, "bold")
        )
        value_label.pack(anchor="w", pady=(10, 5))
        
        # 标签
        label_label = tk.Label(
            content_frame,
            text=label,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        label_label.pack(anchor="w")
        
        return card
    
    def create_tool_card(self, parent, icon, name, desc, color):
        """创建现代工具卡片"""
        card = tk.Frame(
            parent,
            width=200,
            height=160,
            bg=self.colors["card_bg"],
            relief="flat",
            cursor="hand2"
        )
        card.pack_propagate(False)
        
        # 添加阴影效果
        card.config(highlightbackground=self.colors["border"], highlightthickness=1)
        
        content_frame = tk.Frame(card, bg=self.colors["card_bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 图标区域
        icon_frame = tk.Frame(content_frame, bg=color + "20", width=48, height=48)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            bg=color + "20",
            fg=color,
            font=("Segoe UI", 20)
        )
        icon_label.pack(expand=True)
        
        # 工具名称
        name_label = tk.Label(
            content_frame,
            text=name,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        name_label.pack(anchor="w", pady=(15, 5))
        
        # 工具描述
        desc_label = tk.Label(
            content_frame,
            text=desc,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font,
            wraplength=160,
            justify="left"
        )
        desc_label.pack(anchor="w")
        
        # 悬停效果
        def on_enter(e):
            card.config(bg=self.colors["hover"])
            content_frame.config(bg=self.colors["hover"])
            name_label.config(bg=self.colors["hover"])
            desc_label.config(bg=self.colors["hover"])
            icon_frame.config(bg=color + "40")
            icon_label.config(bg=color + "40")
        
        def on_leave(e):
            card.config(bg=self.colors["card_bg"])
            content_frame.config(bg=self.colors["card_bg"])
            name_label.config(bg=self.colors["card_bg"])
            desc_label.config(bg=self.colors["card_bg"])
            icon_frame.config(bg=color + "20")
            icon_label.config(bg=color + "20")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
        
        return card
    
    def create_activity_item(self, parent, time, action):
        """创建活动项"""
        item_frame = tk.Frame(parent, bg=self.colors["background"])
        
        # 时间点
        time_dot = tk.Frame(item_frame, bg=self.colors["primary"], width=8, height=8)
        time_dot.pack(side="left", padx=(0, 12))
        time_dot.pack_propagate(False)
        
        # 内容
        content_frame = tk.Frame(item_frame, bg=self.colors["background"])
        content_frame.pack(side="left", fill="x", expand=True)
        
        action_label = tk.Label(
            content_frame,
            text=action,
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font
        )
        action_label.pack(anchor="w")
        
        time_label = tk.Label(
            content_frame,
            text=time,
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        time_label.pack(anchor="w", pady=(2, 0))
        
        return item_frame
    
    def create_modern_status_bar(self):
        """创建现代状态栏"""
        status_bar = tk.Frame(
            self.root, 
            bg=self.colors["card_bg"], 
            height=36
        )
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)
        
        # 左侧状态信息
        left_frame = tk.Frame(status_bar, bg=self.colors["card_bg"])
        left_frame.pack(side="left", padx=20)
        
        status_label = tk.Label(
            left_frame,
            text="✓ 系统就绪",
            bg=self.colors["card_bg"],
            fg=self.colors["success"],
            font=self.small_font
        )
        status_label.pack(side="left", padx=(0, 20))
        
        # 右侧状态信息
        right_frame = tk.Frame(status_bar, bg=self.colors["card_bg"])
        right_frame.pack(side="right", padx=20)
        
        # CPU和内存信息
        sys_frame = tk.Frame(right_frame, bg=self.colors["card_bg"])
        sys_frame.pack(side="left", padx=(0, 20))
        
        cpu_icon = tk.Label(
            sys_frame,
            text="💻",
            bg=self.colors["card_bg"],
            font=self.small_font
        )
        cpu_icon.pack(side="left", padx=(0, 5))
        
        cpu_label = tk.Label(
            sys_frame,
            text="CPU: 0%",
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        cpu_label.pack(side="left", padx=(0, 10))
        self.cpu_label = cpu_label
        
        memory_icon = tk.Label(
            sys_frame,
            text="💾",
            bg=self.colors["card_bg"],
            font=self.small_font
        )
        memory_icon.pack(side="left", padx=(0, 5))
        
        self.memory_label = tk.Label(
            sys_frame,
            text="内存: 0%",
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        self.memory_label.pack(side="left")
        
        # 时间显示
        self.time_label = tk.Label(
            right_frame,
            text=datetime.now().strftime("%H:%M:%S"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        self.time_label.pack(side="left")
    
    def setup_drag_functionality(self):
        """设置窗口拖动功能"""
        self._offset_x = 0
        self._offset_y = 0
        
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        
        # 标题文字也可以拖动
        for label in self.title_bar.winfo_children():
            if isinstance(label, tk.Label):
                label.bind('<Button-1>', self.start_move)
                label.bind('<B1-Motion>', self.on_move)
    
    def bind_shortcuts(self):
        """绑定全局快捷键"""
        self.root.bind('<Control-f>', lambda e: self.focus_search())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Escape>', lambda e: self.show_home())
    
    def focus_search(self):
        """聚焦搜索框"""
        pass
    
    def start_move(self, event):
        """开始拖动窗口"""
        self._offset_x = event.x
        self._offset_y = event.y
    
    def on_move(self, event):
        """处理窗口拖动"""
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f"+{x}+{y}")
    
    def update_time(self):
        """更新时间显示"""
        if hasattr(self, 'time_label') and self.time_label:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_memory_usage(self):
        """更新CPU和内存使用情况显示"""
        try:
            if hasattr(self, 'memory_label') and self.memory_label:
                # 获取内存使用率
                memory_percent = psutil.virtual_memory().percent
                self.memory_label.config(text=f"内存: {memory_percent}%")
                
                # 获取CPU使用率
                cpu_percent = psutil.cpu_percent(interval=0.1)
                if hasattr(self, 'cpu_label') and self.cpu_label:
                    self.cpu_label.config(text=f"CPU: {cpu_percent}%")
        except Exception as e:
            print(f"获取系统信息失败: {e}")
        self.root.after(2000, self.update_memory_usage)
    
    def minimize_window(self):
        """最小化窗口"""
        self.root.iconify()
    
    def on_closing(self):
        """处理窗口关闭"""
        if messagebox.askokcancel("退出", "确定要退出 Windows R-tools Box 吗？"):
            self.root.destroy()
            sys.exit()
    
    # 侧边栏按钮对应的功能
    def show_home(self):
        """显示首页"""
        self.create_modern_welcome_page(self.workspace)
    
    def show_system_tools(self):
        """显示系统工具"""
        self.show_modern_category_page("系统工具", "⚙️")
    
    def show_file_tools(self):
        """显示文件管理工具"""
        self.show_modern_category_page("文件管理", "📁")
    
    def show_network_tools(self):
        """显示网络工具"""
        self.show_modern_category_page("网络工具", "🌐")
    
    def show_security_tools(self):
        """显示安全工具"""
        self.show_modern_category_page("安全工具", "🔒")
    
    def show_settings(self):
        """显示设置页面"""
        self.show_modern_settings_page()
    
    def show_help(self):
        """显示帮助页面"""
        self.show_modern_help_page()
    
    def show_modern_category_page(self, category_name, icon):
        """显示现代分类工具页面"""
        for widget in self.workspace.winfo_children():
            widget.destroy()
        
        # 创建页面容器
        page_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        page_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 页面标题
        header_frame = tk.Frame(page_frame, bg=self.colors["background"])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text=f"{icon} {category_name}",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 22, "bold")
        )
        title_label.pack(side="left")
        
        # 工具数量
        count_label = tk.Label(
            header_frame,
            text="12个工具可用",
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.body_font
        )
        count_label.pack(side="right", pady=8)
        
        # 占位内容
        placeholder_frame = tk.Frame(page_frame, bg=self.colors["background"])
        placeholder_frame.pack(fill="both", expand=True)
        
        placeholder_icon = tk.Label(
            placeholder_frame,
            text="🚧",
            bg=self.colors["background"],
            font=("Segoe UI", 64)
        )
        placeholder_icon.pack(pady=(50, 20))
        
        placeholder_text = tk.Label(
            placeholder_frame,
            text="功能正在开发中...\n敬请期待",
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.heading_font
        )
        placeholder_text.pack()
    
    def show_modern_settings_page(self):
        """显示现代设置页面"""
        for widget in self.workspace.winfo_children():
            widget.destroy()
        
        # 创建设置页面容器
        settings_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        settings_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 页面标题
        title_label = tk.Label(
            settings_frame,
            text="🎨 个性化设置",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 22, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # 设置项卡片
        settings_cards = [
            ("🌙", "外观主题", "深色/浅色主题切换"),
            ("🌍", "语言设置", "切换界面语言"),
            ("🔔", "通知设置", "管理工具通知"),
            ("⚡", "性能设置", "优化工具性能")
        ]
        
        for icon, title, desc in settings_cards:
            card = self.create_setting_card(settings_frame, icon, title, desc)
            card.pack(fill="x", pady=(0, 15))
    
    def create_setting_card(self, parent, icon, title, desc):
        """创建设置项卡片"""
        card = tk.Frame(
            parent,
            bg=self.colors["card_bg"],
            relief="flat"
        )
        card.config(highlightbackground=self.colors["border"], highlightthickness=1)
        
        # 图标
        icon_label = tk.Label(
            card,
            text=icon,
            bg=self.colors["card_bg"],
            font=("Segoe UI", 20)
        )
        icon_label.pack(side="left", padx=20, pady=20)
        
        # 内容
        content_frame = tk.Frame(card, bg=self.colors["card_bg"])
        content_frame.pack(side="left", fill="x", expand=True, pady=20)
        
        title_label = tk.Label(
            content_frame,
            text=title,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        title_label.pack(anchor="w")
        
        desc_label = tk.Label(
            content_frame,
            text=desc,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        desc_label.pack(anchor="w", pady=(2, 0))
        
        # 开关/选择器
        if "主题" in title:
            var = tk.StringVar(value="浅色")
            theme_combo = ttk.Combobox(
                card,
                textvariable=var,
                values=["浅色", "深色", "自动"],
                state="readonly",
                width=10
            )
            theme_combo.pack(side="right", padx=20)
        
        return card
    
    def show_modern_help_page(self):
        """显示现代帮助页面"""
        for widget in self.workspace.winfo_children():
            widget.destroy()
        
        # 创建帮助页面容器
        help_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        help_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 页面标题
        title_label = tk.Label(
            help_frame,
            text="❓ 帮助中心",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 22, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # 帮助内容卡片
        help_items = [
            ("📚", "用户手册", "详细的使用说明和教程"),
            ("🔄", "检查更新", "获取最新版本和功能"),
            ("🐛", "报告问题", "反馈BUG或提出建议"),
            ("💬", "社区支持", "加入用户社区交流")
        ]
        
        for icon, title, desc in help_items:
            card = self.create_help_card(help_frame, icon, title, desc)
            card.pack(fill="x", pady=(0, 15))
    
    def create_help_card(self, parent, icon, title, desc):
        """创建帮助卡片"""
        card = tk.Frame(
            parent,
            bg=self.colors["card_bg"],
            relief="flat",
            cursor="hand2"
        )
        card.config(highlightbackground=self.colors["border"], highlightthickness=1)
        
        # 悬停效果
        def on_enter(e):
            card.config(bg=self.colors["hover"])
            icon_label.config(bg=self.colors["hover"])
            content_frame.config(bg=self.colors["hover"])
            title_label.config(bg=self.colors["hover"])
            desc_label.config(bg=self.colors["hover"])
        
        def on_leave(e):
            card.config(bg=self.colors["card_bg"])
            icon_label.config(bg=self.colors["card_bg"])
            content_frame.config(bg=self.colors["card_bg"])
            title_label.config(bg=self.colors["card_bg"])
            desc_label.config(bg=self.colors["card_bg"])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # 图标
        icon_label = tk.Label(
            card,
            text=icon,
            bg=self.colors["card_bg"],
            font=("Segoe UI", 20)
        )
        icon_label.pack(side="left", padx=20, pady=20)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        
        # 内容
        content_frame = tk.Frame(card, bg=self.colors["card_bg"])
        content_frame.pack(side="left", fill="x", expand=True, pady=20)
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
        
        title_label = tk.Label(
            content_frame,
            text=title,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        title_label.pack(anchor="w")
        title_label.bind("<Enter>", on_enter)
        title_label.bind("<Leave>", on_leave)
        
        desc_label = tk.Label(
            content_frame,
            text=desc,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        desc_label.pack(anchor="w", pady=(2, 0))
        desc_label.bind("<Enter>", on_enter)
        desc_label.bind("<Leave>", on_leave)
        
        # 箭头图标
        arrow_label = tk.Label(
            card,
            text="→",
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.heading_font
        )
        arrow_label.pack(side="right", padx=20)
        arrow_label.bind("<Enter>", on_enter)
        arrow_label.bind("<Leave>", on_leave)
        
        return card
    
    def run(self):
        """运行主程序"""
        self.root.mainloop()

if __name__ == "__main__":
    # 创建并运行现代应用程序
    app = ModernRToolsBox()
    app.run()
