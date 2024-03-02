from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Firefox()
url = 'https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=sr_1_4?keywords=bags&qid=1697885232&sr=8-4&th=1'
driver.get(url)
driver.implicitly_wait(10)

# Wait for the <h1> element to be loaded
h1_element = driver.find_element(By.XPATH, '//h1[@class="a-size-medium a-spacing-small"]')

# Extract the text content of the <h1> element
product_title = h1_element.text

print(product_title)
manufacturer_ths = driver.find_elements(By.XPATH, '//th[@class="a-color-secondary a-size-base prodDetSectionEntry"]')
values_ths = driver.find_elements(By.XPATH, '//td[@class="a-size-base prodDetAttrValue"]')

# Extract the text content of all <th> elements into a list
manufacturer_labels = [th.text for th in manufacturer_ths]
value_labels = [th.text for th in values_ths]
print(manufacturer_labels)
print(value_labels)
print(len(manufacturer_labels))
print(len(value_labels))
d = dict()
for i in range(min(len(value_labels),len(manufacturer_labels))):
    d[manufacturer_labels[i]] = value_labels[i]
print(d)