#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小米13 Ultra AI摄影指导助手 - Web界面
使用 Streamlit 构建，支持手机浏览器访问
"""

import streamlit as st
import json
from datetime import datetime
from xiaomi13u_assistant import PhotographyAssistant, SCENES

# 页面配置
st.set_page_config(
    page_title="小米13 Ultra AI摄影助手",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .scene-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .param-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .tip-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .device-info {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化
@st.cache_resource
def get_assistant():
    return PhotographyAssistant()

assistant = get_assistant()

# 标题
st.title("📷 小米13 Ultra AI摄影助手")
st.caption("让专业摄影师住进你的手机")

# 设备信息
with st.expander("ℹ️ 设备信息", expanded=False):
    st.markdown("""
    **小米13 Ultra 硬件规格**
    - 📸 主摄: Sony IMX989 1英寸
    - 🔍 焦段: 12mm | 23mm | 75mm | 120mm
    - 🔆 光圈: f/1.9 - f/4.0 可变
    - 🎨 特色: 徕卡色彩 | 街拍模式
    """)

# 场景选择
st.subheader("🎯 选择拍摄场景")

# 创建场景按钮网格
cols = st.columns(2)
scene_names = list(SCENES.keys())
selected_scene = None

for i, scene_name in enumerate(scene_names):
    with cols[i % 2]:
        icon = SCENES[scene_name]['icon']
        if st.button(f"{icon} {scene_name}", key=f"scene_{i}"):
            selected_scene = scene_name

# 显示选中场景的指导
if selected_scene:
    guide = assistant.get_guide(selected_scene)
    
    st.markdown(f"""
    <div class="scene-card">
        <h2>{guide['icon']} {selected_scene}</h2>
        <p>{guide['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 推荐模式
    st.info(f"📷 推荐模式: {guide['mode']}")
    
    # 参数设置
    st.subheader("⚙️ 参数设置")
    settings = guide['settings']
    
    # 创建参数表格
    param_df = []
    for key, value in settings.items():
        param_df.append({"参数": key, "设置值": value})
    
    for param in param_df:
        st.markdown(f"""
        <div class="param-box">
            <b>{param['参数']}</b>: {param['设置值']}
        </div>
        """, unsafe_allow_html=True)
    
    # 构图技巧
    st.subheader("🎨 构图技巧")
    for i, tip in enumerate(guide['构图技巧'], 1):
        st.markdown(f"""
        <div class="tip-box">
            <b>{i}.</b> {tip}
        </div>
        """, unsafe_allow_html=True)
    
    # 推荐距离
    st.success(f"📏 推荐距离: {guide['距离']}")
    
    # 导出按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 复制参数"):
            params_text = f"""
【{selected_scene}】参数设置
模式: {guide['mode']}
{chr(10).join([f"{k}: {v}" for k, v in guide['settings'].items()])}
            """.strip()
            st.code(params_text)
            st.success("参数已显示，可手动复制")
    
    with col2:
        preset_json = json.dumps({
            "device": "小米13 Ultra",
            "scene": selected_scene,
            "created_at": datetime.now().isoformat(),
            "settings": guide["settings"]
        }, ensure_ascii=False, indent=2)
        st.download_button(
            label="💾 导出预设",
            data=preset_json,
            file_name=f"xiaomi13u_preset_{selected_scene}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# 进阶技巧
st.divider()
st.subheader("💡 进阶技巧")

if st.button("🎲 随机获取一个技巧"):
    tip = assistant.get_advanced_tip()
    st.info(tip)

# 场景分析
st.divider()
st.subheader("🔍 场景分析")
user_desc = st.text_area("描述你想拍的场景，AI会推荐参数:", 
                         placeholder="例如: 想拍晚上城市的灯光倒影")
if st.button("分析场景"):
    if user_desc:
        result = assistant.analyze_photo(user_desc)
        st.success(result)
        # 如果识别出场景，显示该场景卡片
        for scene_name in SCENES.keys():
            if scene_name in result:
                guide = assistant.get_guide(scene_name)
                with st.expander(f"查看【{scene_name}】详细参数"):
                    st.json(guide['settings'])
    else:
        st.warning("请先输入场景描述")

# 页脚
st.divider()
st.caption("""
📷 小米13 Ultra AI摄影助手 v1.0.0 | 
记住：最好的相机是你手中的那台
""")
