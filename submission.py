#!/usr/bin/env python

import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sheets import *

# Set Google Profile and driver
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:/Users/maggieluo/Library/Application Support/Google/Chrome/Default")
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

# Open browser
driver.get("https://callink.berkeley.edu/actioncenter/organization/anova/finance")

# Save your login cookie each time you open Chrome
pickle.dump(driver.get_cookies(), open("CallinkCookie.pkl","wb"))

# Get all Stage 0 (Unsubmitted) Reimbursements
sheet = Reimbursements().build_spreadsheet()
incomplete = sheet.get_incomplete()

for i in range(len(incomplete)):
	pr = incomplete[i]
	new_request = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="createRequestToggle"]')))
	new_request.click()
	create_pr = driver.find_element_by_xpath('//*[@id="createRequestSection"]/ul/li/a').click()

	# Request Details
	subject = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Subject"]')))
	subject = driver.find_element_by_xpath('//*[@id="Subject"]')
	subject.send_keys(pr['first_name'] + ' ' + pr['last_name'] + ', ' + pr['description'])
	requested_amount = driver.find_element_by_xpath('//*[@id="RequestedAmount"]').send_keys(pr['amount'])

	category = driver.find_element_by_xpath('//*[@id="CategoryId"]')
	for option in category.find_elements_by_tag_name('option'):
	    if option.text == 'Check Reimbursement - (Amounts over $25.00 or check to be mailed)':
	        option.click()
	        break
	
	# Select the correct account to withdraw money from
	select_account = driver.find_element_by_xpath('//*[@id="accountSelectButton"]').click()
	if pr['type'] == 'Misc':
		misc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="84815"]')))
		misc.click()
	elif pr['type'] == 'Site':
		psc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="96085"]')))
		psc.click()
	else:
		continue 

	# Payee Information
	first_name = driver.find_element_by_xpath('//*[@id="PayeeFirstName"]').send_keys(pr['first_name'])
	last_name = driver.find_element_by_xpath('//*[@id="PayeeLastName"]').send_keys(pr['last_name'])
	street = driver.find_element_by_xpath('//*[@id="PayeeStreet"]').send_keys(pr['street'])
	# street_cont = driver.find_element_by_xpath('//*[@id="PayeeStreet2"]').send_keys("")
	city = driver.find_element_by_xpath('//*[@id="PayeeCity"]').send_keys(pr['city'])
	state = driver.find_element_by_xpath('//*[@id="PayeeState"]').send_keys(pr['state'])
	zip_code = driver.find_element_by_xpath('//*[@id="PayeeZipCode"]').send_keys(pr['zip'])

	# Additional Information
	is_berkeley_student = driver.find_element_by_xpath('//*[@id="28262917"]').click()
	uid = driver.find_element_by_xpath('//*[@id="answerTextBox-28262917-free"]').send_keys(pr['university_id'])
	email = driver.find_element_by_xpath('//*[@id="answerTextBox-13557646-free"]').send_keys(pr['email'])
	phone = driver.find_element_by_xpath('//*[@id="answerTextBox-13557622-free"]').send_keys(pr['phone'])
	expenditure_action = driver.find_element_by_xpath('//*[@id="dropDown-2483087"]')
	for option in expenditure_action.find_elements_by_tag_name('option'):
	    if option.text == pr['expenditure']:
	        option.click()
	        break

	# Submit - Uncomment if you want the script to auto-submit
	submit = driver.find_element_by_xpath('//*[@id="saveButton"]').click()

	# Update spreadsheet so that the current purchase request is set to stage 2
	sheet.set_stage(pr['id'], 2)

driver.close()