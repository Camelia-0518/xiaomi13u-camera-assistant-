#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小米13 Ultra AI摄影指导助手 - Kivy移动端界面
用于构建Android APK
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from xiaomi13u_assistant import PhotographyAssistant, SCENES

# 设置窗口大小（模拟手机屏幕）
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class SceneButton(Button):
    """场景按钮"""
    scene_name = StringProperty('')
    
    def __init__(self, scene_name, icon, **kwargs):
        super().__init__(**kwargs)
        self.scene_name = scene_name
        self.text = f"{icon}\n{scene_name}"
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = '100dp'
        self.background_color = (0.2, 0.6, 0.9, 1)
        self.color = (1, 1, 1, 1)

class GuidePopup(Popup):
    """参数指导弹窗"""
    def __init__(self, guide, **kwargs):
        super().__init__(**kwargs)
        self.title = f"{guide['icon']} {guide.get('scene_name', '参数指导')}"
        self.size_hint = (0.95, 0.9)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 滚动视图
        scroll = ScrollView()
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # 描述
        desc = Label(
            text=guide['description'],
            size_hint_y=None,
            height='40dp',
            color=(0.3, 0.3, 0.3, 1)
        )
        content.add_widget(desc)
        
        # 推荐模式
        mode_label = Label(
            text=f"[b]推荐模式:[/b] {guide['mode']}",
            markup=True,
            size_hint_y=None,
            height='40dp',
            color=(0.1, 0.4, 0.7, 1)
        )
        content.add_widget(mode_label)
        
        # 参数设置
        params_title = Label(
            text="[b]⚙️ 参数设置[/b]",
            markup=True,
            size_hint_y=None,
            height='30dp',
            color=(0.2, 0.2, 0.2, 1)
        )
        content.add_widget(params_title)
        
        for key, value in guide['settings'].items():
            param_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
            key_label = Label(
                text=f"[b]{key}:[/b]",
                markup=True,
                size_hint_x=0.3,
                halign='right',
                color=(0.3, 0.3, 0.3, 1)
            )
            value_label = Label(
                text=value,
                size_hint_x=0.7,
                halign='left',
                color=(0.1, 0.1, 0.1, 1)
            )
            param_box.add_widget(key_label)
            param_box.add_widget(value_label)
            content.add_widget(param_box)
        
        # 构图技巧
        tips_title = Label(
            text="[b]🎨 构图技巧[/b]",
            markup=True,
            size_hint_y=None,
            height='30dp',
            color=(0.2, 0.2, 0.2, 1)
        )
        content.add_widget(tips_title)
        
        for i, tip in enumerate(guide['构图技巧'], 1):
            tip_label = Label(
                text=f"{i}. {tip}",
                size_hint_y=None,
                height='60dp',
                color=(0.2, 0.5, 0.2, 1),
                halign='left',
                valign='top'
            )
            tip_label.bind(size=tip_label.setter('text_size'))
            content.add_widget(tip_label)
        
        # 推荐距离
        distance = Label(
            text=f"[b]📏 推荐距离:[/b] {guide['距离']}",
            markup=True,
            size_hint_y=None,
            height='40dp',
            color=(0.1, 0.4, 0.7, 1)
        )
        content.add_widget(distance)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        # 关闭按钮
        close_btn = Button(
            text='关闭',
            size_hint_y=None,
            height='50dp',
            background_color=(0.9, 0.3, 0.3, 1)
        )
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)
        
        self.content = layout

class MainScreen(BoxLayout):
    """主界面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.assistant = PhotographyAssistant()
        
        # 标题
        title = Label(
            text='[b]📷 小米13 Ultra[/b]\nAI摄影助手',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height='80dp',
            color=(0.2, 0.2, 0.2, 1)
        )
        self.add_widget(title)
        
        # 副标题
        subtitle = Label(
            text='选择拍摄场景获取专业指导',
            font_size='14sp',
            size_hint_y=None,
            height='30dp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.add_widget(subtitle)
        
        # 场景网格
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for scene_name, info in SCENES.items():
            btn = SceneButton(
                scene_name=scene_name,
                icon=info['icon']
            )
            btn.bind(on_press=self.on_scene_select)
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        self.add_widget(scroll)
        
        # 底部按钮
        bottom_layout = BoxLayout(size_hint_y=None, height='60dp', padding=10)
        
        tip_btn = Button(
            text='💡 随机技巧',
            background_color=(0.4, 0.7, 0.4, 1)
        )
        tip_btn.bind(on_press=self.show_random_tip)
        
        info_btn = Button(
            text='ℹ️ 设备信息',
            background_color=(0.7, 0.7, 0.4, 1)
        )
        info_btn.bind(on_press=self.show_device_info)
        
        bottom_layout.add_widget(tip_btn)
        bottom_layout.add_widget(info_btn)
        self.add_widget(bottom_layout)
    
    def on_scene_select(self, instance):
        """选择场景"""
        scene_name = instance.scene_name
        guide = self.assistant.get_guide(scene_name)
        popup = GuidePopup(guide=guide)
        popup.open()
    
    def show_random_tip(self, instance):
        """显示随机技巧"""
        tip = self.assistant.get_advanced_tip()
        popup = Popup(
            title='💡 进阶技巧',
            content=Label(text=tip, color=(0.2, 0.4, 0.2, 1)),
            size_hint=(0.9, 0.6)
        )
        popup.open()
    
    def show_device_info(self, instance):
        """显示设备信息"""
        info = """
[b]小米13 Ultra 硬件规格[/b]

📸 主摄: Sony IMX989 1英寸
🔍 焦段: 12mm | 23mm | 75mm | 120mm
🔆 光圈: f/1.9 - f/4.0 可变
🎨 特色: 徕卡色彩 | 街拍模式

[b]街拍快捷键[/b]
锁屏状态双击音量下键
→ 0.8秒启动并拍照
        """
        popup = Popup(
            title='ℹ️ 设备信息',
            content=Label(text=info, markup=True, color=(0.3, 0.3, 0.3, 1)),
            size_hint=(0.9, 0.7)
        )
        popup.open()

class Xiaomi13UApp(App):
    """Kivy应用"""
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    Xiaomi13UApp().run()
