"""
Test Suite for MemoryGuard
==========================

Tests for memory monitoring, leak detection, and integration.
"""

import pytest
import time
import gc
import sys
import os
from pathlib import Path

# Ensure we test the local package
sys.path.insert(0, str(Path(__file__).parent.parent))

from memoryguard import (
    MemoryGuard,
    MemorySnapshot,
    MemoryAlert,
    ValgrindWrapper,
    track_memory,
    memory_context,
    get_memory_guard,
    MemoryInstrumentedTool,
    MemoryAwareOrchestrator,
    memory_efficient_batch,
    profile_memory,
)


class TestMemoryGuard:
    """Tests for MemoryGuard class"""
    
    def test_initialization(self):
        """Test MemoryGuard initialization"""
        guard = MemoryGuard(threshold_mb=100, critical_threshold_mb=200)
        
        assert guard.threshold_mb == 100
        assert guard.critical_threshold_mb == 200
        assert guard._monitoring is False
        assert len(guard._snapshots) == 0
        
    def test_memory_check_normal(self):
        """Test memory check under normal conditions"""
        guard = MemoryGuard(threshold_mb=10000)  # Very high threshold
        
        alert = guard.check_memory("test")
        
        # Should not trigger with normal memory usage
        assert alert is None
        
    def test_memory_snapshot_creation(self):
        """Test memory snapshot creation"""
        guard = MemoryGuard(enable_snapshots=True)
        
        guard.check_memory("test_snapshot")
        
        assert len(guard._snapshots) == 1
        snapshot = guard._snapshots[0]
        
        assert snapshot.context == "test_snapshot"
        assert snapshot.current_mb > 0
        assert snapshot.timestamp > 0
        
    def test_baseline_reset(self):
        """Test baseline reset for leak detection"""
        guard = MemoryGuard()
        
        original_baseline = guard._baseline
        guard.reset_baseline()
        
        # Baseline should be different object
        assert guard._baseline is not original_baseline
        
    def test_force_gc(self):
        """Test garbage collection forcing"""
        guard = MemoryGuard()
        
        result = guard.force_gc()
        
        assert 'objects_collected' in result
        assert 'memory_freed_mb' in result
        assert 'gc_generations' in result
        
    def test_generate_report(self, tmp_path):
        """Test report generation"""
        guard = MemoryGuard()
        guard.check_memory("test1")
        guard.check_memory("test2")
        
        report_file = tmp_path / "test_report.json"
        path = guard.generate_report(str(report_file))
        
        assert Path(path).exists()
        
        # Verify report content
        import json
        with open(path) as f:
            report = json.load(f)
        
        assert 'generated_at' in report
        assert 'summary' in report
        assert report['summary']['total_snapshots'] == 2
        
    def test_callback_registration(self):
        """Test alert callback registration"""
        guard = MemoryGuard(threshold_mb=1)
        
        callbacks_triggered = []
        
        def test_callback(alert):
            callbacks_triggered.append(alert)
        
        guard.register_callback(test_callback)
        
        # Create memory pressure to trigger alert
        data = ["x" * 1000 for _ in range(100000)]
        guard.check_memory("callback_test")
        del data
        
        assert len(callbacks_triggered) > 0 or len(guard._alerts) > 0


class TestMemoryIntegration:
    """Tests for memory integration with tools"""
    
    def test_instrumented_tool(self):
        """Test MemoryInstrumentedTool base class"""
        
        class TestTool(MemoryInstrumentedTool):
            tool_name = "test_tool"
            
            def run(self):
                with self.memory_context("test_run"):
                    return "success"
        
        tool = TestTool()
        result = tool.run()
        
        assert result == "success"
        assert tool.tool_name == "test_tool"
        
    def test_orchestrator_creation(self):
        """Test MemoryAwareOrchestrator"""
        orchestrator = MemoryAwareOrchestrator(max_memory_mb=1000)
        
        assert orchestrator.max_memory_mb == 1000
        assert orchestrator.memory_guard.threshold_mb == 600  # 60% of 1000
        
    def test_orchestrator_register_tool(self):
        """Test tool registration with orchestrator"""
        orchestrator = MemoryAwareOrchestrator()
        
        class TestTool(MemoryInstrumentedTool):
            tool_name = "test"
            
        tool = TestTool()
        orchestrator.register_tool(tool)
        
        assert "test" in orchestrator.tools
        assert tool.memory_guard == orchestrator.memory_guard
        
    @pytest.mark.asyncio
    async def test_memory_efficient_batch(self):
        """Test batch processing with memory control"""
        import asyncio
        
        items = list(range(100))
        
        async def process_batch(batch):
            await asyncio.sleep(0.001)  # Simulate work
            return [x * 2 for x in batch]
        
        results = await memory_efficient_batch(
            items, process_batch, batch_size=10
        )
        
        assert len(results) == 100
        assert results[0] == 0
        assert results[50] == 100


class TestMemoryDecorators:
    """Tests for memory tracking decorators"""
    
    def test_track_memory_decorator(self):
        """Test @track_memory decorator"""
        guard = MemoryGuard()
        
        @track_memory("test_func", guard)
        def test_function():
            return ["x" * 1000 for _ in range(100)]
        
        result = test_function()
        
        assert len(result) == 100
        
    def test_memory_context_manager(self):
        """Test memory_context context manager"""
        guard = MemoryGuard()
        
        with memory_context("test_context", guard):
            data = ["x" * 1000 for _ in range(100)]
        
        # Should have recorded snapshot
        contexts = [s.context for s in guard._snapshots]
        assert any("test_context" in c for c in contexts)


class TestValgrindWrapper:
    """Tests for Valgrind integration"""
    
    def test_valgrind_availability(self):
        """Test Valgrind availability detection"""
        wrapper = ValgrindWrapper()
        
        # Should not error even if valgrind not available
        assert isinstance(wrapper.available, bool)
        
    def test_valgrind_check_without_valgrind(self):
        """Test valgrind check when not available"""
        wrapper = ValgrindWrapper()
        
        if not wrapper.available:
            result = wrapper.check_python_module("test")
            assert 'error' in result


class TestMemoryEdgeCases:
    """Edge case tests"""
    
    def test_monitoring_start_stop(self):
        """Test monitoring lifecycle"""
        guard = MemoryGuard(check_interval=1)
        
        guard.start_monitoring()
        assert guard._monitoring is True
        assert guard._monitor_thread is not None
        
        time.sleep(0.1)  # Let it start
        
        guard.stop_monitoring()
        assert guard._monitoring is False
        
    def test_tool_memory_profile_empty(self):
        """Test tool profile with no data"""
        guard = MemoryGuard()
        
        profile = guard.get_tool_memory_profile("nonexistent_tool")
        
        assert 'error' in profile


class TestGetMemoryGuard:
    """Tests for singleton get_memory_guard"""
    
    def test_singleton(self):
        """Test that get_memory_guard returns singleton"""
        guard1 = get_memory_guard(threshold_mb=100)
        guard2 = get_memory_guard(threshold_mb=200)
        
        # Should return same instance
        assert guard1 is guard2
        
    def test_singleton_with_different_params(self):
        """Test singleton ignores subsequent params"""
        # Reset by importing fresh
        import importlib
        import memoryguard
        importlib.reload(memoryguard)
        
        guard1 = memoryguard.get_memory_guard(threshold_mb=100)
        guard2 = memoryguard.get_memory_guard(threshold_mb=500)
        
        assert guard1 is guard2
        assert guard1.threshold_mb == 100  # First call wins


class TestProfileMemory:
    """Tests for profile_memory decorator"""
    
    def test_profile_memory_decorator(self):
        """Test profile_memory decorator"""
        
        @profile_memory("test_tool")
        def test_func():
            return sum(range(1000))
        
        result = test_func()
        assert result == 499500


# Benchmark tests

class TestMemoryBenchmarks:
    """Benchmark tests"""
    
    def test_memory_check_performance(self, benchmark):
        """Benchmark memory check performance"""
        guard = MemoryGuard()
        
        def check():
            return guard.check_memory("benchmark")
        
        result = benchmark(check)
        # Should complete without error
        assert result is None or hasattr(result, 'level')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
