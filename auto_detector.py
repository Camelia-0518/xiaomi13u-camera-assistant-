#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小米13 Ultra AI摄影助手 - 自动检测增强版
功能：检测相机启动，自动弹出拍摄建议
"""

import json
import os
import sys
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 导入核心库
from xiaomi13u_assistant import PhotographyAssistant, SCENES

# Android相机包名（小米）
MI_CAMERA_PACKAGES = [
    "com.android.camera",
    "com.miui.camera", 
    "com.android.camera2",
    "com.xiaomi.camera",
    "com.google.android.GoogleCamera"
]

# 检测间隔（秒）
CHECK_INTERVAL = 2

class CameraAutoDetector:
    """相机自动检测器"""
    
    def __init__(self):
        self.assistant = PhotographyAssistant()
        self.last_detected = None
        self.is_running = False
        self.camera_active = False
        
    def check_camera_running(self) -> Tuple[bool, str]:
        """检查相机是否在前台运行
        
        支持多种检测方式：
        1. ADB检测（需USB调试）
        2. dumpsys activity检测
        3. logcat检测
        
        Returns:
            (是否运行, 当前应用包名)
        """
        try:
            # 方式1: 使用dumpsys activity检测前台应用
            result = subprocess.run(
                ['dumpsys', 'activity', 'activities', '|', 'grep', 'mResumedActivity'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=2
            )
            
            output = result.stdout.lower()
            
            for pkg in MI_CAMERA_PACKAGES:
                if pkg.lower() in output:
                    return True, pkg
            
            # 方式2: 检查窗口焦点
            result2 = subprocess.run(
                ['dumpsys', 'window', 'windows', '|', 'grep', '-E', 'mCurrentFocus|mFocusedApp'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=2
            )
            
            output2 = result2.stdout.lower()
            for pkg in MI_CAMERA_PACKAGES:
                if pkg.lower() in output2:
                    return True, pkg
                    
            return False, ""
            
        except Exception as e:
            return False, str(e)
    
    def show_camera_guide(self, context: str = "auto"):
        """显示相机指导
        
        Args:
            context: 场景上下文，"auto"表示智能检测
        """
        import random
        
        print("\n" + "="*60)
        print("📷 检测到相机启动 - 小米13 Ultra 拍摄建议")
        print("="*60)
        
        if context == "auto":
            # 显示快速选择菜单
            print("\n🎯 选择当前拍摄场景：")
            scenes = list(SCENES.keys())
            for i, scene in enumerate(scenes, 1):
                icon = SCENES[scene]['icon']
                print(f"   {i}. {icon} {scene}")
            print(f"   0. 💡 随机技巧")
            print(f"   q. 退出检测")
            
            try:
                choice = input("\n选择场景编号: ").strip()
                
                if choice == 'q':
                    return False
                elif choice == '0':
                    print("\n" + self.assistant.get_advanced_tip())
                elif choice.isdigit() and 1 <= int(choice) <= len(scenes):
                    scene_name = scenes[int(choice) - 1]
                    print(self.assistant.generate_setting_card(scene_name))
                else:
                    print("⚠️ 无效选择")
                    
            except KeyboardInterrupt:
                return False
                
        return True
    
    def start_monitoring(self):
        """开始监控相机启动"""
        print("""
╔══════════════════════════════════════════════════════════╗
║     📷 小米13 Ultra 相机自动检测器                        ║
╠══════════════════════════════════════════════════════════╣
║  正在监控相机应用启动...                                   ║
║  检测到相机启动时将自动弹出拍摄建议                         ║
║                                                          ║
║  按 Ctrl+C 停止监控                                       ║
╚══════════════════════════════════════════════════════════╝
""")
        
        self.is_running = True
        
        try:
            while self.is_running:
                is_camera_running, pkg = self.check_camera_running()
                
                if is_camera_running and not self.camera_active:
                    # 相机刚启动
                    print(f"\n✅ 检测到相机启动: {pkg}")
                    self.camera_active = True
                    self.last_detected = datetime.now()
                    
                    # 显示指导
                    result = self.show_camera_guide("auto")
                    if not result:
                        print("\n👋 停止监控")
                        break
                        
                elif not is_camera_running and self.camera_active:
                    # 相机关闭
                    print("\n📴 相机已关闭，继续监控...")
                    self.camera_active = False
                    
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n👋 监控已停止")
            self.is_running = False
    
    def show_quick_overlay(self):
        """显示快速悬浮提示（Termux/终端支持）"""
        # 简化版快速提示
        quick_tips = """
╔══════════════════════════════════════════════════════════╗
║  ⚡ 小米13U 快速拍摄提示                                  ║
╠══════════════════════════════════════════════════════════╣
║  街拍模式: 锁屏双击音量下键                               ║
║  可变光圈: f/1.9(虚化) / f/4.0(画质)                      ║
║  万能夜景: ISO100 + 2-30秒 + 三脚架                       ║
║  人像虚化: 75mm + f/1.9 + 1.5米                           ║
║  徕卡色彩: 画面加红/黄/蓝色更出片                         ║
╚══════════════════════════════════════════════════════════╝
"""
        print(quick_tips)


def install_tasker_integration():
    """安装Tasker集成脚本"""
    tasker_script = '''#!/bin/bash
# Tasker集成脚本 - 由Tasker调用
# 将此脚本保存到手机存储，Tasker中设置为「相机打开时执行」

cd /data/data/com.termux/files/home/xiaomi13u-camera-assistant
python3 auto_detector.py --quick-tip
'''
    
    # 保存Tasker脚本
    script_path = os.path.expanduser("~/.openclaw/workspace/xiaomi13u-camera-assistant/tasker_integration.sh")
    with open(script_path, 'w') as f:
        f.write(tasker_script)
    
    os.chmod(script_path, 0o755)
    
    print(f"✅ Tasker集成脚本已保存: {script_path}")
    print("""
📱 Tasker设置步骤:
1. 安装 Tasker App
2. 创建新任务: "显示拍摄提示"
3. 添加动作: "Termux" → "执行脚本"
4. 选择: tasker_integration.sh
5. 创建触发器: "应用" → "相机"
6. 完成！打开相机时自动显示提示
""")
    return script_path


def install_accessibility_service():
    """安装无障碍服务说明"""
    guide = """
📱 Android无障碍服务方案（全自动，无需Tasker）

需要开发原生Android App，核心功能：

1. 创建AccessibilityService
2. 监听窗口状态变化
3. 检测到com.android.camera时弹出悬浮窗

实现代码框架：

```kotlin
class CameraAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            val packageName = event.packageName?.toString()
            if (packageName == "com.android.camera") {
                showFloatingGuide()  // 显示拍摄指导
            }
        }
    }
}
```

用户操作：
1. 安装APK
2. 设置 → 无障碍 → 选择「小米13U摄影助手」
3. 开启服务
4. 每次打开相机自动弹出拍摄指导悬浮窗

优势：
- ✅ 全自动，无需Tasker
- ✅ 系统级检测，最可靠
- ✅ 可显示悬浮窗覆盖相机界面

限制：
- ⚠️ 需要用户手动开启无障碍权限
- ⚠️ Android 13+ 有限制，需要额外适配
"""
    print(guide)


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小米13 Ultra 相机自动检测器')
    parser.add_argument('--monitor', '-m', action='store_true', 
                        help='启动相机启动监控')
    parser.add_argument('--quick-tip', '-q', action='store_true',
                        help='显示快速提示')
    parser.add_argument('--install-tasker', action='store_true',
                        help='安装Tasker集成')
    parser.add_argument('--install-accessibility', action='store_true',
                        help='显示无障碍服务安装说明')
    
    args = parser.parse_args()
    
    detector = CameraAutoDetector()
    
    if args.monitor:
        detector.start_monitoring()
    elif args.quick_tip:
        detector.show_quick_overlay()
    elif args.install_tasker:
        install_tasker_integration()
    elif args.install_accessibility:
        install_accessibility_service()
    else:
        # 默认显示帮助
        print("""
📷 小米13 Ultra 相机自动检测器

使用方式:
  python3 auto_detector.py --monitor       # 启动监控模式
  python3 auto_detector.py --quick-tip     # 显示快速提示
  python3 auto_detector.py --install-tasker # 安装Tasker集成

建议设置（Termux环境）:
1. 安装 Termux + Tasker
2. 运行 --install-tasker 生成集成脚本
3. 在Tasker中设置相机打开时执行脚本
4. 享受自动拍摄指导！
""")


if __name__ == "__main__":
    main()
