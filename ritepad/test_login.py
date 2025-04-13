from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to Edge WebDriver
driver_path = r"C:/Users/Hashi/Downloads/edgedriver_win64/msedgedriver.exe"  # Update to your actual path

# Set up WebDriver
service = Service(driver_path)
driver = webdriver.Edge(service=service)

try:
    # Open the login page
    driver.get("http://127.0.0.1:8000/login")  # Replace with the correct URL of your login page

    # Maximize the browser window
    driver.maximize_window()

    # Wait for the username field to be visible
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Locate and fill in the username field
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("testuser")  # Replace with a valid username

    # Locate and fill in the password field
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("Test@1234")  # Replace with the corresponding password

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for redirection or error message
    time.sleep(3)

    # Check if login was successful by URL or page content
    if "/read" in driver.current_url:
        print("Login test passed: Successfully redirected to the reading page.")
    else:
        # Check for error message
        error_message = driver.find_element(By.TAG_NAME, "body").text
        print(f"Login test failed: {error_message}")

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # Close the browser
    driver.quit()
