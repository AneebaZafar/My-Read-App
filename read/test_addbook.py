from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.edge.service import Service

# Path to your webdriver
driver_path = 'C:/Users/Hashi/Downloads/edgedriver_win64/msedgedriver.exe'

def test_add_book():
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    
    try:
        driver.get("http://localhost:8000/login")
        
        # Login
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for redirect after login
        time.sleep(5)
        
        driver.get("http://localhost:8000/read/addbook/")
        
        # Fill out the form fields
        driver.find_element(By.ID, 'book_name').send_keys("Test Book Title")
        driver.find_element(By.ID, 'book_author').send_keys("Test Author")
        driver.find_element(By.ID, 'book_genre').send_keys("supernatural")
        driver.find_element(By.ID, 'description').send_keys("This is a test description of the book.")
        driver.find_element(By.ID, 'pub_date').send_keys("20/11/2024")
        driver.find_element(By.ID, 'image').send_keys(r"C:\Users\Hashi\Desktop\images\supernatural3.jpg")

        # Wait for the submit button to be clickable and then click it
        
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sub_btn"))
        )
        submit_button.click()

        # Wait for a while to ensure the form submission is processed
        time.sleep(5)

        # Verify the page URL after submission
        if "/read/addbook/" in driver.current_url:
            print(f"Testing passed")
        else:
            print(f"Testing Failed. Current URL: {driver.current_url}")
        
    finally:
        driver.quit()

# Run the test
if __name__ == "__main__":
    test_add_book()
