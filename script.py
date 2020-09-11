from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dateutility import dateutility
from datetime import datetime
import schedule
import time
import argparse

def main():
    args = handle_args()
    schedule.every().day.at("00:00").do(reserve, args)
    if len(schedule.jobs) > 0:
        print("script will run at 12:00am.")
    
    # refresh every 10 seconds until time 00:00
    while len(schedule.jobs) > 0:
        schedule.run_pending()
        time.sleep(10)

def num_4digit_type(n):
    n = str(n)
    if len(n) < 4 or not n.isdigit():
        raise argparse.ArgumentTypeError("error parsing time. must be in HHMM form, (4 numbers, no spaces).")
    return int(n)

def handle_args():
    parser = argparse.ArgumentParser(description="script to automatically reserve tennis courts.")
    parser.add_argument("time", type=num_4digit_type, default=1930, nargs='?',
        help="(optional - default 19:30/7:30pm) desired time to reserve the tennis court. Use format HHMM, 24-hour. for example, if 9:30am is desired: python3 script.py 0930")
    return parser.parse_args()
    
def reserve(args):
    username_str = "..."
    password_str = "..."
    name_str = "..."
    phone_str = "..."
    email_str = "..."
    keyfob_str = "..."
    address_str = "..."

    dateutil = dateutility()
    starttime = time.time()

    desired_time_obj = dateutil.int_to_time(args.time)

    print("reserving court for date " + dateutil.get_latest_available_str() + ", time " + str(desired_time_obj))
    
    driver = webdriver.Chrome('./chromedriver')
    driver.get('...')

    # login to website
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "user_login"))).send_keys(username_str)
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "user_pass"))).send_keys(password_str)
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "wp-submit"))).click()
        print("logged in successfully.")
    finally:
        driver.get('...')

    # service step
    try:
        time_elem = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "(//select[contains(@class, 'bookly-select-mobile') and contains(@class, 'bookly-js-select-service')])[2]")))
        time_obj = Select(time_elem)
        time_obj.select_by_visible_text("Tennis 1 Hour")
        court_elem = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "(//select[contains(@class, 'bookly-select-mobile') and contains(@class, 'bookly-js-select-employee')])[2]")))
        court_obj = Select(court_elem)
        court_obj.select_by_visible_text("Any")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bookly-next-step')]"))).click()
        print("selected duration and court successfully.")
    except Exception as e:
        print("ERROR: failed to select duration and/or court (step 1): " + str(e))

    # time step
    try:
        desired_date_str = dateutil.get_latest_available_str()
        desired_date_xpath = "//div[contains(@class, 'picker__day') and contains(@aria-label, '" + desired_date_str + "')]"
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, desired_date_xpath))).click()

        time_selected = False
        while not time_selected:
            print("attempting to select time " + str(desired_time_obj) + "...")
            desired_time_xpath = "//button[contains(@value, '" + str(desired_time_obj) + "')]"
            time_button = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, desired_time_xpath)))
            if time_button.is_enabled():
                print("time " + str(desired_time_obj) + " is available!")
                time_button.click()
                time_selected = True
                print("Selected date and time successfully.")
            else:
                print("time " + str(desired_time_obj) + " is not available :(... decrementing time by 30 mins.")
                desired_time_obj = dateutil.increment_time(desired_time_obj, -30)
    except Exception as e:
        print("ERROR: failed to select date and/or time (step 2): " + str(e))
    
    # detail step
    try:
        name_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'bookly-js-full-name')]")))
        phone_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'bookly-js-user-phone-input')]")))
        email_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'bookly-js-user-email')]")))
        keyfob_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[contains(@class, 'bookly-custom-field')])[1]")))
        address_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[contains(@class, 'bookly-custom-field')])[2]")))

        name_field.clear()
        name_field.send_keys(name_str)
        phone_field.clear()
        phone_field.send_keys(phone_str)
        email_field.clear()
        email_field.send_keys(email_str)
        keyfob_field.clear()
        keyfob_field.send_keys(keyfob_str)
        address_field.clear()
        address_field.send_keys(address_str)

        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@type, 'checkbox')]"))).click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'bookly-next-step')]"))).click()

        print("filled in details successfully.")
        print("success! tennis court was reserved for date " + dateutil.get_latest_available_str() + ", time " + str(desired_time_obj))
        print("script finished in " + (str(time.time() - starttime))[0:5] + " seconds.")

        schedule.clear()
    except Exception as e:
        print("ERROR: failed to fill in details (step 3): " + str(e))       

if __name__ == "__main__":
   main()