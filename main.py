import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
# init

# loadenv
load_dotenv()
url = os.getenv('HardcodeURL')

# soup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

carName = soup.find("h1", class_="sc-1n64n0d-8 sc-j1c9qm-2 gmXvZp kzofPy")
carDesc = soup.find("span", class_="sc-1n64n0d-7 sc-j1c9qm-4 kDYJWK fiumgF")

# if its weird like this do this -> 
price = soup.find("p", attrs={"data-testid": "advert-price"}, class_="sc-1n64n0d-5 sc-1t1ktfs-0 hQsESP etMJIu")

print(carName.get_text())
print(carDesc.get_text())
print(price.get_text())