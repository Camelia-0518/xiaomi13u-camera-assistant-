# Kivy版 - 悬浮窗相机助手
# 可以打包成APK，支持自动检测相机

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from jnius import autoclass, cast
import threading
import time

# Android相关类（仅在Android上可用）
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    ActivityManager = autoclass('android.app.ActivityManager')
    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')
    System = autoclass('java.lang.System')
    Build = autoclass('android.os.Build')
    ANDROID_AVAILABLE = True
except:
    ANDROID_AVAILABLE = False

# 场景数据
SCENES = {
    'portrait': {
        'name': '人像',
        'icon': '👤',
        'color': (0.4, 0.48, 0.92, 1),
        'params': {
            '焦距': '75mm 长焦',
            '光圈': 'f/1.9',
            'ISO': '100-400',
            '快门': '1/125s',
            '对焦': '眼睛对焦'
        },
        'tips': [
            '1.5米距离最佳',
            '人物占画面1/3',
            '使用75mm压缩背景',
            '光圈f/1.9奶油虚化'
        ]
    },
    'night': {
        'name': '夜景',
        'icon': '🌃',
        'color': (0.17, 0.24, 0.31, 1),
        'params': {
            '焦距': '23mm 主摄',
            '光圈': 'f/1.9',
            'ISO': '50-200',
            '快门': '2-30秒',
            '白平衡': '3000-4000K'
        },
        'tips': [
            '必须上三脚架',
            '寻找水面倒影',
            '利用灯光做引导线',
            'EV -0.3防过曝'
        ]
    },
    'street': {
        'name': '街拍',
        'icon': '📸',
        'color': (0.95, 0.61, 0.07, 1),
        'params': {
            '焦距': '23mm 主摄',
            '光圈': 'f/4.0',
            'ISO': '自动',
            '快门': '1/250s',
            'EV': '-0.7'
        },
        'tips': [
            '双击音量下键启动',
            '0.8秒快速抓拍',
            '预判动作提前构图',
            '等决定性瞬间'
        ]
    },
    'landscape': {
        'name': '风景',
        'icon': '🏔️',
        'color': (0.15, 0.68, 0.38, 1),
        'params': {
            '焦距': '12mm 超广',
            '光圈': 'f/4.0',
            'ISO': '50-100',
            '白平衡': '日光',
            '格式': 'RAW+JPG'
        },
        'tips': [
            '黄金时段拍摄',
            '前景+中景+远景',
            '地平线放三分线',
            '超广角夸张前景'
        ]
    },
    'food': {
        'name': '美食',
        'icon': '🍜',
        'color': (0.91, 0.26, 0.58, 1),
        'params': {
            '焦距': '75mm 长焦',
            '光圈': 'f/1.9',
            'ISO': '100-800',
            '快门': '1/60s',
            '角度': '45度俯拍'
        },
        'tips': [
            '30-80cm距离',
            '找纹理对比',
            '蒸汽增加氛围',
            '注意光源方向'
        ]
    },
    'star': {
        'name': '星空',
        'icon': '⭐',
        'color': (0.18, 0.2, 0.21, 1),
        'params': {
            '焦距': '23mm 主摄',
            '光圈': 'f/1.9',
            'ISO': '1600-3200',
            '快门': '15-25秒',
            '对焦': '无限远'
        },
        'tips': [
            '需三脚架',
            '避开月光',
            '找地面前景',
            '快门>25秒拖线'
        ]
    }
}

class SceneCard(BoxLayout):
    def __init__(self, scene_key, scene_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.scene_key = scene_key
        self.scene_data = scene_data
        
        # 设置背景色
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*scene_data['color'])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 图标和名称
        self.add_widget(Label(
            text=f"{scene_data['icon']}\n{scene_data['name']}",
            font_size='24sp',
            color=(1, 1, 1, 1),
            size_hint_y=0.6
        ))
        
        # 简要参数
        params_text = list(scene_data['params'].values())[0]
        self.add_widget(Label(
            text=params_text[:15] + '...' if len(params_text) > 15 else params_text,
            font_size='12sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.4
        ))
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.show_detail()
            return True
        return super().on_touch_down(touch)
    
    def show_detail(self):
        # 创建详情弹窗
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        content.add_widget(Label(
            text=f"{self.scene_data['icon']} {self.scene_data['name']}",
            font_size='28sp',
            size_hint_y=None,
            height=60
        ))
        
        # 参数
        params_text = '\n'.join([f"{k}: {v}" for k, v in self.scene_data['params'].items()])
        content.add_widget(Label(
            text=params_text,
            font_size='16sp',
            size_hint_y=None,
            height=150,
            halign='left',
            text_size=(400, None)
        ))
        
        # 技巧
        tips_text = '\n💡 ' + '\n💡 '.join(self.scene_data['tips'])
        content.add_widget(Label(
            text=tips_text,
            font_size='14sp',
            size_hint_y=None,
            height=120,
            halign='left',
            text_size=(400, None)
        ))
        
        # 关闭按钮
        close_btn = Button(
            text='关闭',
            size_hint_y=None,
            height=50
        )
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=True
        )
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()

class CameraAssistantApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.18, 1)
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        header = BoxLayout(size_hint_y=None, height=80, padding=10)
        header.add_widget(Label(
            text='📷 小米13 Ultra\n摄影助手',
            font_size='24sp',
            halign='center'
        ))
        root.add_widget(header)
        
        # 快速提示
        tips_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            padding=10
        )
        with tips_box.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.2, 0.2, 0.3, 1)
            self.tips_rect = Rectangle(pos=tips_box.pos, size=tips_box.size)
        tips_box.bind(pos=self.update_tips_rect, size=self.update_tips_rect)
        
        tips_box.add_widget(Label(
            text='⚡ 快速记忆',
            font_size='14sp',
            color=(1, 0.42, 0.42, 1),
            size_hint_y=None,
            height=25
        ))
        tips_box.add_widget(Label(
            text='街拍: 锁屏双击音量下\n光圈: f/1.9虚化 f/4.0画质\n夜景: 三脚架+长曝光',
            font_size='13sp',
            halign='left',
            text_size=(400, None)
        ))
        root.add_widget(tips_box)
        
        # 场景网格
        grid = GridLayout(
            cols=3,
            spacing=10,
            padding=10,
            size_hint_y=0.6
        )
        
        for key, data in SCENES.items():
            card = SceneCard(key, data)
            grid.add_widget(card)
        
        root.add_widget(grid)
        
        # 底部提示
        footer = Label(
            text='点击场景查看详细参数',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30
        )
        root.add_widget(footer)
        
        return root
    
    def update_tips_rect(self, instance, value):
        self.tips_rect.pos = instance.pos
        self.tips_rect.size = instance.size

if __name__ == '__main__':
    CameraAssistantApp().run()
