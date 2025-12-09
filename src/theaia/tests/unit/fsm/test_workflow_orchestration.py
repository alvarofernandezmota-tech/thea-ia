"""
Tests for Workflow Orchestration System
Tests complex multi-step workflows with dependencies and rollback.

Author: Álvaro Fernández Mota
Date: 09 December 2025
"""

import pytest
import asyncio
from src.theaia.core.fsm.workflow_orchestration import (
    Workflow,
    WorkflowStep,
    StepStatus,
    WorkflowStatus
)


class TestWorkflowStep:
    """Test WorkflowStep class"""
    
    def test_create_simple_step(self):
        """Test creating a simple step"""
        async def dummy_action(ctx):
            return "result"
        
        step = WorkflowStep(name="test_step", action=dummy_action)
        
        assert step.name == "test_step"
        assert step.action == dummy_action
        assert step.status == StepStatus.PENDING
        assert step.depends_on == []
        assert step.parallel is False
    
    def test_create_step_with_dependencies(self):
        """Test step with dependencies"""
        async def dummy_action(ctx):
            return "result"
        
        step = WorkflowStep(
            name="dependent_step",
            action=dummy_action,
            depends_on=["step1", "step2"]
        )
        
        assert step.depends_on == ["step1", "step2"]
    
    def test_create_step_with_rollback(self):
        """Test step with rollback action"""
        async def action(ctx):
            return "result"
        
        async def rollback(ctx, result):
            pass
        
        step = WorkflowStep(
            name="step",
            action=action,
            rollback_action=rollback
        )
        
        assert step.rollback_action == rollback
    
    def test_step_equality(self):
        """Test step equality based on name"""
        async def action(ctx):
            return "result"
        
        step1 = WorkflowStep(name="same_name", action=action)
        step2 = WorkflowStep(name="same_name", action=action)
        step3 = WorkflowStep(name="different", action=action)
        
        assert step1 == step2
        assert step1 != step3
    
    def test_step_hashable(self):
        """Test that steps can be used in sets"""
        async def action(ctx):
            return "result"
        
        step1 = WorkflowStep(name="step1", action=action)
        step2 = WorkflowStep(name="step2", action=action)
        
        step_set = {step1, step2}
        
        assert len(step_set) == 2
        assert step1 in step_set


class TestWorkflow:
    """Test Workflow class"""
    
    def test_create_workflow(self):
        """Test creating a workflow"""
        workflow = Workflow("test_workflow")
        
        assert workflow.name == "test_workflow"
        assert workflow.status == WorkflowStatus.PENDING
        assert len(workflow.steps) == 0
        assert workflow.auto_rollback is True
    
    def test_create_workflow_no_auto_rollback(self):
        """Test workflow without auto-rollback"""
        workflow = Workflow("test", auto_rollback=False)
        
        assert workflow.auto_rollback is False
    
    def test_add_simple_step(self):
        """Test adding a simple step"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        
        assert "step1" in workflow.steps
        assert workflow.steps["step1"].name == "step1"
    
    def test_add_step_with_metadata(self):
        """Test adding step with metadata"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action, timeout=30, retry=3)
        
        assert workflow.steps["step1"].metadata["timeout"] == 30
        assert workflow.steps["step1"].metadata["retry"] == 3
    
    def test_add_duplicate_step_raises_error(self):
        """Test that adding duplicate step raises error"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        
        with pytest.raises(ValueError, match="already exists"):
            workflow.add_step("step1", action)
    
    def test_add_step_with_missing_dependency_raises_error(self):
        """Test that missing dependency raises error"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        with pytest.raises(ValueError, match="Dependency.*not found"):
            workflow.add_step("step1", action, depends_on=["nonexistent"])
    
    def test_add_step_with_valid_dependency(self):
        """Test adding step with valid dependency"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        workflow.add_step("step2", action, depends_on=["step1"])
        
        assert workflow.steps["step2"].depends_on == ["step1"]
    
    @pytest.mark.asyncio
    async def test_execute_single_step(self):
        """Test executing workflow with single step"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "success"
        
        workflow.add_step("step1", action)
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert result["results"]["step1"] == "success"
        assert "step1" in result["completed_steps"]
        assert result["failed_step"] is None
    
    @pytest.mark.asyncio
    async def test_execute_multiple_steps_sequential(self):
        """Test executing multiple steps sequentially"""
        workflow = Workflow("test")
        
        async def step1_action(ctx):
            ctx["step1_done"] = True
            return "step1_result"
        
        async def step2_action(ctx):
            assert ctx["step1_done"] is True
            return "step2_result"
        
        workflow.add_step("step1", step1_action)
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert result["results"]["step1"] == "step1_result"
        assert result["results"]["step2"] == "step2_result"
        assert result["completed_steps"] == ["step1", "step2"]
    
    @pytest.mark.asyncio
    async def test_execute_with_initial_context(self):
        """Test executing with initial context"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return ctx.get("initial_value", 0) * 2
        
        workflow.add_step("step1", action)
        
        result = await workflow.execute({"initial_value": 5})
        
        assert result["results"]["step1"] == 10
    
    @pytest.mark.asyncio
    async def test_execute_with_failure(self):
        """Test workflow failure handling"""
        workflow = Workflow("test")
        
        async def failing_action(ctx):
            raise ValueError("Test error")
        
        workflow.add_step("failing_step", failing_action)
        
        result = await workflow.execute()
        
        assert result["status"] == "failed"
        assert result["failed_step"] == "failing_step"
        assert "Test error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_rollback_on_failure(self):
        """Test automatic rollback on failure"""
        workflow = Workflow("test")
        rollback_called = []
        
        async def step1_action(ctx):
            return "step1_result"
        
        async def step1_rollback(ctx, result):
            rollback_called.append("step1")
        
        async def step2_action(ctx):
            raise ValueError("Step 2 failed")
        
        workflow.add_step("step1", step1_action, rollback_action=step1_rollback)
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["status"] == "failed"
        assert "step1" in rollback_called
        assert workflow.steps["step1"].status == StepStatus.ROLLED_BACK
    
    @pytest.mark.asyncio
    async def test_no_rollback_when_disabled(self):
        """Test no rollback when auto_rollback=False"""
        workflow = Workflow("test", auto_rollback=False)
        rollback_called = []
        
        async def step1_action(ctx):
            return "step1_result"
        
        async def step1_rollback(ctx, result):
            rollback_called.append("step1")
        
        async def step2_action(ctx):
            raise ValueError("Step 2 failed")
        
        workflow.add_step("step1", step1_action, rollback_action=step1_rollback)
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["status"] == "failed"
        assert len(rollback_called) == 0
        assert workflow.steps["step1"].status == StepStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_parallel_execution(self):
        """Test parallel step execution"""
        workflow = Workflow("test")
        execution_times = []
        
        async def step1_action(ctx):
            execution_times.append(("step1", asyncio.get_event_loop().time()))
            await asyncio.sleep(0.01)
            return "step1"
        
        async def step2_action(ctx):
            execution_times.append(("step2", asyncio.get_event_loop().time()))
            await asyncio.sleep(0.01)
            return "step2"
        
        workflow.add_step("step1", step1_action, parallel=True)
        workflow.add_step("step2", step2_action, parallel=True)
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert len(execution_times) == 2
        # Check they started roughly at the same time (within 50ms)
        time_diff = abs(execution_times[0][1] - execution_times[1][1])
        assert time_diff < 0.05
    
    @pytest.mark.asyncio
    async def test_pre_condition_success(self):
        """Test step with successful pre-condition"""
        workflow = Workflow("test")
        
        def pre_check(ctx):
            return ctx.get("allow_execution", False)
        
        async def action(ctx):
            return "executed"
        
        workflow.add_step("step1", action, pre_condition=pre_check)
        
        result = await workflow.execute({"allow_execution": True})
        
        assert result["status"] == "completed"
        assert result["results"]["step1"] == "executed"
    
    @pytest.mark.asyncio
    async def test_pre_condition_failure_skips_step(self):
        """Test step with failed pre-condition gets skipped"""
        workflow = Workflow("test")
        
        def pre_check(ctx):
            return False
        
        async def action(ctx):
            return "executed"
        
        workflow.add_step("step1", action, pre_condition=pre_check)
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert workflow.steps["step1"].status == StepStatus.SKIPPED
        assert result["results"]["step1"] is None
    
    @pytest.mark.asyncio
    async def test_post_condition_success(self):
        """Test step with successful post-condition"""
        workflow = Workflow("test")
        
        def post_check(ctx, result):
            return result == "expected"
        
        async def action(ctx):
            return "expected"
        
        workflow.add_step("step1", action, post_condition=post_check)
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert result["results"]["step1"] == "expected"
    
    @pytest.mark.asyncio
    async def test_post_condition_failure_fails_workflow(self):
        """Test step with failed post-condition fails workflow"""
        workflow = Workflow("test")
        
        def post_check(ctx, result):
            return result == "expected"
        
        async def action(ctx):
            return "unexpected"
        
        workflow.add_step("step1", action, post_condition=post_check)
        
        result = await workflow.execute()
        
        assert result["status"] == "failed"
        assert "Post-condition failed" in result["error"]
    
    @pytest.mark.asyncio
    async def test_context_sharing_between_steps(self):
        """Test context is shared between steps"""
        workflow = Workflow("test")
        
        async def step1_action(ctx):
            ctx["shared_value"] = 42
            return "step1"
        
        async def step2_action(ctx):
            return ctx.get("shared_value", 0) * 2
        
        workflow.add_step("step1", step1_action)
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["results"]["step2"] == 84
    
    @pytest.mark.asyncio
    async def test_step_results_stored_in_context(self):
        """Test step results are stored in context"""
        workflow = Workflow("test")
        
        async def step1_action(ctx):
            return "step1_result"
        
        async def step2_action(ctx):
            return ctx["step1_result"]
        
        workflow.add_step("step1", step1_action)
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["results"]["step2"] == "step1_result"
    
    @pytest.mark.asyncio
    async def test_complex_dependency_graph(self):
        """Test complex dependency resolution"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return ctx.get("step_name", "unknown")
        
        # Create diamond dependency:
        # step1 -> step2, step3 -> step4
        workflow.add_step("step1", action)
        workflow.add_step("step2", action, depends_on=["step1"])
        workflow.add_step("step3", action, depends_on=["step1"])
        workflow.add_step("step4", action, depends_on=["step2", "step3"])
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert len(result["completed_steps"]) == 4
        
        # Verify execution order (step1 first, step4 last)
        assert result["completed_steps"][0] == "step1"
        assert result["completed_steps"][-1] == "step4"
    
    @pytest.mark.asyncio
    async def test_circular_dependency_raises_error(self):
        """Test circular dependency detection"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        workflow.add_step("step2", action, depends_on=["step1"])
        
        # Manually create circular dependency
        workflow.steps["step1"].depends_on = ["step2"]
        
        result = await workflow.execute()
        
        # Verify the workflow failed with circular dependency error
        assert result["status"] == "failed"
        assert "Circular dependency" in result["error"]
    
    def test_get_status(self):
        """Test getting workflow status"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        workflow.add_step("step2", action, depends_on=["step1"])
        
        status = workflow.get_status()
        
        assert status["name"] == "test"
        assert status["status"] == "pending"
        assert status["total_steps"] == 2
        assert status["completed_steps"] == 0
        assert "step1" in status["steps"]
        assert "step2" in status["steps"]
    
    @pytest.mark.asyncio
    async def test_get_status_after_execution(self):
        """Test status after workflow execution"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        
        await workflow.execute()
        
        status = workflow.get_status()
        
        assert status["status"] == "completed"
        assert status["completed_steps"] == 1
        assert status["steps"]["step1"]["status"] == "completed"
    
    def test_reset_workflow(self):
        """Test resetting workflow to initial state"""
        workflow = Workflow("test")
        
        async def action(ctx):
            return "result"
        
        workflow.add_step("step1", action)
        workflow.status = WorkflowStatus.COMPLETED
        workflow.completed_steps.append("step1")
        workflow.steps["step1"].status = StepStatus.COMPLETED
        
        workflow.reset()
        
        assert workflow.status == WorkflowStatus.PENDING
        assert len(workflow.completed_steps) == 0
        assert workflow.steps["step1"].status == StepStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_rollback_without_rollback_action(self):
        """Test rollback when step has no rollback action"""
        workflow = Workflow("test")
        
        async def step1_action(ctx):
            return "step1_result"
        
        async def step2_action(ctx):
            raise ValueError("Step 2 failed")
        
        workflow.add_step("step1", step1_action)  # No rollback action
        workflow.add_step("step2", step2_action, depends_on=["step1"])
        
        result = await workflow.execute()
        
        assert result["status"] == "failed"
        # Should not crash even without rollback action
        assert workflow.steps["step1"].status == StepStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_multiple_parallel_batches(self):
        """Test multiple batches of parallel execution"""
        workflow = Workflow("test")
        
        async def action(ctx):
            await asyncio.sleep(0.01)
            return "done"
        
        # Batch 1: step1, step2 (parallel)
        workflow.add_step("step1", action)
        workflow.add_step("step2", action)
        
        # Batch 2: step3, step4 (parallel, depend on batch 1)
        workflow.add_step("step3", action, depends_on=["step1", "step2"])
        workflow.add_step("step4", action, depends_on=["step1", "step2"])
        
        result = await workflow.execute()
        
        assert result["status"] == "completed"
        assert len(result["completed_steps"]) == 4
