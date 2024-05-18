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

courses = [
    "art-on-superyachts", "boatyard-and-marina-operations", "health-and-safety-in-ship-operations",
    "lng-shipping", "marine-insurance-claims", "marine-pilotage", "marine-salvage",
    "maritime-fire-prevention-fire-fighting-and-fire-safety", "maritime-law", "offshore-operations",
    "offshore-wind-energy", "port-state-control", "restoration-of-historic-ships-boats",
    "ship-security", "ship-surveying", "shipbuilding-and-ship-repair", "superyacht-management",
    "superyacht-project-management-refit-and-newbuilding", "superyacht-pursers", "superyacht-surveying",
    "superyacht-operations", "tanker-operations", "technical-ship-management", "yacht-boat-building",
    "yacht-small-craft-surveying", "yacht-brokerage", "cargo-surveying", "conducting-an-inclining-test",
    "introduction-to-port-state-inspection", "introduction-to-the-ism-code", "introduction-to-the-superyacht-industry",
    "introduction-to-ship-surveying", "introduction-to-the-inventory-of-hazardous-materials-on-ships",
    "marine-incident-investigation", "maritime-emergency-preparation-and-response", "sails-and-rigs",
    "superyacht-deckhands", "surveying-yacht-and-small-craft-engines", "surveying-yacht-and-small-craft-systems"
]

base_url = "https://maritimetrainingacademy.com/courses/"

course_names = []
descriptions = []
outlines = []

for course in courses:
    url = base_url + course
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    course_name_tag = soup.select_one('.et_pb_text_0 h1')
    course_name = course_name_tag.text.strip() if course_name_tag else 'No course name available'
    course_names.append(course_name)

    description_tags = soup.select('.et_pb_text_inner h2 + p')
    description = ' '.join([tag.get_text(strip=True) for tag in description_tags]) if description_tags else 'No description available'
    descriptions.append(description)

    outline_tags = soup.select('h5.et_pb_toggle_title')
    if outline_tags:
        outline = ', '.join([tag.get_text(strip=True) for tag in outline_tags])
    else:
        li_tags = soup.select('li')
        outline = ', '.join([tag.get_text(strip=True) for tag in li_tags]) if li_tags else 'No outline available'

    outlines.append(outline)

driver.quit()

df = pd.DataFrame({
    'Course Name': course_names,
    'Description': descriptions,
    'Outline': outlines
})

df.to_excel('maritime_courses.xlsx', index=False)
