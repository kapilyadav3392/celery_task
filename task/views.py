from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Scrap_data

# @shared_task
def scrape_proxy_data(request):
    try:
        url = "https://geonode.com/free-proxy-list"
        response = requests.get(url)
        print(response)
        print("--------------------11--------------------------")
        soup = BeautifulSoup(response.content, 'html5lib')
        print(soup.prettify())
        print("---------------------22-------------------------")
        
        proxies_table = soup.find('table')
        print(proxies_table)
        
        print("---------------------33-------------------------")
        
        proxies = proxies_table.find_all('tr')[1:]  # skipping the header row
        for proxy_row in proxies:
            proxy_data = proxy_row.find_all('td')
            ip = proxy_data[0].text.strip()
            port = proxy_data[1].text.strip()
            protocol = proxy_data[6].text.strip()
            country = proxy_data[3].text.strip()
            uptime = proxy_data[8].text.strip()
            Scrap_data.objects.create(ip=ip, port=port, protocol=protocol, country=country, uptime=uptime)
    except Exception as e:
        print(str(e))

