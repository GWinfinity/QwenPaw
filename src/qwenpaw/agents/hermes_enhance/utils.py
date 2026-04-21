# -*- coding: utf-8 -*-
"""
Utils Compatibility Layer for Hermes
===================================

提供 Hermes 所需的 utils 模块兼容实现
"""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def atomic_json_write(file_path: str | Path, data: Any) -> None:
    """原子写入 JSON 文件
    
    先写入临时文件，然后原子地重命名到目标文件
    这确保文件要么完全写入，要么完全不写入
    """
    file_path = Path(file_path)
    
    # 获取临时目录（优先使用与目标文件相同的目录）
    temp_dir = file_path.parent
    
    # 创建临时文件
    fd, temp_path = tempfile.mkstemp(
        suffix='.tmp',
        prefix='.atomic_write_',
        dir=str(temp_dir),
    )
    
    try:
        # 写入 JSON
        with open(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 原子重命名
        Path(temp_path).replace(file_path)
        
    except Exception as e:
        # 清理临时文件
        try:
            Path(temp_path).unlink()
        except Exception:
            pass
        logger.error(f"atomic_json_write failed: {e}")
        raise


def read_json_safe(file_path: str | Path) -> Any:
    """安全读取 JSON 文件"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        return None


def ensure_dir(file_path: str | Path) -> Path:
    """确保目录存在"""
    path = Path(file_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_read_text(file_path: str | Path, default: str = "") -> str:
    """安全读取文本文件"""
    try:
        return Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        logger.warning(f"Failed to read {file_path}: {e}")
        return default


def safe_write_text(file_path: str | Path, content: str) -> bool:
    """安全写入文本文件"""
    try:
        Path(file_path).write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        logger.error(f"Failed to write {file_path}: {e}")
        return False
