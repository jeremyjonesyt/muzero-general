import matplotlib.pyplot as plt
import csv
import os

log_path = 'loss_log.csv'

try:
    losses = []
    with open(log_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            losses.append(float(row[0]))

    plt.figure(figsize=(10, 6))
    plt.plot(losses, label='Total Loss')
    plt.title('Agent Learning Curve')
    plt.xlabel('Training Iteration')
    plt.ylabel('Loss Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('learning_curve.png')
    print("Success: Graph saved as learning_curve.png")
except Exception as e:
    print(f"Error: {e}. Ensure 'loss_log.csv' exists in the current folder.")
