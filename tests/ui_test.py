import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

@pytest.fixture
def user1():
    return {'username': 'studentbaduser', 
            'firstname': 'bad', 
            'lastname': 'user', 
            'wpi_id': '123456789', 
            'email': 'studentbad@wpi.edu', 
            'phone': '1234567890', 
            'password': 'a',
            'gpa': '3.50',
            'gradyear': '2027',}

@pytest.fixture
def user2():
    return {'username': 'baduser', 
            'firstname': 'bad', 
            'lastname': 'user', 
            'wpi_id': '123456789', 
            'email': 'baduser@wpi.edu', 
            'phone': '1234567890', 
            'password': 'verystrong',
            'gpa': '3.50',
            'gradyear': '2027',}

def createCourse():
    return {'cyear': '2029', 'course': '08', 'saNum': '3', 'minGPA':'2.5'}

@pytest.fixture
def browser():
    CHROME_PATH = "/Users/alicia/Downloads/chromedriver-mac-arm64"
    print(CHROME_PATH)

    service = Service(executable_path = CHROME_PATH + '/chromedriver')
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)

    yield driver

    driver.quit()

def test_student_register(browser,user1):
    browser.get('http://127.0.0.1:5000/student/register')
    browser.maximize_window()

    browser.find_element(By.NAME, "username").send_keys(user1['username'])
    sleep(1)
    browser.find_element(By.NAME, "firstname").send_keys(user1['firstname'])
    sleep(1)
    browser.find_element(By.NAME, "lastname").send_keys(user1['lastname'])
    sleep(1)
    browser.find_element(By.NAME, "email").send_keys(user1['email'])    
    sleep(1)
    browser.find_element(By.NAME, "wpi_id").send_keys(user1['wpi_id'])
    sleep(1)
    browser.find_element(By.NAME, "phone").send_keys(user1['phone'])    
    sleep(1)
    browser.find_element(By.NAME, "gpa").send_keys(user1['gpa'])
    sleep(1)
    browser.find_element(By.NAME, "grad_year").send_keys(user1['gradyear'])
    sleep(1)
    browser.find_element(By.NAME, "password").send_keys(user1['password'])    
    sleep(1)
    browser.find_element(By.NAME, "password2").send_keys(user1['password'])    
    sleep(4)
    browser.find_element(By.NAME, "submit").click()
    sleep(4)
    content = browser.page_source
    assert 'Congratulations' in content

def test_teacher_register(browser,user2):
    browser.get('http://127.0.0.1:5000/teacher/register')
    browser.maximize_window()

    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    sleep(1)
    browser.find_element(By.NAME, "firstname").send_keys(user2['firstname'])
    sleep(1)
    browser.find_element(By.NAME, "lastname").send_keys(user2['lastname'])
    sleep(1)
    browser.find_element(By.NAME, "email").send_keys(user2['email'])    
    sleep(1)
    browser.find_element(By.NAME, "wpi_id").send_keys(user2['wpi_id'])
    sleep(1)
    browser.find_element(By.NAME, "phone").send_keys(user2['phone'])    
    sleep(1)
    browser.find_element(By.NAME, "password").send_keys(user2['password'])    
    sleep(1)
    browser.find_element(By.NAME, "password2").send_keys(user2['password'])    
    sleep(4)
    browser.find_element(By.NAME, "submit").click()
    sleep(4)
    content = browser.page_source
    assert 'Congratulations' in content


def test_register_error(browser,user2, user1):
    browser.get('http://127.0.0.1:5000/teacher/register')
    browser.maximize_window()

    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    sleep(2)
    browser.find_element(By.NAME, "firstname").send_keys(user2['firstname'])
    sleep(2)
    browser.find_element(By.NAME, "lastname").send_keys(user2['lastname'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(user2['email'])    
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(user2['wpi_id'])
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(user2['phone'])    
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(user2['password'])    
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(user1['password'])    
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Register' in content
    assert 'equal to' in content

def test_login_form(browser,user2):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    sleep(1)
    browser.find_element(By.NAME, "password").send_keys(user2['password'])
    sleep(1)
    browser.find_element(By.NAME, "remember_me").click()
    sleep(1)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Sections' in content
    assert user2['username'] in content

def test_invalidlogin(browser,user2):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys('badpassword')
    sleep(2)
    browser.find_element(By.NAME, "remember_me").click()
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Invalid username or password' in content
    assert 'Sign In' in content

def test_create_section(browser, user2):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    browser.find_element(By.NAME, "password").send_keys('verystrong')
    browser.find_element(By.NAME, "submit").click()

    sleep(1)
    browser.get('http://127.0.0.1:5000/course/section/create')
    sleep(2)
    browser.find_element(By.NAME, "year").send_keys('2028')
    sleep(1)
    browser.find_element(By.NAME, "section_num").send_keys('08')
    sleep(1)
    browser.find_element(By.NAME, "sa_num").send_keys('2')
    sleep(1)
    browser.find_element(By.NAME, "min_gpa").send_keys('1.5')
    sleep(1)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    content = browser.page_source
    assert '2' in content
    assert 'Your section has been successfully created' in content

def test_apply(browser):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "username").send_keys('studentbaduser')
    browser.find_element(By.NAME, "password").send_keys('a')
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://127.0.0.1:5000/student/application/1')
    sleep(1)
    browser.find_element(By.NAME, "reason").send_keys('i want to be sa')
    sleep(2)
    browser.find_element(By.NAME, "submit").click()

    content = browser.page_source
    assert 'Application submitted successfully!' in content

def test_edit(browser):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "username").send_keys('studentbaduser')
    browser.find_element(By.NAME, "password").send_keys('a')
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://127.0.0.1:5000/student/edit/application/1')
    browser.find_element(By.NAME, "reason").send_keys('eeeeee')
    sleep(1)
    browser.find_element(By.NAME, "submit").click()
    sleep(1)
    content = browser.page_source
    assert 'Application updated successfully!' in content