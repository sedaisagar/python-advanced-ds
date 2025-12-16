from bs4 import BeautifulSoup
import requests,time

class BsScraper:
    def __init__(self, link=None):
        self.link = link
        self.has_next_page = True
        self.quotes = []
        self.current_page = 1 

    def get_html_content(self):
        self.actual_link = f"{self.link}/{self.current_page}/"

        print(f"\nRequesting for -> {self.actual_link}","-"*25)
        
        start_time = time.perf_counter()
        
        response = requests.get(self.actual_link).text
        
        end_time = time.perf_counter()
        
        print(f"Request completed -> {self.actual_link}","-"*25)
        
        print(f"Total time elapsed -> {end_time - start_time}","-"*25,"\n")
        
        return response

    def soupify(self):
        html_content = self.get_html_content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        quotes = soup.find_all("div", {"class": "quote"})
        for i in quotes:
            quote = i.find("span", {"itemprop": "text"}).text
            self.quotes.append(quote)

        next_page = soup.find("li", {"class":"next"})
        
        if next_page and next_page.text :
            self.current_page += 1 
            self.soupify()

        return self.quotes


    def scrap(self):
        if not self.link:
            return

        return self.soupify()