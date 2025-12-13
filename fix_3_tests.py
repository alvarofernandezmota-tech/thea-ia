import re

file_path = "src/theaia/tests/unit/multi_agent/test_agent_coordination.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Línea 139 (test_vote_on_expired_proposal)
content = content.replace(
    '''proposal_id = await engine.propose(
            proposer_id="agent_1",
            timeout_seconds=0.1
        )''',
    '''proposal_id = await engine.propose(
            proposer_id="agent_1",
            description="Test expired proposal",
            timeout_seconds=0.1
        )'''
)

# Fix 2: Línea 156 (test_get_result)
content = content.replace(
    '''proposal_id = await engine.propose(
            proposer_id="agent_1",
            required_votes=1
        )''',
    '''proposal_id = await engine.propose(
            proposer_id="agent_1",
            description="Test get result",
            required_votes=1
        )'''
)

# Fix 3: Línea 175 (test_cleanup_expired_proposals)
content = content.replace(
    '''await engine.propose(
                proposer_id=f"agent_{i}",
                timeout_seconds=0.1
            )''',
    '''await engine.propose(
                proposer_id=f"agent_{i}",
                description=f"Test proposal {i}",
                timeout_seconds=0.1
            )'''
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed 3 tests successfully!")
print("  - test_vote_on_expired_proposal (line 139)")
print("  - test_get_result (line 156)")
print("  - test_cleanup_expired_proposals (line 175)")
