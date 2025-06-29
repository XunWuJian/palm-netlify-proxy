#!/usr/bin/env python3
"""
AI宠物启动脚本 - 自动检查并启动Ollama服务
"""

import subprocess
import time
import requests
import logging
import sys
import os
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_pet_startup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('ai_pet_startup')

class OllamaManager:
    """Ollama服务管理器"""
    
    def __init__(self, host="localhost", port=11434):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        
    def check_ollama_status(self):
        """检查Ollama服务状态"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def start_ollama_service(self):
        """启动Ollama服务"""
        try:
            logger.info("🚀 正在启动Ollama服务...")
            
            # 检查ollama命令是否存在
            result = subprocess.run(["which", "ollama"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("❌ 未找到ollama命令，请确保Ollama已正确安装")
                return False
            
            # 启动ollama serve（后台运行）
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # 创建新的进程组
            )
            
            logger.info(f"📡 Ollama服务进程已启动 (PID: {process.pid})")
            
            # 等待服务启动
            max_wait_time = 30  # 最多等待30秒
            for i in range(max_wait_time):
                if self.check_ollama_status():
                    logger.info("✅ Ollama服务启动成功")
                    return True
                
                logger.info(f"⏳ 等待Ollama服务启动... ({i+1}/{max_wait_time})")
                time.sleep(1)
            
            logger.error("❌ Ollama服务启动超时")
            return False
            
        except Exception as e:
            logger.error(f"❌ 启动Ollama服务失败: {e}")
            return False
    
    def ensure_model_available(self, model_name="nomic-embed-text"):
        """确保所需的模型可用"""
        try:
            logger.info(f"🔍 检查模型 {model_name} 是否可用...")
            
            # 检查模型是否已下载
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if model_name in result.stdout:
                logger.info(f"✅ 模型 {model_name} 已可用")
                return True
            
            logger.info(f"📥 正在下载模型 {model_name}...")
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                logger.info(f"✅ 模型 {model_name} 下载成功")
                return True
            else:
                logger.error(f"❌ 模型 {model_name} 下载失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ 下载模型 {model_name} 超时")
            return False
        except Exception as e:
            logger.error(f"❌ 检查/下载模型失败: {e}")
            return False

def check_system_requirements():
    """检查系统要求"""
    logger.info("🔍 检查系统要求...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error("❌ 需要Python 3.8或更高版本")
        return False
    
    logger.info(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的包
    required_packages = ['requests', 'mem0ai']  # 根据你的实际需求调整
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ 包 {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"⚠️ 包 {package} 未安装")
    
    if missing_packages:
        logger.error(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        logger.info("请运行: pip install " + " ".join(missing_packages))
        return False
    
    return True

def start_ai_pet_application():
    """启动AI宠物应用程序"""
    logger.info("🐾 正在启动AI宠物应用程序...")
    
    # 这里替换为你的实际AI宠物启动代码
    # 例如：
    # from your_ai_pet_module import main as ai_pet_main
    # ai_pet_main()
    
    # 临时示例代码 - 请替换为你的实际代码
    try:
        # 假设你的AI宠物主程序在 ai_pet_main.py 中
        if os.path.exists("ai_pet_main.py"):
            logger.info("📂 找到AI宠物主程序文件")
            subprocess.run([sys.executable, "ai_pet_main.py"], check=True)
        else:
            logger.warning("⚠️ 未找到AI宠物主程序文件，请手动指定")
            logger.info("请在此处添加你的AI宠物启动代码")
            
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ AI宠物应用程序启动失败: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ 启动AI宠物应用程序时发生错误: {e}")
        raise

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("🚀 AI宠物启动脚本开始运行")
    logger.info("=" * 50)
    
    try:
        # 1. 检查系统要求
        if not check_system_requirements():
            logger.error("❌ 系统要求检查失败，程序退出")
            sys.exit(1)
        
        # 2. 初始化Ollama管理器
        ollama_manager = OllamaManager()
        
        # 3. 检查Ollama服务状态
        if ollama_manager.check_ollama_status():
            logger.info("✅ Ollama服务已运行")
        else:
            logger.info("📡 Ollama服务未运行，正在启动...")
            if not ollama_manager.start_ollama_service():
                logger.error("❌ 无法启动Ollama服务，程序退出")
                sys.exit(1)
        
        # 4. 确保所需模型可用
        if not ollama_manager.ensure_model_available("nomic-embed-text"):
            logger.warning("⚠️ 嵌入模型不可用，但继续启动应用程序")
        
        # 5. 启动AI宠物应用程序
        start_ai_pet_application()
        
        logger.info("✅ AI宠物应用程序启动完成")
        
    except KeyboardInterrupt:
        logger.info("⏹️ 用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ 程序运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
