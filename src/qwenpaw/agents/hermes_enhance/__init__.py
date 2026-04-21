# -*- coding: utf-8 -*-
"""
Hermes Enhancement for QwenPaw (精简版)
=======================================

仅保留 QwenPaw 原有代码未覆盖的独特功能：
- ContextCompressor: 丰富的上下文压缩策略（Resolved/Pending 问题跟踪、Handoff framing 等）
- usage_pricing: 美元计费功能

Source: https://github.com/NousResearch/hermes-agent
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Try to setup compatibility layer
try:
    from ._compat import setup_compat
    setup_compat()
except Exception as e:
    logger.warning(f"Hermes compat setup failed: {e}")


def setup() -> bool:
    """Setup Hermes compatibility layer

    Call this before importing Hermes modules

    Returns:
        bool: True if successful
    """
    try:
        from ._compat import setup_compat
        setup_compat()
        logger.info("Hermes enhancement setup complete")
        return True
    except Exception as e:
        logger.error(f"Failed to setup Hermes enhancement: {e}")
        return False


# Import key classes/functions
try:
    from .context_compressor import ContextCompressor
except ImportError as e:
    logger.warning(f"Could not import ContextCompressor: {e}")
    ContextCompressor = None

try:
    from .usage_pricing import CostResult, CanonicalUsage
except ImportError as e:
    logger.warning(f"Could not import usage_pricing: {e}")
    CostResult = None
    CanonicalUsage = None

try:
    from .model_metadata import get_model_context_length
except ImportError as e:
    logger.warning(f"Could not import model_metadata: {e}")
    get_model_context_length = None


__all__ = [
    # Setup
    "setup",
    # Context Compressor
    "ContextCompressor",
    # Pricing
    "CostResult",
    "CanonicalUsage",
    # Model
    "get_model_context_length",
]
