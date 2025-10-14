# src/theaia/tests/core/test_context_manager.py

from src.theaia.core.context_manager import ContextManager

def test_create_and_get_context():
    mgr = ContextManager()
    ctx = mgr.create_context("U100", "S101")
    assert mgr.get_context("S101") == ctx

def test_save_and_delete_context():
    mgr = ContextManager()
    ctx = mgr.create_context("U100", "S101")
    mgr.save_context(ctx)
    assert mgr.get_context("S101") == ctx
    assert mgr.delete_context("S101")
    assert mgr.get_context("S101") is None

def test_list_contexts():
    mgr = ContextManager()
    mgr.create_context("U100", "S101")
    mgr.create_context("U101", "S102")
    contexts = mgr.list_contexts()
    assert "S101" in contexts and "S102" in contexts
