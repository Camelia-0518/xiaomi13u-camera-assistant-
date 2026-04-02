# 小米13 Ultra 摄影助手 - 打包成软件

三种方式把你的摄影助手变成真正的App：

---

## 方案1: WebView打包（最简单，推荐）

用 **Cordova** 把网页打包成APK，5分钟搞定。

### 步骤

```bash
cd mobile-app-cordova

# 安装依赖
npm install

# 全局安装Cordova
npm install -g cordova

# 添加Android平台
cordova platform add android

# 构建APK
cordova build android

# APK位置
# platforms/android/app/build/outputs/apk/debug/app-debug.apk
```

### 安装到手机

```bash
adb install platforms/android/app/build/outputs/apk/debug/app-debug.apk
# 或复制到手机文件管理器安装
```

**特点：**
- ✅ 超简单，网页直接变App
- ✅ 跨平台（Android/iOS）
- ✅ 可以添加原生功能（后续可扩展）
- ⚠️ 需要Android SDK环境

---

## 方案2: Android原生App（功能最强）

用 **Android Studio** 编译之前创建的完整Android项目。

### 步骤

```bash
cd android-auto-camera

# 方式A: 命令行编译（需Android SDK）
./gradlew assembleDebug

# APK输出位置
# app/build/outputs/apk/debug/app-debug.apk

# 方式B: Android Studio打开
# 1. 打开Android Studio
# 2. File → Open → 选择android-auto-camera文件夹
# 3. Build → Build APK
```

### 安装到手机

```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

**特点：**
- ✅ 全自动检测相机启动（无障碍服务）
- ✅ 悬浮窗覆盖相机界面
- ✅ 原生性能，流畅体验
- ⚠️ 需要Android开发环境
- ⚠️ 需要用户开启无障碍权限

---

## 方案3: Python Kivy打包（跨平台）

用 **Buildozer** 把Python脚本打包成APK。

### 步骤

```bash
# 安装buildozer
pip install buildozer

# 初始化
cd ~/.openclaw/workspace/xiaomi13u-camera-assistant
buildozer init

# 编辑buildozer.spec（已提供）
# 确保 source.include_exts = py,png,jpg,kv,atlas,json,txt

# 构建（第一次很慢，需下载NDK/SDK）
buildozer android debug

# APK位置
# bin/xiaomi13u-camera-assistant-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

**特点：**
- ✅ 用Python写，打包成App
- ✅ 跨平台（Android/iOS/Desktop）
- ⚠️ 第一次构建很慢（1-2小时）
- ⚠️ APK体积较大（包含Python运行时）

---

## 快速推荐

| 你的情况 | 推荐方案 | 时间 |
|---------|---------|------|
| 最快搞定 | 方案1 (Cordova) | 5分钟 |
| 功能最强 | 方案2 (Android原生) | 30分钟 |
| 会Python | 方案3 (Kivy) | 1-2小时 |

---

## 免编译方案：直接下载APK

如果不想自己编译，可以使用**在线打包服务**：

### 方法A: PhoneGap Build (Adobe)
1. 访问 https://build.phonegap.com
2. 上传 `mobile-app-cordova/` 文件夹压缩包
3. 自动编译成APK下载

### 方法B: Appilix
1. 访问 https://appilix.com
2. 输入网页URL或上传HTML
3. 在线生成APK

### 方法C: WebIntoApp
1. 访问 https://webintoapp.com
2. 输入网址: `http://你的IP:8080` 或上传HTML
3. 免费生成APK

---

## 安装后的效果

打包成App后：
1. 📱 桌面出现图标「小米13U摄影助手」
2. 🔘 点击打开，显示8大场景
3. 👆 点击场景，展开参数卡片
4. 💾 可离线使用，无需网络
5. 🔄 随时卸载，零残留

---

## 下一步

你想用哪种方式？我可以帮你：
1. 运行Cordova打包脚本
2. 配置Android Studio项目
3. 使用在线打包服务

选一种，我直接给你执行。
