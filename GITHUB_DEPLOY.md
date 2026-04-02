# 🚀 GitHub 自动编译指南

## 你需要做的（3步）

### 第1步：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写：
   - Repository name: `xiaomi13u-camera-assistant`
   - Description: `小米13 Ultra 摄影助手 - 自动显示拍摄参数`
   - 选择 **Public**（免费）
   - ✅ 勾选 "Add a README file"
3. 点击 **Create repository**

### 第2步：获取仓库地址

创建后，复制仓库地址（HTTPS）：
```
https://github.com/你的用户名/xiaomi13u-camera-assistant.git
```

### 第3步：推送代码

在服务器上执行：

```bash
cd ~/.openclaw/workspace/xiaomi13u-camera-assistant

# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/xiaomi13u-camera-assistant.git

# 推送代码
git branch -M main
git push -u origin main
```

**需要输入GitHub账号密码**（或配置SSH密钥）

---

## 等待编译完成

推送成功后：

1. 访问 `https://github.com/你的用户名/xiaomi13u-camera-assistant/actions`
2. 你会看到正在运行的 workflow
3. 等待 3-5 分钟（绿色✓表示成功）

---

## 下载APK

编译完成后：

1. 点击最新的 workflow 运行记录
2. 找到 "Artifacts" 部分
3. 下载 `xiaomi13u-camera-assistant-apk`
4. 解压得到 `app-debug.apk`
5. 发送到手机安装

---

## 手机安装步骤

```
1. 将APK发送到手机（微信/QQ/邮件）
2. 手机点击APK文件
3. 允许"未知来源"安装
4. 安装完成
5. 打开APP，开启无障碍服务
6. 打开相机，享受自动指导！
```

---

## 功能说明

安装后：
- 📱 桌面出现「小米13U摄影助手」图标
- 🔘 打开APP，开启「无障碍服务」权限
- 📷 打开相机，自动弹出悬浮指导
- 👆 点击场景按钮，查看详细参数
- ✕ 点击关闭或退出相机自动消失

---

## 注意事项

**首次使用需要授权：**
1. 无障碍服务（检测相机启动）
2. 悬浮窗权限（显示指导界面）

**回退方法：**
```
设置 → 应用管理 → 小米13U摄影助手 → 卸载
```

---

## 遇到问题？

1. **GitHub推送失败** → 检查用户名/密码，或使用SSH
2. **编译失败** → 检查Actions日志，通常会自动重试
3. **安装失败** → 确保允许"未知来源"安装
4. **无法检测相机** → 检查是否开启了无障碍服务

---

## 快捷命令

```bash
# 我已经帮你初始化好了，只需执行：
cd ~/.openclaw/workspace/xiaomi13u-camera-assistant
git remote add origin https://github.com/你的用户名/xiaomi13u-camera-assistant.git
git push -u origin main
```

---

🎉 完成后告诉我，我帮你检查！
