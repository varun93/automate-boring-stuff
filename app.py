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
from parse_csv import parseData

def saveCookies(driver):
    pickle.dump(driver.get_cookies() , open("cookies.pkl", "wb"))

def addCookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def enterData(registrationNumber, data, driver):

    farmerSearchElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtFarmerSearch")
    farmerSearchElement.send_keys(registrationNumber)

    farmerSearchAction = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnFarmerSearch")
    farmerSearchAction.click()

    WebDriverWait(driver, 10).until(EC.staleness_of(driver.find_element_by_id("ctl00_ContentPlaceHolder1_gvfarmerDetails")))

    viewFarmer = driver.find_element_by_id("ctl00_ContentPlaceHolder1_gvfarmerDetails_ctl02_lnkAddfarm")
    viewFarmer.send_keys(Keys.RETURN)

    addEditElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_GVFarmEntry_ctl02_imgbtnNewAdd")
    addEditElement.send_keys(Keys.RETURN)

    products = data[registrationNumber]
    
    for product in products:

        productCode = product["productCode"]
        # print(productCode)

        # 
        productDetails = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtSearchValue")
        productDetails.clear()
        productDetails.send_keys(productCode)
        productDetails.send_keys(Keys.RETURN)

        productHyperlink = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Grdview_ctl02_lnkView"))
        )

        # productHyperlink = WebDriverWait(driver, 20).until(
        #     EC.staleness_of((By.ID, "ctl00_ContentPlaceHolder1_Grdview_ctl02_lnkView"))
        # )
        
        # print("Passed the hurdle!")

        productHyperlink.click()

        cropTypeData = product["cropType"]
        cropVarietyData = product["cropVariety"]
        cropAreaData = product["cropArea"]
        cropSeasonData = product["cropSeason"]
        cropHarvestData = product["cropHarvest"]
        expectedYieldData = product["expectedYield"]

        # Crop Type
        cropType = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLCropType'))
        cropType.select_by_value(cropTypeData)

        # Crop Variety
        cropVariety = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtVariety")
        cropVariety.send_keys(cropVarietyData)

        # Crop Area
        cropArea = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtTotalArea")
        cropArea.send_keys(cropAreaData)

        # Season
        season = driver.find_element_by_xpath("//label[normalize-space()='{}']/preceding-sibling::input".format(cropSeasonData))
        season.click()

        # Estimated Quantity
        try:
            estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
            estimatedQuantity.click()
            estimatedQuantity.clear()
            estimatedQuantity.send_keys(expectedYieldData)

            estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
            estimatedQuantity.click()
            estimatedQuantity.clear()
            estimatedQuantity.send_keys(expectedYieldData)
        except:
            estimatedQuantity = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtQuantity")
            estimatedQuantity.click()
            estimatedQuantity.clear()
            estimatedQuantity.send_keys(expectedYieldData)

        # Harvesting Technique
        try:
            harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
            harvestingTechnique.select_by_value(cropHarvestData)
            harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
            harvestingTechnique.select_by_value(cropHarvestData)
        except:
            harvestingTechnique = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_DDLHarvestingTechnique'))
            harvestingTechnique.select_by_value(cropHarvestData)

        driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSave").click()

        # go back
        # driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnback").click()


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# get instance of a driver
driver = webdriver.Chrome()

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

scopeCertificationItem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 
    "#ctl00_HorizontalMenu1_tdmenu > div > ul > li:nth-child(5)"))
)

scopeCertificationItem.click()

renewalMenuItem = scopeCertificationItem.find_element_by_css_selector("ul > li:nth-child(2)")
renewalMenuItem.click()

farmerDetailsElement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnFarmerDetails")
farmerDetailsElement.click()

driver.implicitly_wait(10)

driver.switch_to.frame(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ifrmID"))

data = parseData()

# for registrationNumber in data:
registrationNumber = "TN2704001157"
enterData(registrationNumber, data, driver)

driver.close()