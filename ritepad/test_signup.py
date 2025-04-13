from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import time

# Set up the WebDriver (Ensure the correct path for your browser driver)
driver_path = r"C:\Users\Hashi\Downloads\edgedriver_win64\msedgedriver.exe"


# Set up Edge WebDriver
service = Service(driver_path)
driver = webdriver.Edge(service=service)
try:
    # Open the signup page
    driver.get("http://127.0.0.1:8000/")  # Replace with your local or hosted signup URL
    
    # Maximize browser window for better visibility
    driver.maximize_window()
    
    # Locate and interact with the username field
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("testuser")
    
    # Locate and interact with the email field
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("testuser@example.com")
    
    # Locate and interact with the password fields
    password1_input = driver.find_element(By.ID, "password1")
    password1_input.send_keys("Test@1234")
    
    password2_input = driver.find_element(By.ID, "password2")
    password2_input.send_keys("Test@1234")
    
    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    
    # Wait for the response page to load
    time.sleep(3)
    
    # Check if redirected to the login page or a success message is displayed
    if "login/" in driver.current_url:
        print("Signup test passed: Redirected to login page.")
    else:
        # Capture any validation errors or failure messages
        error_message = driver.find_element(By.TAG_NAME, "body").text
        print(f"Signup test failed: {error_message}")

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # Close the browser
    driver.quit()
