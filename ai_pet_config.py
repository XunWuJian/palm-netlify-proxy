"""
AI宠物配置文件
请根据你的实际环境修改以下配置
"""

# Ollama配置
OLLAMA_CONFIG = {
    "host": "localhost",
    "port": 11434,
    "base_url": "http://localhost:11434",
    "timeout": 30,  # 启动超时时间（秒）
    "required_models": [
        "nomic-embed-text",  # 嵌入模型
        # 如果需要其他模型，请在这里添加
        # "llama2",
        # "codellama",
    ]
}

# AI宠物应用程序配置
AI_PET_CONFIG = {
    # 主程序文件路径（相对于启动脚本的位置）
    "main_script": "ai_pet_main.py",
    
    # 备选主程序文件
    "fallback_scripts": [
        "main.py",
        "app.py",
        "run.py"
    ],
    
    # Python解释器路径
    "python_executable": "python3",
    
    # 虚拟环境路径（如果使用虚拟环境）
    "venv_path": None,  # 例如: "venv/bin/activate"
    
    # 启动参数
    "startup_args": [],
    
    # 环境变量
    "env_vars": {
        # 例如：
        # "DEEPSEEK_API_KEY": "your-api-key-here",
        # "OPENAI_API_KEY": "your-openai-key-here",
    }
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "log_file": "ai_pet_startup.log",
    "max_log_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# 系统检查配置
SYSTEM_CHECK_CONFIG = {
    "min_python_version": (3, 8),
    "required_packages": [
        "requests",
        "mem0ai",
        # 根据你的实际需求添加其他包
    ],
    "check_disk_space": True,
    "min_disk_space_mb": 1000,  # 最小磁盘空间要求（MB）
}

# 启动选项
STARTUP_OPTIONS = {
    "auto_download_models": True,  # 自动下载缺失的模型
    "wait_for_ollama": True,      # 等待Ollama服务启动
    "check_system_requirements": True,  # 检查系统要求
    "create_backup": False,       # 启动前创建备份
    "cleanup_on_exit": True,      # 退出时清理临时文件
}

# 错误处理配置
ERROR_HANDLING = {
    "max_retries": 3,            # 最大重试次数
    "retry_delay": 5,            # 重试延迟（秒）
    "auto_restart_on_failure": False,  # 失败时自动重启
    "send_error_notifications": False,  # 发送错误通知
}

# 监控配置
MONITORING_CONFIG = {
    "enable_health_check": True,  # 启用健康检查
    "health_check_interval": 60,  # 健康检查间隔（秒）
    "monitor_memory_usage": True, # 监控内存使用
    "monitor_cpu_usage": True,    # 监控CPU使用
    "max_memory_usage_mb": 2048,  # 最大内存使用（MB）
    "max_cpu_usage_percent": 80,  # 最大CPU使用率（%）
}

# 开发模式配置
DEV_MODE_CONFIG = {
    "enabled": False,            # 是否启用开发模式
    "debug_logging": True,       # 调试日志
    "auto_reload": False,        # 自动重载
    "test_mode": False,          # 测试模式
}

def get_config():
    """获取完整配置"""
    return {
        "ollama": OLLAMA_CONFIG,
        "ai_pet": AI_PET_CONFIG,
        "logging": LOGGING_CONFIG,
        "system_check": SYSTEM_CHECK_CONFIG,
        "startup": STARTUP_OPTIONS,
        "error_handling": ERROR_HANDLING,
        "monitoring": MONITORING_CONFIG,
        "dev_mode": DEV_MODE_CONFIG,
    }

def validate_config():
    """验证配置"""
    errors = []
    
    # 检查必要的配置项
    if not AI_PET_CONFIG.get("main_script"):
        errors.append("AI_PET_CONFIG.main_script 不能为空")
    
    if not OLLAMA_CONFIG.get("host"):
        errors.append("OLLAMA_CONFIG.host 不能为空")
    
    if not isinstance(OLLAMA_CONFIG.get("port"), int):
        errors.append("OLLAMA_CONFIG.port 必须是整数")
    
    # 检查Python版本格式
    min_version = SYSTEM_CHECK_CONFIG.get("min_python_version")
    if not isinstance(min_version, tuple) or len(min_version) != 2:
        errors.append("SYSTEM_CHECK_CONFIG.min_python_version 必须是包含两个元素的元组")
    
    return errors

if __name__ == "__main__":
    # 验证配置
    config_errors = validate_config()
    if config_errors:
        print("配置验证失败:")
        for error in config_errors:
            print(f"  - {error}")
    else:
        print("配置验证通过")
        
    # 打印当前配置
    import json
    config = get_config()
    print("\n当前配置:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
