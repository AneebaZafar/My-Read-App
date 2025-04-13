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
        driver.find_element(By.ID, 'book_name').send_keys("Test Book Title2")
        driver.find_element(By.ID, 'book_author').send_keys("Test Author2")
        driver.find_element(By.ID, 'book_genre').send_keys("supernatural")
        driver.find_element(By.ID, 'description').send_keys("This is a test description of the book.")
        driver.find_element(By.ID, 'pub_date').send_keys("20/11/2024")
        driver.find_element(By.ID, 'image').send_keys(r"C:\Users\Hashi\Desktop\images\supernatural2.jfif")

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

        book_id = 13  # Replace with the actual book ID you're testing with
        driver.get(f"http://localhost:8000/read/addchapter/{book_id}")
        
        # Wait until the chapter_name input field is present in the DOM
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'chapter_name')))
        
        # 3. Fill out the form fields for the chapter
        driver.find_element(By.ID, 'chapter_name').send_keys("Test Chapter Title")
        driver.find_element(By.ID, 'chapter_description').send_keys("This is a test description for the chapter.")

        # 4. Wait for the submit button to be clickable and submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sub_btn"))
        )

        # 5. Scroll into view and click the submit button
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

        # 6. Wait for the result page to load
        time.sleep(5)

        # 7. Check if we're still on the addchapter page (meaning the chapter was not added successfully)
        if f"/read/addchapter/{book_id}" in driver.current_url:
            print(f"Test passed: The chapter is added and the user is on the add chapter page.")
        else:
            print(f"Test failed: The user was redirected unexpectedly.")

    except Exception as e:
        print(f"An error occurred during the test: {e}")
        
    finally:
        driver.quit()

# Run the test
if __name__ == "__main__":
    test_add_book()
