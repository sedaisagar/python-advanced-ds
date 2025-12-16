# from utils.graphical import PlotlyUtil


# plotly_instance = PlotlyUtil()
# plotly_instance.plot()


# from utils.basic import BasicUtil

# # basic_instance = BasicUtil()
# # basic_instance.plot()
# # basic_instance.plot_bar()


# from utils.normal import SeabornUtility
# # normal_instance = SeabornUtility()
# # normal_instance.plot()
# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.DataFrame({
#     'category': ['A', 'B', 'C', 'D', 'E', 'F'],
#     'value': [10, 20, 15, 25, 30, 11],
#     'x': [1, 2, 3, 4, 5, 6],
#     'y': [5, 7, 4, 9, 3, 8]
# })

# df.plot(kind='bar', x='x', y='y', title='Bar Graph Example')
# plt.tight_layout()
# plt.show()


# df.set_index('category')['value'].plot(kind='pie', autopct='%1.1f%%', title='Pie Chart Example')
# plt.ylabel('')
# plt.tight_layout()
# plt.show()

# df.plot(kind='scatter', x='x', y='y', title='Scatter Plot Example')
# plt.show()


# df[['value']].plot(kind='box', title='Box Plot Example')
# plt.show()


# Line Graph
# df.plot(kind='line', x='x', y='value', marker='o', title='Line Graph Example')
# plt.show()

# x = "sagar"

# assert  x != "sagar"



# from ui.main import CRUDApp as MainUiComponent

# ui_component = MainUiComponent()

# ui_component.show_ui()


from scraper.bs_scraper import BsScraper
from scraper.scrapy_scraper import ScrapyScraper


bs_instance = BsScraper(link="https://quotes.toscrape.com/page")
rv = bs_instance.scrap()
print(rv)