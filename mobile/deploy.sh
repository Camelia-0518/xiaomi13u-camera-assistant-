#!/bin/bash
# 一键部署脚本 - 手机扫码或下载使用

echo "📷 小米13 Ultra 摄影助手 - 手机部署"
echo "══════════════════════════════════════════════════"
echo ""

# 获取IP
IP=$(hostname -I | awk '{print $1}')
URL="http://${IP}:8080"

echo "✅ 本地服务器已启动: $URL"
echo ""

echo "📱 获取方式（任选一种）："
echo ""
echo "方式1: 手机浏览器直接访问"
echo "   $URL"
echo ""

echo "方式2: 文件路径（复制到手机）"
echo "   ~/.openclaw/workspace/xiaomi13u-camera-assistant/mobile/index.html"
echo ""

echo "方式3: ADB推送（手机连接电脑时）"
echo "   adb push mobile/index.html /sdcard/Download/"
echo "   然后在手机文件管理器打开"
echo ""

echo "📋 添加到主屏幕方法："
echo "   1. 手机浏览器打开 $URL"
echo "   2. 点击菜单 → 添加到主屏幕"
echo "   3. 以后像App一样使用"
echo ""

echo "💡 提示：此HTML文件可离线使用，保存到手机后无需网络"
echo ""
