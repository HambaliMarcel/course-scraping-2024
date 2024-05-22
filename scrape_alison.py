import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    return driver

def get_course_links(driver, url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    course_links = [link['href'] for link in soup.select('.card__more--mobile')]
    return course_links

def get_course_details(driver, url2, course_link):
    url3 = url2 + course_link
    driver.get(url3)
    time.sleep(4)
    
    course_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    course_name_tag = course_soup.find(class_='course-title')
    course_name = course_name_tag.text.strip() if course_name_tag else 'No course name available'
    
    outline_tags = course_soup.find(class_='l-mods__topics-inner')
    outline = ' '.join([tag.get_text(strip=True) for tag in outline_tags]) if outline_tags else 'No outline available'
    
    accept_button = driver.find_element(By.CSS_SELECTOR, '[data-tab="course-desc"]')
    if accept_button:
        accept_button.click()
        time.sleep(2)
    
    description_tags = course_soup.find(class_='course-desc')
    description = ' '.join([tag.get_text(strip=True) for tag in description_tags]) if description_tags else 'No description available'
    
    return course_name, description, outline

def save_to_excel(course_names, descriptions, outlines):
    df = pd.DataFrame({
        'Course Name': course_names,
        'Description': descriptions,
        'Outline': outlines
    })
    df.to_excel('alison.xlsx', index=False)

def scrape_courses():
    driver = setup_driver()
    url = "https://alison.com/courses?tag=supply-chain-management&tag=aviation&tag=shipping&tag=maritime-law&tag=sdg-14-life-below-water&tag=marine-engineering&language=en&query=port"
    url2 = "https://alison.com/courses"
    
    course_links = get_course_links(driver, url)
    
    course_names = []
    descriptions = []
    outlines = []
    
    for course_link in course_links:
        course_name, description, outline = get_course_details(driver, url2, course_link)
        course_names.append(course_name)
        descriptions.append(description)
        outlines.append(outline)
    
    driver.quit()
    
    save_to_excel(course_names, descriptions, outlines)

if __name__ == "__main__":
    scrape_courses()
