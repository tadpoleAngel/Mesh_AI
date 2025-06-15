def compute_reward(true_value, predicted_value):
    """
    Compute reward based on how close the prediction is to the true value.
    Lower error yields higher reward. Reward can be negative.
    """
    error = abs(true_value - predicted_value)
    reward = -error  # Inverse reward: lower error means higher reward
    return reward, error


def compute_summary(true_value, predicted_value):
    """
    Provide a breakdown summary for the agents.
    """
    error = abs(true_value - predicted_value)
    summary = {
        "true_value": true_value,
        "predicted_value": predicted_value,
        "error": error,
        "squared_error": error ** 2,
        "reward": -error
    }
    return summary