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

driver_path = r'C:\Users\ANEEBA ZAFAR\Downloads\edgedriver_win64\msedgedriver.exe'

def test_bookview():
    try:
        service = Service(driver_path)
        driver = webdriver.Edge(service=service)

        driver.get("http://localhost:8000/login")
            
            # Login
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("Test@1234")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for redirect after login

        # time.sleep(5)

        book_id=5
        driver.get(f"http://localhost:8000/read/bookview/{book_id}")
            

        library_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add_reading"))
        )    
        library_button.click() 
        time.sleep(2)

        if f"/read" in driver.current_url:
            print(f"Test passed: book successfully added")
        else:
            print(f"Test failed: The user was redirected unexpectedly.")
    except Exception as e:
        print(f"An error occurred during the test: {e}")
        
    finally:
        driver.quit()

# Run the test
if __name__ == "__main__":
    test_bookview()


        
