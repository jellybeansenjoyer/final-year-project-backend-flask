from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

driver = webdriver.Firefox()
url = 'https://www.amazon.in/Whirlpool-7-5-Semi-Automatic-ACE-SUPREME/dp/B083G25P9L/ref=sr_1_20?_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&dib=eyJ2IjoiMSJ9.huIQjSkTuPfYXaUe3MtXkURXTCCq9Glj01c89ASnHbi2m5CSAM1-yw_Y14AjH7bMugEsgorg_rKbhysn0Oa1nUHZ8L7wREMmSl53GHOvCdYROfbJ8B8jXywNgw9CQ1aP8sV4Q5z0XgZJbJf7qfDdciV2vKQVElSvZ0oEfO22KDxYxOeIpSOcIlV3TnVQ6eetD8Qugraz299z0MIVbFA2VttCl0OjUV5f8DjSbyVh2rneCSuoLTFELfKqWjRD60pLNMmW-YJGIrEzwDj0UhTfY-KoID_Ru3qF7v2JzwpOwVE.81UMYDTcujs8gjQfye2pBLMqcNr85UfVn_tmvjhuXKk&dib_tag=se&pd_rd_r=f4b69a0a-c2e1-4630-933b-7218a36f020c&pd_rd_w=CI3BF&pd_rd_wg=hl0TS&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=JW18VJVZQ7KT05BN5XQ5&qid=1710224637&refinements=p_85%3A10440599031&rps=1&s=kitchen&sr=1-20'
driver.get(url)

try:
    # Wait for the product title element to be visible
    print("Title Extraction Begins:")
    product_title_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "productTitle"))
    )
    
    # Extract the product title text
    product_title_text = product_title_element.text.strip()
    print("Title:", product_title_text)
except Exception as e:
    print("An error occurred:", e)

try:
    print("Price extraction begins:")
    # Wait for the price element to be visible
    price_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='a-price-whole']"))
    )

    # Extract the price text
    price_text = price_element.text.strip()
    print("Price:", price_text)
except Exception as e:
    print("An error occurred:", e)    
    try:
        
        # Wait for the price element to be visible
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'p.a-spacing-none.a-text-left.a-size-mini.twisterSwatchPrice'))
        )

        # Extract the price text
        price_text = price_element.text.strip()
        print("Price:", price_text)

    except Exception as e:
        print("An error occurred:", e)
try:
    print("Details Extraction begins:")
    # Wait for the list of span elements to be present
    spans = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item"))
    )
    
    # Extract the text from each span and store it in a list
    text_list = [span.text.strip() for span in spans]
    print("List of Texts inside Span elements:")
    print("Details:", text_list)
except Exception as e:
    print("An error occurred:", e)
try:
    print("Product Tech Details Extraction begins:")
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
try:
    print("Product Tech Details Additional Extraction begins:")
    # Wait for the product details table to be visible
    table_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "productDetails_detailBullets_sections1"))
    )
    
    # Get the HTML content of the table
    table_html = table_element.get_attribute('innerHTML')
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(table_html, 'html.parser')
    
    # Find all rows in the table
    rows = soup.find_all('tr')
    
    # Create an empty dictionary to store the extracted data
    data_dict = {}
    
    # Loop through each row
    for row in rows:
        # Find the header and data cells
        header_cell = row.find('th')
        data_cell = row.find('td')
        
        # Extract the text from header and data cells
        if header_cell and data_cell:
            header_text = header_cell.text.strip()
            data_text = data_cell.text.strip()
            
            # Add the name-value pair to the dictionary
            data_dict[header_text] = data_text
    
    # Print the extracted data dictionary
    print("Technical_Details:")
    cleaned_data_dict.update(data_dict)
    print(cleaned_data_dict)
except Exception as e:
    print("An error occurred:", e)
    

try:
    print("Category extraction begins:")
    # Wait for the div element to be visible
    div_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "wayfinding-breadcrumbs_feature_div"))
    )
    
    # Get the HTML content of the div
    div_html = div_element.get_attribute('innerHTML')
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(div_html, 'html.parser')
    
    # Find the ul element inside the div
    ul_element = soup.find('ul', class_='a-unordered-list')
    
    a_tag = ul_element.find('a')
    # Extract the text of the <a> tag
    if a_tag:
        a_tag_text = a_tag.text.strip()
        print("Category:", a_tag_text)
    else:
        print("No <a> tag found within the <ul> element.")

except Exception as e:
    print("An error occurred:", e)    # Quit the driver

try:
    print("Image Extraction Begins:")
    # Wait for the image element to be visible
    image_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "landingImage"))
    )

    # Extract the image source URL
    image_url = image_element.get_attribute("src")
    print("Image URL:", image_url)

except Exception as e:
    print("An error occurred:", e)

