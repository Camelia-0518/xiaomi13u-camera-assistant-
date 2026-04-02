#!/bin/bash
# 快速打包成Android APK脚本

echo "📦 小米13U摄影助手 - APK打包脚本"
echo "══════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 需要Node.js，正在安装..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

# 检查Cordova
if ! command -v cordova &> /dev/null; then
    echo "📥 安装Cordova..."
    npm install -g cordova
fi

# 安装依赖
echo "📥 安装项目依赖..."
npm install

# 添加Android平台
echo "📱 添加Android平台..."
cordova platform add android

# 构建APK
echo "🔨 构建APK..."
cordova build android --release

# 签名（可选，需要keystore）
APK_PATH="platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk"
SIGNED_APK="xiaomi13u-camera-assistant.apk"

if [ -f "$APK_PATH" ]; then
    echo ""
    echo "✅ 构建成功！"
    echo "📱 APK位置: $APK_PATH"
    echo ""
    
    # 如果没有签名，复制一份未签名的
    cp "$APK_PATH" "$SIGNED_APK"
    echo "💡 未签名APK已复制到: $SIGNED_APK"
    echo ""
    echo "⚠️ 注意: 未签名APK安装时需要允许'未知来源'"
    echo ""
    echo "📥 发送到手机:"
    echo "   adb install $SIGNED_APK"
    echo "   或"
    echo "   用微信/QQ发送到手机安装"
fi
