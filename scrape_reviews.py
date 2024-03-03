from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

options = webdriver.FirefoxOptions()
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Firefox(options=options)

# Navigate to the website
driver.get('https://www.amazon.in/OnePlus-Nord-Chromatic-128GB-Storage/product-reviews/B0BY8MCQ9S/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')

# Extract data from current page
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.find_all('div', class_='a-section celwidget')
#many items containing that div
for item in items:
    # Extract review title
    review_title = item.find('a', {'data-hook': 'review-title'}).text.strip()

    # Extract review rating
    review_rating = item.find('i', {'class': 'a-icon-star'}).find('span', {'class': 'a-icon-alt'}).text.strip()

    # Extract review date
    review_date = item.find('span', {'data-hook': 'review-date'}).text.strip()

    # Extract review body
    review_body = item.find('span', {'data-hook': 'review-body'}).text.strip()

    # Process the data (e.g., store it, print it, etc.)
    print("Review Title:", review_title)
    print("Review Rating:", review_rating)
    print("Review Date:", review_date)
    print("Review Body:", review_body)
    print()  # Add a newline for clarity
    

# Close the WebDriver
driver.quit()
