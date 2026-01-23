# main.py - 主程序入口（最小化修改）
import webview
import sys
import json
import os
from pathlib import Path

# 导入配置和工具
from config import config
from utils import get_system_info, format_system_info_for_display, scan_tools, open_url_in_browser, launch_tool

class Api:
    def __init__(self):
        self.tools = []
        self.favorites = []
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        self.tools = scan_tools(config.tools_dir)
        # 加载收藏的工具
        self.favorites = [tool for tool in self.tools if tool.get('favorite', False)]
    
    def get_system_info(self):
        """获取系统信息"""
        info = get_system_info()
        formatted = format_system_info_for_display(info)
        return {
            'success': True,
            'info': formatted
        }
    
    def get_tools(self):
        """获取工具列表"""
        self.load_data()
        return {
            'success': True,
            'tools': self.tools,
            'favorites': self.favorites
        }
    
    def get_search_engines(self):
        """获取搜索引擎"""
        return {
            'success': True,
            'engines': config.search_engines,
            'default': config.settings.get('default_search', '百度')
        }
    
    def get_favorite_sites(self):
        """获取收藏网站"""
        return {
            'success': True,
            'sites': config.favorite_sites
        }
    
    def search(self, query, engine='百度'):
        """执行搜索"""
        if engine in config.search_engines:
            url = config.search_engines[engine]['url'].format(query=query)
            success = open_url_in_browser(url)
            return {
                'success': success,
                'message': f'使用 {engine} 搜索: {query}'
            }
        return {
            'success': False,
            'message': '搜索引擎不存在'
        }
    
    def open_site(self, url):
        """打开网站"""
        success = open_url_in_browser(url)
        return {
            'success': success,
            'message': f'打开网站: {url}'
        }
    
    def launch_tool(self, tool_id):
        """启动工具"""
        success = launch_tool(tool_id)
        return {
            'success': success,
            'message': f'启动工具: {tool_id}'
        }
    
    def toggle_favorite(self, tool_id, favorite):
        """切换收藏状态"""
        for tool in self.tools:
            if tool['id'] == tool_id:
                tool['favorite'] = favorite
                self.load_data()  # 重新加载数据
                return {
                    'success': True,
                    'message': f'工具已{"收藏" if favorite else "取消收藏"}'
                }
        return {
            'success': False,
            'message': '工具不存在'
        }
    
    def get_settings(self):
        """获取设置"""
        return {
            'success': True,
            'settings': config.settings
        }
    
    def save_settings(self, settings):
        """保存设置"""
        config.settings.update(settings)
        success = config.save_config()
        return {
            'success': success,
            'message': '设置已保存' if success else '保存失败'
        }
    
    # 窗口控制方法
    def minimize(self):
        """最小化窗口"""
        try:
            webview.windows[0].minimize()
            return {'success': True}
        except:
            return {'success': False}
    
    def maximize(self):
        """最大化/还原窗口"""
        try:
            window = webview.windows[0]
            if window.maximized:
                window.restore()
            else:
                window.maximize()
            return {'success': True}
        except:
            return {'success': False}
    
    def close(self):
        """关闭窗口"""
        try:
            webview.windows[0].destroy()
            return {'success': True}
        except:
            return {'success': False}

# HTML内容 - 基于原始设计的最小化修改
HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Windows R-tools Box 🧰</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }
        
        :root {
            --primary: #002FA7;        /* 克莱因蓝 */
            --primary-dark: #001F6E;
            --primary-light: #4A6FC1;
            --secondary: #FF6B35;
            --dark: #1f2937;
            --light: #f9fafb;
            --gray: #9ca3af;
            --border: #e5e7eb;
            --card-shadow: 0 4px 6px -1px rgba(0, 47, 167, 0.1), 0 2px 4px -1px rgba(0, 47, 167, 0.06);
            --sidebar-width: 260px;
        }
        
        body {
            background-color: #f8fafc;
            color: var(--dark);
            overflow: hidden;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
        }
        
        /* 自定义标题栏 */
        .title-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 32px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 15px;
            z-index: 1000;
            -webkit-app-region: drag;
            user-select: none;
        }
        
        .title-bar-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .app-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .app-logo i {
            color: white;
        }
        
        .window-controls {
            display: flex;
            -webkit-app-region: no-drag;
        }
        
        .window-btn {
            width: 46px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            color: white;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 12px;
        }
        
        .window-btn:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .window-btn.close:hover {
            background: #ff4757;
        }
        
        /* 侧边栏样式 */
        .sidebar {
            width: var(--sidebar-width);
            background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
            color: white;
            padding: 40px 0 20px;
            display: flex;
            flex-direction: column;
            box-shadow: 2px 0 10px rgba(0, 47, 167, 0.1);
            z-index: 10;
            margin-top: 32px;
        }
        
        .logo-container {
            padding: 0 20px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.3rem;
            font-weight: 700;
        }
        
        .logo i {
            color: var(--secondary);
            font-size: 1.5rem;
        }
        
        .logo-text {
            color: white;
        }
        
        .tagline {
            font-size: 0.75rem;
            color: var(--gray);
            margin-top: 5px;
            margin-left: 42px;
        }
        
        .nav-menu {
            flex: 1;
            overflow-y: auto;
            padding: 0 10px;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            margin: 4px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            color: #d1d5db;
            text-decoration: none;
        }
        
        .nav-item:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        .nav-item.active {
            background-color: rgba(255, 255, 255, 0.15);
            color: white;
            border-left: 3px solid var(--secondary);
        }
        
        .nav-item i {
            width: 20px;
            text-align: center;
        }
        
        .nav-item span {
            font-size: 0.9rem;
        }
        
        .badge {
            background-color: var(--secondary);
            color: white;
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: auto;
        }
        
        .footer-info {
            padding: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.75rem;
            color: var(--gray);
            text-align: center;
        }
        
        .footer-info a {
            color: #90caf9;
            text-decoration: none;
        }
        
        /* 主内容区样式 */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            margin-top: 32px;
        }
        
        .top-bar {
            background-color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0, 47, 167, 0.05);
            z-index: 5;
        }
        
        .page-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--primary-dark);
        }
        
        .actions {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .btn {
            padding: 8px 16px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background-color: var(--primary);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: var(--primary-dark);
        }
        
        .btn-secondary {
            background-color: white;
            color: var(--dark);
            border: 1px solid var(--border);
        }
        
        .btn-secondary:hover {
            background-color: #f3f4f6;
        }
        
        .search-box {
            position: relative;
        }
        
        .search-box input {
            padding: 10px 16px 10px 40px;
            border-radius: 6px;
            border: 1px solid var(--border);
            width: 250px;
            font-size: 0.9rem;
            background-color: #f9fafb;
        }
        
        .search-box i {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
        }
        
        .content-area {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            background-color: #f8fafc;
        }
        
        /* 搜索区域样式 */
        .search-section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: var(--card-shadow);
            margin-bottom: 30px;
            border: 1px solid var(--border);
        }
        
        .search-engine-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .engine-btn {
            padding: 8px 16px;
            border-radius: 20px;
            border: 2px solid var(--border);
            background: white;
            color: var(--dark);
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
            font-weight: 500;
        }
        
        .engine-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--card-shadow);
        }
        
        .engine-btn.active {
            border-color: var(--primary);
            background: var(--primary);
            color: white;
        }
        
        .search-container {
            position: relative;
        }
        
        .search-input-large {
            width: 100%;
            padding: 15px 60px 15px 25px;
            border-radius: 10px;
            border: 2px solid var(--border);
            font-size: 16px;
            background: white;
            box-shadow: var(--card-shadow);
            transition: all 0.3s;
        }
        
        .search-input-large:focus {
            outline: none;
            border-color: var(--primary);
        }
        
        .search-btn-large {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: var(--primary);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        
        .search-btn-large:hover {
            background: var(--primary-dark);
        }
        
        /* 工具卡片样式 */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .tool-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--card-shadow);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border);
            cursor: pointer;
        }
        
        .tool-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 47, 167, 0.1);
        }
        
        .tool-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 12px;
        }
        
        .tool-icon {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
        }
        
        .icon-system {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        }
        
        .icon-security {
            background: linear-gradient(135deg, #10b981, #047857);
        }
        
        .icon-network {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        }
        
        .icon-utility {
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }
        
        .tool-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--dark);
        }
        
        .tool-desc {
            color: #6b7280;
            line-height: 1.5;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }
        
        .tool-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        
        .tool-status {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.8rem;
        }
        
        .status-on {
            color: #10b981;
        }
        
        .status-off {
            color: #ef4444;
        }
        
        .tool-actions button {
            padding: 6px 12px;
            font-size: 0.85rem;
        }
        
        /* 收藏网站卡片样式 */
        .site-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--card-shadow);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border);
            cursor: pointer;
        }
        
        .site-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 47, 167, 0.1);
        }
        
        .site-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 12px;
        }
        
        .site-icon {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            background: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
        }
        
        .site-info h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 5px;
        }
        
        .site-info p {
            color: #6b7280;
            font-size: 0.85rem;
        }
        
        .site-category {
            display: inline-block;
            padding: 3px 8px;
            background: rgba(0, 47, 167, 0.1);
            color: var(--primary);
            border-radius: 4px;
            font-size: 0.75rem;
            margin-top: 5px;
        }
        
        /* 系统信息样式 */
        .system-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .info-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border);
        }
        
        .info-card h3 {
            color: var(--primary);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0, 47, 167, 0.1);
            font-size: 1.1rem;
        }
        
        .info-item {
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(0, 47, 167, 0.05);
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .info-label {
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 3px;
            font-size: 0.9rem;
        }
        
        .info-value {
            color: var(--text);
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        /* 页面切换效果 */
        .page {
            display: none;
            animation: fadeIn 0.3s ease;
        }
        
        .page.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 响应式设计 */
        @media (max-width: 1024px) {
            .sidebar {
                width: 70px;
            }
            
            .logo-text, .tagline, .nav-item span, .badge {
                display: none;
            }
            
            .logo-container {
                padding: 15px 10px;
            }
            
            .logo {
                justify-content: center;
            }
            
            .footer-info {
                font-size: 0.65rem;
                padding: 10px;
            }
            
            .search-box input {
                width: 200px;
            }
            
            .tools-grid {
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            }
        }
        
        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            
            .tools-grid {
                grid-template-columns: 1fr;
            }
            
            .system-info-grid {
                grid-template-columns: 1fr;
            }
            
            .search-box input {
                width: 150px;
            }
        }
        
        /* 滚动条样式 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary-light);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary);
        }
        
        /* 通知样式 */
        .notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(0, 47, 167, 0.2);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    </style>
</head>
<body>
    <!-- 自定义标题栏 -->
    <div class="title-bar">
        <div class="title-bar-left">
            <div class="app-logo">
                <i class="fas fa-toolbox"></i>
                <span class="logo-text">R-tools Box</span>
            </div>
        </div>
        <div class="window-controls">
            <button class="window-btn" onclick="minimizeWindow()">
                <i class="fas fa-minus"></i>
            </button>
            <button class="window-btn" onclick="maximizeWindow()">
                <i class="far fa-window-maximize"></i>
            </button>
            <button class="window-btn close" onclick="closeWindow()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    </div>
    
    <div class="app-container">
        <!-- 侧边栏 -->
        <div class="sidebar">
            <div class="logo-container">
                <div class="logo">
                    <i class="fas fa-toolbox"></i>
                    <span class="logo-text">R-tools Box</span>
                </div>
                <div class="tagline">让开源的工具，赋予Windows更多可能</div>
            </div>
            
            <div class="nav-menu">
                <a href="#" class="nav-item active" onclick="switchPage('dashboard')">
                    <i class="fas fa-home"></i>
                    <span>主页</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('system')">
                    <i class="fas fa-desktop"></i>
                    <span>系统信息</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('tools')">
                    <i class="fas fa-tools"></i>
                    <span>所有工具</span>
                    <span class="badge" id="tools-count">0</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('settings')">
                    <i class="fas fa-cog"></i>
                    <span>设置</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('about')">
                    <i class="fas fa-info-circle"></i>
                    <span>关于</span>
                </a>
            </div>
            
            <div class="footer-info">
                <p>版本 1.0.0 | <a href="#" onclick="switchPage('license')">AGPL v3</a></p>
                <p>© 2024 Regulus-forteen & 贡献者</p>
            </div>
        </div>
        
        <!-- 主内容区 -->
        <div class="main-content">
            <div class="top-bar">
                <div class="page-title" id="page-title">主页</div>
                
                <div class="actions">
                    <div class="search-box">
                        <i class="fas fa-search"></i>
                        <input type="text" id="search-tools" placeholder="搜索工具..." onkeyup="searchTools()">
                    </div>
                    
                    <button class="btn btn-secondary" onclick="refreshTools()">
                        <i class="fas fa-sync-alt"></i>
                        刷新
                    </button>
                    
                    <button class="btn btn-primary" onclick="checkForUpdates()">
                        <i class="fas fa-download"></i>
                        检查更新
                    </button>
                </div>
            </div>
            
            <div class="content-area">
                <!-- 主页 -->
                <div id="dashboard" class="page active">
                    <!-- 搜索区域 -->
                    <div class="search-section">
                        <h3 style="color: var(--primary); margin-bottom: 15px;">快速搜索</h3>
                        <div class="search-engine-selector" id="engine-selector">
                            <!-- 搜索引擎按钮将通过JS动态生成 -->
                        </div>
                        <div class="search-container">
                            <input type="text" class="search-input-large" id="main-search-input" 
                                   placeholder="输入要搜索的内容，按回车键搜索..." 
                                   onkeypress="if(event.keyCode==13) performMainSearch()">
                            <button class="search-btn-large" onclick="performMainSearch()">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    </div>
                    
                    <!-- 收藏网站 -->
                    <h3 style="color: var(--primary); margin: 20px 0 15px;">
                        <i class="fas fa-star" style="margin-right: 10px;"></i>
                        收藏网站
                    </h3>
                    <div class="tools-grid" id="favorite-sites">
                        <!-- 收藏网站将通过JS动态生成 -->
                    </div>
                    
                    <!-- 收藏工具 -->
                    <h3 style="color: var(--primary); margin: 30px 0 15px;">
                        <i class="fas fa-tools" style="margin-right: 10px;"></i>
                        收藏工具
                    </h3>
                    <div class="tools-grid" id="favorite-tools">
                        <!-- 收藏工具将通过JS动态生成 -->
                    </div>
                </div>
                
                <!-- 系统信息页面 -->
                <div id="system" class="page">
                    <h2 style="color: var(--primary); margin-bottom: 20px;">系统信息</h2>
                    <p style="color: var(--text-light); margin-bottom: 25px;">详细的系统硬件和软件信息</p>
                    
                    <div class="system-info-grid" id="system-info-grid">
                        <!-- 系统信息将通过JS动态生成 -->
                    </div>
                </div>
                
                <!-- 所有工具页面 -->
                <div id="tools" class="page">
                    <h2 style="color: var(--primary); margin-bottom: 20px;">所有工具</h2>
                    <p style="color: var(--text-light); margin-bottom: 25px;">工具箱中的所有可用工具</p>
                    
                    <div class="tools-grid" id="all-tools">
                        <!-- 所有工具将通过JS动态生成 -->
                    </div>
                </div>
                
                <!-- 设置页面 -->
                <div id="settings" class="page">
                    <h2 style="color: var(--primary); margin-bottom: 20px;">设置</h2>
                    <p style="color: var(--text-light); margin-bottom: 25px;">自定义工具箱的行为和外观</p>
                    
                    <div class="info-card" style="max-width: 700px;">
                        <h3>常规设置</h3>
                        
                        <div class="info-item">
                            <div class="info-label">默认搜索引擎</div>
                            <select id="default-engine" class="search-input-large" style="width: 100%; margin-top: 5px; padding: 10px;">
                                <!-- 搜索引擎选项将通过JS动态生成 -->
                            </select>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">启动时检查更新</div>
                            <label style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                                <input type="checkbox" id="check-updates">
                                <span>自动检查新版本</span>
                            </label>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">显示收藏网站</div>
                            <label style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                                <input type="checkbox" id="show-sites">
                                <span>在主页显示收藏网站</span>
                            </label>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">显示收藏工具</div>
                            <label style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                                <input type="checkbox" id="show-tools">
                                <span>在主页显示收藏工具</span>
                            </label>
                        </div>
                        
                        <button class="btn btn-primary" style="width: 100%; margin-top: 20px;" onclick="saveSettings()">
                            <i class="fas fa-save"></i> 保存设置
                        </button>
                    </div>
                </div>
                
                <!-- 关于页面 -->
                <div id="about" class="page">
                    <h2 style="color: var(--primary); margin-bottom: 20px;">关于 Windows R-tools Box</h2>
                    
                    <div class="info-card" style="max-width: 800px;">
                        <h3>开源工具箱</h3>
                        <div class="info-item">
                            <div class="info-label">版本</div>
                            <div class="info-value">1.0.0</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">作者</div>
                            <div class="info-value">Regulus-forteen & Windows R-tools box 贡献者</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">许可证</div>
                            <div class="info-value">GNU Affero 通用公共许可证 v3.0 (AGPL v3)</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">描述</div>
                            <div class="info-value">
                                <p>一个为Windows用户打造的高效、纯净、可扩展的开源工具箱。</p>
                                <p>旨在聚合实用的系统工具，让<strong>新手用户开箱即用，高级用户自由定制</strong>。</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">特色</div>
                            <div class="info-value">
                                <p>🛡️ <strong>纯净透明</strong>：所有代码开源，无任何捆绑、后台或隐私收集。</p>
                                <p>🔧 <strong>即开即用</strong>：无需复杂配置，下载即可获得强大的工具集合。</p>
                                <p>🧩 <strong>模块化设计</strong>：每个工具独立，支持自由组合与扩展。</p>
                                <p>⚙️ <strong>尊重自由</strong>：不仅提供工具，更赋予您查看、修改和重新分发的权利。</p>
                            </div>
                        </div>
                        <button class="btn btn-secondary" onclick="window.pywebview.api.open_repository ? window.pywebview.api.open_repository() : alert('GitHub仓库功能未实现')">
                            <i class="fab fa-github"></i> 访问GitHub仓库
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 全局变量
        let currentSearchEngine = '百度';
        let toolsData = [];
        
        // 页面切换函数
        function switchPage(pageId) {
            // 更新活动导航项
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // 更新页面标题
            const pageTitles = {
                'dashboard': '主页',
                'system': '系统信息',
                'tools': '所有工具',
                'settings': '设置',
                'about': '关于'
            };
            document.getElementById('page-title').textContent = pageTitles[pageId] || 'R-tools Box';
            
            // 切换页面内容
            document.querySelectorAll('.page').forEach(page => {
                page.classList.remove('active');
            });
            document.getElementById(pageId).classList.add('active');
            
            // 如果切换到工具页面，加载工具
            if (['tools', 'dashboard'].includes(pageId)) {
                loadToolsForPage(pageId);
            } else if (pageId === 'system') {
                loadSystemInfo();
            } else if (pageId === 'dashboard') {
                loadHomePage();
            }
            
            return false;
        }
        
        // 加载主页
        async function loadHomePage() {
            // 加载搜索引擎
            await loadSearchEngines();
            
            // 加载收藏网站
            await loadFavoriteSites();
            
            // 加载收藏工具
            await loadFavoriteTools();
        }
        
        // 加载搜索引擎
        async function loadSearchEngines() {
            try {
                const response = await window.pywebview.api.get_search_engines();
                if (response.success) {
                    const selector = document.getElementById('engine-selector');
                    selector.innerHTML = '';
                    
                    for (const [name, engine] of Object.entries(response.engines)) {
                        const btn = document.createElement('button');
                        btn.className = `engine-btn ${name === response.default ? 'active' : ''}`;
                        btn.innerHTML = `<i class="${engine.icon}"></i> ${name}`;
                        btn.onclick = () => selectSearchEngine(name, btn);
                        selector.appendChild(btn);
                        
                        if (name === response.default) {
                            currentSearchEngine = name;
                        }
                    }
                }
            } catch (error) {
                console.error('加载搜索引擎失败:', error);
            }
        }
        
        // 选择搜索引擎
        function selectSearchEngine(engine, button) {
            currentSearchEngine = engine;
            document.querySelectorAll('.engine-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            button.classList.add('active');
        }
        
        // 执行主搜索
        async function performMainSearch() {
            const query = document.getElementById('main-search-input').value.trim();
            if (!query) return;
            
            try {
                const response = await window.pywebview.api.search(query, currentSearchEngine);
                showNotification(response.message, response.success ? 'info' : 'error');
            } catch (error) {
                showNotification('搜索失败', 'error');
            }
        }
        
        // 加载收藏网站
        async function loadFavoriteSites() {
            try {
                const response = await window.pywebview.api.get_favorite_sites();
                if (response.success) {
                    const container = document.getElementById('favorite-sites');
                    container.innerHTML = '';
                    
                    response.sites.forEach(site => {
                        const card = document.createElement('div');
                        card.className = 'site-card';
                        card.onclick = () => openSite(site.url);
                        card.innerHTML = `
                            <div class="site-header">
                                <div class="site-icon">
                                    <i class="${site.icon}"></i>
                                </div>
                                <div class="site-info">
                                    <h3>${site.name}</h3>
                                    <p>${site.url}</p>
                                    <span class="site-category">${site.category}</span>
                                </div>
                            </div>
                        `;
                        container.appendChild(card);
                    });
                }
            } catch (error) {
                console.error('加载收藏网站失败:', error);
            }
        }
        
        // 加载收藏工具
        async function loadFavoriteTools() {
            try {
                const response = await window.pywebview.api.get_tools();
                if (response.success) {
                    toolsData = response.tools;
                    const container = document.getElementById('favorite-tools');
                    container.innerHTML = '';
                    
                    const favorites = response.favorites;
                    if (favorites.length === 0) {
                        container.innerHTML = '<p style="text-align: center; color: #999; grid-column: 1 / -1;">暂无收藏的工具</p>';
                        return;
                    }
                    
                    favorites.forEach(tool => {
                        const card = createToolCard(tool);
                        container.appendChild(card);
                    });
                    
                    // 更新工具数量
                    document.getElementById('tools-count').textContent = toolsData.length;
                }
            } catch (error) {
                console.error('加载收藏工具失败:', error);
            }
        }
        
        // 加载所有工具
        async function loadAllTools() {
            try {
                const response = await window.pywebview.api.get_tools();
                if (response.success) {
                    toolsData = response.tools;
                    const container = document.getElementById('all-tools');
                    container.innerHTML = '';
                    
                    toolsData.forEach(tool => {
                        const card = createToolCard(tool);
                        container.appendChild(card);
                    });
                    
                    // 更新工具数量
                    document.getElementById('tools-count').textContent = toolsData.length;
                }
            } catch (error) {
                console.error('加载工具失败:', error);
            }
        }
        
        // 加载系统信息
        async function loadSystemInfo() {
            try {
                const response = await window.pywebview.api.get_system_info();
                if (response.success) {
                    const container = document.getElementById('system-info-grid');
                    container.innerHTML = '';
                    
                    response.info.forEach(([title, info]) => {
                        const card = document.createElement('div');
                        card.className = 'info-card';
                        
                        let content = '';
                        if (typeof info === 'object') {
                            for (const [key, value] of Object.entries(info)) {
                                content += `
                                    <div class="info-item">
                                        <div class="info-label">${key}</div>
                                        <div class="info-value">${value}</div>
                                    </div>
                                `;
                            }
                        } else {
                            content = `
                                <div class="info-item">
                                    <div class="info-value">${info}</div>
                                </div>
                            `;
                        }
                        
                        card.innerHTML = `
                            <h3>${title}</h3>
                            ${content}
                        `;
                        container.appendChild(card);
                    });
                }
            } catch (error) {
                console.error('加载系统信息失败:', error);
            }
        }
        
        // 创建工具卡片
        function createToolCard(tool) {
            const card = document.createElement('div');
            card.className = 'tool-card';
            card.innerHTML = `
                <div class="tool-header">
                    <div class="tool-icon icon-${tool.category}">
                        <i class="${tool.icon || 'fas fa-tools'}"></i>
                    </div>
                    <div>
                        <div class="tool-title">${tool.name}</div>
                        <div class="tool-status">
                            <i class="fas fa-circle status-${tool.status}"></i>
                            <span>${tool.status === 'on' ? '可用' : '维护中'}</span>
                        </div>
                    </div>
                </div>
                <div class="tool-desc">${tool.description || '暂无描述'}</div>
                <div class="tool-footer">
                    <div class="tool-status">
                        <i class="fas fa-heart" style="color: ${tool.favorite ? '#ef4444' : '#9ca3af'}; cursor: pointer;" 
                           onclick="toggleFavorite('${tool.id}')" title="${tool.favorite ? '取消收藏' : '收藏'}"></i>
                        <span style="margin-left: 5px;">${tool.category === 'system' ? '系统' : 
                                                       tool.category === 'security' ? '安全' : 
                                                       tool.category === 'network' ? '网络' : '实用'}</span>
                    </div>
                    <button class="btn ${tool.status === 'on' ? 'btn-primary' : 'btn-secondary'}" 
                            onclick="launchTool('${tool.id}')" ${tool.status === 'off' ? 'disabled' : ''}>
                        <i class="fas fa-play"></i>
                        ${tool.status === 'on' ? '启动' : '暂不可用'}
                    </button>
                </div>
            `;
            
            return card;
        }
        
        // 搜索工具
        function searchTools() {
            const searchTerm = document.getElementById('search-tools').value.toLowerCase();
            const container = document.getElementById('all-tools');
            if (!container) return;
            
            const toolCards = container.querySelectorAll('.tool-card');
            
            toolCards.forEach(card => {
                const title = card.querySelector('.tool-title').textContent.toLowerCase();
                const desc = card.querySelector('.tool-desc').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || desc.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // 启动工具
        async function launchTool(toolId) {
            try {
                const response = await window.pywebview.api.launch_tool(toolId);
                showNotification(response.message, response.success ? 'info' : 'error');
            } catch (error) {
                showNotification('启动失败', 'error');
            }
        }
        
        // 切换收藏状态
        async function toggleFavorite(toolId) {
            const tool = toolsData.find(t => t.id === toolId);
            if (tool) {
                const newFavorite = !tool.favorite;
                try {
                    const response = await window.pywebview.api.toggle_favorite(toolId, newFavorite);
                    if (response.success) {
                        tool.favorite = newFavorite;
                        
                        // 重新加载收藏工具
                        await loadFavoriteTools();
                        await loadAllTools();
                        
                        showNotification(response.message, 'info');
                    }
                } catch (error) {
                    showNotification('操作失败', 'error');
                }
            }
        }
        
        // 打开网站
        async function openSite(url) {
            try {
                const response = await window.pywebview.api.open_site(url);
                if (!response.success) {
                    showNotification('打开失败', 'error');
                }
            } catch (error) {
                showNotification('打开失败', 'error');
            }
        }
        
        // 刷新工具
        async function refreshTools() {
            showNotification('正在刷新工具列表...', 'info');
            
            try {
                const response = await window.pywebview.api.get_tools();
                if (response.success) {
                    toolsData = response.tools;
                    
                    const activePage = document.querySelector('.page.active').id;
                    if (activePage === 'tools') {
                        await loadAllTools();
                    } else if (activePage === 'dashboard') {
                        await loadFavoriteTools();
                    }
                    
                    showNotification('工具列表已刷新', 'success');
                }
            } catch (error) {
                showNotification('刷新失败', 'error');
            }
        }
        
        // 检查更新
        async function checkForUpdates() {
            showNotification('正在检查更新...', 'info');
            // 这里可以调用API检查更新
            setTimeout(() => {
                showNotification('当前已是最新版本 (v1.0.0)', 'info');
            }, 1000);
        }
        
        // 显示通知
        function showNotification(message, type = 'info') {
            // 移除现有的通知
            const existing = document.querySelector('.notification');
            if (existing) {
                existing.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => existing.remove(), 300);
            }
            
            // 创建新通知
            const notification = document.createElement('div');
            notification.className = `notification`;
            notification.style.backgroundColor = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#002FA7';
            
            notification.innerHTML = `
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            `;
            
            document.body.appendChild(notification);
            
            // 3秒后自动移除
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOut 0.3s ease';
                    setTimeout(() => notification.remove(), 300);
                }
            }, 3000);
        }
        
        // 加载设置
        async function loadSettings() {
            try {
                const response = await window.pywebview.api.get_settings();
                if (response.success) {
                    document.getElementById('check-updates').checked = response.settings.check_updates;
                    document.getElementById('show-sites').checked = response.settings.show_favorites;
                    document.getElementById('show-tools').checked = response.settings.show_tools;
                    
                    // 加载搜索引擎选项
                    const engines = await window.pywebview.api.get_search_engines();
                    const select = document.getElementById('default-engine');
                    select.innerHTML = '';
                    
                    for (const [name, engine] of Object.entries(engines.engines)) {
                        const option = document.createElement('option');
                        option.value = name;
                        option.textContent = name;
                        if (name === response.settings.default_search) {
                            option.selected = true;
                        }
                        select.appendChild(option);
                    }
                }
            } catch (error) {
                console.error('加载设置失败:', error);
            }
        }
        
        // 保存设置
        async function saveSettings() {
            const settings = {
                default_search: document.getElementById('default-engine').value,
                check_updates: document.getElementById('check-updates').checked,
                show_favorites: document.getElementById('show-sites').checked,
                show_tools: document.getElementById('show-tools').checked
            };
            
            try {
                const response = await window.pywebview.api.save_settings(settings);
                showNotification(response.message, response.success ? 'success' : 'error');
                
                // 更新当前搜索引擎
                if (settings.default_search !== currentSearchEngine) {
                    await loadSearchEngines();
                }
            } catch (error) {
                showNotification('保存失败', 'error');
            }
        }
        
        // 窗口控制函数
        function minimizeWindow() {
            window.pywebview.api.minimize();
        }
        
        function maximizeWindow() {
            window.pywebview.api.maximize();
        }
        
        function closeWindow() {
            window.pywebview.api.close();
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', async () => {
            // 等待API就绪
            const checkApi = setInterval(() => {
                if (window.pywebview && window.pywebview.api) {
                    clearInterval(checkApi);
                    
                    // 加载主页数据
                    loadHomePage();
                }
            }, 100);
            
            // 搜索框回车事件
            document.getElementById('main-search-input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') performMainSearch();
            });
        });
    </script>
</body>
</html>'''

def main():
    # 初始化API
    api = Api()
    
    # 打印启动信息
    print("=" * 60)
    print(f"正在启动 Windows R-tools Box...")
    print(f"版本: 1.0.0")
    print(f"作者: Regulus-forteen")
    print(f"许可证: AGPL v3")
    print("=" * 60)
    
    # 检查管理员权限
    if sys.platform == 'win32':
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("⚠️  注意：某些系统工具可能需要管理员权限。")
                print("建议以管理员身份运行以获得完整功能。")
        except:
            pass
    
    print("🎯 功能特色:")
    print("  • 🛡️  纯净透明 - 所有代码开源，无捆绑、无后台")
    print("  • 🔧  即开即用 - 无需复杂配置，下载即用")
    print("  • 🧩  模块化设计 - 工具独立，自由组合扩展")
    print("  • ⚙️  尊重自由 - 查看、修改、重新分发")
    print("-" * 60)
    print("🚀 正在加载主界面...")
    
    try:
        # 创建窗口
        window = webview.create_window(
            "Windows R-tools Box 🧰",
            html=HTML_CONTENT,
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True,
            easy_drag=False,
            js_api=api,
            frameless=True  # 无边框窗口
        )
        
        print("✅ 窗口创建成功")
        
        # 启动应用
        webview.start(debug=False)
        print("👋 程序已退出")
        
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # 检查依赖
    try:
        import webview
        import psutil
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("💡 请安装依赖:")
        print("   pip install pywebview psutil")
        sys.exit(1)
    
    # 运行主函数
    main()
