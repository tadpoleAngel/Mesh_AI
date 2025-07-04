from agents.alice import Alice
from agents.bob import Bob
from agents.charlie import Charlie
from environment.function_generators.linear_fn import LinearFunction
from environment.function_generators.qudratic_fn import QuadraticFunction
from environment.tick_engine import run_tick
from utils.live_plotter import LivePlotter


def main():
    # Create function (y = 2x + 5 as a simple test)
    # fn = LinearFunction(slope=4, intercept=0.0)
    fn = QuadraticFunction(a=1.0, b=0.0, c=0.0)  # Example quadratic function

    # Instantiate agents
    alice = Alice("alice")
    bob = Bob("bob")
    charlie = Charlie("charlie", max_ticks=51)

    alice.load_simulation_data([
        {"tick": t, "value": fn.get_value(t)} for t in range(100)
    ])

    plotter = LivePlotter()

    for _ in range(25):
        for tick in range(50):
            # print(f"\n--- TICK {tick} ---")
            result = run_tick(tick, alice, bob, charlie)

            result = run_tick(tick, alice, bob, charlie)
            if result.get("done"):
                print("Simulation ended (Alice out of data).")
                break


            # print(f"Actual Value     : {result['actual_value']}")
            # print(f"Charlie Predicted: {result['charlie_prediction']}")
            # print(f"Prediction Error : {result['error']:.4f}")
            # print(f"Reward           : {result['reward']:.4f}")
            # print(f"Knowledge Levels :")
            # print(f"  Alice   → {alice.knowledge_level}")
            # print(f"  Bob     → {bob.knowledge_level}")
            # print(f"  Charlie → {charlie.knowledge_level}")

            plotter.update(
                tick=tick,
                pred=result['charlie_prediction'],
                actual=result['actual_value'],
                error=result['error'],
                knowledge_dict={
                    "Alice": alice.knowledge_level,
                    "Bob": bob.knowledge_level,
                    "Charlie": charlie.knowledge_level
                }
            )

        # print("Starting next round...\n\n")
        alice.load_simulation_data([
        {"tick": t, "value": fn.get_value(t)} for t in range(100)
    ])

if __name__ == "__main__":
    main()
