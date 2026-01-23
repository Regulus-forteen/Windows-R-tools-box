# create_structure.py - 创建项目结构
import json
from pathlib import Path

def create_basic_structure():
    """创建最基本的项目结构"""
    base_dir = Path(__file__).parent
    
    print("=" * 60)
    print("正在创建 Windows R-tools Box 基本结构...")
    print("=" * 60)
    
    # 创建必要目录
    directories = [
        "tools/system",
        "tools/security", 
        "tools/network",
        "tools/utilities",
        "icons"
    ]
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {dir_path}")
    
    # 创建示例工具
    example_tools = [
        {
            "id": "system_cleaner",
            "name": "系统清理大师",
            "description": "清理系统垃圾文件和注册表，优化系统性能",
            "executable": "cleaner.exe",
            "version": "1.0.0",
            "author": "R-tools Team",
            "icon": "fas fa-broom",
            "status": "on",
            "favorite": True,
            "category": "system",
            "requires_admin": True
        }
    ]
    
    for tool in example_tools:
        category = tool['category']
        tool_file = base_dir / f"tools/{category}/{tool['id']}.json"
        with open(tool_file, 'w', encoding='utf-8') as f:
            json.dump(tool, f, ensure_ascii=False, indent=2)
        print(f"✓ 创建示例工具: tools/{category}/{tool['id']}.json")
    
    # 创建默认配置文件
    config_file = base_dir / "config.json"
    if not config_file.exists():
        default_config = {
            "theme": "light",
            "default_search": "百度",
            "show_favorites": True,
            "show_tools": True,
            "check_updates": True,
            "window_size": [1200, 800]
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print("✓ 创建配置文件: config.json")
    
    print("\n" + "=" * 60)
    print("✅ 项目结构创建完成！")
    print("\n🎯 运行程序:")
    print("1. 安装依赖: pip install pywebview psutil")
    print("2. 运行程序: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    create_basic_structure()
