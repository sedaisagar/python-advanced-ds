from bs4 import BeautifulSoup
import requests,time

class BsScraper:
    def __init__(self, link=None, mode = "quote"):
        self.mode = mode
        self.link = link
        self.has_next_page = True
        self.quotes = []
        self.current_page = 1 
        self.news = []
        

    def get_html_content(self):
        match self.mode :
            case "sidhakura":
                self.actual_link = f"{self.link}?page={self.current_page}"
            case "quote":
                self.actual_link = f"{self.link}/{self.current_page}/"

        print(f"\nRequesting for -> {self.actual_link}","-"*25)
        
        start_time = time.perf_counter()
        
        response = requests.get(self.actual_link).text
        
        end_time = time.perf_counter()
        
        print(f"Request completed -> {self.actual_link}","-"*25)
        
        print(f"Total time elapsed -> {end_time - start_time}","-"*25,"\n")
        
        return response

    def quotes_to_scrap_bs(self):
        html_content = self.get_html_content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        quotes = soup.find_all("div", {"class": "quote"})
        for i in quotes:
            quote = i.find("span", {"itemprop": "text"}).text
            self.quotes.append(quote)

        next_page = soup.find("li", {"class":"next"})
        
        if next_page and next_page.text :
            self.current_page += 1 
            self.quotes_to_scrap_bs()

        return self.quotes
    
    def sidhakura_to_scrap_bs(self):
        html_content = self.get_html_content()
        soup = BeautifulSoup(html_content, 'html.parser')
        # class="course-card "
        news_main_box = soup.find("div", {"class": "full-samachar-list"})
        items = news_main_box.find_all("div", {"class" : "items"})
        for i in items:
            title = i.find_all("a")[1].text
            image = i.find("figure").find("img")["data-src"]
            date = i.find("span", {"class":"date-line"}).text
            data = dict(
                title = title,
                image = image,
                date = date,
            )

            self.news.append(data)

        next_page = soup.find("a", {"class":"nextpostslink"})
        
        if next_page and next_page.text and self.current_page <= 10:
            self.current_page += 1 
            self.sidhakura_to_scrap_bs()

        return self.news


    def scrap(self):
        if not self.link:
            return

        match self.mode:
            case "sidhakura":
                return self.sidhakura_to_scrap_bs()
            case "quote":
                return self.quotes_to_scrap_bs()
            case _:
                return {"details":"Invalid mode received!"}

# 
# async def fetch():
#     ...
#     xyz = await fetch()