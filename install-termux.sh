#!/bin/bash
# 小米13U摄影助手 - Termux全自动安装脚本
# 在手机上运行：curl -fsSL [URL] | bash

echo "📷 小米13 Ultra 摄影助手 - 自动安装"
echo "══════════════════════════════════════════════════"
echo ""

# 检查Termux环境
if [ -z "$TERMUX_VERSION" ]; then
    echo "⚠️  请在Termux中运行此脚本"
    echo "   下载Termux: https://f-droid.org/packages/com.termux/"
    exit 1
fi

echo "✅ Termux环境检测通过"
echo ""

# 更新软件源
echo "📥 更新软件源..."
pkg update -y

# 安装必要软件
echo "📥 安装Python和依赖..."
pkg install -y python termux-api

pip install --upgrade pip
pip install flask

# 创建工作目录
WORK_DIR="$HOME/xiaomi13u-camera-assistant"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "✅ 工作目录创建: $WORK_DIR"
echo ""

# 下载核心脚本
echo "📥 下载检测脚本..."

cat > camera_detector.py << 'PYTHON_EOF'
#!/usr/bin/env python3
import subprocess
import time
import json
import os
import sys

# 小米相机包名列表
CAMERA_PACKAGES = [
    "com.android.camera",
    "com.miui.camera",
    "com.android.camera2",
    "com.xiaomi.camera",
    "com.google.android.GoogleCamera"
]

# 场景数据
SCENES = {
    "portrait": {
        "name": "人像",
        "icon": "👤",
        "params": "75mm长焦 + f/1.9 + 眼睛对焦",
        "tips": "1.5米距离最佳，人物占画面1/3"
    },
    "night": {
        "name": "夜景",
        "icon": "🌃",
        "params": "23mm主摄 + ISO100 + 2-30秒",
        "tips": "必须上三脚架，找水面倒影"
    },
    "street": {
        "name": "街拍",
        "icon": "📸",
        "params": "双击音量下键快速启动",
        "tips": "0.8秒抓拍，f/4.0增加景深"
    },
    "landscape": {
        "name": "风景",
        "icon": "🏔️",
        "params": "12mm超广 + f/4.0",
        "tips": "黄金时段拍摄，前景+中景+远景"
    },
    "food": {
        "name": "美食",
        "icon": "🍜",
        "params": "75mm长焦 + 45度俯拍",
        "tips": "30-80cm距离，找纹理对比"
    },
    "star": {
        "name": "星空",
        "icon": "⭐",
        "params": "ISO1600 + 15-25秒",
        "tips": "需三脚架，快门>25秒星星拖线"
    }
}

def get_current_app():
    """获取当前前台应用"""
    try:
        result = subprocess.run(
            ["dumpsys", "window", "windows"],
            capture_output=True,
            text=True,
            timeout=2
        )
        output = result.stdout
        
        for line in output.split('\n'):
            if 'mCurrentFocus' in line or 'mFocusedApp' in line:
                for pkg in CAMERA_PACKAGES:
                    if pkg in line:
                        return pkg
        return None
    except Exception as e:
        print(f"检测错误: {e}")
        return None

def show_notification(scene_key=None):
    """显示参数通知"""
    if scene_key and scene_key in SCENES:
        scene = SCENES[scene_key]
        title = f"{scene['icon']} {scene['name']}模式"
        content = f"{scene['params']}\n💡 {scene['tips']}"
    else:
        title = "📷 小米13U摄影助手"
        content = "检测到相机启动\n点击选择拍摄场景"
    
    # 使用termux-notification
    try:
        subprocess.run([
            "termux-notification",
            "--title", title,
            "--content", content,
            "--priority", "high",
            "--vibrate", "100"
        ], check=False, timeout=5)
    except:
        # 备用：toast提示
        subprocess.run([
            "termux-toast",
            content
        ], check=False)

def show_scene_selector():
    """显示场景选择对话框"""
    items = []
    for key, scene in SCENES.items():
        items.append(f"{scene['icon']} {scene['name']}")
    
    try:
        # 使用termux-dialog创建选择列表
        result = subprocess.run(
            ["termux-dialog", "sheet", "-v", ",".join(items)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # 解析选择结果
            selected = result.stdout.strip()
            for key, scene in SCENES.items():
                if scene['name'] in selected:
                    show_notification(key)
                    return
    except:
        pass
    
    # 备用：显示所有场景
    show_notification()

def main():
    print("📷 小米13U摄影助手 - 相机检测启动")
    print("═══════════════════════════════════")
    print("功能：打开相机自动显示拍摄指导")
    print("退出：Ctrl+C")
    print("")
    
    camera_active = False
    check_interval = 2  # 检测间隔(秒)
    
    try:
        while True:
            current_app = get_current_app()
            
            if current_app and not camera_active:
                # 相机刚打开
                print(f"📸 检测到相机启动: {current_app}")
                show_scene_selector()
                camera_active = True
                
            elif not current_app and camera_active:
                # 相机关闭
                print("📴 相机已关闭")
                camera_active = False
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 已退出")
        sys.exit(0)

if __name__ == "__main__":
    main()
PYTHON_EOF

chmod +x camera_detector.py

echo "✅ 脚本下载完成"
echo ""

# 创建启动脚本
cat > start.sh << 'EOF'
#!/bin/bash
cd ~/xiaomi13u-camera-assistant
python3 camera_detector.py
EOF

chmod +x start.sh

# 创建快捷方式
echo "📱 创建快捷启动方式..."

mkdir -p $HOME/.shortcuts
cat > $HOME/.shortcuts/摄影助手 << 'EOF'
#!/bin/bash
cd ~/xiaomi13u-camera-assistant
python3 camera_detector.py
EOF

chmod +x $HOME/.shortcuts/摄影助手

# 配置自启动
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-camera-assistant << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/xiaomi13u-camera-assistant
nohup python3 camera_detector.py > detector.log 2>&1 &
EOF

chmod +x ~/.termux/boot/start-camera-assistant

echo ""
echo "══════════════════════════════════════════════════"
echo "✅ 安装完成！"
echo ""
echo "🚀 使用方法："
echo ""
echo "方式1: 立即启动"
echo "   cd ~/xiaomi13u-camera-assistant"
echo "   python3 camera_detector.py"
echo ""
echo "方式2: 下拉通知栏快捷方式"
echo "   长按Termux通知栏快捷方式"
echo "   选择「摄影助手」"
echo ""
echo "方式3: 开机自启动（已配置）"
echo "   重启手机后自动运行"
echo ""
echo "📱 效果："
echo "   打开小米相机 → 自动弹出参数提示"
echo ""
echo "⚙️ 如需停止："
echo "   Ctrl+C 或杀掉Termux进程"
echo ""
echo "══════════════════════════════════════════════════"
