# 🎯 小米13 Ultra AI摄影助手 - 完整方案

## 你已获得的全部内容

### 📁 项目结构

```
xiaomi13u-camera-assistant/
│
├── 📱 Android无障碍App（全自动）
│   └── android-auto-camera/          ← 原生Android项目
│       ├── app/src/main/java/...     ← Java源码
│       ├── app/src/main/res/...      ← 界面布局
│       ├── build.gradle              ← 构建配置
│       └── README.md                 ← Android版说明
│
├── 💻 Python工具包（多平台）
│   ├── xiaomi13u_assistant.py        ← 核心库（8大场景）
│   ├── auto_detector.py              ← 自动检测器
│   ├── web_app.py                    ← Web界面(Streamlit)
│   ├── mobile_app.py                 ← Kivy移动端
│   └── setup_auto_detect.sh          ← 自动配置脚本
│
├── 📖 文档
│   ├── README.md                     ← 主文档（你在这里）
│   ├── QUICK_REFERENCE.md            ← 快速参考卡
│   ├── VERSION.md                    ← 版本/回退指南
│   └── requirements.txt              ← 依赖列表
│
└── 🔧 配置文件
    ├── start.sh                      ← 一键启动脚本
    ├── buildozer.spec                ← APK构建配置
    └── tasker_integration.sh         ← Tasker集成脚本
```

---

## 🎬 三种使用方式

### 方式1: Android App（全自动）⭐⭐⭐

**效果**：打开相机 → 悬浮窗自动弹出 → 点击场景查看参数

```bash
# 编译安装
cd android-auto-camera
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

**使用**：
1. 打开「小米13U摄影助手」APP
2. 开启无障碍服务 + 悬浮窗权限
3. 打开相机
4. 点击场景按钮（人像/夜景/街拍等）
5. 按提示设置相机参数

**回退**：设置 → 应用 → 卸载（零残留）

---

### 方式2: Termux+Python（半自动）⭐⭐

**效果**：Tasker检测相机 → 调用Termux脚本 → 显示参数

```bash
# 在Termux中运行
./setup_auto_detect.sh
# 选择 Tasker方案 或 Termux方案
```

**使用**：
- Tasker方案：打开相机自动触发
- Termux方案：手动运行或后台监控

---

### 方式3: CLI/Web（手动）⭐

**效果**：手动打开工具 → 选择场景 → 查看参数

```bash
# CLI交互
python3 xiaomi13u_assistant.py

# Web界面
streamlit run web_app.py
```

---

## ⚡ 5分钟快速上手

### 步骤1: 选择适合你的方案

| 你的情况 | 推荐方案 | 命令 |
|---------|---------|------|
| 会装APK，要全自动 | Android App | 见方式1 |
| 有Tasker，要简单 | Tasker集成 | `./setup_auto_detect.sh` |
| 只用Termux，要免费 | Termux监控 | `./setup_auto_detect.sh` |
| 临时用一下 | CLI/Web | `python3 xiaomi13u_assistant.py` |

### 步骤2: 查看快速参考

```bash
cat QUICK_REFERENCE.md
```

重点记忆：
- **街拍快捷键**：锁屏双击音量下键
- **可变光圈**：f/1.9虚化，f/4.0画质
- **万能夜景**：ISO100 + 2-30秒 + 三脚架
- **人像虚化**：75mm + f/1.9 + 1.5米

### 步骤3: 拍摄！

打开相机，根据提示设置参数，享受专业摄影体验。

---

## 📱 各方案详细对比

| 特性 | Android App | Tasker+Termux | CLI/Web |
|------|------------|---------------|---------|
| **自动化程度** | ⭐⭐⭐ 全自动 | ⭐⭐☆ 半自动 | ⭐☆☆ 手动 |
| **安装难度** | 中（需装APK） | 低（配置Tasker） | 低（Python即可） |
| **系统要求** | Android 8+ | Tasker App | Python 3.8+ |
| **悬浮窗** | ✅ 原生支持 | ⚠️ 需额外配置 | ❌ 不支持 |
| **离线运行** | ✅ 完全离线 | ✅ 离线 | ✅ 离线 |
| **回退难度** | 极易（卸载） | 易（禁用Tasker） | 极易（关闭终端） |
| **最佳场景** | 日常使用 | 已有Tasker用户 | 临时/电脑使用 |

---

## 🔄 版本回退（你的核心要求）

### Android App 回退
```
设置 → 应用管理 → 小米13U摄影助手 → 卸载
```
无任何残留，相机恢复原状。

### Termux/Python 回退
```bash
# 停止监控
pkill -f auto_detector.py

# 完全删除
rm -rf ~/xiaomi13u-camera-assistant

# Tasker用户：删除Tasker中的配置
```

---

## 🎁 额外福利

### 快速参考卡

保存 `QUICK_REFERENCE.md` 到手机相册，随时查阅：

```bash
# 在手机上显示快速提示
python3 auto_detector.py --quick-tip
```

### 导出预设

```bash
# 导出夜景参数
python3 -c "
from xiaomi13u_assistant import PhotographyAssistant
a = PhotographyAssistant()
a.export_preset('夜景', 'my_night_preset.json')
print('预设已导出')
"
```

### 参数卡片

```bash
# 生成人像参数卡片
python3 -c "
from xiaomi13u_assistant import PhotographyAssistant
a = PhotographyAssistant()
print(a.generate_setting_card('人像'))
"
```

---

## 🐛 常见问题

### Q: Android App 安装不了？
A: 检查「允许未知来源应用」，或尝试关闭MIUI优化。

### Q: 无障碍服务开启后不工作？
A: 
1. 检查悬浮窗权限是否开启
2. 在电池优化中设为「不限制」
3. 重启APP

### Q: Termux方案太复杂？
A: 直接用方案1（Android App），最简单。

### Q: 能直接控制相机参数吗？
A: 不能，小米相机API不开放。本方案是「指导」而非「控制」。

### Q: 支持其他手机吗？
A: 支持，但参数针对小米13 Ultra优化。其他手机可能需要调整。

---

## 🗺️ 未来计划

### v1.1.0
- [ ] 更多场景（宠物、运动、文档）
- [ ] AI识别当前场景
- [ ] 语音播报参数

### v2.0.0
- [ ] 拍照后AI分析
- [ ] 与Google相册集成
- [ ] iOS版本（如有需求）

---

## 📞 需要帮助？

1. 查看 `README.md` 详细文档
2. 查看 `QUICK_REFERENCE.md` 快速参考
3. 运行 `./setup_auto_detect.sh` 交互式配置

---

**记住：最好的相机是你手中的那台。**

现在开始拍摄吧！📷
