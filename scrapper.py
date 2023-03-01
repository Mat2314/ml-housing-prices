# Module contains tools to scrap housing data form given page

from bs4 import BeautifulSoup
import requests
import re
import csv
import time
from tqdm import tqdm

class HousingScrapper:
    def __init__(self):
        pass
    
    def get_page(self, url: str):
        """Returns HTML page content"""
        response = requests.get(url)
        response.raise_for_status()
        
        return response.text
    
    def _extract_price(self, price: str):
        return price[0:price.find('\xa0')]
    
    def _extract_rooms(self, rooms: str):
        text = rooms.split(' ')[0]
        return re.sub("[^0-9]", "", text)
    
    def _extract_square_meters(self, sqm: str):
        text = sqm.split(' ')[0]
        return re.sub("[^0-9^.]", "", text)
    
    def _first_content_index(self, contents: list):
        """Return the index of element that has house price. Find 'zł' string in it."""
        for index,element in enumerate(contents):
            if 'zł' in element.text:
                return index
        
        return 0
    
    def extract_houses_data(self, html_data: str):
        soup = BeautifulSoup(html_data, 'html.parser')
        page_offers = soup.select('.es62z2j18')
        
        data_list = []
        
        # Go through all every page offer and extract particular house data
        for offer in page_offers:
            soup_offer = BeautifulSoup(str(offer), 'html.parser')
            district = soup_offer.select(".es62z2j11")[0].text.split(",")[1]
            district = re.sub('[\W\d]+', '', district)
            
            numerical_data = soup_offer.select(".e1brl80i2")[0]
            
            first_index = self._first_content_index(numerical_data.contents)
            numerical_data = numerical_data.contents[first_index:first_index+3] # Leave only price, rooms number and sqare meters
            price_tag, rooms_tag, square_meters_tag = numerical_data
            
            price = self._extract_price(price_tag.text)
            rooms = self._extract_rooms(rooms_tag.text)
            square_meters = self._extract_square_meters(square_meters_tag.text)
            
            data_list.append([district, rooms, square_meters, price])
        
        return data_list
        
    def extract_from_page(self, page: str):
        content = self.get_page(page)
        data = self.extract_houses_data(content)
        return data
    
    def save_to_csv(self, filename: str, data: list):
        header = ['district', 'rooms', 'square_meters', 'price']
        with open(filename, "w", encoding='UTF8', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(data)
            

def run():
    """Custom function to adjust the behavior of the class"""
    scrapper = HousingScrapper()
    num_pages = 173
    all_rows = []
    
    for page in tqdm(range(1, num_pages+1)):
        time.sleep(2)
        url = f"https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/warszawa?page={page}&limit=24"
        rows = scrapper.extract_from_page(url)
        all_rows.extend(rows)
    
    scrapper.save_to_csv("warsaw_houses.csv", all_rows)


if __name__ == '__main__':
    # scrapper = HousingScrapper()
    # url = "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/warszawa?page=1&limit=24"
    # rows = scrapper.extract_from_page(url)
    # scrapper.save_to_csv("test.csv", rows)
    pass
    run()