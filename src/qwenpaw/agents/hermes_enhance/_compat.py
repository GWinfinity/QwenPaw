# -*- coding: utf-8 -*-
"""
Hermes Compatibility Layer for QwenPaw
======================================

Provides compatibility for Hermes modules to run in QwenPaw environment
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# Simulate hermes_constants
# ============================================================================

class _HermesConstants:
    """Simulate hermes_constants module"""
    
    @staticmethod
    def get_hermes_home() -> str:
        """Get Hermes home directory"""
        home = os.environ.get("HERMES_HOME")
        if home:
            return home
        default_paths = [
            Path.home() / ".hermes",
            Path.cwd() / ".hermes",
            Path(__file__).parent.parent.parent / ".hermes",
        ]
        for p in default_paths:
            if p.exists():
                return str(p)
        hermes_dir = Path.cwd() / ".hermes"
        hermes_dir.mkdir(exist_ok=True)
        return str(hermes_dir)
    
    @staticmethod
    def get_skills_dir() -> str:
        """Get skills directory"""
        home = _HermesConstants.get_hermes_home()
        skills_dir = Path(home) / "skills"
        skills_dir.mkdir(exist_ok=True)
        return str(skills_dir)
    
    @staticmethod
    def is_wsl() -> bool:
        """Check if running in WSL"""
        try:
            return sys.platform == "linux" and "microsoft" in Path("/proc/version").read_text().lower()
        except Exception:
            return False
    
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
    DEFAULT_TIMEOUT = 60
    MAX_RETRIES = 3


# ============================================================================
# Simulate tools.registry
# ============================================================================

def tool_error(tool_name: str, error: Exception) -> str:
    """Format tool error message"""
    return f"Tool '{tool_name}' failed: {str(error)}"


# ============================================================================
# Setup function
# ============================================================================

def setup_compat():
    """Setup compatibility layer"""
    if "hermes_constants" not in sys.modules:
        hermes_constants = ModuleType("hermes_constants")
        hermes_constants.get_hermes_home = _HermesConstants.get_hermes_home
        hermes_constants.get_skills_dir = _HermesConstants.get_skills_dir
        hermes_constants.is_wsl = _HermesConstants.is_wsl
        hermes_constants.OPENROUTER_BASE_URL = _HermesConstants.OPENROUTER_BASE_URL
        hermes_constants.OPENROUTER_MODELS_URL = _HermesConstants.OPENROUTER_MODELS_URL
        sys.modules["hermes_constants"] = hermes_constants
        logger.debug("Registered: hermes_constants")


def get_hermes_home() -> str:
    """Get Hermes home directory"""
    return _HermesConstants.get_hermes_home()


def get_skills_dir() -> str:
    """Get skills directory"""
    return _HermesConstants.get_skills_dir()
