from agents.alice import Alice
from agents.bob import Bob
from agents.charlie import Charlie
from environment.tick_engine import run_tick
from environment.function_generators.linear_fn import LinearFunction

# --- Configuration ---
NUM_TICKS = 20

# Create agents
alice = Alice()
bob = Bob()
charlie = Charlie()

# Create a simple data stream from a known function
fn = LinearFunction(slope=1.5, intercept=2.0)
data_sequence = [
    {"tick": t, "value": fn.get_value(t)} for t in range(NUM_TICKS)
]
alice.load_simulation_data(data_sequence)

# Optional: Store tick history or results
results = []

# Run the simulation loop
tick = 0
while tick < NUM_TICKS:
    tick_result = run_tick(tick, alice, bob, charlie)
    results.append(tick_result)
    tick += 1

# Output final results
print("\nFinal Results Summary:\n")
for r in results:
    print(f"Tick {r['tick']} | Prediction: {r['charlie_prediction']} | Actual: {r['actual_value']} | Error: {r['error']:.4f}")
