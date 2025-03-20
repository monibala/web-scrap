import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Logging setup
logger = logging.getLogger(__name__)

# Global stores for scraped and sent data
scraped_data_store = []
sent_data_store = []

# Utility functions
def add_scraped_data(new_data):
    global scraped_data_store
    for data in new_data:
        if data not in scraped_data_store:
            scraped_data_store.append(data)

def get_new_data():
    global scraped_data_store, sent_data_store
    new_data = []
    for data in scraped_data_store:
        if data not in sent_data_store:
            new_data.append(data)
            sent_data_store.append(data)
    return new_data

def scroll_element(driver, element, scroll_distance=500, pause_time=2):
    action = ActionChains(driver)
    current_scroll_position = 0

    while True:
        action.move_to_element(element).perform()
        driver.execute_script("arguments[0].scrollTop += arguments[1];", element, scroll_distance)
        time.sleep(pause_time)
        new_scroll_position = driver.execute_script("return arguments[0].scrollTop", element)
        if new_scroll_position == current_scroll_position:
            break
        current_scroll_position = new_scroll_position

# Scraper class
class GoogleMapsScraper:
    def __init__(self, query):
        self.query = query

    def scrape_progressively(self):
        businesses = self.scrape_google_maps(self.query)
        for business in businesses:
            print(f"Yielding business: {business}")
            yield business
            time.sleep(1)

    def scrape_google_maps(self, search_query, yield_partial=False, max_results=100):
        chrome_options = Options()
        # Uncomment below for headless mode
        chrome_options.add_argument("--headless")
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
            logger.info("Scraper started")
            time.sleep(5)

            # Collect business details
            businesses = self._collect_businesses(driver, max_results)
            add_scraped_data(businesses)

            if yield_partial:
                yield businesses

        except Exception as e:
            logger.error(f"Error occurred: {e}")
        finally:
            driver.quit()

        return businesses

    def _collect_businesses(self, driver, max_results):
        businesses = []
        business_names = []
        business_links = []
        previous_results_len = 0
        result_count = 0

        while result_count < max_results:
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
                name = result.get_attribute("aria-label")
                link = result.get_attribute("href")

                if name and name not in business_names:
                    business_names.append(name)
                    business_links.append(link)
                    result_count += 1

            # Scroll down to load more
            driver.execute_script("arguments[0].scrollIntoView();", results[-1])
            time.sleep(2)

        businesses = [
            {"name": name, "link": link}
            for name, link in zip(business_names, business_links)
        ]
        return self._scrape_detailed_info(driver, businesses)

    def _scrape_detailed_info(self, driver, businesses):
        business_details = []

        for business in businesses:
            driver.get(business["link"])
            time.sleep(2)

            try:
                script = """
                let results = {addresses: [], mobiles: [], websites: []};
                let elements = document.querySelectorAll('.Io6YTe.fontBodyMedium, .Io6YTe.fontBodyLarge');
                elements.forEach(el => {
                    let text = el.textContent.trim();
                    if (text.match(/^\\+?[\\d\\s()-]+$/)) results.mobiles.push(text);
                    else if (text.includes("http") || text.includes(".com")) results.websites.push(text);
                    else results.addresses.push(text);
                });
                return results;
                """
                details = driver.execute_script(script)
                business_details.append({
                    "name": business["name"],
                    "link": business["link"],
                    "addresses": details["addresses"],
                    "mobiles": details["mobiles"],
                    "websites": details["websites"],
                })
            except Exception as e:
                logger.warning(f"Failed to fetch details for {business['name']}: {e}")

        return business_details
