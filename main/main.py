# main.py
import webview
import sys
import os
import json
from pathlib import Path
import webbrowser

# API类 - 暴露给JavaScript的方法
class Api:
    def __init__(self):
        self.tools = []
        self.settings = {
            'check_updates': True,
            'theme': 'light',
            'auto_start': False
        }
        self.load_tools()
    
    def load_tools(self):
        """加载工具数据"""
        self.tools = [
            {"id": 1, "name": "系统优化器", "desc": "清理临时文件、优化启动项和系统设置", "category": "system", "icon": "fas fa-rocket", "status": "on", "favorite": True},
            {"id": 2, "name": "隐私清理", "desc": "清除浏览器历史记录、Cookies和隐私数据", "category": "security", "icon": "fas fa-user-shield", "status": "on", "favorite": True},
            {"id": 3, "name": "网络诊断", "desc": "检测网络连接问题，分析网络速度", "category": "network", "icon": "fas fa-wifi", "status": "on", "favorite": False},
            {"id": 4, "name": "文件批量重命名", "desc": "批量重命名文件，支持多种规则", "category": "utilities", "icon": "fas fa-file-signature", "status": "on", "favorite": True},
            {"id": 5, "name": "进程管理器", "desc": "查看和管理系统进程，结束异常进程", "category": "system", "icon": "fas fa-tasks", "status": "on", "favorite": False},
            {"id": 6, "name": "密码生成器", "desc": "生成安全的随机密码", "category": "security", "icon": "fas fa-key", "status": "off", "favorite": True},
            {"id": 7, "name": "端口扫描器", "desc": "扫描本地或远程主机的开放端口", "category": "network", "icon": "fas fa-search", "status": "on", "favorite": False},
            {"id": 8, "name": "截图工具", "desc": "快速截图并编辑，支持多种格式", "category": "utilities", "icon": "fas fa-camera", "status": "on", "favorite": True},
            {"id": 9, "name": "注册表清理", "desc": "安全清理无效的注册表项", "category": "system", "icon": "fas fa-database", "status": "off", "favorite": False},
            {"id": 10, "name": "文件加密", "desc": "使用AES加密算法保护敏感文件", "category": "security", "icon": "fas fa-lock", "status": "on", "favorite": False},
            {"id": 11, "name": "网络速度测试", "desc": "测试上传和下载速度", "category": "network", "icon": "fas fa-tachometer-alt", "status": "on", "favorite": True},
            {"id": 12, "name": "单位转换器", "desc": "转换长度、重量、温度等单位", "category": "utilities", "icon": "fas fa-exchange-alt", "status": "on", "favorite": False}
        ]
        return self.tools
    
    def get_tools(self):
        """获取工具列表"""
        return {
            'success': True,
            'tools': self.tools
        }
    
    def get_tool_stats(self):
        """获取工具统计信息"""
        total = len(self.tools)
        active = sum(1 for tool in self.tools if tool["status"] == "on")
        favorite = sum(1 for tool in self.tools if tool["favorite"])
        return {
            'total': total,
            'active': active,
            'favorite': favorite
        }
    
    def launch_tool(self, tool_id):
        """启动工具"""
        tool = next((t for t in self.tools if t["id"] == tool_id), None)
        if tool:
            # 在实际应用中，这里会启动对应的工具
            print(f"正在启动工具: {tool['name']} (ID: {tool_id})")
            return {
                'success': True,
                'message': f'工具 "{tool["name"]}" 启动成功'
            }
        return {
            'success': False,
            'message': '工具不存在'
        }
    
    def toggle_favorite(self, tool_id, favorite):
        """切换收藏状态"""
        for tool in self.tools:
            if tool["id"] == tool_id:
                tool["favorite"] = favorite
                return {
                    'success': True,
                    'message': f'工具已{"收藏" if favorite else "取消收藏"}'
                }
        return {
            'success': False,
            'message': '工具不存在'
        }
    
    def update_setting(self, key, value):
        """更新设置"""
        if key in self.settings:
            self.settings[key] = value
            return {'success': True}
        return {'success': False, 'message': '设置项不存在'}
    
    def save_settings(self):
        """保存设置"""
        # 在实际应用中，这里会保存到配置文件
        print(f"保存设置: {json.dumps(self.settings, indent=2, ensure_ascii=False)}")
        return {'success': True}
    
    def check_updates(self):
        """检查更新"""
        return {
            'has_update': False,
            'latest_version': '1.0.0',
            'message': '当前已是最新版本'
        }
    
    def open_repository(self):
        """打开GitHub仓库"""
        try:
            webbrowser.open('https://github.com/Regulus-forteen/Windows-R-tools-box')
            return {'success': True}
        except:
            return {'success': False, 'message': '无法打开浏览器'}

# HTML 内容
def get_html_content():
    return '''<!DOCTYPE html>
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
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #10b981;
            --dark: #1f2937;
            --light: #f9fafb;
            --gray: #9ca3af;
            --border: #e5e7eb;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
        
        /* 侧边栏样式 */
        .sidebar {
            width: var(--sidebar-width);
            background: linear-gradient(180deg, var(--dark) 0%, #111827 100%);
            color: white;
            padding: 20px 0;
            display: flex;
            flex-direction: column;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            z-index: 10;
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
            font-size: 1.5rem;
            font-weight: 700;
        }
        
        .logo i {
            color: var(--secondary);
            font-size: 1.8rem;
        }
        
        .logo-text {
            background: linear-gradient(90deg, #60a5fa, var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .tagline {
            font-size: 0.8rem;
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
            padding: 14px 16px;
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
            background-color: rgba(37, 99, 235, 0.2);
            color: white;
            border-left: 3px solid var(--primary);
        }
        
        .nav-item i {
            width: 20px;
            text-align: center;
        }
        
        .nav-item span {
            font-size: 0.95rem;
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
            padding: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.8rem;
            color: var(--gray);
            text-align: center;
        }
        
        .footer-info a {
            color: #60a5fa;
            text-decoration: none;
        }
        
        /* 主内容区样式 */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .top-bar {
            background-color: white;
            padding: 18px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            z-index: 5;
        }
        
        .page-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--dark);
        }
        
        .actions {
            display: flex;
            gap: 15px;
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
            padding: 30px;
            overflow-y: auto;
            background-color: #f8fafc;
        }
        
        /* 工具卡片样式 */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 24px;
            margin-top: 20px;
        }
        
        .tool-card {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--card-shadow);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border);
        }
        
        .tool-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        .tool-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 16px;
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
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
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
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark);
        }
        
        .tool-desc {
            color: #6b7280;
            line-height: 1.5;
            margin-bottom: 20px;
            font-size: 0.95rem;
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
            font-size: 0.85rem;
        }
        
        .status-on {
            color: var(--secondary);
        }
        
        .status-off {
            color: #ef4444;
        }
        
        .tool-actions button {
            padding: 6px 12px;
            font-size: 0.85rem;
        }
        
        /* 仪表板样式 */
        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: var(--card-shadow);
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .stat-info h3 {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--dark);
        }
        
        .stat-info p {
            color: var(--gray);
            font-size: 0.9rem;
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
            from { opacity: 0; }
            to { opacity: 1; }
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
                padding: 20px 10px;
            }
            
            .logo {
                justify-content: center;
            }
            
            .footer-info {
                font-size: 0.7rem;
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
            
            .dashboard-stats {
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
            background: #c1c1c1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
        
        /* 通知样式 */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .notification.success {
            background-color: #10b981;
        }
        
        .notification.error {
            background-color: #ef4444;
        }
        
        .notification.info {
            background-color: #3b82f6;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        /* 加载动画 */
        .loader {
            border: 3px solid #f3f3f3;
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 50px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
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
                    <span>仪表板</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('tools')">
                    <i class="fas fa-tools"></i>
                    <span>所有工具</span>
                    <span class="badge" id="tools-count">12</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('system')">
                    <i class="fas fa-desktop"></i>
                    <span>系统工具</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('security')">
                    <i class="fas fa-shield-alt"></i>
                    <span>安全工具</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('network')">
                    <i class="fas fa-network-wired"></i>
                    <span>网络工具</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('utilities')">
                    <i class="fas fa-cogs"></i>
                    <span>实用工具</span>
                </a>
                
                <a href="#" class="nav-item" onclick="switchPage('settings')">
                    <i class="fas fa-sliders-h"></i>
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
                <div class="page-title" id="page-title">仪表板</div>
                
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
                <!-- 仪表板页面 -->
                <div id="dashboard" class="page active">
                    <h2>欢迎使用 Windows R-tools Box</h2>
                    <p class="tool-desc">一个为Windows用户打造的高效、纯净、可扩展的开源工具箱。</p>
                    
                    <div class="dashboard-stats">
                        <div class="stat-card">
                            <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);">
                                <i class="fas fa-tools" style="color: white;"></i>
                            </div>
                            <div class="stat-info">
                                <h3 id="total-tools">12</h3>
                                <p>可用工具</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: linear-gradient(135deg, #10b981, #047857);">
                                <i class="fas fa-check-circle" style="color: white;"></i>
                            </div>
                            <div class="stat-info">
                                <h3 id="active-tools">8</h3>
                                <p>运行中</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
                                <i class="fas fa-star" style="color: white;"></i>
                            </div>
                            <div class="stat-info">
                                <h3 id="favorite-tools">5</h3>
                                <p>收藏工具</p>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
                                <i class="fas fa-clock" style="color: white;"></i>
                            </div>
                            <div class="stat-info">
                                <h3 id="last-update">今日</h3>
                                <p>最近更新</p>
                            </div>
                        </div>
                    </div>
                    
                    <h3 style="margin-top: 30px;">快速开始</h3>
                    <div class="tools-grid" id="quick-tools">
                        <!-- 快速访问工具将通过JS动态加载 -->
                    </div>
                </div>
                
                <!-- 所有工具页面 -->
                <div id="tools" class="page">
                    <h2>所有工具</h2>
                    <p class="tool-desc">工具箱中的所有可用工具，支持搜索和分类筛选。</p>
                    
                    <div class="tools-grid" id="all-tools">
                        <!-- 所有工具将通过JS动态加载 -->
                    </div>
                </div>
                
                <!-- 系统工具页面 -->
                <div id="system" class="page">
                    <h2>系统工具</h2>
                    <p class="tool-desc">优化、管理和维护Windows系统的工具集合。</p>
                    
                    <div class="tools-grid" id="system-tools">
                        <!-- 系统工具将通过JS动态加载 -->
                    </div>
                </div>
                
                <!-- 关于页面 -->
                <div id="about" class="page">
                    <h2>关于 Windows R-tools Box</h2>
                    
                    <div class="tool-card" style="max-width: 800px; margin-top: 20px;">
                        <div class="tool-header">
                            <div class="tool-icon icon-system">
                                <i class="fas fa-toolbox"></i>
                            </div>
                            <div>
                                <div class="tool-title">开源工具箱</div>
                                <div class="tool-status">
                                    <i class="fas fa-circle status-on"></i>
                                    <span>版本 1.0.0</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="tool-desc">
                            <p><strong>Windows R-tools Box</strong> 是一个为Windows用户打造的高效、纯净、可扩展的开源工具箱。</p>
                            <p>旨在聚合实用的系统工具，让<strong>新手用户开箱即用，高级用户自由定制</strong>。</p>
                            
                            <h4 style="margin-top: 20px;">为什么选择我们？</h4>
                            <ul style="margin-left: 20px; margin-top: 10px;">
                                <li>🛡️ <strong>纯净透明</strong>：所有代码开源，无任何捆绑、后台或隐私收集。</li>
                                <li>🔧 <strong>即开即用</strong>：无需复杂配置，下载即可获得强大的工具集合。</li>
                                <li>🧩 <strong>模块化设计</strong>：每个工具独立，支持自由组合与扩展。</li>
                                <li>⚙️ <strong>尊重自由</strong>：不仅提供工具，更赋予您查看、修改和重新分发的权利。</li>
                            </ul>
                            
                            <h4 style="margin-top: 20px;">许可证</h4>
                            <p>本仓库内的所有原创工具、代码及修改，均采用 <strong>GNU Affero 通用公共许可证 v3.0</strong> 开源。</p>
                            <p>我们采用此许可证，是为了坚守一个简单的信念：<strong>开源的价值在于共享与回馈</strong>。</p>
                            
                            <h4 style="margin-top: 20px;">贡献</h4>
                            <p>我们热烈欢迎您的贡献！无论是添加新工具、修复BUG还是改进文档。</p>
                            <p>请参考项目仓库中的 <strong>CONTRIBUTING.md</strong> 文件了解如何参与贡献。</p>
                            
                            <p style="margin-top: 30px; text-align: center; font-style: italic;">
                                <strong>让开源的工具，赋予Windows更多可能。</strong> ✨
                            </p>
                        </div>
                        
                        <div class="tool-footer">
                            <div class="tool-status">
                                <i class="fas fa-code-branch"></i>
                                <span>GitHub: Regulus-forteen/Windows-R-tools-box</span>
                            </div>
                            <button class="btn btn-primary" onclick="openRepository()">
                                <i class="fab fa-github"></i>
                                访问仓库
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- 其他页面内容 -->
                <div id="security" class="page">
                    <h2>安全工具</h2>
                    <p class="tool-desc">保护系统安全和隐私的工具集合。</p>
                    <div class="tools-grid" id="security-tools"></div>
                </div>
                
                <div id="network" class="page">
                    <h2>网络工具</h2>
                    <p class="tool-desc">网络诊断、优化和监控工具。</p>
                    <div class="tools-grid" id="network-tools"></div>
                </div>
                
                <div id="utilities" class="page">
                    <h2>实用工具</h2>
                    <p class="tool-desc">日常使用的小工具和实用程序。</p>
                    <div class="tools-grid" id="utilities-tools"></div>
                </div>
                
                <div id="settings" class="page">
                    <h2>设置</h2>
                    <p class="tool-desc">自定义工具箱的行为和外观。</p>
                    
                    <div class="tool-card" style="max-width: 700px;">
                        <h3 style="margin-bottom: 15px;">常规设置</h3>
                        
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">启动时检查更新</label>
                            <label class="tool-status">
                                <input type="checkbox" id="check-updates" checked onchange="toggleSetting('check-updates')">
                                <span style="margin-left: 8px;">自动检查新版本</span>
                            </label>
                        </div>
                        
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">工具箱主题</label>
                            <select id="theme-select" style="padding: 8px; border-radius: 6px; border: 1px solid var(--border); width: 200px;" onchange="changeTheme()">
                                <option value="light">浅色主题</option>
                                <option value="dark">深色主题</option>
                                <option value="auto">跟随系统</option>
                            </select>
                        </div>
                        
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">工具默认行为</label>
                            <label class="tool-status">
                                <input type="checkbox" id="auto-start" onchange="toggleSetting('auto-start')">
                                <span style="margin-left: 8px;">启动时自动运行收藏的工具</span>
                            </label>
                        </div>
                        
                        <div style="margin-top: 30px;">
                            <button class="btn btn-primary" onclick="saveSettings()">
                                <i class="fas fa-save"></i>
                                保存设置
                            </button>
                            <button class="btn btn-secondary" style="margin-left: 10px;" onclick="resetSettings()">
                                <i class="fas fa-undo"></i>
                                恢复默认
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- 许可证页面 -->
                <div id="license" class="page">
                    <h2>AGPL v3 许可证</h2>
                    
                    <div class="tool-card" style="max-width: 900px;">
                        <h3>GNU Affero 通用公共许可证 v3.0</h3>
                        
                        <div class="tool-desc">
                            <p><strong>本仓库内的所有原创工具、代码及修改，均采用 GNU Affero 通用公共许可证 v3.0 开源。</strong></p>
                            
                            <h4 style="margin-top: 20px;">许可证对我们的意义</h4>
                            <p>我们采用此许可证，是为了坚守一个简单的信念：<strong>开源的价值在于共享与回馈</strong>。</p>
                            
                            <h4 style="margin-top: 20px;">对您意味着</h4>
                            <ul style="margin-left: 20px; margin-top: 10px;">
                                <li>✅ <strong>自由使用</strong>：个人、商业、教育用途均可。</li>
                                <li>✅ <strong>自由研究</strong>：可随意查看、学习所有实现。</li>
                                <li>✅ <strong>自由修改</strong>：可根据需求自行定制工具。</li>
                                <li>✅ <strong>自由分发</strong>：可以分享给任何人。</li>
                                <li>⚠️ <strong>唯一条件</strong>：若您<strong>修改</strong>了代码并<strong>通过网络提供服务</strong>，则<strong>必须</strong>将修改后的完整源代码向您的用户开放。</li>
                            </ul>
                            
                            <p style="margin-top: 20px; font-style: italic;">
                                <strong>简单来说</strong>：我们欢迎任何人（包括商业公司）使用本项目，但如果您用它构建了在线服务并进行了修改，那么您有义务将这些改进开源。<strong>这确保了开发者和社区的贡献不会被私有化垄断。</strong>
                            </p>
                            
                            <p style="margin-top: 30px;">
                                <strong>完整许可证文本请查看 LICENSE 文件。</strong> 使用本项目即表示您同意遵守此许可证的条款。
                            </p>
                        </div>
                        
                        <div class="tool-footer">
                            <button class="btn btn-secondary" onclick="switchPage('about')">
                                <i class="fas fa-arrow-left"></i>
                                返回关于
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 工具数据
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
                'dashboard': '仪表板',
                'tools': '所有工具',
                'system': '系统工具',
                'security': '安全工具',
                'network': '网络工具',
                'utilities': '实用工具',
                'settings': '设置',
                'about': '关于',
                'license': '许可证'
            };
            document.getElementById('page-title').textContent = pageTitles[pageId] || 'R-tools Box';
            
            // 切换页面内容
            document.querySelectorAll('.page').forEach(page => {
                page.classList.remove('active');
            });
            document.getElementById(pageId).classList.add('active');
            
            // 如果切换到工具页面，加载工具
            if (['tools', 'system', 'security', 'network', 'utilities', 'dashboard'].includes(pageId)) {
                loadToolsForPage(pageId);
            }
            
            return false;
        }
        
        // 加载工具到页面
        function loadToolsForPage(pageId) {
            let containerId, filteredTools;
            
            switch(pageId) {
                case 'tools':
                    containerId = 'all-tools';
                    filteredTools = toolsData;
                    break;
                case 'system':
                    containerId = 'system-tools';
                    filteredTools = toolsData.filter(tool => tool.category === 'system');
                    break;
                case 'security':
                    containerId = 'security-tools';
                    filteredTools = toolsData.filter(tool => tool.category === 'security');
                    break;
                case 'network':
                    containerId = 'network-tools';
                    filteredTools = toolsData.filter(tool => tool.category === 'network');
                    break;
                case 'utilities':
                    containerId = 'utilities-tools';
                    filteredTools = toolsData.filter(tool => tool.category === 'utilities');
                    break;
                case 'dashboard':
                    containerId = 'quick-tools';
                    filteredTools = toolsData.filter(tool => tool.favorite).slice(0, 4);
                    break;
            }
            
            const container = document.getElementById(containerId);
            if (!container) return;
            
            container.innerHTML = '';
            
            if (filteredTools.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #6b7280; padding: 40px;">暂无工具</p>';
                return;
            }
            
            filteredTools.forEach(tool => {
                const toolCard = document.createElement('div');
                toolCard.className = 'tool-card';
                toolCard.innerHTML = `
                    <div class="tool-header">
                        <div class="tool-icon icon-${tool.category}">
                            <i class="${tool.icon}"></i>
                        </div>
                        <div>
                            <div class="tool-title">${tool.name}</div>
                            <div class="tool-status">
                                <i class="fas fa-circle status-${tool.status}"></i>
                                <span>${tool.status === 'on' ? '可用' : '维护中'}</span>
                            </div>
                        </div>
                    </div>
                    <div class="tool-desc">${tool.desc}</div>
                    <div class="tool-footer">
                        <div class="tool-status">
                            <i class="fas fa-heart" style="color: ${tool.favorite ? '#ef4444' : '#9ca3af'}; cursor: pointer;" 
                               onclick="toggleFavorite(${tool.id})" title="${tool.favorite ? '取消收藏' : '收藏'}"></i>
                            <span style="margin-left: 5px;">${tool.category === 'system' ? '系统' : 
                                                           tool.category === 'security' ? '安全' : 
                                                           tool.category === 'network' ? '网络' : '实用'}</span>
                        </div>
                        <button class="btn ${tool.status === 'on' ? 'btn-primary' : 'btn-secondary'}" 
                                onclick="launchTool(${tool.id})" ${tool.status === 'off' ? 'disabled' : ''}>
                            <i class="fas fa-play"></i>
                            ${tool.status === 'on' ? '启动' : '暂不可用'}
                        </button>
                    </div>
                `;
                container.appendChild(toolCard);
            });
            
            // 更新统计信息
            if (pageId === 'dashboard') {
                updateStats();
            }
        }
        
        // 更新统计信息
        function updateStats() {
            document.getElementById('total-tools').textContent = toolsData.length;
            document.getElementById('active-tools').textContent = toolsData.filter(t => t.status === 'on').length;
            document.getElementById('favorite-tools').textContent = toolsData.filter(t => t.favorite).length;
            document.getElementById('tools-count').textContent = toolsData.length;
        }
        
        // 搜索工具
        function searchTools() {
            const searchTerm = document.getElementById('search-tools').value.toLowerCase();
            
            // 在活动页面中搜索
            const activePage = document.querySelector('.page.active').id;
            let containerId;
            
            switch(activePage) {
                case 'tools': containerId = 'all-tools'; break;
                case 'system': containerId = 'system-tools'; break;
                case 'security': containerId = 'security-tools'; break;
                case 'network': containerId = 'network-tools'; break;
                case 'utilities': containerId = 'utilities-tools'; break;
                default: return;
            }
            
            const container = document.getElementById(containerId);
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
        function launchTool(toolId) {
            window.pywebview.api.launch_tool(toolId).then(response => {
                if (response.success) {
                    showNotification(response.message || `工具启动成功`, 'success');
                } else {
                    showNotification(response.message || `启动失败`, 'error');
                }
            }).catch(error => {
                showNotification(`启动失败: ${error}`, 'error');
            });
        }
        
        // 切换收藏状态
        function toggleFavorite(toolId) {
            const tool = toolsData.find(t => t.id === toolId);
            if (tool) {
                const newFavorite = !tool.favorite;
                window.pywebview.api.toggle_favorite(toolId, newFavorite).then(response => {
                    if (response.success) {
                        tool.favorite = newFavorite;
                        
                        // 重新加载当前页面的工具
                        const activePage = document.querySelector('.page.active').id;
                        if (activePage && activePage !== 'settings' && activePage !== 'about' && activePage !== 'license') {
                            loadToolsForPage(activePage);
                        }
                        
                        updateStats();
                        showNotification(response.message || `已${newFavorite ? '收藏' : '取消收藏'}`, 'info');
                    }
                });
            }
        }
        
        // 刷新工具
        function refreshTools() {
            showNotification('正在刷新工具列表...', 'info');
            
            window.pywebview.api.get_tools().then(response => {
                if (response.success) {
                    toolsData = response.tools;
                    updateStats();
                    
                    const activePage = document.querySelector('.page.active').id;
                    if (activePage && activePage !== 'settings' && activePage !== 'about' && activePage !== 'license') {
                        loadToolsForPage(activePage);
                    }
                    
                    showNotification('工具列表已刷新', 'success');
                }
            }).catch(error => {
                showNotification('刷新失败', 'error');
            });
        }
        
        // 检查更新
        function checkForUpdates() {
            showNotification('正在检查更新...', 'info');
            
            window.pywebview.api.check_updates().then(response => {
                if (response.has_update) {
                    showNotification(`发现新版本: ${response.latest_version}`, 'info');
                    if (confirm(`发现新版本 ${response.latest_version}，是否前往下载？`)) {
                        window.pywebview.api.open_repository();
                    }
                } else {
                    showNotification(response.message || '当前已是最新版本', 'info');
                }
            }).catch(error => {
                showNotification('检查更新失败', 'error');
            });
        }
        
        // 打开仓库
        function openRepository() {
            window.pywebview.api.open_repository().then(response => {
                if (!response.success) {
                    showNotification(response.message || '无法打开仓库', 'error');
                }
            });
        }
        
        // 显示通知
        function showNotification(message, type = 'info') {
            // 移除现有的通知
            const existing = document.querySelector('.notification');
            if (existing) {
                existing.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => existing.remove(), 300);
            }
            
            // 创建通知元素
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            // 3秒后移除通知
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }
        
        // 设置相关函数
        function toggleSetting(settingId) {
            const value = document.getElementById(settingId).checked;
            window.pywebview.api.update_setting(settingId, value);
        }
        
        function changeTheme() {
            const theme = document.getElementById('theme-select').value;
            window.pywebview.api.update_setting('theme', theme);
        }
        
        function saveSettings() {
            window.pywebview.api.save_settings().then(response => {
                if (response.success) {
                    showNotification('设置已保存', 'success');
                }
            });
        }
        
        function resetSettings() {
            document.getElementById('check-updates').checked = true;
            document.getElementById('theme-select').value = 'light';
            document.getElementById('auto-start').checked = false;
            showNotification('设置已恢复为默认值', 'info');
        }
        
        // 初始化函数
        function initApp() {
            // 加载工具数据
            window.pywebview.api.get_tools().then(response => {
                if (response.success) {
                    toolsData = response.tools;
                    updateStats();
                    loadToolsForPage('dashboard');
                }
            }).catch(error => {
                console.error('加载工具失败:', error);
                // 使用默认数据
                toolsData = [
                    {"id": 1, "name": "系统优化器", "desc": "清理临时文件、优化启动项和系统设置", "category": "system", "icon": "fas fa-rocket", "status": "on", "favorite": true},
                    {"id": 2, "name": "隐私清理", "desc": "清除浏览器历史记录、Cookies和隐私数据", "category": "security", "icon": "fas fa-user-shield", "status": "on", "favorite": true},
                    {"id": 3, "name": "网络诊断", "desc": "检测网络连接问题，分析网络速度", "category": "network", "icon": "fas fa-wifi", "status": "on", "favorite": false},
                    {"id": 4, "name": "文件批量重命名", "desc": "批量重命名文件，支持多种规则", "category": "utilities", "icon": "fas fa-file-signature", "status": "on", "favorite": true}
                ];
                updateStats();
                loadToolsForPage('dashboard');
            });
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            // 等待pywebview API加载完成
            const checkApi = setInterval(() => {
                if (window.pywebview && window.pywebview.api) {
                    clearInterval(checkApi);
                    initApp();
                }
            }, 100);
        });
    </script>
</body>
</html>'''

def main():
    # 初始化API
    api = Api()
    
    # 打印启动信息
    print("=" * 60)
    print("正在启动 Windows R-tools Box...")
    print("版本 1.0.0 | © 2024 Regulus-forteen & 贡献者")
    print("许可证: AGPL v3")
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
    
    # 创建窗口
    window = webview.create_window(
        'Windows R-tools Box 🧰',
        html=get_html_content(),
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        text_select=True,
        easy_drag=True,
        js_api=api  # 将API实例传递给窗口
    )
    
    # 启动应用
    try:
        webview.start(debug=False)
        print("👋 程序已退出")
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请确保已正确安装依赖:")
        print("   pip install pywebview")

if __name__ == '__main__':
    # 检查依赖
    try:
        import webview
    except ImportError:
        print("❌ 未找到 pywebview 库")
        print("💡 请安装依赖: pip install pywebview")
        sys.exit(1)
    
    # 运行主函数
    main()
