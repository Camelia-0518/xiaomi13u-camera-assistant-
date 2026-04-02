[app]
# 应用标题
title = 小米13U摄影助手

# 包名
package.name = cameraassistant
package.domain = com.kimiclaw

# 源文件
source.dir = .

# 包含的文件扩展名
source.include_exts = py,png,jpg,kv,atlas,ttf,txt

# 版本
version = 1.0.0

# 依赖
requirements = python3,kivy,android

# Android API版本
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 权限
android.permissions = INTERNET

# 架构
android.archs = arm64-v8a, armeabi-v7a

# 图标（可选）
# icon.filename = %(source.dir)s/data/icon.png

# 启动方向
orientation = portrait

# 全屏
fullscreen = 0

# Android特定选项
android.enable_androidx = True

[buildozer]
# Buildozer日志级别
log_level = 2

# 警告级别
warn_on_root = 1
