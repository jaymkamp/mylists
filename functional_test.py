from selenium import webdriver

browser = webdriver.Firefox(executable_path = 'C:\\python_scripts\geckodriver\geckodriver.exe')
browser.get('http://localhost:8000')

assert 'Django' in browser.title