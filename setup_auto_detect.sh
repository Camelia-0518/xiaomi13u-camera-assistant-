#!/bin/bash
# 自动设置脚本 - 一键配置相机自动检测
# 适用于 Termux 环境

echo "📷 小米13 Ultra 相机自动检测设置"
echo "═══════════════════════════════════════"

# 检测环境
if [ -n "$TERMUX_VERSION" ]; then
    echo "✅ 检测到 Termux 环境"
    INSTALL_DIR="$HOME/xiaomi13u-camera-assistant"
else
    echo "✅ 检测到标准 Linux 环境"
    INSTALL_DIR="$HOME/.openclaw/workspace/xiaomi13u-camera-assistant"
fi

# 创建目录
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 复制核心文件
echo "📦 安装核心组件..."

# 检查文件是否存在
if [ ! -f "$INSTALL_DIR/xiaomi13u_assistant.py" ]; then
    echo "⚠️ 核心文件缺失，请确保在正确目录运行"
    exit 1
fi

chmod +x auto_detector.py

echo ""
echo "✅ 基础安装完成！"
echo ""

# 选择设置方式
echo "请选择自动检测方式："
echo ""
echo "1️⃣  Tasker方案（推荐）"
echo "     优点：简单可靠，无需root"
echo "     缺点：需要安装Tasker（付费App）"
echo ""
echo "2️⃣  Termux自启动方案"
echo "     优点：完全免费"
echo "     缺点：需要保持Termux后台运行"
echo ""
echo "3️⃣  ADB方案（电脑辅助）"
echo "     优点：最可靠"
echo "     缺点：需要电脑连接"
echo ""
echo "4️⃣  手动触发（快捷方式）"
echo "     优点：最简单"
echo "     缺点：非自动，需手动打开"
echo ""

read -p "选择方案 [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "📱 Tasker 设置指南"
        echo "────────────────────────────────────────"
        python3 auto_detector.py --install-tasker
        echo ""
        echo "下一步操作："
        echo "1. 安装 Tasker App (Google Play / 酷安)"
        echo "2. 打开 Tasker → 任务 → + → 命名「拍摄提示」"
        echo "3. 添加操作 → 插件 → Termux → Termux:Task"
        echo "4. 配置："
        echo "   - 可执行文件: $INSTALL_DIR/tasker_integration.sh"
        echo "5. 返回 → 配置文件 → + → 应用 → 相机"
        echo "6. 选择刚创建的任务"
        echo "7. ✅ 完成！打开相机测试"
        ;;
    
    2)
        echo ""
        echo "🤖 Termux 自启动方案"
        echo "────────────────────────────────────────"
        
        # 创建自启动脚本
        cat > "$HOME/.termux/boot/start-camera-monitor" << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
# Termux自启动 - 相机监控
termux-wake-lock
cd ~/xiaomi13u-camera-assistant
python3 auto_detector.py --monitor > camera_monitor.log 2>&1 &
EOF
        chmod +x "$HOME/.termux/boot/start-camera-monitor"
        
        echo "✅ 已创建自启动脚本"
        echo ""
        echo "设置步骤："
        echo "1. 安装 Termux:Boot App"
        echo "2. 重启手机或运行: termux-boot"
        echo "3. 监控将自动在后台运行"
        echo ""
        echo "查看日志: tail -f $INSTALL_DIR/camera_monitor.log"
        ;;
    
    3)
        echo ""
        echo "🔌 ADB 方案"
        echo "────────────────────────────────────────"
        cat > "$INSTALL_DIR/adb_monitor.sh" << EOF
#!/bin/bash
# ADB监控脚本 - 需要在电脑上运行

PHONE_IP=\${1:-192.168.1.100}
echo "连接手机: \$PHONE_IP"
adb connect \$PHONE_IP:5555

echo "开始监控相机启动..."
adb shell "while true; do 
    if dumpsys activity activities | grep -q 'com.android.camera'; then
        if [ ! -f /tmp/camera_active ]; then
            touch /tmp/camera_active
            echo '相机启动 detected'
            # 这里可以触发通知或执行脚本
        fi
    else
        rm -f /tmp/camera_active 2>/dev/null
    fi
    sleep 2
done"
EOF
        chmod +x "$INSTALL_DIR/adb_monitor.sh"
        
        echo "✅ ADB监控脚本已创建"
        echo ""
        echo "使用方式："
        echo "1. 手机开启USB调试 + ADB网络调试"
        echo "2. 电脑运行: ./adb_monitor.sh [手机IP]"
        echo "3. 打开相机时会在电脑显示提示"
        ;;
    
    4)
        echo ""
        echo "📲 手动触发方案"
        echo "────────────────────────────────────────"
        
        # 创建快捷方式脚本
        cat > "$INSTALL_DIR/quick_launch.sh" << 'EOF'
#!/bin/bash
# 快速启动 - 添加到桌面快捷方式
cd ~/xiaomi13u-camera-assistant
python3 auto_detector.py --quick-tip
EOF
        chmod +x "$INSTALL_DIR/quick_launch.sh"
        
        echo "✅ 快速启动脚本已创建"
        echo ""
        echo "设置步骤："
        echo "1. 安装 Termux:Widget"
        echo "2. 创建快捷方式到桌面"
        echo "3. 点击快捷方式显示拍摄提示"
        echo ""
        echo "或者最简单的方式："
        echo "- 打开 Termux → 输入: cd xiaomi13u-camera-assistant && ./start.sh"
        ;;
    
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════"
echo "📖 其他有用命令："
echo ""
echo "显示完整指导:"
echo "  python3 xiaomi13u_assistant.py"
echo ""
echo "生成参数卡片:"
echo "  python3 -c \"from xiaomi13u_assistant import PhotographyAssistant;"
echo "  a=PhotographyAssistant();"
echo "  print(a.generate_setting_card('人像'))\""
echo ""
echo "查看快速参考:"
echo "  cat QUICK_REFERENCE.md"
echo ""
