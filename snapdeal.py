import time
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

def isLoaded(driver):
	return driver.find_element_by_tag_name("body") != None

WAIT_TIME = 10
INC = False

test_username = raw_input("Enter your snapdeal username: ")
test_password = raw_input("Enter you snapdeal password: ")

driver = webdriver.PhantomJS()

try:
	print "Opening Snapdeal"
	driver.get("https://www.snapdeal.com/login")
	wait = ui.WebDriverWait(driver, WAIT_TIME)
	wait.until(isLoaded)

	print "Entering email"
	emailVal = driver.find_element_by_id("userName")
	emailVal.clear()
	emailVal.send_keys(test_username)
	driver.find_element_by_id("checkUser").click()

	try:
		print "Entering password"
		wait = ui.WebDriverWait(driver, WAIT_TIME)
		passwordVal = wait.until(expected_conditions.element_to_be_clickable((By.ID,'j_password_login_uc')))
		passwordVal.clear()
		passwordVal.send_keys(test_password)
		driver.find_element_by_id("submitLoginUC").click()

	except Exception, e:
		print "Incorrect credentials"
		INC = True

	if not INC:
		print "Waiting for page to load"
		
		try:
			wait = ui.WebDriverWait(driver, WAIT_TIME)
			wait.until(lambda driver: driver.current_url == "https://www.snapdeal.com/?loginSuccess=success&")
		except Exception, e:
			pass
		finally:
			print driver.current_url
		
			if driver.current_url == "https://www.snapdeal.com/?loginSuccess=success&":
				print "Adding Google Pixel to the cart"
				driver.get("https://www.snapdeal.com/product/google-pixel-32gb-quite-black/645205836557")
				wait = ui.WebDriverWait(driver, WAIT_TIME)
				cartVal = wait.until(expected_conditions.element_to_be_clickable((By.ID,'add-cart-button-id')))
				cartVal.click()

				print "Logging you out"
				wait = ui.WebDriverWait(driver, WAIT_TIME)		
				driver.get("https://www.snapdeal.com/logout")
				wait = ui.WebDriverWait(driver, WAIT_TIME)
				wait.until(isLoaded)
			else:
				print "Incorrect credentials"
	
except Exception, e:
	print "Error - Check screenshot."
	driver.save_screenshot('error.png')

driver.quit()
