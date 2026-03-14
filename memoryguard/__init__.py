"""
MemoryGuard - Modular Python Memory Monitoring
=============================================

🔍 Like Lego for your Code - Drop-in memory monitoring for any Python project.

Features:
- Real-time memory tracking
- Automatic leak detection
- Valgrind integration for C extensions
- Live terminal dashboard
- CI/CD ready

Quick Start:
    >>> from memoryguard import MemoryGuard, track_memory
    >>> 
    >>> guard = MemoryGuard()
    >>> 
    >>> @track_memory("my_function", guard)
    >>> def my_function():
    ...     return heavy_computation()

For more info: https://github.com/SHAdd0WTAka/memoryguard
"""

__version__ = "1.0.2"
__author__ = "Security Team"
__license__ = "MIT"

from .core import (
    MemoryGuard,
    MemorySnapshot,
    MemoryAlert,
    ValgrindWrapper,
    track_memory,
    memory_context,
    get_memory_guard,
)

from .integration import (
    MemoryInstrumentedTool,
    MemoryAwareOrchestrator,
    memory_efficient_batch,
    profile_memory,
)

# Optional dashboard (requires rich)
try:
    from .dashboard import MemoryDashboard, MemoryDashboardAPI
    __all__ = [
        "MemoryGuard",
        "MemorySnapshot", 
        "MemoryAlert",
        "ValgrindWrapper",
        "track_memory",
        "memory_context",
        "get_memory_guard",
        "MemoryInstrumentedTool",
        "MemoryAwareOrchestrator",
        "memory_efficient_batch",
        "profile_memory",
        "MemoryDashboard",
        "MemoryDashboardAPI",
    ]
except ImportError:
    # Rich not installed, dashboard not available
    __all__ = [
        "MemoryGuard",
        "MemorySnapshot",
        "MemoryAlert", 
        "ValgrindWrapper",
        "track_memory",
        "memory_context",
        "get_memory_guard",
        "MemoryInstrumentedTool",
        "MemoryAwareOrchestrator",
        "memory_efficient_batch",
        "profile_memory",
    ]
