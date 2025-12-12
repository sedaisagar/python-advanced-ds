import plotly.express as px

class PlotlyUtil:
    def plot(self):
        fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
        fig.show()