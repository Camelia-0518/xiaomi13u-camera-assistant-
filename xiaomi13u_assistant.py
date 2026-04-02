#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小米13 Ultra AI摄影指导助手
Xiaomi 13 Ultra AI Photography Assistant

功能：根据拍摄场景提供专业摄影参数指导
版本：1.0.0
作者：Kimi Claw
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# 小米13 Ultra 硬件参数
DEVICE_SPECS = {
    "name": "小米13 Ultra",
    "sensor": "Sony IMX989 1英寸",
    "aperture": ["f/1.9", "f/4.0"],  # 可变光圈
    "focal_lengths": ["12mm(超广)", "23mm(主摄)", "75mm(长焦)", "120mm(超长焦)"],
    "features": ["徕卡色彩", "街拍模式", "专业模式", "夜景模式"]
}

# 场景数据库 - 基于搜集的专业参数
SCENES = {
    "人像": {
        "icon": "👤",
        "description": "拍摄人物，强调肤色和背景虚化",
        "mode": "专业模式或人像模式",
        "settings": {
            "焦距": "75mm 长焦镜头 (3.2x)",
            "光圈": "f/1.9 (最大虚化)",
            "ISO": "100-400 (根据光线)",
            "快门": "1/125s 或更快",
            "白平衡": "自动 或 日光/阴天",
            "对焦": "眼睛对焦",
            "徕卡风格": "徕卡生动 (肤色更暖)",
            "影调": "+5 至 +10 (增加对比)",
            "锐度": "+5 (保持自然)"
        },
        "构图技巧": [
            "使用 75mm 长焦压缩背景",
            "光圈 f/1.9 获得奶油般虚化",
            "人物占画面 1/3 到 1/2",
            "眼睛放在上三分线",
            "利用街道、门窗作为框架"
        ],
        "距离": "1.5-3米 (75mm镜头最佳距离)"
    },
    
    "夜景": {
        "icon": "🌃",
        "description": "城市夜景、灯光场景",
        "mode": "专业模式 (必须上三脚架)",
        "settings": {
            "焦距": "23mm 主摄 (画质最好)",
            "光圈": "f/1.9 (进光最大化)",
            "ISO": "50-200 (控制噪点)",
            "快门": "2-30秒 (根据环境光)",
            "白平衡": "3000-4000K (暖色调)",
            "对焦": "无限远",
            "徕卡风格": "徕卡经典 (暗部细节丰富)",
            "影调": "+10 (增强电影感)",
            "EV": "-0.3 至 -0.7 (防止高光过曝)"
        },
        "构图技巧": [
            "寻找水面倒影增加对称美",
            "利用灯光做引导线",
            "包含前景增加层次感",
            "拍摄光轨需要10秒以上快门",
            "星芒效果用小光圈 f/4.0 + 点光源"
        ],
        "距离": "根据构图决定，注意前景层次"
    },
    
    "星空": {
        "icon": "⭐",
        "description": "银河、星轨、天体摄影",
        "mode": "专业模式 + 三脚架/稳定器",
        "settings": {
            "焦距": "23mm 主摄 (最广)",
            "光圈": "f/1.9 (最大进光)",
            "ISO": "1600-3200 (视光污染)",
            "快门": "15-25秒 (超过25秒会拖线)",
            "白平衡": "4000K 或 钨丝灯",
            "对焦": "手动对焦到无限远",
            "徕卡风格": "徕卡经典",
            "格式": "RAW (方便后期)",
            "倒计时": "3秒 (避免手震)"
        },
        "构图技巧": [
            "包含地面景物作为前景",
            "寻找银河拱桥角度",
            "使用Star Walk等APP找银河位置",
            "避开月光，选择农历月末月初",
            "光污染等级3以下效果最佳"
        ],
        "距离": "前景距离3-10米，背景无限远"
    },
    
    "街拍/人文": {
        "icon": "📸",
        "description": "快速抓拍、街头瞬间",
        "mode": "街拍模式 (最快) 或 专业模式",
        "settings": {
            "焦距": "23mm 主摄 或 35mm 裁切",
            "光圈": "f/4.0 (增加景深容错)",
            "ISO": "自动 (上限设3200)",
            "快门": "1/250s 或更快",
            "对焦": "超焦距 (2米-无限远清晰)",
            "徕卡风格": "徕卡经典 (德味)",
            "影调": "+10",
            "青品调": "+10",
            "EV": "-0.7 (保留高光细节)"
        },
        "构图技巧": [
            "开启街拍模式：锁屏双击音量下键",
            "预判动作，提前构图",
            "使用23mm广角带入环境",
            "寻找光影对比强烈的场景",
            "等一个决定性瞬间"
        ],
        "距离": "0.5-5米 (街拍通常较近)"
    },
    
    "美食": {
        "icon": "🍜",
        "description": "食物、饮品特写",
        "mode": "专业模式",
        "settings": {
            "焦距": "75mm 长焦 (避免透视变形)",
            "光圈": "f/1.9 (虚化背景杂物)",
            "ISO": "100-800",
            "快门": "1/60s 或更快",
            "白平衡": "自动 或 根据光源调整",
            "对焦": "食物最突出的部分",
            "徕卡风格": "徕卡生动 (色彩鲜艳)",
            "饱和度": "+5 至 +10",
            "锐度": "+10"
        },
        "构图技巧": [
            "45度俯拍最保险",
            "利用餐具、手作为引导",
            "寻找纹理对比 (粗糙vs光滑)",
            "蒸汽可以增加氛围感",
            "注意光源方向，避免顶光"
        ],
        "距离": "30-80cm (近摄距离)"
    },
    
    "风景": {
        "icon": "🏔️",
        "description": "自然风光、山川湖海",
        "mode": "专业模式",
        "settings": {
            "焦距": "12mm 超广 或 23mm 主摄",
            "光圈": "f/4.0 (最佳画质 + 景深)",
            "ISO": "50-100 (最低噪点)",
            "快门": "根据光线，可用慢门拍流水",
            "白平衡": "日光 或 自动",
            "对焦": "超焦距或无穷远",
            "徕卡风格": "徕卡经典 (层次丰富)",
            "格式": "RAW + JPG"
        },
        "构图技巧": [
            "三分法：地平线放在上/下三分线",
            "前景、中景、远景三层",
            "利用引导线 (道路、河流、栏杆)",
 "黄金时段：日出后1小时、日落前1小时",
            "超广角夸张前景增加冲击力"
        ],
        "距离": "前景30cm-1m，背景无限远"
    },
    
    "微距": {
        "icon": "🌸",
        "description": "花卉、昆虫、细节",
        "mode": "专业模式 + 长焦微距",
        "settings": {
            "焦距": "75mm 长焦 (支持近摄)",
            "光圈": "f/4.0 (增加景深避免虚化过度)",
            "ISO": "100-400",
            "快门": "1/125s 或更快",
            "对焦": "手动精确对焦",
            "徕卡风格": "徕卡生动",
            "锐度": "+10",
            "辅助": "开启峰值对焦 (如有)"
        },
        "构图技巧": [
            "寻找简洁背景",
            "利用长焦压缩空间",
            "注意景深极浅，对焦要精确",
            "尝试不同角度",
            "清晨露珠效果最佳"
        ],
        "距离": "10-30cm (75mm最近对焦距离)"
    },
    
    "建筑": {
        "icon": "🏢",
        "description": "城市建筑、室内设计",
        "mode": "专业模式",
        "settings": {
            "焦距": "12mm 超广 或 23mm 主摄",
            "光圈": "f/4.0-f/5.6 (最佳画质)",
            "ISO": "50-200",
            "快门": "根据光线",
            "白平衡": "自动 或 校正偏色",
            "对焦": "无穷远",
            "徕卡风格": "徕卡经典 (线条锐利)",
            "畸变校正": "开启"
        },
        "构图技巧": [
            "寻找对称构图",
            "利用前景框架",
            "注意垂直线条不要倾斜 (或后期校正)",
            "蓝调时刻拍摄最出片",
            "寻找几何图案和重复元素"
        ],
        "距离": "根据建筑大小决定"
    }
}

# 进阶技巧库
ADVANCED_TIPS = {
    "徕卡色彩玄学": {
        "原理": "徕卡对红、黄、蓝三原色敏感，适当让画面包含这些颜色",
        "应用": "拍摄时寻找红墙、蓝天、黄叶等元素"
    },
    "可变光圈": {
        "f/1.9": "最大虚化，适合人像、特写",
        "f/4.0": "最佳画质，适合风景、建筑、街拍"
    },
    "专业模式自定义画质": {
        "设置路径": "专业模式 → 左下角图标 → 自定义画质",
        "推荐预设": "影调+10, 青品调+10, 锐度+10, 徕卡经典"
    }
}

class PhotographyAssistant:
    def __init__(self):
        self.scenes = SCENES
        self.device = DEVICE_SPECS
        self.history = []
        
    def list_scenes(self) -> List[str]:
        """列出所有可用场景"""
        return [f"{info['icon']} {name}" for name, info in self.scenes.items()]
    
    def get_guide(self, scene_name: str) -> Optional[Dict]:
        """获取指定场景的拍摄指导"""
        if scene_name not in self.scenes:
            return None
        
        guide = self.scenes[scene_name].copy()
        guide['scene_name'] = scene_name
        guide['timestamp'] = datetime.now().isoformat()
        
        # 记录历史
        self.history.append({
            'scene': scene_name,
            'time': datetime.now().isoformat()
        })
        
        return guide
    
    def generate_setting_card(self, scene_name: str) -> str:
        """生成可打印的参数卡片"""
        guide = self.get_guide(scene_name)
        if not guide:
            return f"未知场景: {scene_name}"
        
        card = f"""
╔══════════════════════════════════════════════════════════╗
║  📷 小米13 Ultra 摄影参数卡 - {guide['icon']} {scene_name:12s} ║
╠══════════════════════════════════════════════════════════╣
║  模式: {guide['mode']:45s} ║
╠══════════════════════════════════════════════════════════╣
║  【基础参数】                                            ║
"""
        for key, value in guide['settings'].items():
            card += f"║  {key:8s}: {value:45s} ║\n"
        
        card += "╠══════════════════════════════════════════════════════════╣\n"
        card += "║  【构图要点】                                            ║\n"
        for i, tip in enumerate(guide['构图技巧'][:4], 1):
            card += f"║  {i}. {tip:50s} ║\n"
        
        card += f"║  【推荐距离】{guide['距离']:42s} ║\n"
        card += "╚══════════════════════════════════════════════════════════╝"
        
        return card
    
    def analyze_photo(self, description: str) -> str:
        """基于文字描述给出拍摄建议（简化版AI分析）"""
        # 关键词匹配
        keywords = {
            "人": "人像",
            "脸": "人像", 
            "肖像": "人像",
            "夜景": "夜景",
            "晚上": "夜景",
            "灯光": "夜景",
            "星空": "星空",
            "银河": "星空",
            "星星": "星空",
            "街": "街拍/人文",
            "人文": "街拍/人文",
            "吃": "美食",
            "食物": "美食",
            "菜": "美食",
            "山": "风景",
            "海": "风景",
            "风景": "风景",
            "花": "微距",
            "虫": "微距",
            "细节": "微距",
            "楼": "建筑",
            "建筑": "建筑"
        }
        
        matched_scenes = []
        for keyword, scene in keywords.items():
            if keyword in description:
                matched_scenes.append(scene)
        
        if matched_scenes:
            most_common = max(set(matched_scenes), key=matched_scenes.count)
            return f"根据描述，建议查看【{most_common}】场景的参数设置。"
        
        return "无法识别场景，请从以下场景中选择：" + ", ".join(self.scenes.keys())
    
    def export_preset(self, scene_name: str, filename: str = None):
        """导出参数预设为JSON文件"""
        guide = self.get_guide(scene_name)
        if not guide:
            return False
        
        if not filename:
            filename = f"xiaomi13u_preset_{scene_name}_{datetime.now().strftime('%Y%m%d')}.json"
        
        preset = {
            "device": self.device["name"],
            "scene": scene_name,
            "created_at": datetime.now().isoformat(),
            "settings": guide["settings"],
            "composition_tips": guide["构图技巧"],
            "recommended_distance": guide["距离"]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(preset, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def get_advanced_tip(self, topic: str = None) -> str:
        """获取进阶技巧"""
        if topic and topic in ADVANCED_TIPS:
            tip = ADVANCED_TIPS[topic]
            return f"【{topic}】\n" + "\n".join([f"{k}: {v}" for k, v in tip.items()])
        
        # 随机返回一个技巧
        import random
        topic = random.choice(list(ADVANCED_TIPS.keys()))
        tip = ADVANCED_TIPS[topic]
        return f"【随机技巧 - {topic}】\n" + "\n".join([f"  {k}: {v}" for k, v in tip.items()])


def interactive_cli():
    """交互式命令行界面"""
    assistant = PhotographyAssistant()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║     📷 小米13 Ultra AI摄影指导助手 v1.0.0               ║
║     Xiaomi 13 Ultra AI Photography Assistant            ║
╠══════════════════════════════════════════════════════════╣
║  输入场景名称获取参数指导                                 ║
║  输入 'list' 查看所有场景                                 ║
║  输入 'card [场景]' 生成参数卡片                          ║
║  输入 'export [场景]' 导出预设文件                        ║
║  输入 'tip' 获取进阶技巧                                  ║
║  输入 'quit' 退出                                         ║
╚══════════════════════════════════════════════════════════╝
""")
    
    while True:
        try:
            user_input = input("\n🎯 请输入场景或命令: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！记住：最好的相机是你手中的那台。")
                break
            
            elif user_input.lower() == 'list':
                print("\n📋 可用场景列表:")
                for scene in assistant.list_scenes():
                    print(f"   {scene}")
            
            elif user_input.lower().startswith('card '):
                scene = user_input[5:].strip()
                print(assistant.generate_setting_card(scene))
            
            elif user_input.lower().startswith('export '):
                scene = user_input[7:].strip()
                filename = assistant.export_preset(scene)
                if filename:
                    print(f"✅ 预设已导出: {filename}")
                else:
                    print(f"❌ 未知场景: {scene}")
            
            elif user_input.lower() == 'tip':
                print(assistant.get_advanced_tip())
            
            elif user_input in assistant.scenes:
                guide = assistant.get_guide(user_input)
                print(f"\n{'='*60}")
                print(f"{guide['icon']} {user_input} - {guide['description']}")
                print(f"{'='*60}")
                print(f"\n📷 推荐模式: {guide['mode']}")
                print(f"\n⚙️ 参数设置:")
                for key, value in guide['settings'].items():
                    print(f"   {key:10s}: {value}")
                print(f"\n🎨 构图技巧:")
                for i, tip in enumerate(guide['构图技巧'], 1):
                    print(f"   {i}. {tip}")
                print(f"\n📏 推荐距离: {guide['距离']}")
                print(f"{'='*60}")
            
            else:
                # 尝试分析描述
                result = assistant.analyze_photo(user_input)
                print(result)
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    interactive_cli()
