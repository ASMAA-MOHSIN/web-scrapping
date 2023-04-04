#1.Produce a program that:Scrape the index webpage hosted at `cfcunderwriting.com`
#2.Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hostedon cfcunderwriting.com) to a JSON output file.
#3. Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
page
#4. Use the privacy policy URL identified in step 3 and scrape the pages content.Produce a case-insensitive word frequency count for all of the
#visible text on the page.Your frequency count should also be written to a JSON output file..

from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time
import requests
url = 'http://cfcunderwriting.com'
source = requests.get(url)
soup = BeautifulSoup(source.content , 'html.parser')
#html_content = soup.content


#finding images that are hosted externally
external_resources = []
for img in soup.find_all('img'):
    if img.get('src') and not img['src'].startswith(url):
        external_resources.append(img['src'])
        #writing in json file and indenting to write in a list form
with open('external_resources.json', 'w') as outfile:
    json.dump(external_resources, outfile, indent = 4)
    
#finding hyperlinks
for link in soup.find_all('link'):
    if link.get('href') and not link['href'].startswith(url):
        external_resources.append(link['href'])
    # Write the list of external resources to a JSON file
with open('external_resources.json', 'w') as outfile:
    json.dump(external_resources, outfile, indent=4)

# Find the Privacy Policy link
tcs_links = soup.find('p', class_='tcs-links')
privacy_policy_link = tcs_links.find('a', href=lambda href: href and 'privacy-policy' in href)
privacy_policy_url = privacy_policy_link['href']
privacy_policy_text = privacy_policy_link.text
# get all visible text from the page
visible_text = soup.get_text()

# convert all text to lowercase for case-insensitive comparison
visible_text = visible_text.lower()

# split the text into words and count their frequency
word_count = {}
for word in visible_text.split():
    word_count[word] = word_count.get(word, 0) + 1

# print the word frequency count
for word, count in word_count.items():
    #print(f'{word}: {count}')
    with open('privacy_policy.json', 'w') as outfile:
        json.dump(privacy_policy_url, outfile, indent = 4)
 #finding fonts

# Set up the Selenium web driver
service = Service(r'C:\Users\WALEED TRADERS\Download\chromedriver_win32') 
driver = webdriver.Chrome(service=service)

# Navigate to the web page you want to scrape
driver.get('http://cfcunderwriting.com')

# Wait for the page to load
time.sleep(5)

# Find all elements with a "style" attribute that contains "font-family"
elements_with_font_family = driver.find_elements(By.CSS_SELECTOR, '*[style*="font-family:"]')

# Navigate to the web page you want to scrape
driver.get('cfcunderwriting.com')

# Find all elements with a "style" attribute that contains "font-family"
elements_with_font_family = driver.find_elements(By.CSS_SELECTOR, '*[style*="font-family:"]')

# Extract font family information from each matching element
font_families = set()
for element in elements_with_font_family:
    font_family = element.get_attribute('style').replace('font-family:', '').replace('"', '').strip()
    font_families.add(font_family)
with open(r'C:\Users\WALEED TRADERS/fonts.json', 'w', encoding='utf-8') as outfile:
    json.dump(list(font_families), outfile, ensure_ascii=False, indent=4)

# Close the web driver
driver.quit()

