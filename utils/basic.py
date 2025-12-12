import matplotlib.pyplot as plt
import numpy as np

class BasicUtil:
    def plot(self):
        t = np.linspace(-50, 50, 500)
        sig = 1 / (1 + np.exp(-t)) # Sigmoid Function

        fig, ax = plt.subplots()
        ax.axhline(y=0, color="black", linestyle="--")
        ax.axhline(y=0.5, color="black", linestyle=":")
        ax.axhline(y=1.0, color="black", linestyle="--")
        ax.axvline(color="grey")
        ax.axline(
            (0, 0.5), slope=0.25, 
            color="black", linestyle=(0, (5, 5))
        )
        ax.plot(
            t, sig, linewidth=2, 
            label=r"$\sigma(t) = \frac{1}{1 + e^{-t}}$"
        )
        ax.set(xlim=(-10, 10), xlabel="t")
        ax.legend(fontsize=14)
        
        plt.show()

    def plot_bar(self):
        fig, ax = plt.subplots()

        fruits = ['apple', 'blueberry', 'cherry', 'orange']
        counts = [40, 100, 30, 55]
        bar_labels = ['red', 'blue', '_red', 'orange']
        bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

        ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        ax.set_ylabel('fruit supply')
        ax.set_xlabel("Fruit Varieties")
        ax.set_title('Fruit supply by kind and color')
        ax.legend(title='Fruit color')
        ax.set_title("Fruits")
        plt.show()