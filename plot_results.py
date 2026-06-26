import pandas as pd
import matplotlib.pyplot as plt

def plot_performance():
    try:
        df = pd.read_csv('logs/experiment_results.csv')
        fig, ax1 = plt.subplots()
        ax1.plot(df['episode'], df['loss'], color='red', label='Loss')
        ax2 = ax1.twinx()
        ax2.plot(df['episode'], df['reward'], color='blue', label='Reward')
        plt.title('Agent Learning Performance')
        plt.show()
    except Exception as e:
        print(f"Error plotting data: {e}")

if __name__ == '__main__':
    plot_performance()
