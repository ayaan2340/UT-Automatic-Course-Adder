from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import argparse
import getpass

def getStatus(SEASON, YEAR, show_gui, refresh_interval):
    login_url = f'https://utdirect.utexas.edu/apps/registrar/course_schedule/{YEAR}{9 if SEASON == "fall" else 2}/{UNIQUE_ID}/'
    options = Options()

    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options)
    
    print('Log in and authenticate with Duo')

    driver.get(login_url)
    driver.set_window_size(600,600)

    useCreds = input("Would you like to the script to handle credentials? (Still needs Duo) Enter Y/N: ")
    assert useCreds == 'Y' or useCreds == 'N'
    useCreds = useCreds == 'Y'

    if(useCreds):
        username = input("Enter UT EID: ")
        password = getpass.getpass(prompt="Enter your password: ")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.NAME, "_eventId_proceed").click()


    WebDriverWait(driver, 60, 0.1).until(EC.presence_of_element_located((By.ID, "registration_info")))
    print("Successfully logged in")
    last_status = None
    if not show_gui:
        driver.minimize_window()

    while (True):
        try:
            WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.ID, "registration_info")))
        except:
            driver.get(login_url)
            if(useCreds):
                print("Attempting relogin, link must have timed out")
                driver.find_element(By.ID, "username").send_keys(username)
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.NAME, "_eventId_proceed").click()
                WebDriverWait(driver, 20, 0.1).until(EC.presence_of_element_located((By.ID, "registration_info")))
            else:
                print("Relogin, page failed to load, most likely auto logout")

        className = driver.find_elements(by=By.TAG_NAME, value="h2")[0].text
        matches = driver.find_elements(by=By.TAG_NAME, value="td")
        cur_status = [ x for x in matches if 
            x.text == "waitlisted" or 
            x.text == "open" or 
            x.text == "open; reserved" or 
            x.text == "closed"
        ][0].text

        SLEEP_TIME = refresh_interval if refresh_interval else 60 # every minute is the default refresh time

        if (cur_status == last_status):
            print(f"Unique ID {UNIQUE_ID} is still {last_status}.")
            time.sleep(SLEEP_TIME)
            driver.refresh()
            continue
        else:
            if (cur_status == "closed"):
                print(f"{className} with unique ID {UNIQUE_ID} is currently " + cur_status)
            elif cur_status == "cancelled":
                print(f"{className} with unique ID {UNIQUE_ID} is cancelled for {YEAR}.")
                exit(0)
            else:
                goToRegistrationPage(driver)
        
        last_status = cur_status
        time.sleep(SLEEP_TIME)
        driver.refresh()
        
def goToRegistrationPage(driver):
    driver.maximize_window()
    quickRegURL = f'https://utdirect.utexas.edu/registration/registration.WBX?s_ccyys={YEAR}{9 if SEASON == "fall" else 2}&s_af_unique={UNIQUE_ID}'
    registrationURL = "https://utdirect.utexas.edu/registration/chooseSemester.WBX"
    newDriver = driver

    newDriver.get(quickRegURL)

    try:
        WebDriverWait(newDriver, 5, 0.1).until(EC.presence_of_element_located((By.ID, "s_unique_add")))
    except:
        # Determine button text based on season and year
        newDriver.get(registrationURL)
        season_display = "Fall" if SEASON.lower() == "fall" else "Summer" if SEASON.lower() == "spring" else SEASON.capitalize()
        button_text = f"{season_display} {YEAR} Registration"
        
        # Wait for the submit buttons to be present
        WebDriverWait(newDriver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//form//input[@name='submit']"))
        )
        
        # Find and click the button that matches the season and year
        try:
            registration_button = newDriver.find_element(By.XPATH, f"//form//input[@name='submit'][@value='{button_text}']")
            registration_button.click()
        except:
            print(f"Could not find registration button for {button_text}. Attempting to use the first available button.")
            newDriver.find_element(By.XPATH, "//form//input[@name='submit']").click()
        
        WebDriverWait(newDriver, 10).until(EC.presence_of_element_located((By.ID, "s_unique_add")))

    if DROP_ADD:
        drop_dropdown = driver.find_element(By.ID, "s_swap_unique_drop")
        select = Select(drop_dropdown)
        select.select_by_value(str(DROP_ID))
        newDriver.find_element(By.ID, "s_request_STSWP").click()

        swap_input_field = newDriver.find_element(By.ID, "s_swap_unique_add")
        swap_input_field.send_keys(UNIQUE_ID)
        swap_input_field.send_keys(Keys.RETURN)
    else:
        add_input_field = newDriver.find_element(By.ID, "s_unique_add")
        add_input_field.send_keys(UNIQUE_ID)
        add_input_field.send_keys(Keys.RETURN)

    time.sleep(1.5)
    if newDriver.find_elements(By.XPATH, "//div//span[@class='error']"):
        WebDriverWait(newDriver, 30).until(EC.presence_of_element_located((By.ID, "s_request_STAWL")))
        waitlist_radio = newDriver.find_element(By.ID, "s_request_STAWL")
        if waitlist_radio:
            if SWAP_NUMBER != 0:
                dropdown = driver.find_element(By.ID, "s_waitlist_swap_unique")

                select = Select(dropdown)
                select.select_by_value(str(SWAP_NUMBER))
            waitlist_radio.click()
            newDriver.find_element(By.NAME, "s_submit").click()
        else:
            print("Could not add class for some reason")
            exit(1)
            
    input("Should have added/dropped class")
    exit(0)
        

def main():
    global UNIQUE_ID, SWAP_NUMBER, DROP_ADD, DROP_ID, SEASON, YEAR
    global ADVANCED 
    ADVANCED = False

    parser = argparse.ArgumentParser(prog='UT Automatic Course Adder', description='A tool to help' \
            'you automatically check class openings')
    parser.add_argument('-a', '--advanced', type=str, metavar='',
            help='Advanced format to enter with Add/Drop, ID to Add, ID to Drop, ' \
            'ID to Swap for WL (only enter if Drop on Add), Season, Year, Display Y/N. ' \
            'Example: (enter without quotations) \"Drop 12345 12346 0 fall 2025 Y\" ')

    args = parser.parse_args()

    if args.advanced:
        ADVANCED = True
        fieldValues = args.advanced.split()
        DROP_ADD = fieldValues[0]
        assert DROP_ADD == "Add" or DROP_ADD == "Drop"
        DROP_ADD = DROP_ADD == "Drop"
        del fieldValues[0]
    else: 
        DROP_ADD = input("Would you like to add a class or drop upon successful add? (Enter 'Add' or 'Drop') ")
        assert DROP_ADD == "Add" or DROP_ADD == "Drop"
        DROP_ADD = DROP_ADD == "Drop"
        
        # Prepare the input fields based on the DROP_ADD flag
        if DROP_ADD:
            fieldNames = ["Unique ID to add ", "Unique ID to drop ", "Unique ID to swap if waitlisted (0 if N/A) ", "Season ", "Year ", "Show display? (Y/N) "]
        else:
            fieldNames = ["Unique ID to add ", "Unique ID to swap if waitlisted (0 if N/A) ", "Season ", "Year ", "Show display? (Y/N) "]
        
        # Ask for the input fields
        fieldValues = []
        for field in fieldNames:
            value = input(f"Enter {field}")
            fieldValues.append(value if value else "")
    
    # Assign input values to corresponding variables
    DROP_ID = 0
    if DROP_ADD:
        UNIQUE_ID, DROP_ID, SWAP_NUMBER, season, year, show_gui = fieldValues
    else:
        UNIQUE_ID, SWAP_NUMBER, season, year, show_gui = fieldValues
    
    # Convert input to the appropriate data types
    UNIQUE_ID = int(UNIQUE_ID)
    if DROP_ADD:
        DROP_ID = int(DROP_ID)
        assert DROP_ID >= 10000 and DROP_ID <= 99999
    SWAP_NUMBER = int(SWAP_NUMBER)
    YEAR = int(year)
    SEASON = season.lower()
    refresh_interval = 10
    show_gui = True if show_gui == "Y" else False
    assert UNIQUE_ID >= 10000 and UNIQUE_ID <= 99999
    assert SEASON == "fall" or SEASON == "spring"
    assert SWAP_NUMBER == 0 or (SWAP_NUMBER >= 10000 and SWAP_NUMBER <= 99999)
    
    getStatus(SEASON, YEAR, show_gui, refresh_interval)

if __name__ == "__main__":
    main()