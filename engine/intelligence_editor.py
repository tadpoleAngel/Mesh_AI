class IntelligenceEditor:
    def __init__(self, agents_dict):
        """
        agents_dict: dict of {agent_name: agent_object}
        """
        self.agents = agents_dict

def apply_knowledge_changes(agent_dict, proposed_changes):
    """
    Applies proposed knowledge level changes to each agent.

    Args:
        agent_dict (dict): Mapping of agent names to agent instances.
        proposed_changes (dict): Nested dict of the form:
            {
                "Alice": {"Bob": +3, "Charlie": -2},
                "Bob": {"Alice": +1},
                ...
            }

    Notes:
        - Each agent may propose changes to any other agent, but not to themselves.
        - Each individual change is clamped to ±3 (max influence from one agent).
        - The total change to any target agent is clamped to ±6 (max combined effect).
          This enforces your original design where two agents can each change another
          by ±3, totaling at most ±6.
    """

    # Accumulate total proposed changes per target agent
    total_changes = {name: 0 for name in agent_dict}

    for source, changes in proposed_changes.items():
        for target, delta in changes.items():
            if target not in agent_dict or target == source:
                continue  # Skip self-edits or unknown targets

            # Clamp individual proposal to ±3
            clamped_delta = max(min(delta, 3), -3)

            # Check remaining capacity for this target under ±6 rule
            remaining_capacity = 6 - abs(total_changes[target])
            # Only allow changes within the remaining capacity
            if abs(clamped_delta) > remaining_capacity:
                clamped_delta = remaining_capacity * (1 if clamped_delta > 0 else -1)

            # Apply if there's still effect to give
            if clamped_delta != 0:
                agent_dict[target].knowledge_level += clamped_delta
                total_changes[target] += clamped_delta
