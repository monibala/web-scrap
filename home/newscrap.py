import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
class GoogleMapsScraper:
    def __init__(self, query):
        self.query = query

    def scrape_google_maps(self, search_query, max_results=5):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Uncomment for headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--window-size=1920x1080')

        # Automatically download and use the correct ChromeDriver version
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com/maps")

        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)  # Allow initial results to load

            for business_data in self._collect_businesses(driver, max_results):
                yield business_data

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            driver.quit()

    def _collect_businesses(self, driver, max_results):
        scraped_names = set()
        result_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 10

        while result_count < max_results and scroll_attempts < max_scroll_attempts:
            try:
                results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
                )

                for i, result in enumerate(results):
                    name = result.get_attribute("aria-label")

                    # Skip if already scraped
                    if not name or name in scraped_names:
                        continue

                    scraped_names.add(name)
                    print(f"Scraped Business: {name}")

                    # Extract link and open details in a new tab
                    link = result.get_attribute("href")
                    if not link:
                        continue

                    business_details = self._scrape_details_in_new_tab(driver, link)
                    business_details["name"] = name
                    business_details["link"] = link

                    yield business_details
                    result_count += 1

                    if result_count >= max_results:
                        return

                # Scroll down to load more results
                driver.execute_script("arguments[0].scrollIntoView();", results[-1])
                time.sleep(3)
                scroll_attempts = 0  # Reset scroll attempts
            except Exception as e:
                print(f"Error during scraping: {e}")
                scroll_attempts += 1

    def _scrape_details_in_new_tab(self, driver, link):
        """Scrape business details by opening the link in a new tab."""
        details = {"mobiles": [], "websites": [], "addresses": []}

        try:
            # Open new tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

            # Load the business link
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class^="Io6YTe"]'))
            )

            # Scrape details
            elements = driver.find_elements(By.CSS_SELECTOR, '[class^="Io6YTe"]')
            for el in elements:
                text = el.text.strip()

                if text.startswith("+") or text.replace(" ", "").isdigit():
                    details["mobiles"].append(text)
                elif "http" in text or ".com" in text:
                    details["websites"].append(text)
                else:
                    details["addresses"].append(text)

            print(f"Scraped Details: {details}")
            return details
        except Exception as e:
            print(f"Error scraping details: {e}")
        finally:
            # Close the tab and return to the main window
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        return details
