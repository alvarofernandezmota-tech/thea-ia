import re

# Leer archivo
with open('src/theaia/tests/unit/multi_agent/test_agent_coordination.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: test_vote_on_expired_proposal
content = re.sub(
    r'(proposal_id = await engine\.propose\(\s+proposer_id="agent_1",)\s+(timeout_seconds=0\.1)',
    r'\1\n            description="Test expired proposal",\n            \2',
    content
)

# Fix 2: test_get_result
content = re.sub(
    r'(proposal_id = await engine\.propose\(\s+proposer_id="agent_1",)\s+(required_votes=2)',
    r'\1\n            description="Test get result",\n            \2',
    content
)

# Fix 3: test_cleanup_expired_proposals
content = re.sub(
    r'(await engine\.propose\(\s+proposer_id=f"agent_\{i\}",)\s+(timeout_seconds=0\.1)',
    r'\1\n                description=f"Test proposal {i}",\n                \2',
    content
)

# Guardar archivo
with open('src/theaia/tests/unit/multi_agent/test_agent_coordination.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixes aplicados correctamente")
