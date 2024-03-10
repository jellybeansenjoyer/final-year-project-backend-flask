from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
url = 'https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=sr_1_4?keywords=bags&qid=1697885232&sr=8-4&th=1'
driver.get(url)

try:
    # Wait for the product title element to be visible
    product_title_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "productTitle"))
    )
    
    # Extract the product title text
    product_title_text = product_title_element.text.strip()
    print("Title:", product_title_text)
    
    # Find the price element
    price_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "a-price-whole"))
    )
    
    # Extract the price text
    price_text = price_element.text.strip()
    print("Price:", price_text)
    
    # Wait for the list of span elements to be present
    spans = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item"))
    )
    
    # Extract the text from each span and store it in a list
    text_list = [span.text.strip() for span in spans]
    print("List of Texts inside Span elements:")
    print("Details:", text_list)
    
    # Get the HTML of the table
    table_html = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "productDetails_techSpec_section_1"))
    ).get_attribute("innerHTML")
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(table_html, "html.parser")
    
    # Find all rows in the table
    rows = soup.find_all("tr")
    
    # Create an empty dictionary to store name-value pairs
    data_dict = {}
    
    # Loop through each row
    for row in rows:
        # Find the header and data cells
        header_cell = row.find("th")
        data_cell = row.find("td")
        
        # Extract the text from header and data cells
        if header_cell and data_cell:
            header_text = header_cell.text.strip()
            data_text = data_cell.text.strip()
            
            # Add the name-value pair to the dictionary
            data_dict[header_text] = data_text
            
    # Print the dictionary
    print("Technical Specifications:")
    
    cleaned_data_dict = {}

    # Iterate through each key-value pair in the original dictionary
    for key, value in data_dict.items():
        # Remove special characters from the value
        cleaned_value = value.strip('\u200e')
        # Add the cleaned key-value pair to the new dictionary
        cleaned_data_dict[key] = cleaned_value

    # Print the cleaned dictionary
    print("Cleaned Technical Specifications:")
    print(cleaned_data_dict)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Quit the driver
    driver.quit()
