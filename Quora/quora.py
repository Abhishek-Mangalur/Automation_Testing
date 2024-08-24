import os
import csv
import time
import unittest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException 

class LoginTest(unittest.TestCase):
    def setUp(self):
        # Set up the Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.implicitly_wait(10)  # Implicit wait for 10 seconds 
        self.passed_tests = 0
        self.failed_tests = 0

    def write_to_csv(self, actual_output, result):
        # Define the CSV file path
        self.csv_file_path = 'test_results.csv'
        
        # Check if the CSV file exists
        if os.path.isfile(self.csv_file_path):
            # Read the existing CSV file
            existing_data = pd.read_csv(self.csv_file_path)
            
            # If columns 'C' and 'D' don't exist, create them
            if 'Actual Output' not in existing_data.columns:
                existing_data['Actual Output'] = pd.NA
            if 'Result' not in existing_data.columns:
                existing_data['Result'] = pd.NA
            
            # Find the first empty cell in column 'C'
            first_empty_row = existing_data['Actual Output'].isna().idxmax()
            
            # Update the empty cell in column 'C' and corresponding cell in column 'D'
            if pd.isna(existing_data.at[first_empty_row, 'Actual Output']):
                existing_data.at[first_empty_row, 'Actual Output'] = actual_output
                existing_data.at[first_empty_row, 'Result'] = result
            else:
                # If there is no empty cell, append a new row with the data
                new_row = pd.DataFrame({'A': [pd.NA], 'B': [pd.NA], 'Actual Output': [actual_output], 'Result': [result]})
                existing_data = pd.concat([existing_data, new_row], ignore_index=True)
        else:
            # If the file does not exist, create it with headers and the new data
            existing_data = pd.DataFrame({'A': [pd.NA], 'B': [pd.NA], 'Actual Output': [actual_output], 'Result': [result]})

        # Update pass/fail count
        if result == 'PASS':
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        # Save the updated data back to CSV
        existing_data.to_csv(self.csv_file_path, index=False)

    def test_login_and_click(self):
        driver = self.driver
        driver.get("https://www.quora.com/")  # Replace with the actual login URL

        try:
            # Invalid username & password
            username_field = driver.find_element(By.NAME, 'email')
            username_field.send_keys('wajiji8411@gmail.com')
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys('Bengaluru123+')
            print('\nLogin Failed due to invalid login credential')
            print('1st test case completed')
            self.write_to_csv('Login Failed due to invalid login credential', 'PASS')
            time.sleep(5)
            driver.refresh()

            # Valid username & password
            username_field = driver.find_element(By.NAME, 'email')
            # username_field.send_keys('sevogi1100@vasomly.com')
            username_field.send_keys('lanog93602@sablecc.com')
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys('Bengaluru@2021')
            
            # Submit form
            login_button = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/button/div/div/div")
            time.sleep(5)
            login_button.click()

            # Wait until the login process is complete and the element is present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div/div[2]"))
            )
            print("Login Successful..!")
            print('2nd test case completed')
            self.write_to_csv('Login Successful..!', 'PASS')

            # Click on the 'Search' button
            search = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div/div/div/div/div/input")
            time.sleep(5)
            search.send_keys('Bengaluru')
            time.sleep(5)
            search2 = driver.find_element(By.XPATH, "//*[@id=\"selector-option-0\"]/div/div/div")
            search2.click()
            print('Bengaluru result searched')
            print('3rd test case completed')
            self.write_to_csv('Bengaluru result searched', 'PASS')

            # Click on the 'Answers' button
            answers = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[2]/div[3]/div/div")
            answers.click()
            time.sleep(5)
            print('Shows the answers for Bengaluru related question')
            print('4th test case completed')
            self.write_to_csv('Shows the answers for Bengaluru related question', 'PASS')

            # Click on the 'Topic' button
            topic = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[2]/div[6]/div/div")
            topic.click()
            print('Shows the topics related to Bengaluru')
            print('5th test case completed')
            self.write_to_csv('Shows the topics related to Bengaluru', 'PASS')
            time.sleep(5)

            # Home
            home = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[2]/div/div[2]/div/a[1]/div/div[2]")
            driver.execute_script("arguments[0].scrollIntoView(true);", home)
            driver.execute_script("arguments[0].click();", home)
            time.sleep(5)

            # Click on the 'Ask Question' button
            ask_question_btn = driver.find_element(By.XPATH, "//*[@id=\"mainContent\"]/div/div/div[1]/div/div/div[1]/div/div[2]")
            ask_question_btn.send_keys(Keys.RETURN)
            time.sleep(5)
            ask_question_field = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/textarea")
            time.sleep(5)
            ask_question_field.send_keys('What is the current temperature in Bengaluru')
            create_post = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[3]/div/div/div/div[2]/div")
            time.sleep(5)
            create_post.click()
            post_description = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div[1]/div/div")
            time.sleep(5)
            post_description.send_keys('Simple post...')
            close_post = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/button")
            time.sleep(5)
            close_post.click()
            print('Add question/poster')
            print('6th test case completed')
            self.write_to_csv('Add question/poster', 'PASS')

            # Following
            following = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[2]/div/div[2]/div/a[2]/div/div[2]")
            driver.execute_script("arguments[0].scrollIntoView(true);", following)
            driver.execute_script("arguments[0].click();", following)
            time.sleep(5)
            print('Switch to followings')
            print('7th test case completed')
            self.write_to_csv('Switch to followings', 'PASS')

            # Upvote
            upvote = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/span[1]/div/div/div/button")
            upvote.click()
            time.sleep(5)
            upvote.click()

            # Downvote
            downvote = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/span[1]/div/div/div/div[2]/div")
            downvote.click()
            time.sleep(5)
            downvote.click()
            print('Upvote & Downvote operations performed')
            print('8th test case completed')
            self.write_to_csv('Upvote & Downvote operations performed', 'PASS')

            # comment
            comment_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/span[2]/div/div/div")
            comment_btn.click()

            # write comment
            write_comment = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div")
            write_comment.send_keys("Nice job...")
            time.sleep(5)

            # post comment
            post_comment = driver.find_element(By.XPATH, "//*[@id=\"mainContent\"]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div/div/div[2]/div/button")
            post_comment.click()
            time.sleep(5)
            print('Comment to the question')
            print('9th test case completed')
            self.write_to_csv('Comment to the question', 'PASS')

            # comment options
            comment_options = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/button")
            comment_options.click()
            time.sleep(5)

            # edit comment
            edit_comment = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]")
            edit_comment.click()
            time.sleep(5)

            # edited comment write
            edit_comment_write = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div")
            time.sleep(5)
            edit_comment_write.send_keys(' & Excellent work...')

            # post edited comment
            post_edited_comment = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]")
            post_edited_comment.click()
            time.sleep(5)
            print('Edit comment & repost')
            print('10th test case completed')
            self.write_to_csv('Edit comment & repost', 'PASS')

            # comment options
            comment_options = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/button")
            comment_options.click()
            time.sleep(5)

            # delete comment
            delete_comment = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]")
            delete_comment.click()
            time.sleep(5)

            # conform_delete comment
            conform_delete_comment = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div[3]/div[2]/button")
            conform_delete_comment.click()
            time.sleep(5)
            print('Comment Deleted Successfully')
            print('11th test case completed')
            self.write_to_csv('Comment Deleted Successfully', 'PASS')

            # Answer
            answer = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[2]/div/div[2]/div/a[3]/div/div[2]")
            driver.execute_script("arguments[0].scrollIntoView(true);", answer)
            driver.execute_script("arguments[0].click();", answer)
            time.sleep(5)
            print('Switch to answer section')
            print('12th test case completed')
            self.write_to_csv('Switch to answer section', 'PASS')

            # Answer to the question
            answer_to_question = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/button[1]")
            answer_to_question.click()
            time.sleep(5)
            cancel_answering = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/button")
            time.sleep(5)
            cancel_answering.click()

            # Follow
            follow = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/button[2]")
            follow.click()
            time.sleep(5)
            follow.click()
            print('Answer the question & follow')
            print('13th test case completed')
            self.write_to_csv('Answer the question & follow', 'PASS')

            # passs
            passs = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div/div/button")
            passs.click()
            time.sleep(5)
            passs.click()

            # report other post
            report_other_post = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[6]")
            report_other_post.click()
            time.sleep(5)
            print('Report the post')
            print('14th test case completed')
            self.write_to_csv('Report the post', 'PASS')

            # cancel report
            cancel_report = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/button")
            cancel_report.click()
            time.sleep(5)

            # Spaces
            spaces = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[2]")
            driver.execute_script("arguments[0].scrollIntoView(true);", spaces)
            driver.execute_script("arguments[0].click();", spaces)
            time.sleep(5)
            spaces2 = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div[3]/a/div")
            spaces2.click()
            time.sleep(5)
            print('Switch to Spaces')
            print('15th test case completed')
            self.write_to_csv('Switch to Spaces', 'PASS')

            # Notification
            notification = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/a[4]/div/div[2]")
            driver.execute_script("arguments[0].scrollIntoView(true);", notification)
            driver.execute_script("arguments[0].click();", notification)
            time.sleep(5)
            print("Switch to Notifications")
            print('16th test case completed')
            self.write_to_csv('Switch to Notifications', 'PASS')

            # Logout profile
            logout_profile = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div"))
            )
            time.sleep(5)
            logout_profile.click()
            time.sleep(5)
            # Logout button
            logout_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div"))
            )
            logout_button.click()
            print("Logout Successful..!")
            print('17th test case completed')
            self.write_to_csv('Logout Successful..!', 'PASS')

        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
            print(f"Error: {e}")
            self.write_to_csv('Failed', str(e))

    def tearDown(self):
        # Print the test report
        executed = self.passed_tests + self.failed_tests
        defects = self.failed_tests
        print("\n==========Test Report==========")
        print("No. of Test Cases Executed: ", executed)
        print("No. of Test Cases Passed: ", self.passed_tests)
        print("No. of Test Cases Failed: ", self.failed_tests)
        print("No. of Test Defects Raised: ", defects)

        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
