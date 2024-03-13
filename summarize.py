import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL to scrape
url = 'http://192.168.0.190:1338/chat/'
#url = 'https://chat.openai.com/chat'
# Initialize Selenium WebDriver (assuming Firefox)
driver = webdriver.Firefox()
driver.get(url)
def expect_recom(txt):
    # Wait for the page to load completely
    driver.implicitly_wait(10)

    # Find the textarea element by its id
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "message-input"))
    )

    # Input the provided text into the textarea
    text = '''These are my product reviews - Absolutely love this product!
    It exceeded my expectations in every way.
    The quality is top-notch, and it works like a charm.
    Plus, the customer service was fantastic.
    Highly recommend!
    Good product overall.
    It serves its purpose, but I did encounter some minor issues with durability after a few weeks of use.
    Customer service was helpful in resolving my concerns though.
    Not impressed.
    The product arrived damaged, and it didn't function as described.
    It was a hassle to return, and I'm still waiting for a refund.
    Very disappointing experience.
    Works well and feels sturdy. Give me in points how should i improve the quality of my product give only in one line points'''

    prmpt = 'Give me in points how should i improve the quality of my product give only in 5 one line points, '
    text = txt+prmpt
    element.send_keys(text)

    # Click the send button
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "send-button"))
    )
    send_button.click()

    # Wait for the response to load
    time.sleep(10)

    # Find the div element with class "content"
    # Wait for the response to load
    time.sleep(10)

    # Find the div element with class "content"
    element.send_keys(text)

    # Click the send button
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "send-button"))
    )
    send_button.click()

    content_div = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'message'))
    )

    print(content_div)
    # Print the entire HTML content of the content_div
    print(content_div.get_attribute("outerHTML"))

    # Extract all the <li> elements within the div
    list_items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.content li'))
    )

    # Print the number of <li> elements found
    print("Number of <li> elements found:", len(list_items))

    # Extract text from each <li> element and store in a list
    li_texts = [li.text for li in list_items]

    # Print the list of <li> element texts
    for text in li_texts:
        print(text)

    # Close the browser
    time.sleep(5)
    driver.quit()
    return li_texts
