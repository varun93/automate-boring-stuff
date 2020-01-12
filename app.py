from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


def saveCookies(driver):
    pickle.dump(driver.get_cookies() , open("cookies.pkl", "wb"))

def addCookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

# User Id : ctl00_ContentPlaceHolder1_txtUserID
# Password : ctl00_ContentPlaceHolder1_txtPassword
# Submit Button: ctl00_ContentPlaceHolder1_btnSubmit
# Starting Url:  https://traceability.apeda.gov.in


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# get instance of a driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
# get the required page
driver.get("https://traceability.apeda.gov.in")

# Login Page
# enter user id
userIdElem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtUserID")
userIdElem.clear()
userIdElem.send_keys(USERNAME)
# enter password
passwordElem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPassword")
passwordElem.clear()
passwordElem.send_keys(PASSWORD)
# now submit the credentials
submitElem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSubmit")
submitElem.click()

# wait for 10 seconds
driver.implicitly_wait(20)

scopeCertificationItem = driver.find_element_by_css_selector("#ctl00_HorizontalMenu1_tdmenu > div > ul > li:nth-child(5)")
scopeCertificationItem.click()

renewalMenuItem = scopeCertificationItem.find_element_by_css_selector("ul > li:nth-child(2)")
renewalMenuItem.click()

farmerDetailsElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnFarmerDetails")
farmerDetailsElement.click()

driver.implicitly_wait(10)

driver.switch_to.frame(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ifrmID"))

farmerSearchElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtFarmerSearch")
farmerSearchElement.send_keys("TN2704001157")

farmerSearchAction = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnFarmerSearch")

resultsTable = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gvfarmerDetails")
farmerSearchAction.click()
wait.until(EC.staleness_of(resultsTable))

viewFarmer = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gvfarmerDetails_ctl02_lnkAddfarm")
viewFarmer.send_keys(Keys.RETURN)

# edit the farmer details
addEditElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_GVFarmEntry_ctl02_imgbtnNewAdd")
addEditElement.send_keys(Keys.RETURN)

productDetails = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtSearchValue")
productDetails.send_keys("709601002")
productDetails.send_keys(Keys.RETURN)

driver.find_element_by_id("ctl00_ContentPlaceHolder1_Grdview_ctl02_lnkView").click()

driver.implicitly_wait(10)

# Crop Type
cropType = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLCropType'))
cropType.select_by_visible_text("Main")

# Crop Variety
cropVariety = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtVariety")
cropVariety.send_keys("Local") 

# Crop Area
cropArea = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtTotalArea")
cropArea.send_keys("1.2")

# Season
season = driver.find_element_by_xpath("//label[normalize-space()='Rabi']/preceding-sibling::input")
season.click()

# Estimated Quantity
try:
    estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
    estimatedQuantity.click()
    estimatedQuantity.clear()
    estimatedQuantity.send_keys("10.9")

    estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
    estimatedQuantity.click()
    estimatedQuantity.clear()
    estimatedQuantity.send_keys("10.9")
except:
    estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
    estimatedQuantity.click()
    estimatedQuantity.clear()
    estimatedQuantity.send_keys("10.9")

# Harvesting Technique
try:
    harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
    harvestingTechnique.select_by_visible_text("Single Harvest")
    harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
    harvestingTechnique.select_by_visible_text("Single Harvest")
except:
    harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
    harvestingTechnique.select_by_visible_text("Single Harvest")

driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSave").click()

# ========== Details Page ===================================

# Crop Type -> ctl00_ContentPlaceHolder1_DDLCropType
# Crop Variety -> ctl00_ContentPlaceHolder1_txtVariety
# Crop Area -> ctl00_ContentPlaceHolder1_txtTotalArea
# Crop Season -> ctl00_ContentPlaceHolder1_DDLSeason
# Estimated Quantity -> ctl00_ContentPlaceHolder1_txtQuantity
# Harvest -> ctl00_ContentPlaceHolder1_DDLHarvestingTechnique 
# Submit Button -> ctl00_ContentPlaceHolder1_btnSave

driver.close()
