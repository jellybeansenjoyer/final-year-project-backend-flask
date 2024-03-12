from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Selenium WebDriver
driver = webdriver.Firefox()
url = 'https://www.amazon.in/Lloyd-Window-Copper-Golden-GLW18C4YWGEW/dp/B0BRKX5WWK/ref=sr_1_25?_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&dib=eyJ2IjoiMSJ9.LpujZ4uISPUK8sa_6yNGVRbnpLAogbToTOMZRXNZaZL_lzG0mGiDVmo13WY0Ic5h--vBF_zwQhz5gJfnLcSxrm6CySTsa24gd8pNPWXFFx99O5XvrF67hJ_LXxnGjdEEVV5qwuYxWDqFEdb1dIIakWgWG8YvWWGgWjlz9tJ6Y4J0jk76K_m2-zD6N2FZ1Xh6Yk14wCLUVkoy68i_yhuFwJqswvJqylfcwHbfKTJ4zT3XdcQqwq-nPQBkM_IBpKruAHkCsO_580xrlLXyEkvE9iErOwncieH9COwzRps_c54.OFysy0qPj0YUaYWiTakzcoms6HdSMvs94Uh04cFnhKo&dib_tag=se&pd_rd_r=a9e97b88-6b2a-4f55-8f0e-11322119276f&pd_rd_w=bYL5B&pd_rd_wg=QIle5&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=8GKBT68W16RRSJF23TDW&qid=1710218113&refinements=p_85%3A10440599031&rps=1&s=kitchen&sr=1-25'
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'productDetails_techSpec_section_1')))

# Get the HTML content of the page after it's loaded
html_content = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table containing product details
table = soup.find('table', {'id': 'productDetails_techSpec_section_1'})

# Extract properties and values
properties_and_values = {}
for row in table.find_all('tr'):
    cells = row.find_all(['th', 'td'])
    if len(cells) == 2:
        property_name = cells[0].text.strip()
        property_value = cells[1].text.strip()
        properties_and_values[property_name] = property_value

# Print the extracted properties and values
for prop, value in properties_and_values.items():
    print(f"{prop}: {value}")
