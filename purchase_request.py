#!/usr/bin/env python

import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Google Profile and driver
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:/Users/maggieluo/Library/Application Support/Google/Chrome/Default")
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

# Open browser
driver.get("https://callink.berkeley.edu/actioncenter/organization/anova/Finance/CreatePurchaseRequest")

# Save your login cookie each time you open Chrome
pickle.dump(driver.get_cookies(), open("CallinkCookie.pkl","wb"))

######### Payee Information #########

subject = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Subject"]')))

# Subject
subject = driver.find_element_by_xpath('//*[@id="Subject"]').send_keys("Jane Smith")

# Description
desc = driver.find_element_by_xpath('//*[@id="Description"]').send_keys("N/A")

# Requested Amount
requested_amount = driver.find_element_by_xpath('//*[@id="RequestedAmount"]').send_keys("100")

# Category
category = driver.find_element_by_xpath('//*[@id="CategoryId"]')
for option in category.find_elements_by_tag_name('option'):
    if option.text == 'Check Reimbursement - (Amounts over $25.00 or check to be mailed)':
        option.click()
        break

# Account
select_account = driver.find_element_by_xpath('//*[@id="accountSelectButton"]').click()
select_misc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div[1]/div/div[2]/table/tbody/tr[4]/td[1]/a"))).click()

######### Payee Information #########

# First and Last Name
first_name = driver.find_element_by_xpath('//*[@id="PayeeFirstName"]').send_keys("Jane")
last_name = driver.find_element_by_xpath('//*[@id="PayeeLastName"]').send_keys("Smith")

# Address
street = driver.find_element_by_xpath('//*[@id="PayeeStreet"]').send_keys("123 Street Ave")
street_cont = driver.find_element_by_xpath('//*[@id="PayeeStreet2"]').send_keys("")
city = driver.find_element_by_xpath('//*[@id="PayeeCity"]').send_keys("Berkeley")
state = driver.find_element_by_xpath('//*[@id="PayeeState"]').send_keys("CA")
zip_code = driver.find_element_by_xpath('//*[@id="PayeeZipCode"]').send_keys("94704")

######### Additional Information #########

# University ID
is_berkeley_student = driver.find_element_by_xpath('//*[@id="28262917"]').click()
uid = driver.find_element_by_xpath('//*[@id="answerTextBox-28262917-free"]').send_keys("1234567")

# Contact Info
email = driver.find_element_by_xpath('//*[@id="answerTextBox-13557646-free"]').send_keys("maggiedluo@berkeley.edu")
phone = driver.find_element_by_xpath('//*[@id="answerTextBox-13557622-free"]').send_keys("1234567890")
expenditure_action = driver.find_element_by_xpath('//*[@id="dropDown-2483087"]')
for option in expenditure_action.find_elements_by_tag_name('option'):
    if option.text == 'Hold for Pickup-LEAD Ctr, 432 Eshleman Hall':
        option.click()
        break

# Submit - uncomment if you want the script to auto-submit
# submit = driver.find_element_by_xpath('//*[@id="saveButton"]').click()


# driver.close()