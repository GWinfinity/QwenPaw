# -*- coding: utf-8 -*-
"""
Auxiliary LLM Client for Hermes Enhancement
==========================================

简化版的 LLM 调用客户端，用于上下文压缩等辅助任务

This is a simplified version compatible with QwenPaw
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


async def call_llm(
    prompt: str,
    model: Optional[str] = None,
    system: Optional[str] = None,
    timeout: int = 60,
    max_tokens: int = 4096,
    temperature: float = 0.3,
    **kwargs,
) -> str:
    """调用 LLM 生成文本
    
    简化实现，尝试使用 QwenPaw 的模型工厂
    
    Args:
        prompt: 用户提示
        model: 模型名称
        system: 系统提示
        timeout: 超时秒数
        max_tokens: 最大生成 token 数
        temperature: 温度参数
        **kwargs: 其他参数
        
    Returns:
        str: 生成的文本
    """
    try:
        # 尝试使用 QwenPaw 的模型
        from qwenpaw.agents.model_factory import create_model_and_formatter
        from agentscope.message import Msg
        
        # 确定模型
        model_name = model or os.environ.get("HERMES_MODEL", "gpt-4o-mini")
        
        # 创建模型
        model_instance, formatter = create_model_and_formatter(
            model_name=model_name,
            **kwargs,
        )
        
        # 构建消息
        messages = []
        if system:
            messages.append(Msg(name="system", role="system", content=system))
        messages.append(Msg(name="user", role="user", content=prompt))
        
        # 调用模型
        response = await model_instance(messages, stream=False)
        
        # 提取文本
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)
            
    except ImportError as e:
        logger.warning(f"QwenPaw model not available: {e}")
        return f"[LLM call placeholder - QwenPaw model not configured: {e}]"
        
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return f"[LLM call failed: {str(e)}]"


async def call_llm_with_messages(
    messages: List[Any],
    model: Optional[str] = None,
    timeout: int = 60,
    max_tokens: int = 4096,
    temperature: float = 0.3,
    **kwargs,
) -> str:
    """使用消息列表调用 LLM
    
    Args:
        messages: 消息列表
        model: 模型名称
        timeout: 超时秒数
        max_tokens: 最大生成 token 数
        temperature: 温度参数
        **kwargs: 其他参数
        
    Returns:
        str: 生成的文本
    """
    try:
        from qwenpaw.agents.model_factory import create_model_and_formatter
        
        # 确定模型
        model_name = model or os.environ.get("HERMES_MODEL", "gpt-4o-mini")
        
        # 创建模型
        model_instance, formatter = create_model_and_formatter(
            model_name=model_name,
            **kwargs,
        )
        
        # 调用模型
        response = await model_instance(messages, stream=False)
        
        # 提取文本
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)
            
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return f"[LLM call failed: {str(e)}]"
