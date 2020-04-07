#!/usr/bin/env python

import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from sheets import *

# Find your profile path by visiting chrome://version in Google Chrome
PROFILE_PATH = ''

try:
	# Get all Stage 0 (Unsubmitted) Reimbursements
	sheet = Reimbursements()
	build = sheet.build_spreadsheet()
	incomplete = sheet.get_incomplete()

	if not incomplete:
		print("There are no reimbursements in Stage 0.")
	else:
		# Set Google Profile and configure the browser
		options = webdriver.ChromeOptions()
		options.add_argument("user-data-dir=C:" + PROFILE_PATH)
		browser = webdriver.Chrome(executable_path='./chromedriver', options=options)

		# Open browser
		browser.get("https://callink.berkeley.edu/actioncenter/organization/anova/finance")

		# Save your login cookie each time you open Chrome
		pickle.dump(browser.get_cookies(), open("CallinkCookie.pkl","wb"))

		for pr in incomplete:
			new_request = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="createRequestToggle"]')))
			new_request.click()
			create_pr = browser.find_element_by_xpath('//*[@id="createRequestSection"]/ul/li/a').click()

			# Request Details
			subject = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Subject"]')))
			subject = browser.find_element_by_xpath('//*[@id="Subject"]')
			subject.send_keys(pr['first_name'] + ' ' + pr['last_name'] + ', ' + pr['description'])
			requested_amount = browser.find_element_by_xpath('//*[@id="RequestedAmount"]').send_keys(pr['amount'])

			category = browser.find_element_by_xpath('//*[@id="CategoryId"]')
			for option in category.find_elements_by_tag_name('option'):
			    if option.text == 'Check Reimbursement - (Amounts over $25.00 or check to be mailed)':
			        option.click()
			        break
			
			# Select the correct account to withdraw money from
			select_account = browser.find_element_by_xpath('//*[@id="accountSelectButton"]').click()
			if pr['type'] == 'Misc':
				misc = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="84815"]')))
				misc.click()
			elif pr['type'] == 'Site':
				psc = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="96085"]')))
				psc.click()
			elif pr['type'] == 'Alcohol':
				print("Please Venmo: " + pr['first_name'] + ' ' + pr['last_name'] + ', ' + pr['description'])
				sheet.set_stage(pr['id'], 3)
			else:
				continue 

			# Payee Information
			first_name = browser.find_element_by_xpath('//*[@id="PayeeFirstName"]').send_keys(pr['first_name'])
			last_name = browser.find_element_by_xpath('//*[@id="PayeeLastName"]').send_keys(pr['last_name'])
			street = browser.find_element_by_xpath('//*[@id="PayeeStreet"]').send_keys(pr['street'])
			# street_cont = browser.find_element_by_xpath('//*[@id="PayeeStreet2"]').send_keys("")
			city = browser.find_element_by_xpath('//*[@id="PayeeCity"]').send_keys(pr['city'])
			state = browser.find_element_by_xpath('//*[@id="PayeeState"]').send_keys(pr['state'])
			zip_code = browser.find_element_by_xpath('//*[@id="PayeeZipCode"]').send_keys(pr['zip'])

			# Additional Information
			is_berkeley_student = browser.find_element_by_xpath('//*[@id="28262917"]').click()
			uid = browser.find_element_by_xpath('//*[@id="answerTextBox-28262917-free"]').send_keys(pr['university_id'])
			email = browser.find_element_by_xpath('//*[@id="answerTextBox-13557646-free"]').send_keys(pr['email'])
			phone = browser.find_element_by_xpath('//*[@id="answerTextBox-13557622-free"]').send_keys(pr['phone'])
			expenditure_action = browser.find_element_by_xpath('//*[@id="dropDown-2483087"]')
			for option in expenditure_action.find_elements_by_tag_name('option'):
			    if option.text == pr['expenditure']:
			        option.click()
			        break

			# Submit
			submit = browser.find_element_by_xpath('//*[@id="saveButton"]').click()

			# Update spreadsheet so that the current purchase request is set to stage 1
			sheet.set_stage(pr['id'], 1)
			print("Purchase request created for " + pr['first_name'] + ' ' + pr['last_name'] + ', ' + pr['description'])
except InvalidArgumentException:
	print("Please close all open Google Chrome windows before continuing.")