import seaborn as sns
import matplotlib.pyplot as plt

class SeabornUtility:
    def plot(self):
        # Apply the default theme
        sns.set_theme()

        # Load an example dataset
        tips = sns.load_dataset("tips")
        print(tips)
        # Create a visualization
        sns.relplot(
            data=tips,
            x="total_bill", y="tip", col="time",
            hue="smoker", style="smoker", size="size",
        )
        plt.show()
