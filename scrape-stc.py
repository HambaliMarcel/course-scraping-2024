import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(), options=chrome_options)

url = "https://stc-international.nl/courses/"

driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

course_links = [link['href'] for link in soup.select('.w-grid-item-anchor')]

course_names = []
descriptions = []
outlines = []

for course_link in course_links:
    driver.get(course_link)
    time.sleep(3)

    course_soup = BeautifulSoup(driver.page_source, 'html.parser')

    course_name_tag = course_soup.find(class_='w-post-elm post_title entry-title color_link_inherit')
    course_name = course_name_tag.text.strip() if course_name_tag else 'No course name available'
    course_names.append(course_name)

    description_tags = course_soup.select('.mc--content p')
    description = ' '.join([tag.get_text(strip=True) for tag in description_tags]) if description_tags else 'No description available'
    descriptions.append(description)

    outline_tags = course_soup.select('.mc--content li')
    outline = ' '.join([tag.get_text(strip=True) for tag in outline_tags]) if outline_tags else 'No outline available'
    outlines.append(outline)

driver.quit()

df = pd.DataFrame({
    'Course Name': course_names,
    'Description': descriptions,
    'Outline': outlines
})

df.to_excel('stc-international.xlsx', index=False)
