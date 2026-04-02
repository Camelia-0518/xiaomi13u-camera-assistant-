#!/bin/bash
# 小米13 Ultra 摄影助手启动脚本
# 自动检测环境并启动最佳界面

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📷 小米13 Ultra AI摄影助手"
echo "═══════════════════════════════════════"

# 检测运行环境
if [ -n "$TERMUX_VERSION" ]; then
    echo "✅ 检测到 Termux 环境"
    RUN_MODE="termux"
elif [ -n "$DISPLAY" ] && command -v python3 &> /dev/null; then
    # 检查是否有streamlit
    if python3 -c "import streamlit" 2>/dev/null; then
        echo "✅ 检测到桌面环境 + Streamlit"
        RUN_MODE="web"
    else
        echo "✅ 检测到桌面环境 (CLI模式)"
        RUN_MODE="cli"
    fi
else
    echo "✅ 使用 CLI 模式"
    RUN_MODE="cli"
fi

echo ""

# 根据环境启动
case $RUN_MODE in
    "web")
        echo "🌐 启动 Web 界面..."
        echo "   访问地址: http://localhost:8501"
        echo "   按 Ctrl+C 停止"
        echo ""
        streamlit run web_app.py
        ;;
    "termux"|"cli")
        echo "💻 启动 CLI 交互界面..."
        echo ""
        python3 xiaomi13u_assistant.py
        ;;
esac
