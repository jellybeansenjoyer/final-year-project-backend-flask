from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Selenium WebDriver
driver = webdriver.Firefox()
url = 'https://amazon.in/Logitech-B100-Optical-Mouse-Black/dp/B003L62T7W/ref=pd_rhf_dp_s_pd_crcd_d_sccl_2_2/258-0255438-8839862?pd_rd_w=H6IMm&content-id=amzn1.sym.785b16db-ca40-46a3-ae75-2b38bb48d1aa&pf_rd_p=785b16db-ca40-46a3-ae75-2b38bb48d1aa&pf_rd_r=J58HSRP2XYYWNQVQE7M2&pd_rd_wg=1ycQb&pd_rd_r=4eb2ed65-98a2-46d5-931b-e4715d9bf0d7&pd_rd_i=B003L62T7W&psc=1'
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
