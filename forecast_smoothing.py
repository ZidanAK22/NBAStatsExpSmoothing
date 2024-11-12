import json
import numpy as np
import matplotlib.pyplot as plt
with open("player_games.json", "r") as f:
    data = json.load(f)

body = data["body"]

points_array = []

for i, player in enumerate(body):
    try:
        points = player["points"]  # ADJUST FEATURE HERE
        points_array.append(int(points))
    except KeyError:
        points_array.append(0)

for i, points in enumerate(points_array):
    print(f"Game {i+1}: Points {points}")


def exponential_smoothing(data, alpha):
    """
    Performs exponential smoothing on a given data series.

    Args:
        data: A list of data points.
        alpha: The smoothing factor (0 <= alpha <= 1).

    Returns:
        A list of smoothed values.
    """

    smoothed_data = [data[0]]
    for i in range(1, len(data)):
        if data[i] != 0:  # Skip 0 values
            smoothed_data.append(alpha * data[i] + (1 - alpha) * smoothed_data[-1])
        else:
            smoothed_data.append(smoothed_data[-1])  # Maintain last value

    return smoothed_data

def mean_squared_error(actual, predicted):
    """
    Calculates the Mean Squared Error between actual and predicted values.

    Args:
        actual: A list of actual values.
        predicted: A list of predicted values.

    Returns:
        The Mean Squared Error.
    """

    return np.mean((np.array(actual) - np.array(predicted))**2)

# Experiment with different alpha values
alpha_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for alpha in alpha_values:
    mse_values = []
    for i in range(10, len(points_array), 10):
        # Extract a 10-game period
        period_data = points_array[i-10:i]
        
        # Apply exponential smoothing
        smoothed_data = exponential_smoothing(period_data, alpha)

        # Calculate MSE for the period
        mse = mean_squared_error(period_data[1:], smoothed_data[1:])  # Skip the first value
        mse_values.append(mse)

    average_mse = np.mean(mse_values)
    print(f"Alpha: {alpha}, Average MSE: {average_mse:.2f}")

alpha = 0.9  # Replace with the best alpha value

# Perform a rolling forecast, predicting each next game based on past games
forecasted_points = [points_array[0]]  # Start with the first actual point
for i in range(1, len(points_array)):
    # Forecast next point based on previous points using exponential smoothing
    next_point = alpha * points_array[i-1] + (1 - alpha) * forecasted_points[-1]
    forecasted_points.append(next_point)

# Plot actual vs. rolling forecasted points
plt.figure(figsize=(10, 6))
plt.plot(points_array, label="Actual Points")
plt.plot(forecasted_points, label="Forecasted Points (Rolling)", linestyle='--')
plt.xlabel("Game")
plt.ylabel("Points")
plt.title(f"Actual vs. Rolling Forecasted Points (Alpha={alpha})")
plt.legend()
plt.show()

# Calculate residuals (errors) between actual points and smoothed/forecasted points
residuals = np.array(points_array) - np.array(forecasted_points)

# Plot the actual points, smoothed/forecasted points, and the residuals
plt.figure(figsize=(12, 6))

# Plot actual points and smoothed points
plt.plot(points_array, label="Actual Points", color="blue")
plt.plot(forecasted_points, label="Smoothed/Forecasted Points", color="orange")

# Plot residuals as a separate line, showing errors
plt.plot(residuals, label="Error (Residuals)", color="red", linestyle="--")

plt.xlabel("Game")
plt.ylabel("Points")
plt.title(f"Actual vs. Smoothed/Forecasted Points with Error (Alpha={alpha})")
plt.legend()
plt.show()
