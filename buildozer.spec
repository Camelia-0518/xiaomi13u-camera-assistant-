# Buildozer 配置文件
# 用于构建小米13 Ultra摄影助手Android APK

[app]
# 应用标题
title = 小米13U摄影助手

# 包名
package.name = xiaomi13ucamera
package.domain = org.kimiclaw

# 源文件
source.dir = .

# 包含的文件
source.include_exts = py,png,jpg,kv,atlas,json,md
source.include_patterns = assets/*

# 版本
version = 1.0.0

# 依赖项
requirements = python3,kivy==2.2.1,pygments

# 图标
# icon.filename = assets/icon.png

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# API级别
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# 架构
android.archs = arm64-v8a, armeabi-v7a

# 应用类型
orientation = portrait
fullscreen = 0

# 日志
android.logcat_filters = *:S python:D

[buildozer]
# 构建目录
build_dir = ./.buildozer

# 日志级别
log_level = 2

# 警告模式
warn_on_root = 1
