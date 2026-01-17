import tkinter as tk
from tkinter import ttk, messagebox, font
import platform
import psutil
import threading
import time
from datetime import datetime
import sys
import os


class RToolsBox:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows R-tools Box")

        # 设置窗口图标
        icon_path_32 = os.path.join("main", "R-tools 32x32.ico")
        icon_path_128 = os.path.join("main", "R-tools 128x128.ico")

        # 优先使用32x32图标，如果不存在则使用128x128
        if os.path.exists(icon_path_32):
            self.root.iconbitmap(icon_path_32)
        elif os.path.exists(icon_path_128):
            self.root.iconbitmap(icon_path_128)

        # 移除默认标题栏
        self.root.overrideredirect(True)

        # 设置窗口为屏幕3/4大小并居中
        self.setup_window_size()

        # 初始化颜色方案
        self.colors = {
            "primary": "#1e88e5",
            "primary_dark": "#1565c0",
            "primary_light": "#e3f2fd",
            "background": "#ffffff",
            "sidebar_bg": "#f5f5f5",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "text_light": "#ffffff",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336",
            "border": "#e0e0e0",
            "hover": "#f0f0f0",
            "card_bg": "#ffffff"
        }

        # 初始化字体
        self.setup_fonts()

        # 创建自定义标题栏
        self.create_title_bar()

        # 创建主容器
        self.create_main_container()

        # 创建侧边栏
        self.create_sidebar()

        # 创建主工作区
        self.create_main_workspace()

        # 创建状态栏
        self.create_status_bar()

        # 创建标题栏拖动功能
        self.setup_drag_functionality()

        # 初始化内存监控
        self.memory_label = None
        self.update_memory_usage()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

    def setup_fonts(self):
        """初始化字体设置"""
        # 尝试获取系统字体，如果不存在则使用默认字体
        try:
            self.title_font = font.Font(family="Microsoft YaHei", size=14, weight="bold")
            self.heading_font = font.Font(family="Microsoft YaHei", size=12, weight="bold")
            self.body_font = font.Font(family="Microsoft YaHei", size=10)
            self.small_font = font.Font(family="Microsoft YaHei", size=9)
            self.mono_font = font.Font(family="Consolas", size=10)
        except:
            self.title_font = font.Font(size=14, weight="bold")
            self.heading_font = font.Font(size=12, weight="bold")
            self.body_font = font.Font(size=10)
            self.small_font = font.Font(size=9)
            self.mono_font = font.Font(family="Courier", size=10)

    def create_title_bar(self):
        """创建自定义标题栏"""
        title_bar = tk.Frame(
            self.root,
            bg=self.colors["primary"],
            height=40,
            relief="flat"
        )
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        # 标题栏拖动区域
        self.title_bar = title_bar

        # Logo和标题
        logo_frame = tk.Frame(title_bar, bg=self.colors["primary"])
        logo_frame.pack(side="left", padx=(15, 10), pady=10)

        # 模拟Logo（可以用Canvas绘制或使用图片）
        logo_canvas = tk.Canvas(
            logo_frame,
            width=32,
            height=32,
            bg=self.colors["primary"],
            highlightthickness=0
        )
        logo_canvas.pack(side="left")
        # 绘制一个简单的蓝色方形作为Logo
        logo_canvas.create_rectangle(4, 4, 28, 28, fill="#ffffff", outline="")
        logo_canvas.create_text(16, 16, text="R", font=self.title_font, fill=self.colors["primary"])

        title_label = tk.Label(
            title_bar,
            text="Windows R-tools Box",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.title_font
        )
        title_label.pack(side="left", pady=10)

        # 标题栏按钮区域
        button_frame = tk.Frame(title_bar, bg=self.colors["primary"])
        button_frame.pack(side="right", padx=5, pady=10)

        # 最小化按钮
        minimize_btn = tk.Button(
            button_frame,
            text="─",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.title_font,
            bd=0,
            padx=12,
            pady=0,
            activebackground=self.colors["primary_dark"],
            activeforeground=self.colors["text_light"],
            relief="flat",
            command=self.minimize_window
        )
        minimize_btn.pack(side="left", padx=(0, 5))

        # 关闭按钮
        close_btn = tk.Button(
            button_frame,
            text="×",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.title_font,
            bd=0,
            padx=12,
            pady=0,
            activebackground="#f44336",
            activeforeground=self.colors["text_light"],
            relief="flat",
            command=self.on_closing
        )
        close_btn.pack(side="left")

    def create_main_container(self):
        """创建主容器"""
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill="both", expand=True)

        # 侧边栏和主工作区容器
        content_frame = tk.Frame(main_container, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True)

        self.content_frame = content_frame

    def create_sidebar(self):
        """创建侧边导航栏"""
        sidebar = tk.Frame(
            self.content_frame,
            width=220,
            bg=self.colors["sidebar_bg"],
            relief="flat",
            bd=1
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # 侧边栏顶部区域
        sidebar_top = tk.Frame(sidebar, bg=self.colors["sidebar_bg"], height=60)
        sidebar_top.pack(fill="x", pady=(0, 10))
        sidebar_top.pack_propagate(False)

        # 搜索框
        search_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        search_frame.pack(fill="x", padx=10, pady=(10, 15))

        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            font=self.body_font,
            bd=1,
            relief="solid",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["primary"]
        )
        search_entry.pack(fill="x", ipady=4)
        search_entry.insert(0, "搜索工具...")

        # 工具分类列表
        categories_frame = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        categories_frame.pack(fill="both", expand=True, padx=10, pady=10)

        categories = [
            ("🏠", "首页/概览", self.show_home),
            ("🔧", "系统工具", self.show_system_tools),
            ("📁", "文件管理", self.show_file_tools),
            ("🌐", "网络工具", self.show_network_tools),
            ("🛡️", "安全工具", self.show_security_tools),
            ("⚙️", "设置与配置", self.show_settings),
            ("📖", "帮助与文档", self.show_help)
        ]

        self.sidebar_buttons = []
        for icon, text, command in categories:
            btn_frame = tk.Frame(categories_frame, bg=self.colors["sidebar_bg"])
            btn_frame.pack(fill="x", pady=2)

            btn = tk.Button(
                btn_frame,
                text=f"  {icon}  {text}",
                anchor="w",
                bg=self.colors["sidebar_bg"],
                fg=self.colors["text_primary"],
                font=self.body_font,
                bd=0,
                padx=10,
                pady=8,
                activebackground=self.colors["hover"],
                activeforeground=self.colors["text_primary"],
                relief="flat",
                command=command
            )
            btn.pack(fill="x", ipady=4)
            self.sidebar_buttons.append(btn)

        # 侧边栏底部区域
        sidebar_bottom = tk.Frame(sidebar, bg=self.colors["sidebar_bg"], height=80)
        sidebar_bottom.pack(side="bottom", fill="x", pady=(10, 0))
        sidebar_bottom.pack_propagate(False)

        # 版本信息
        version_label = tk.Label(
            sidebar_bottom,
            text="版本: v1.0.0",
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        version_label.pack(anchor="w", padx=10, pady=(5, 0))

        # 按钮区域
        button_bottom_frame = tk.Frame(sidebar_bottom, bg=self.colors["sidebar_bg"])
        button_bottom_frame.pack(fill="x", padx=10, pady=5)

        # GitHub Star 按钮
        github_btn = tk.Button(
            button_bottom_frame,
            text="⭐ GitHub",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.small_font,
            bd=0,
            padx=15,
            pady=4,
            activebackground=self.colors["primary_dark"],
            activeforeground=self.colors["text_light"],
            relief="flat"
        )
        github_btn.pack(side="left", padx=(0, 5))

        # 赞助按钮
        sponsor_btn = tk.Button(
            button_bottom_frame,
            text="❤️ 赞助",
            bg="#ff4081",
            fg=self.colors["text_light"],
            font=self.small_font,
            bd=0,
            padx=15,
            pady=4,
            activebackground="#f50057",
            activeforeground=self.colors["text_light"],
            relief="flat"
        )
        sponsor_btn.pack(side="left")

    def create_main_workspace(self):
        """创建主工作区"""
        workspace = tk.Frame(
            self.content_frame,
            bg=self.colors["background"],
            relief="flat"
        )
        workspace.pack(side="right", fill="both", expand=True)

        # 创建欢迎页面
        self.create_welcome_page(workspace)

        self.workspace = workspace

    def create_welcome_page(self, parent):
        """创建欢迎页面"""
        # 清除现有内容
        for widget in parent.winfo_children():
            widget.destroy()

        # 欢迎页面容器
        welcome_frame = tk.Frame(parent, bg=self.colors["background"])
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            welcome_frame,
            text="欢迎使用 Windows R-tools Box",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=self.title_font
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # 简介卡片
        intro_card = tk.Frame(
            welcome_frame,
            bg=self.colors["card_bg"],
            relief="solid",
            bd=1
        )
        intro_card.pack(fill="x", pady=(0, 20))

        intro_text = """一个为Windows用户打造的高效、纯净、可扩展的开源工具箱。
旨在聚合实用的系统工具，让新手用户开箱即用，高级用户自由定制。

为什么选择我们？
• 纯净透明：所有代码开源，无任何捆绑、后台或隐私收集。
• 即开即用：无需复杂配置，下载即可获得强大的工具集合。
• 模块化设计：每个工具独立，支持自由组合与扩展。
• 尊重自由：不仅提供工具，更赋予您查看、修改和重新分发的权利。"""

        intro_label = tk.Label(
            intro_card,
            text=intro_text,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            justify="left",
            anchor="w"
        )
        intro_label.pack(padx=20, pady=20, fill="both")

        # 快捷功能区域
        quick_tools_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        quick_tools_frame.pack(fill="x", pady=(0, 20))

        quick_label = tk.Label(
            quick_tools_frame,
            text="快捷功能",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        quick_label.pack(anchor="w", pady=(0, 10))

        # 快捷工具卡片容器
        tools_container = tk.Frame(quick_tools_frame, bg=self.colors["background"])
        tools_container.pack(fill="x")

        # 计算每行可以放置的卡片数量
        card_width = 180
        card_height = 150
        spacing = 20
        available_width = self.window_width - 220 - 40  # 减去侧边栏和内边距

        # 创建4个示例工具卡片
        tools = [
            ("磁盘清理", "清理系统临时文件，释放磁盘空间"),
            ("系统信息", "查看详细的系统硬件和软件信息"),
            ("网络诊断", "检测网络连接问题和速度测试"),
            ("文件批量重命名", "批量修改文件名，支持多种规则")
        ]

        for i, (name, desc) in enumerate(tools):
            row = i // 3
            col = i % 3

            card_frame = tk.Frame(
                tools_container,
                width=card_width,
                height=card_height,
                bg=self.colors["card_bg"],
                relief="solid",
                bd=1
            )
            card_frame.grid(row=row, column=col, padx=(0, spacing), pady=(0, spacing))
            card_frame.grid_propagate(False)

            # 工具图标
            icon_label = tk.Label(
                card_frame,
                text="🛠️",
                bg=self.colors["card_bg"],
                font=("Arial", 24)
            )
            icon_label.pack(pady=(15, 5))

            # 工具名称
            name_label = tk.Label(
                card_frame,
                text=name,
                bg=self.colors["card_bg"],
                fg=self.colors["text_primary"],
                font=self.body_font,
                wraplength=card_width - 20
            )
            name_label.pack(pady=(0, 5))

            # 工具描述
            desc_label = tk.Label(
                card_frame,
                text=desc,
                bg=self.colors["card_bg"],
                fg=self.colors["text_secondary"],
                font=self.small_font,
                wraplength=card_width - 20
            )
            desc_label.pack(pady=(0, 10))

            # 使用按钮
            use_btn = tk.Button(
                card_frame,
                text="使用",
                bg=self.colors["primary"],
                fg=self.colors["text_light"],
                font=self.small_font,
                bd=0,
                padx=15,
                pady=3,
                activebackground=self.colors["primary_dark"],
                activeforeground=self.colors["text_light"],
                relief="flat"
            )
            use_btn.pack()

            # 绑定悬停效果
            self.bind_hover_effect(card_frame, use_btn)

        # 更新日志区域
        update_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        update_frame.pack(fill="x", pady=(0, 20))

        update_label = tk.Label(
            update_frame,
            text="最近更新",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.heading_font
        )
        update_label.pack(anchor="w", pady=(0, 10))

        update_text = """• v1.0.0 (2024-01-01): 初始版本发布
• 包含10个常用系统工具
• 优化了用户界面和体验
• 修复了已知的兼容性问题"""

        update_text_label = tk.Label(
            update_frame,
            text=update_text,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.small_font,
            justify="left",
            anchor="w",
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        update_text_label.pack(fill="x")

    def create_status_bar(self):
        """创建状态栏"""
        status_bar = tk.Frame(
            self.root,
            bg=self.colors["sidebar_bg"],
            height=30,
            relief="flat"
        )
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)

        # 左侧状态信息
        status_label = tk.Label(
            status_bar,
            text="就绪",
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        status_label.pack(side="left", padx=(10, 0))

        # 中间进度条区域（默认隐藏）
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_bar,
            variable=self.progress_var,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(side="left", padx=(50, 0))
        self.progress_bar.pack_forget()  # 默认隐藏

        # 右侧状态信息
        right_frame = tk.Frame(status_bar, bg=self.colors["sidebar_bg"])
        right_frame.pack(side="right", padx=(0, 10))

        # 内存使用情况
        memory_frame = tk.Frame(right_frame, bg=self.colors["sidebar_bg"])
        memory_frame.pack(side="left", padx=(0, 15))

        memory_icon = tk.Label(
            memory_frame,
            text="💾",
            bg=self.colors["sidebar_bg"],
            font=self.small_font
        )
        memory_icon.pack(side="left")

        self.memory_label = tk.Label(
            memory_frame,
            text="0%",
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        self.memory_label.pack(side="left", padx=(2, 0))

        # 时间显示
        self.time_label = tk.Label(
            right_frame,
            text=datetime.now().strftime("%H:%M:%S"),
            bg=self.colors["sidebar_bg"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        self.time_label.pack(side="left")

        # 更新时间显示
        self.update_time()

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
        current_time = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'time_label'):
            self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_memory_usage(self):
        """更新内存使用情况显示"""
        if hasattr(self, 'memory_label'):
            memory_percent = psutil.virtual_memory().percent
            self.memory_label.config(text=f"{memory_percent}%")
        self.root.after(5000, self.update_memory_usage)

    def minimize_window(self):
        """最小化窗口"""
        self.root.iconify()

    def on_closing(self):
        """处理窗口关闭"""
        if messagebox.askokcancel("退出", "确定要退出 Windows R-tools Box 吗？"):
            self.root.destroy()
            sys.exit()

    def bind_hover_effect(self, widget, button=None):
        """为部件绑定悬停效果"""

        def on_enter(e):
            if button:
                button.config(bg=self.colors["primary_dark"])
            widget.config(bg=self.colors["hover"])

        def on_leave(e):
            if button:
                button.config(bg=self.colors["primary"])
            widget.config(bg=self.colors["card_bg"])

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

        if button:
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

    # 侧边栏按钮对应的功能
    def show_home(self):
        """显示首页"""
        self.create_welcome_page(self.workspace)

    def show_system_tools(self):
        """显示系统工具"""
        self.show_category_page("系统工具", "🔧")

    def show_file_tools(self):
        """显示文件管理工具"""
        self.show_category_page("文件管理工具", "📁")

    def show_network_tools(self):
        """显示网络工具"""
        self.show_category_page("网络工具", "🌐")

    def show_security_tools(self):
        """显示安全工具"""
        self.show_category_page("安全工具", "🛡️")

    def show_settings(self):
        """显示设置页面"""
        self.show_settings_page()

    def show_help(self):
        """显示帮助页面"""
        self.show_help_page()

    def show_category_page(self, category_name, icon):
        """显示分类工具页面"""
        # 清除现有内容
        for widget in self.workspace.winfo_children():
            widget.destroy()

        # 创建分类页面容器
        category_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        category_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            category_frame,
            text=f"{icon} {category_name}",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=self.title_font
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # 工具数量显示
        count_label = tk.Label(
            category_frame,
            text=f"共 0 个工具",
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.small_font
        )
        count_label.pack(anchor="w", pady=(0, 20))

        # 提示信息
        info_label = tk.Label(
            category_frame,
            text="工具正在开发中，敬请期待...",
            bg=self.colors["background"],
            fg=self.colors["text_secondary"],
            font=self.body_font
        )
        info_label.pack(expand=True)

    def show_settings_page(self):
        """显示设置页面"""
        # 清除现有内容
        for widget in self.workspace.winfo_children():
            widget.destroy()

        # 创建设置页面容器
        settings_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            settings_frame,
            text="⚙️ 设置与配置",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=self.title_font
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # 标签页
        tab_control = ttk.Notebook(settings_frame)

        # 常规设置标签
        general_tab = tk.Frame(tab_control, bg=self.colors["background"])
        tab_control.add(general_tab, text='常规')

        # 外观设置标签
        appearance_tab = tk.Frame(tab_control, bg=self.colors["background"])
        tab_control.add(appearance_tab, text='外观')

        # 高级设置标签
        advanced_tab = tk.Frame(tab_control, bg=self.colors["background"])
        tab_control.add(advanced_tab, text='高级')

        # 关于标签
        about_tab = tk.Frame(tab_control, bg=self.colors["background"])
        tab_control.add(about_tab, text='关于')

        tab_control.pack(fill="both", expand=True)

        # 填充常规设置标签
        self.fill_general_settings(general_tab)

        # 填充关于标签
        self.fill_about_tab(about_tab)

        # 底部按钮
        button_frame = tk.Frame(settings_frame, bg=self.colors["background"])
        button_frame.pack(fill="x", pady=(20, 0))

        save_btn = tk.Button(
            button_frame,
            text="保存设置",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.body_font,
            bd=0,
            padx=30,
            pady=8,
            activebackground=self.colors["primary_dark"],
            activeforeground=self.colors["text_light"],
            relief="flat"
        )
        save_btn.pack(side="right", padx=(10, 0))

        reset_btn = tk.Button(
            button_frame,
            text="重置",
            bg=self.colors["border"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            bd=0,
            padx=30,
            pady=8,
            activebackground=self.colors["hover"],
            activeforeground=self.colors["text_primary"],
            relief="flat"
        )
        reset_btn.pack(side="right")

    def fill_general_settings(self, parent):
        """填充常规设置"""
        # 语言设置
        lang_frame = tk.Frame(parent, bg=self.colors["background"])
        lang_frame.pack(fill="x", padx=20, pady=15)

        lang_label = tk.Label(
            lang_frame,
            text="语言设置:",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            width=15,
            anchor="w"
        )
        lang_label.pack(side="left")

        lang_var = tk.StringVar(value="简体中文")
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=lang_var,
            values=["简体中文", "English"],
            state="readonly",
            width=20
        )
        lang_combo.pack(side="left")

        # 启动设置
        startup_frame = tk.Frame(parent, bg=self.colors["background"])
        startup_frame.pack(fill="x", padx=20, pady=15)

        startup_label = tk.Label(
            startup_frame,
            text="启动选项:",
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            width=15,
            anchor="w"
        )
        startup_label.pack(side="left")

        auto_start_var = tk.BooleanVar()
        auto_start_check = tk.Checkbutton(
            startup_frame,
            text="开机自动启动",
            variable=auto_start_var,
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            anchor="w"
        )
        auto_start_check.pack(side="left")

    def fill_about_tab(self, parent):
        """填充关于标签"""
        about_text = """Windows R-tools Box
版本: v1.0.0
发布日期: 2024-01-01

许可证: GNU Affero 通用公共许可证 v3.0
版权所有 (c) 2024 Regulus-forteen & Windows R-tools box 贡献者

项目主页: https://github.com/Regulus-forteen/Windows-R-tools-box

感谢所有贡献者和用户的支持！"""

        about_label = tk.Label(
            parent,
            text=about_text,
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            justify="left",
            anchor="w"
        )
        about_label.pack(padx=20, pady=20, fill="both", expand=True)

        # 检查更新按钮
        update_btn = tk.Button(
            parent,
            text="检查更新",
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            font=self.body_font,
            bd=0,
            padx=30,
            pady=8,
            activebackground=self.colors["primary_dark"],
            activeforeground=self.colors["text_light"],
            relief="flat"
        )
        update_btn.pack(pady=(0, 20))

    def show_help_page(self):
        """显示帮助页面"""
        # 清除现有内容
        for widget in self.workspace.winfo_children():
            widget.destroy()

        # 创建帮助页面容器
        help_frame = tk.Frame(self.workspace, bg=self.colors["background"])
        help_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            help_frame,
            text="📖 帮助与文档",
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=self.title_font
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # 帮助内容
        help_text = """Windows R-tools Box 使用指南

1. 快速开始
   • 从侧边栏选择工具分类
   • 点击工具卡片中的"使用"按钮启动工具
   • 根据工具提示配置参数并运行

2. 常用快捷键
   • Ctrl+F: 聚焦搜索框
   • Ctrl+Q: 退出程序
   • Esc: 返回上一级

3. 获取帮助
   • 查看在线文档: https://github.com/Regulus-forteen/Windows-R-tools-box/wiki
   • 提交问题: https://github.com/Regulus-forteen/Windows-R-tools-box/issues
   • 加入社区讨论

4. 许可证信息
   本软件采用 AGPL v3 许可证，详情请查看 LICENSE 文件。

5. 贡献代码
   欢迎提交 Pull Request 或报告问题！"""

        help_label = tk.Label(
            help_frame,
            text=help_text,
            bg=self.colors["background"],
            fg=self.colors["text_primary"],
            font=self.body_font,
            justify="left",
            anchor="w"
        )
        help_label.pack(fill="both", expand=True)

    def run(self):
        """运行主程序"""
        self.root.mainloop()


if __name__ == "__main__":
    # 创建并运行应用程序
    app = RToolsBox()
    app.run()