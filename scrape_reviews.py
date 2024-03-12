from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
def scrape_reviews_fn(url):
    # Set up Chrome WebDriver using ChromeDriverManager
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Firefox()

    # Navigate to the website
    # 'https://www.amazon.in/Redmi-Arctic-Storage-Dimensity-Slimmest/product-reviews/B0CQPGG8KG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    driver.get(url)

    # Extract data from each page
        # Extract data from current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', class_='a-section celwidget')
    
    lst = []
    
    for item in items:
        # Extract review details
        ele = {}
        review_title = item.find('a', {'data-hook': 'review-title'}).text.strip()
        review_rating = item.find('i', {'class': 'a-icon-star'}).find('span', {'class': 'a-icon-alt'}).text.strip()
        review_date = item.find('span', {'data-hook': 'review-date'}).text.strip()
        review_body = item.find('span', {'data-hook': 'review-body'}).text.strip()
        # for _ in range(5):  
        #     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        #     time.sleep(1)
        # Print review details
        print("Review Title:", review_title)
        print("Review Rating:", review_rating)
        print("Review Date:", review_date)
        print("Review Body:", review_body)
        print()  # Add a newline for clarity
        ele = {
            "title":review_title,
            "review":review_rating,
            "rating":review_body
        }
        lst.append(ele)
        # next_button = driver.find_element(By.XPATH, '//li[@class="a-last"]/a')
        # if 'a-disabled' in next_button.get_attribute('class'):
        #     break  # No more pages available, exit the loop
        
        # # Click on the "next" button
        # next_button.click()
        
        # Wait for the page to load
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-section celwidget')))
        # time.sleep(5)  # Additional wait time (adjust as needed)
    print(lst)
    # Close the WebDriver
    driver.quit()
    return lst