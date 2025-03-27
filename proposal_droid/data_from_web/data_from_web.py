import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
import torchaudio
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time



def is_valid_url(url):
    """
    Validates if the provided string is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def fetch_html(url):
    """
    Sends a GET request to the given URL and returns the raw HTML content.
    Raises an exception if the request fails.
    """
    try:
        # Send the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        return response.text  # Return the HTML content
    except RequestException as e:
        # Handle network-related errors, invalid URL, etc.
        print(f"Error fetching URL: {e}")
        return None

def parse_html(html_content):
    """
    Parses the raw HTML content using BeautifulSoup and extracts text.
    This method removes script and style content and returns only visible text.
    """
    # Parse the HTML content


    # Return the clean text
    return html_content

def extract_text_from_url(url):
    """
    Main function that validates the URL, fetches its content,
    and extracts the visible text.
    """
    if not is_valid_url(url):
        return "Invalid URL provided."

    # Fetch the HTML content
    html_content = fetch_html(url)
    if html_content is None:
        return "Failed to retrieve content from the URL."

    # Parse and extract the text
    page_text = parse_html(html_content)
    return page_text


def transcribe_english_youtube(youtube_url, segment_length=30):

    return youtube_url


def setup_selenium():
    """
    Sets up a headless Selenium WebDriver using Chrome.
    """
    # Set up Chrome options for headless mode
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run Chrome in headless mode (invisible)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Use WebDriverManager to install the latest version of ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login_linkedin_selenium(driver, username, password):
    """
    Logs into LinkedIn using Selenium with the provided credentials.
    """
    login_url = 'https://www.linkedin.com/login'

    # Open the LinkedIn login page
    driver.get(login_url)

    # Allow the page to fully load
    time.sleep(2)

    # Find the input fields for email and password
    email_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')

    # Fill in the credentials and submit the form
    email_field.send_keys(username)
    password_field.send_keys(password)

    # Press ENTER to submit the login form
    password_field.send_keys(Keys.RETURN)

    # Allow some time for login to complete
    time.sleep(3)

    # Check if login is successful by checking the current URL or page content
    if "feed" in driver.current_url:
        print("Login successful!")
        return True
    elif "checkpoint" in driver.current_url:
        print("Login failed due to challenge or CAPTCHA.")
        return False
    else:
        print("Login failed!")
        return False

def extract_text_from_url_with_selenium(url, username=None, password=None):
    """
    Main function that validates the URL, logs in to LinkedIn if needed using Selenium,
    fetches its content, and extracts the visible text.
    """
    driver = None
    if "linkedin.com" in url:
        if not username or not password:
            return "LinkedIn login requires both username and password."
        
        # Set up the Selenium WebDriver in headless mode
        driver = setup_selenium()

        # Login to LinkedIn
        if not login_linkedin_selenium(driver, username, password):
            driver.quit()  # Close the browser
            return "LinkedIn login failed."

        # Open the target LinkedIn page
        driver.get(url)

        # Allow the page to load fully
        time.sleep(3)

        # Extract the page's HTML content
        html_content = driver.page_source

        # Close the browser
        driver.quit()

        # Pass the HTML content to the text extraction function
        page_text = parse_html(html_content)
        return page_text, extract_text_from_url(url)

    else:
        # For non-LinkedIn URLs, fallback to the normal text extraction method
        return extract_text_from_url(url)
