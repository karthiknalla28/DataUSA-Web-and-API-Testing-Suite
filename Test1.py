import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataUSAHomePage:
    """
    A class to represent and interact with the Data USA homepage in a web browser.
    It provides functionality to navigate to different sections of the website.
    """

    def __init__(self, driver):
        """
        Initializes a new instance of the DataUSAHomePage class.
        
        :param driver: Selenium WebDriver to control the browser.
        """
        self.driver = driver

    def navigate_to_section(self, section_link, wait_time=0):
        """
        Navigates to a specific section of the Data USA website by clicking its link.
        
        :param section_link: CSS selector for the link to the section.
        :param wait_time: Optional time in seconds to wait after navigation.
        """
        try:
            # Wait until the link is visible and then click it
            link = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, section_link))
            )
            link.click()

            # Wait until the body of the new page is present, indicating the page has loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Optionally wait for additional time specified by the user
            if wait_time > 0:
                time.sleep(wait_time)
        except TimeoutException:
            print(f"Loading the {section_link} section took too long!")
        except NoSuchWindowException:
            print("The browser window was closed unexpectedly.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def init_driver(browser_name):
    """
    Initializes and returns a WebDriver instance for the specified browser.

    :param browser_name: Name of the browser (e.g., 'Edge', 'Chrome', 'Firefox').
    :return: WebDriver instance for the specified browser.
    """
    if browser_name == "Edge":
        return webdriver.Edge()
    elif browser_name == "Chrome":
        return webdriver.Chrome()
    elif browser_name == "Firefox":
        return webdriver.Firefox()
    else:
        raise ValueError("The specified browser is not supported.")

def smooth_scroll(driver, scroll_duration):
    """
    Smoothly scrolls down the webpage over the specified duration.
    
    :param driver: Selenium WebDriver instance controlling the browser.
    :param scroll_duration: Duration in milliseconds over which to scroll down.
    """
    end_time = time.time() + scroll_duration / 1000  # Convert duration to seconds
    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, 20);")  # Scroll down by 20 pixels
        time.sleep(0.02)  # Short pause (20 ms) between scrolls

if __name__ == "__main__":
    # Set the browser to use (change to 'Edge' or 'Firefox' as needed)
    browser_name = "Chrome"

    # Initialize the web driver for the specified browser and maximize the browser window
    driver = init_driver(browser_name)
    driver.maximize_window()

    # Create an instance of the DataUSAHomePage class
    data_usa_home = DataUSAHomePage(driver)

    # Open the Data USA homepage
    driver.get("https://datausa.io")

    # Perform smooth scrolling for 5 seconds
    smooth_scroll(driver, 5000)

    # Wait for a few seconds before navigating to a different section
    time.sleep(3)

    # Navigate to the 'About' section and wait for 3 seconds after navigation
    data_usa_home.navigate_to_section("a[href='/about']", wait_time=3)

    # Navigate to the 'Maps' section and wait for 3 seconds after navigation
    data_usa_home.navigate_to_section("a[href='/map']", wait_time=3)

    # Wait for user input in the console before closing the browser
    input("Press Enter in the console to close the browser...")
    driver.quit()
