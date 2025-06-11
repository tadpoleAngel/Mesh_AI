import random
from environment.function_generators.switcher import get_function_generator
from environment.tick_engine import TickEngine
from agents.alice import Alice
from agents.bob import Bob
from agents.charlie import Charlie
from engine.reward_system import compute_reward
from engine.intelligence_editor import apply_knowledge_changes

# TEMP: configurable values for development
total_ticks = 100
function_type = "linear"

# === Initialize Components === #
function_generator = get_function_generator(function_type)
tick_engine = TickEngine(function_generator)

alice = Alice("Alice")
bob = Bob("Bob")
charlie = Charlie("Charlie")

agents = {"Alice": alice, "Bob": bob, "Charlie": charlie}

# Logging structures (for later analysis)
prediction_log = []
reward_log = []
message_log = []

# === Main Loop === #
for tick in range(total_ticks):
    print(f"\n--- Tick {tick} ---")

    # --- Step 1: Advance the environment --- #
    current_value = tick_engine.advance()

    # --- Step 2: Alice observes the data --- #
    alice_observation = alice.observe(current_value)
    alice_message = alice.generate_message()

    # --- Step 3: Bob receives Alice's message --- #
    bob.receive_message(alice_message)
    bob_message = bob.generate_message()

    # --- Step 4: Charlie receives Bob's message --- #
    charlie.receive_message(bob_message)
    prediction = charlie.predict_next()

    # --- Step 5: Compute reward --- #
    true_next = tick_engine.peek_next()
    reward = compute_reward(prediction, true_next)
    reward_log.append(reward)

    # --- Step 6: Logging predictions --- #
    prediction_log.append({
        "tick": tick,
        "prediction": prediction,
        "true_value": true_next,
        "reward": reward
    })

    # --- Step 7: Agents send optional messages --- #
    outbound_messages = {}
    for agent_name, agent in agents.items():
        outbound_messages[agent_name] = agent.generate_outbound_messages()

    for sender, messages in outbound_messages.items():
        for recipient, message in messages:
            if recipient in agents:
                agents[recipient].receive_message(message)
                message_log.append({"from": sender, "to": recipient, "content": message})

    # --- Step 8: Intelligence editing --- #
    knowledge_deltas = {}
    for sender_name, sender in agents.items():
        knowledge_deltas[sender_name] = sender.propose_knowledge_changes()

    apply_knowledge_changes(agents, knowledge_deltas)

# === Post-run Summary === #
print("\n--- Experiment Complete ---")
print(f"Final average reward: {sum(reward_log)/len(reward_log):.4f}")
