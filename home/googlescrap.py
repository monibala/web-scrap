# import logging
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# # Logging setup
# logger = logging.getLogger(__name__)

# # Global stores for scraped and sent data
# scraped_data_store = []
# sent_data_store = []

# # Utility functions
# def add_scraped_data(new_data):
#     global scraped_data_store
#     for data in new_data:
#         if data not in scraped_data_store:
#             scraped_data_store.append(data)

# def get_new_data():
#     global scraped_data_store, sent_data_store
#     new_data = []
#     for data in scraped_data_store:
#         if data not in sent_data_store:
#             new_data.append(data)
#             sent_data_store.append(data)
#     return new_data


# class GoogleMapsScraper:
#     def __init__(self, query):
#         self.query = query

#     def scrape_progressively(self):
#         businesses = self.scrape_google_maps(self.query)
#         for business in businesses:
#             print(f"Yielding business: {business}")
#             yield business
#             time.sleep(1)
    

#     def scrape_google_maps(self, search_query, max_results=10):
#         chrome_options = Options()
#         # chrome_options.add_argument("--headless")  # Uncomment if you want headless mode
#         chrome_options.add_argument("--disable-gpu")

#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get("https://www.google.com/maps")
#         logger.info("Google Maps loaded")

#         try:
#             # Search for the query
#             search_box = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "searchboxinput"))
#             )
#             search_box.send_keys(search_query)
#             search_box.send_keys(Keys.RETURN)
#             logger.info("Scraper started")
#             time.sleep(5)

#             # Yield businesses progressively
#             yield from self._collect_businesses(driver, max_results)

#         except Exception as e:
#             logger.error(f"Error occurred: {e}")
#         finally:
#             driver.quit()

#     def _collect_businesses(self, driver, max_results):
#         business_names = []
#         business_links = []
#         previous_results_len = 0
#         result_count = 0

#         while result_count < max_results:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
#             )

#             results = driver.find_elements(By.CLASS_NAME, "hfpxzc")
#             current_results_len = len(results)

#             if current_results_len == previous_results_len:
#                 logger.info("End of list reached.")
#                 break

#             previous_results_len = current_results_len

#             for result in results[result_count:max_results]:
#                 name = result.get_attribute("aria-label")
#                 link = result.get_attribute("href")

#                 if name and name not in business_names:
#                     business_names.append(name)
#                     business_links.append(link)
#                     result_count += 1
#                     logger.info(f"Scraped business: {name}")
#                     yield {"name": name, "link": link}  # Yielding data incrementally

#                     # Display immediately
#                     print(f"Scraped Business: {name}, Link: {link}", flush=True)

#             # Scroll down to load more
#             driver.execute_script("arguments[0].scrollIntoView();", results[-1])
#             time.sleep(2)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging

# Logging setup
logger = logging.getLogger(__name__)

class GoogleMapsScraper:
    def __init__(self, query):
        self.query = query

    def scrape_google_maps(self, search_query, max_results=10):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com/maps")
        logger.info("Google Maps loaded")

        try:
            # Search for the query
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            logger.info("Search initiated")
            time.sleep(5)

            # Fetch basic business information and details
            # return self._collect_businesses(driver, max_results)
            # Yield businesses progressively
            yield from self._collect_businesses(driver, max_results)

        except Exception as e:
            logger.error(f"Error occurred: {e}")
        finally:
            driver.quit()

    def _collect_businesses(self, driver, max_results):
        business_details = []
        result_count = 0
        previous_results_len = 0

        while result_count < max_results:
            # Wait for results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
            )

            results = driver.find_elements(By.CLASS_NAME, "hfpxzc")
            current_results_len = len(results)

            if current_results_len == previous_results_len:
                logger.info("End of list reached.")
                break

            previous_results_len = current_results_len

            for result in results[result_count:max_results]:
                if result_count >= max_results:
                    break

                # Scrape business name
                name = result.get_attribute("aria-label")
                link = result.get_attribute("href")

                if name:
                    logger.info(f"Scraped business: {name}")
                    business_detail = self._scrape_details(driver, link)
                    business_detail["name"] = name
                    # business_details.append(business_detail)
                    yield business_detail
                    result_count += 1

            # Scroll to load more results
            driver.execute_script("arguments[0].scrollIntoView();", results[-1])
            time.sleep(20)

        return business_details

    def _scrape_details(self, driver, link):
        """Scrape additional details from the business details page."""
        details = {"addresses": [], "mobiles": [], "websites": []}

        try:
            driver.get(link)
            time.sleep(15)  # Allow details page to load

            script = """
            let details = {addresses: [], mobiles: [], websites: []};
            let elements = document.querySelectorAll('[class^="Io6YTe"]');  // Matches classes starting with Io6YTe

            elements.forEach((el) => {
                let text = el.textContent.trim();
                if (/^\\+?[\\d\\s()-]+$/.test(text)) {
                    details.mobiles.push(text);  // Mobile numbers
                } else if (text.includes("http") || text.includes(".com")) {
                    details.websites.push(text);  // Websites
                } else {
                    details.addresses.push(text);  // Addresses
                }
            });
            return details;
            """
            details.update(driver.execute_script(script))
        except Exception as e:
            logger.error(f"Error scraping details: {e}")

        return details
