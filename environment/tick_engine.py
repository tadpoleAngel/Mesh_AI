from engine.reward_system import compute_reward
from engine.intelligence_editor import apply_knowledge_changes
from agents.alice import Alice
from agents.bob import Bob
from agents.charlie import Charlie

def run_tick(tick, alice: Alice, bob: Bob, charlie: Charlie):
    """
    Executes a single simulation tick:
    1. Alice observes the data and passes it to Bob.
    2. Bob combines, transforms, and passes to Charlie.
    3. Charlie makes a prediction.
    4. Reward is calculated based on prediction error.
    5. Agents exchange messages.
    6. Knowledge edits are proposed and applied.
    """
    # --- Step 1: Alice observes the current tick ---
    raw_data = alice.observe(tick)

    # If no more data, stop processing
    if raw_data is None:
        return {
            "done": True,
            "actual_value": None,
            "charlie_prediction": None,
            "reward": 0.0,
            "error": None,
        }


    # --- Step 2: Bob processes Alice’s data and commentary ---
    bob_input = alice.generate_message()
    bob.receive_message(bob_input)
    bob_processed = bob.observe(bob_input)

    # --- Step 3: Charlie receives processed data and predicts ---
    charlie_input = bob.generate_message()
    charlie.receive_message(charlie_input)

    if bob_processed and "content" in bob_processed and bob_processed["content"]:
        charlie.observe(bob_processed["content"])
    
    prediction = charlie.predict_next()

    # --- Step 4: Compute actual and reward ---
    actual_value = raw_data["value"]
    reward, error = compute_reward(actual_value, prediction)

    # --- Step 5: Messaging phase (up to 2 outbound each) ---
    all_agents = {"alice": alice, "bob": bob, "charlie": charlie}
    for agent in all_agents.values():
        outbound = agent.generate_outbound_messages()
        for recipient_name, message in outbound:
            if recipient_name in all_agents:
                all_agents[recipient_name].receive_message(message)

    # --- Step 6: Knowledge updates ---
    proposed_changes = {
        agent_name: agent.propose_knowledge_changes()
        for agent_name, agent in all_agents.items()
    }
    apply_knowledge_changes(all_agents, proposed_changes)

    return {
        "tick": tick,
        "charlie_prediction": prediction,
        "actual_value": actual_value,
        "error": error,
        "reward": reward
    }
