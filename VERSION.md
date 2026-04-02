# 版本历史与回退指南

## 版本记录

### v1.0.0 (2026-04-02)
**代号**: Genesis
**状态**: ✅ 当前稳定版

**功能清单**:
- [x] 8大摄影场景参数指导
- [x] CLI交互式界面
- [x] Web界面 (Streamlit)
- [x] Kivy移动端框架
- [x] 参数导出功能
- [x] 场景分析AI

**包含场景**:
1. 👤 人像
2. 🌃 夜景
3. ⭐ 星空
4. 📸 街拍/人文
5. 🍜 美食
6. 🏔️ 风景
7. 🌸 微距
8. 🏢 建筑

**文件清单**:
```
xiaomi13u-camera-assistant/
├── xiaomi13u_assistant.py    # 核心库
├── web_app.py                 # Web界面
├── mobile_app.py              # Kivy移动端
├── start.sh                   # 启动脚本
├── buildozer.spec             # APK构建配置
├── README.md                  # 使用文档
├── VERSION.md                 # 本文件
└── requirements.txt           # 依赖列表
```

---

## 回退方法

### 方法1: Git版本回退（推荐）

```bash
cd ~/.openclaw/workspace/xiaomi13u-camera-assistant

# 查看所有版本
git log --oneline

# 回退到指定版本
git checkout v1.0.0

# 如果需要保存当前修改
git stash
git checkout v1.0.0

# 恢复修改
git checkout main
git stash pop
```

### 方法2: 完全重新安装

```bash
# 删除当前版本
rm -rf ~/.openclaw/workspace/xiaomi13u-camera-assistant

# 重新克隆稳定版
cd ~/.openclaw/workspace
git clone --branch v1.0.0 https://github.com/yourname/xiaomi13u-camera-assistant.git
```

### 方法3: 备份恢复

如果你创建了备份:
```bash
# 恢复备份
cp -r ~/backups/xiaomi13u-assistant-v1.0.0 \
      ~/.openclaw/workspace/xiaomi13u-camera-assistant
```

---

## 版本升级

### 升级到最新开发版

```bash
cd ~/.openclaw/workspace/xiaomi13u-camera-assistant
git pull origin main
```

### 安全升级（保留旧版）

```bash
# 备份当前版本
cp -r xiaomi13u-camera-assistant xiaomi13u-camera-assistant-backup

# 升级
cd xiaomi13u-camera-assistant
git pull origin main

# 如果出问题，恢复备份
rm -rf xiaomi13u-camera-assistant
mv xiaomi13u-camera-assistant-backup xiaomi13u-camera-assistant
```

---

## 版本兼容性

| 版本 | Python | Kivy | Streamlit | Android API |
|------|--------|------|-----------|-------------|
| v1.0.0 | 3.8+ | 2.2.1 | 1.28+ | 21-33 |

---

## 已知问题

### v1.0.0
- [ ] Kivy移动端界面需要进一步优化
- [ ] 缺少拍照后的AI分析功能
- [ ] 不支持直接控制相机（系统限制）

---

## 路线图

### v1.1.0 (计划中)
- [ ] 添加更多场景（宠物、运动、文档等）
- [ ] 拍照后AI分析（调用OpenAI Vision）
- [ ] 优化的移动端界面
- [ ] 参数收藏夹功能

### v2.0.0 (远期)
- [ ] 完整的Android App
- [ ] 相机参数实时显示（需ADB权限）
- [ ] 与小米相机快捷方式集成

---

## 创建版本标签

作为开发者，创建新版本：

```bash
# 提交所有更改
git add .
git commit -m "v1.0.0: Initial release"

# 打标签
git tag -a v1.0.0 -m "First stable release"

# 推送
git push origin main --tags
```

---

*最后更新: 2026-04-02*
