#!/bin/bash

# AI宠物启动脚本 - 自动检查并启动Ollama服务
# 使用方法: ./start_ai_pet.sh

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# 检查Ollama是否安装
check_ollama_installed() {
    if ! command -v ollama &> /dev/null; then
        log_error "Ollama未安装或不在PATH中"
        log_info "请访问 https://ollama.com/download 下载安装Ollama"
        return 1
    fi
    log_success "Ollama已安装"
    return 0
}

# 检查Ollama服务状态
check_ollama_status() {
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 启动Ollama服务
start_ollama() {
    log_info "正在启动Ollama服务..."
    
    # 后台启动ollama serve
    nohup ollama serve > /dev/null 2>&1 &
    local ollama_pid=$!
    
    log_info "Ollama服务进程已启动 (PID: $ollama_pid)"
    
    # 等待服务启动
    local max_wait=30
    local count=0
    
    while [ $count -lt $max_wait ]; do
        if check_ollama_status; then
            log_success "Ollama服务启动成功"
            return 0
        fi
        
        log_info "等待Ollama服务启动... ($((count+1))/$max_wait)"
        sleep 1
        ((count++))
    done
    
    log_error "Ollama服务启动超时"
    return 1
}

# 检查并下载所需模型
ensure_model() {
    local model_name=${1:-"nomic-embed-text"}
    
    log_info "检查模型 $model_name 是否可用..."
    
    if ollama list | grep -q "$model_name"; then
        log_success "模型 $model_name 已可用"
        return 0
    fi
    
    log_info "正在下载模型 $model_name..."
    if ollama pull "$model_name"; then
        log_success "模型 $model_name 下载成功"
        return 0
    else
        log_error "模型 $model_name 下载失败"
        return 1
    fi
}

# 启动AI宠物应用程序
start_ai_pet_app() {
    log_info "正在启动AI宠物应用程序..."
    
    # 请根据你的实际情况修改以下启动命令
    # 示例1: 如果是Python脚本
    # python3 ai_pet_main.py
    
    # 示例2: 如果是其他可执行文件
    # ./ai_pet_executable
    
    # 示例3: 如果需要激活虚拟环境
    # source venv/bin/activate && python3 ai_pet_main.py
    
    # 临时占位符 - 请替换为你的实际启动命令
    if [ -f "ai_pet_main.py" ]; then
        log_info "找到AI宠物主程序文件，正在启动..."
        python3 ai_pet_main.py
    elif [ -f "main.py" ]; then
        log_info "找到main.py文件，正在启动..."
        python3 main.py
    else
        log_warning "未找到AI宠物主程序文件"
        log_info "请在脚本中指定正确的启动命令"
        log_info "当前目录内容:"
        ls -la
        return 1
    fi
}

# 清理函数
cleanup() {
    log_info "正在清理..."
    # 如果需要，可以在这里添加清理代码
    # 例如：杀死后台进程等
}

# 信号处理
trap cleanup EXIT
trap 'log_info "收到中断信号，正在退出..."; exit 130' INT TERM

# 主函数
main() {
    echo "=================================================="
    log_info "🚀 AI宠物启动脚本开始运行"
    echo "=================================================="
    
    # 1. 检查Ollama是否安装
    if ! check_ollama_installed; then
        exit 1
    fi
    
    # 2. 检查Ollama服务状态
    if check_ollama_status; then
        log_success "✅ Ollama服务已运行"
    else
        log_info "📡 Ollama服务未运行，正在启动..."
        if ! start_ollama; then
            log_error "❌ 无法启动Ollama服务，程序退出"
            exit 1
        fi
    fi
    
    # 3. 确保所需模型可用
    if ! ensure_model "nomic-embed-text"; then
        log_warning "⚠️ 嵌入模型不可用，但继续启动应用程序"
    fi
    
    # 4. 启动AI宠物应用程序
    if start_ai_pet_app; then
        log_success "✅ AI宠物应用程序启动完成"
    else
        log_error "❌ AI宠物应用程序启动失败"
        exit 1
    fi
}

# 检查是否以root权限运行（可选）
if [ "$EUID" -eq 0 ]; then
    log_warning "正在以root权限运行，请确保这是必要的"
fi

# 运行主函数
main "$@"
