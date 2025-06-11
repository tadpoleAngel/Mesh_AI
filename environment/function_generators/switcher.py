from environment.function_generators.linear_fn import LinearFunction
# Future imports: e.g., from .sinusoidal_fn import SinusoidalFunction


def get_function_generator(name: str):
    """
    Returns a function generator instance based on the specified name.
    """
    name = name.lower()

    if name == "linear":
        return LinearFunction()

    # Future additions can go here:
    # elif name == "sinusoidal":
    #     return SinusoidalFunction()

    raise ValueError(f"Unknown function type: {name}")