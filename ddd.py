from selenium import webdriver
from bs4 import BeautifulSoup

# URL to scrape
url = 'http://192.168.0.104:1338/chat/'

# Initialize Selenium WebDriver (assuming Firefox)
driver = webdriver.Firefox()
driver.get(url)

# Wait for the page to load completely (you may need to adjust the timeout)
driver.implicitly_wait(10)

# Get the HTML content of the page after it's loaded
html_content = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the div with class 'content' and id 'gpt_7345436862975740175'
content_div = soup.find('div', {'class': 'content', 'id': 'gpt_7345436862975740175'})

# Extract the text inside the div
text = content_div.get_text(strip=True)

print(text)
