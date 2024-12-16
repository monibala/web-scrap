import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
def setup_driver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')  # Open browser in full screen
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        return driver
    except Exception as e:
        raise RuntimeError(f"Error setting up the WebDriver: {e}")

# Perform Google Maps Search
def search_google_maps(driver, query):
    if not query:
        raise ValueError("Query parameter 'q' is required.")  # Ensure query is passed correctly
    
    print(f"Performing search for: {query}")  # Debugging line to check the query
    
    driver.get("https://www.google.com/maps")  # Navigate to Google Maps
    try:
        # Wait for the search box to load
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        
        # Ensure the search box is visible and interactable
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Nv2PK"))
        )
    except Exception as e:
        raise RuntimeError(f"Error performing search: {e}")

# Scrape Business Details
# Scrape Business Details
def scrape_business_details(driver):
    try:
        # Wait for and extract the name of the business (adjust selector as needed)
        name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "x3AX1-LfntMc-header-title-title"))
        ).text

        # Extract the photo URL (example)
        # photo = driver.find_element(By.CSS_SELECTOR, "button[jsaction*='photo']").get_attribute("style")
        # photo_url = photo.split('url("')[1].split('")')[0] if 'url("' in photo else None

        # # Extract website (if available)
        # website = None
        # try:
        #     website_element = driver.find_element(By.CSS_SELECTOR, "a[data-tooltip*='Website']")
        #     website = website_element.get_attribute("href")
        # except Exception:
        #     pass

        # Return a dictionary of extracted data
        return {
            "name": name,
            # "photo_url": photo_url,
            # "website": website,
        }
        
    except Exception as e:
        return {"error": f"Failed to scrape business details: {str(e)}"}

# Example Usage
if __name__ == "__main__":
    driver = setup_driver()
    try:
        search_google_maps(driver, "pranavs kudil mappedu")  # Ensure query is passed correctly
        details = scrape_business_details(driver)
        print(details)
    finally:
        driver.quit()
