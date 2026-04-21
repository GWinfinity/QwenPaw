# -*- coding: utf-8 -*-
"""
Hermes Enhancement for QwenPaw
===============================

Complete Hermes Agent modules adapted for QwenPaw

Source: https://github.com/NousResearch/hermes-agent

Quick start:
    from qwenpaw.agents.hermes_enhance import setup
    setup()
    from qwenpaw.agents.hermes_enhance import ContextCompressor
"""

from __future__ import annotations

import logging
import sys

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


def get_hermes_home() -> str:
    """Get Hermes home directory"""
    from ._compat import get_hermes_home
    return get_hermes_home()


def get_skills_dir() -> str:
    """Get skills directory"""
    from ._compat import get_skills_dir
    return get_skills_dir()


# Import key classes/functions
try:
    from .context_compressor import ContextCompressor
except ImportError as e:
    logger.warning(f"Could not import ContextCompressor: {e}")
    ContextCompressor = None

try:
    from .memory_manager import MemoryManager
except ImportError as e:
    logger.warning(f"Could not import MemoryManager: {e}")
    MemoryManager = None

try:
    from .memory_provider import MemoryProvider
except ImportError as e:
    logger.warning(f"Could not import MemoryProvider: {e}")
    MemoryProvider = None

try:
    from .retry_utils import jittered_backoff
except ImportError as e:
    logger.warning(f"Could not import jittered_backoff: {e}")
    jittered_backoff = None

try:
    from .rate_limit_tracker import RateLimitState
except ImportError as e:
    logger.warning(f"Could not import RateLimitState: {e}")
    RateLimitState = None

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

try:
    from .skill_utils import parse_frontmatter
except ImportError as e:
    logger.warning(f"Could not import parse_frontmatter: {e}")
    parse_frontmatter = None


__all__ = [
    # Setup
    "setup",
    "get_hermes_home",
    "get_skills_dir",
    
    # Context Compressor
    "ContextCompressor",
    
    # Memory
    "MemoryProvider",
    "MemoryManager",
    
    # Retry
    "jittered_backoff",
    
    # Rate Limit
    "RateLimitState",
    
    # Pricing
    "CostResult",
    "CanonicalUsage",
    
    # Model
    "get_model_context_length",
    
    # Skills
    "parse_frontmatter",
]
