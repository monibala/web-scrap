from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from home.models import ScrapedData
from selenium.webdriver.chrome.options import Options
import logging
logger = logging.getLogger(__name__)
scraped_data_store = []
sent_data_store = []
def add_scraped_data(new_data):
    global scraped_data_store
    for data in new_data:
        if data not in scraped_data_store:
            scraped_data_store.append(data)
    # scraped_data_store.extend(new_data)
def get_new_data():
    global scraped_data_store,sent_data_store
    new_data = []
    for data in scraped_data_store:
        if data not in sent_data_store:
            new_data.append(data)
            sent_data_store.append(data)
    return new_data
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.action_chains import ActionChains

def scroll_element(driver, element, scroll_distance=500, pause_time=2):
    action = ActionChains(driver)
    current_scroll_position = 0

    while True:
        # Scroll down
        action.move_to_element(element).perform()
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];", element, scroll_distance)
        time.sleep(pause_time)

        # Check if scrolling has reached the bottom
        new_scroll_position = driver.execute_script("return arguments[0].scrollTop", element)
        if new_scroll_position == current_scroll_position:
            break  # Exit if no new content is loaded

        current_scroll_position = new_scroll_position

class GoogleMapsScraper:
    def __init__(self, query):
        self.query = query

    def scrape_progressively(self):
        # Start scraping
        businesses = self.scrape_google_maps(self.query)

        # Yield each business one by one
        for business in businesses:
            print(f"Yielding business: {business}") 
            yield business
            time.sleep(1) 
    def scrape_google_maps(self, search_query, yield_partial=False,max_results=8):
        # Set up Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Disable GPU (useful in headless mode)

        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com/maps")
        print("Google Maps loaded")

        # Wait for the search box to load
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        logger.info("Scraper Started")
        time.sleep(5)  # Allow time for initial results to load

        try:
            businesses = []
            business_names = []
            business_links = []
            previous_results_len = 0
            result_count = 0  # Initialize counter to track results

            while result_count < max_results:
            # To display all results set while True
            # while True:
                # Wait for the results to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
                )

                # Get all the results
                results = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                current_results_len = len(results)
                print(f"Number of results loaded: {current_results_len}")

                # Check if the number of results has increased
                if current_results_len == previous_results_len:
                    print("End of list reached.")
                    break  # If no new results are added, stop scrolling

                previous_results_len = current_results_len

                # Extract business names and links
                for result in results:
                    # Include this if stmt if we limit the results
                    if result_count >= max_results:
                        break 
                    name = result.get_attribute("aria-label")
                    if name and name not in business_names:
                        business_names.append(name)

                    link = result.get_attribute("href")
                    if link and link not in business_links:
                        business_links.append(link)

                # Scroll to the last result to load more
                driver.execute_script("arguments[0].scrollIntoView();", results[-1])
                time.sleep(3)  # Wait for more results to load

            print(f"Names: {business_names}")
            print(f"Links: {business_links}")

            # Append data to businesses list
            businesses = [{"name": name, "link": link} for name, link in zip(business_names, business_links)]

            # Scrape detailed information for each business
            business_details = []
            for link, name in zip(business_links, business_names):
                driver.get(link)
                time.sleep(5)  # Allow details page to load

                # Javascript to scrape additional details
                script = """
                let results = {addresses: [], mobiles: [], websites: []};
                let elements = document.querySelectorAll('.Io6YTe.fontBodyMedium, .Io6YTe.fontBodyLarge');
                elements.forEach((el) => {
                    let text = el.textContent.trim();
                    if (text.match(/^\\+?[\\d\\s()-]+$/)) results.mobiles.push(text);  // Mobile numbers
                    else if (text.includes("http") || text.includes(".com")) results.websites.push(text);  // Websites
                    else results.addresses.push(text);  // Addresses
                });
                return results;
                """
                details = driver.execute_script(script)

                business_details.append({
                    "name": name,
                    "link": link,
                    "addresses": details["addresses"],
                    "mobiles": details["mobiles"],
                    "websites": details["websites"],
                })

            businesses.extend(business_details)
            add_scraped_data(businesses)
            print(businesses)

            if yield_partial:
                yield business_details

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            driver.quit()

        return businesses



    # def scrape_google_maps(self,search_query,yield_partial = False):
    #     # Set up Chrome options (optional)
    #     # options = webdriver.ChromeOptions()
    #     # options.add_argument('--start-maximized')  # Option to start the browser maximized
    #     # options.add_argument("--headless")
    #     # options.add_argument("--disable-gpu")
    #     # Set up Chrome options
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")  # Enable headless mode
    #     chrome_options.add_argument("--disable-gpu")  # Disable GPU (can be useful in headless mode)

    #     # Initialize WebDriver with headless mode
    #     driver = webdriver.Chrome(options=chrome_options)
    #     # Initialize ChromeDriver with WebDriver Manager
    #     # driver = webdriver.Chrome(
    #     #     service=ChromeService(ChromeDriverManager().install()),  # Automatically manage and install ChromeDriver
    #     #     options=options  # Use the defined options (like 'start-maximized')
    #     # )

    #     driver.get("https://www.google.com/maps")
    #     print("Google Maps loaded")

    #     # Wait for the search box to load
    #     search_box = driver.find_element(By.ID, "searchboxinput")
    #     search_box.send_keys(search_query)
    #     search_box.send_keys(Keys.RETURN)
    #     logger.info("Scraper Started")
    #     time.sleep(50)  # Allow time for results to load
        
    #     businesses = []

    #     try:
    #         # Find all elements that hold restaurant names
    #         elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    #         business_names = []

    #         # Extract restaurant names using the aria-label attribute
    #         for element in elements:
    #             name = element.get_attribute("aria-label")
    #             if name:  # Ensure non-empty names
    #                 business_names.append(name)
            
    #         print(f"Names: {business_names}")
            
    #         business_links = []
    #         try:
    #             elements = driver.find_elements(By.CSS_SELECTOR, '.hfpxzc')  # Selector for search result elements
    #             for elem in elements:
    #                 link = elem.get_attribute("href")
    #                 if link:
    #                     business_links.append(link)
    #         except Exception as e:
    #             print(f"Error scraping business links: {e}")

    #         # print(f"Found {len(business_links)} business links.")

            
    #         business_details = []
    #         try:
    #             # Extract business links
    #             elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    #             business_links = [elem.get_attribute("href") for elem in elements if elem.get_attribute("href")]

    #             # print(f"Found {len(business_links)} business links.")

                
    #             for link,name in zip(business_links,business_names):
    #                 driver.get(link)
    #                 time.sleep(5)

    #                 # Javascript code 
    #                 script = """
    #                 let results = {addresses: [], mobiles: [], websites: []};
                    
    #                 let elements = document.querySelectorAll('.Io6YTe.fontBodyMedium, .Io6YTe.fontBodyLarge');
    #                 elements.forEach((el) => {
    #                     let text = el.textContent.trim();
    #                     // Mobile number
    #                     if (text.match(/^\\+?\\(?\\d{1,4}\\)?[\\s-]?\\d{2,5}[\\s-]?\\d{4,5}$/) || text.match(/^\\d{3,4}[\\s\\-]?\\d{4,5}$/)) {
    #                         results.mobiles.push(text);
    #                     } 
    #                     // Match websites (simple check for .com, .edu, etc.)
    #                     else if (text.includes("http") || text.includes(".com") || text.includes(".edu")) {
    #                         results.websites.push(text);
    #                     } 
    #                     // Capture addresses (simple check for street names and landmarks)
    #                     else if (!text.toLowerCase().includes("claim this business") && text.match(/[A-Za-z]+ [0-9]{1,4}/)) {
    #                         results.addresses.push(text);
    #                     }
    #                 });
    #                 return results;
    #                 """
    #                 details = driver.execute_script(script)

                    
    #                 business_details.append({
    #                     "name" : name,
    #                     "link": link,
    #                     "addresses": details["addresses"],
    #                     "mobiles": details["mobiles"],
    #                     "websites": details["websites"],
    #                 })
                    
    #             businesses.extend(business_details)
    #             add_scraped_data(businesses)
    #             print(businesses)
    #             if yield_partial:
    #                 yield business_details
    #         except Exception as e:
    #             print(f"Error occurred: {e}")

        
    #     finally:
    #         driver.quit()
        
    #     return businesses
