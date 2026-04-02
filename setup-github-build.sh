#!/bin/bash
# 一键部署脚本 - 用GitHub Actions自动编译APK

echo "📦 小米13U摄影助手 - GitHub自动编译方案"
echo "══════════════════════════════════════════════════"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 创建GitHub Actions工作流
mkdir -p .github/workflows

cat > .github/workflows/build-apk.yml <> 'EOF'
name: Build APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Java
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Setup Android SDK
      uses: android-actions/setup-android@v2
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y python3-pip
        pip3 install buildozer cython
    
    - name: Build APK with Buildozer
      run: |
        cd kivy_app
        buildozer android debug
      env:
        ANDROID_HOME: ${{ env.ANDROID_HOME }}
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: xiaomi13u-camera-assistant-apk
        path: kivy_app/bin/*.apk
EOF

echo "✅ GitHub Actions配置已创建"
echo ""
echo "📋 使用步骤："
echo ""
echo "1. 创建GitHub仓库"
echo "   访问: https://github.com/new"
echo "   仓库名: xiaomi13u-camera-assistant"
echo ""
echo "2. 上传代码到GitHub:"
echo "   cd $PROJECT_DIR"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/你的用户名/xiaomi13u-camera-assistant.git"
echo "   git push -u origin main"
echo ""
echo "3. GitHub自动编译:"
echo "   上传后访问: https://github.com/你的用户名/xiaomi13u-camera-assistant/actions"
echo "   等待2-3分钟，下载编译好的APK"
echo ""
echo "4. 手机安装:"
echo "   下载APK → 允许未知来源 → 安装"
echo ""
echo "══════════════════════════════════════════════════"
