# env
import os
from dotenv import load_dotenv
# scrape
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# init

# loadenv
load_dotenv()
url = os.getenv("origin")

# Find the listings
with sync_playwright() as p:
  browser = p.chromium.launch(
      headless=False, args=["--disable-blink-features=AutomationControlled"]
  )

  context = browser.new_context(
      viewport={"width": 1920, "height": 1080},
      user_agent=(
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
  )

  # Anti-detection flag override
  context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

  page = context.new_page()
  page.goto(url, wait_until="networkidle")

  # Extract all href attributes
  links = page.locator("a").evaluate_all(
      "elements => elements.map(el => el.href)"
  )

  browser.close()

# Filter to ONLY include links containing '.co.uk/car-details/'
car_links = sorted(
    list(
        set(link for link in links if link and ".co.uk/car-details/" in link)
    )
)

# Loop and find specific vehicle information

for i in range(len(car_links)):
  response = requests.get(car_links[i])
  soup = BeautifulSoup(response.content, 'html.parser')



  carName = soup.find("h1", class_="sc-1n64n0d-8 sc-j1c9qm-2 gmXvZp kzofPy")
  carDesc = soup.find("span", class_="sc-1n64n0d-7 sc-j1c9qm-4 kDYJWK fiumgF")
  price = soup.find("p", attrs={"data-testid": "advert-price"}, class_="sc-1n64n0d-5 sc-1t1ktfs-0 hQsESP etMJIu")
  mileage = soup.find("button", class_="YRCjRq__root atds-link sc-1eqq2tl-0 fUeNoL")
  gearbox = soup.find("p", class_="sc-1n64n0d-7 sc-1yzvd0s-6 kDYJWK isZEA-d")
  fuel = soup.find("p", class_="sc-1n64n0d-7 sc-1yzvd0s-6 kDYJWK isZEA-d")

  print(carName.get_text(), carDesc.get_text(), price.get_text(), mileage.get_text(), gearbox.get_text(), fuel.get_text())
