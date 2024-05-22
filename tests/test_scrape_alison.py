import pytest
import pandas as pd
from scrape_alison import setup_driver, get_course_links, get_course_details, save_to_excel

def test_setup_driver():
    driver = setup_driver()
    assert driver is not None
    driver.quit()

def test_get_course_links(mocker):
    driver = setup_driver()
    url = "https://alison.com/courses?tag=supply-chain-management&tag=aviation&tag=shipping&tag=maritime-law&tag=sdg-14-life-below-water&tag=marine-engineering&language=en&query=port"
    mocker.patch('time.sleep', return_value=None)  # Mocking time.sleep for faster tests
    course_links = get_course_links(driver, url)
    assert isinstance(course_links, list)
    driver.quit()

def test_get_course_details(mocker):
    driver = setup_driver()
    url2 = "https://alison.com/courses"
    course_link = "/some-course-link"  # Use a sample course link for testing

    mocker.patch('time.sleep', return_value=None)  # Mocking time.sleep for faster tests

    # Mocking the course page content
    course_name, description, outline = get_course_details(driver, url2, course_link)

    assert isinstance(course_name, str)
    assert isinstance(description, str)
    assert isinstance(outline, str)

    driver.quit()

def test_save_to_excel():
    course_names = ['Course 1', 'Course 2']
    descriptions = ['Description 1', 'Description 2']
    outlines = ['Outline 1', 'Outline 2']

    save_to_excel(course_names, descriptions, outlines)

    df = pd.read_excel('alison.xlsx')

    assert not df.empty
    assert list(df.columns) == ['Course Name', 'Description', 'Outline']
    assert df.shape == (2, 3)
