from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
import time
from datetime import timedelta, datetime, date
import json
import tweepy
from config import *
from utils import *
import os
import gspread

def bypass_block(retry = 0, area = "Downtown East Toronto"):
    # Bypass JS challenge
    try:
        driver.get("https://www.google.com/url?sa=t&url=" + CLINIC_URL + "?key=" + AREA_KEY[area])
        element = driver.find_element_by_xpath('.//a')

        ActionChains(driver) \
            .key_down(Keys.COMMAND) \
            .click(element) \
            .key_up(Keys.COMMAND) \
            .perform()

        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        time.sleep(CLOUDFLARE_SEC)
        WebDriverWait(driver, CLOUDFLARE_SEC).until(lambda x: x.title != "Just a moment...")
        driver.minimize_window()
    except:
        if (retry < MAX_RETRY):
            driver.delete_all_cookies()
            return(bypass_block(retry + 1, area))
        else:
            log("ERROR", "fail to bypass Cloudflare after maximum retries.")
            return(False)

    # Stop if maintenance page detected
    if (driver.title == "COVID-19 Vaccination"):
        log("ERROR", "fail to bypass maintenance page.")
        #twitter_api.update_profile(description = ACCOUNT_BIO + " Last checked: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", booking site currently closed")
        return(False)

    # Wait in line
    try:
        WebDriverWait(driver, WAITROOM_SEC).until(lambda x: x.title != "COVID-19 Waiting Room") #in ["Shell", "COVID-19 Vaccination", "Unity Health Toronto - Book a COVID-19 Vaccination Appointment"])
    except:
        log("ERROR", "fail to pass waitroom after maximum wait time.")
        return(False)
    
    return(True)

def checker(area, last_availability, debug = True):
    location_lst = AREA_CLINIC[area]
    availability_details = {"total": 0, "eligibility": {}}
    date_lst = []

    today = date.today()
    for i in range(0, 8):
        date_lst.append((today + timedelta(days = i)).strftime("%Y-%m-%dT00:00:00.000-04:00"))

    if (bypass_block(0, area) == False):
        return {"total": -1, "eligibility": {}}

    for eligibility_text, slot_type in ELIGIBILITY[area].items():
        url = BASE_URL + "?slot_type=" + slot_type + "&key=" + AREA_KEY[area]
        availability_details["eligibility"][eligibility_text] = {}

        for location in location_lst:
            availability_details["eligibility"][eligibility_text][location] = {"total": 0, "details": {}}
            for day in date_lst:
                driver.execute_script("document.title = \"Checking " + location + " " + day[:-19] + " " + slot_type + "\"")
                current_url = url + "&location_id=" + location + "&day=" + day
                
                try:
                    response = driver.execute_script(generate_request_js(current_url))
                    slots_left = int(json.loads(response)["slots_left"])
                except:
                    log("ERROR", "fail to check availability.\tlocation: " + location + '\tdate: ' + day)
                    return {"total": -1, "eligibility": {}}

                log("INFO", "location: " + location + '\ttype: ' + slot_type + '\tdate: ' + day + '\tslots: ' + str(slots_left))
                availability_details["total"] += slots_left
                availability_details["eligibility"][eligibility_text][location]["total"] += slots_left
                availability_details["eligibility"][eligibility_text][location]["details"][day] = slots_left
                time.sleep(INTERVAL_SEC)

            if ((availability_details["eligibility"][eligibility_text][location]["total"] > 0) and (
                    (last_availability["eligibility"][eligibility_text][location]["total"] == 0 and 
                     availability_details["eligibility"][eligibility_text][location]["total"] > 1) or
                    (last_availability["eligibility"][eligibility_text][location]["total"] > 0 and 
                     availability_details["eligibility"][eligibility_text][location]["total"] > last_availability["eligibility"][eligibility_text][location]["total"] + 10)
                )):
                breakdown_text = ""
                for day, slots_left in availability_details["eligibility"][eligibility_text][location]["details"].items():
                    if slots_left > 0:
                        breakdown_text += '''{slots} on {day}
'''.format(slots = str(slots_left), day = datetime.strptime(day, "%Y-%m-%dT00:00:00.000-04:00").strftime("%b %d"))
                breakdown_text = breakdown_text[:-1]
                tweet_text = TWEET_TEMPLATE.format( slot_str = str(availability_details["eligibility"][eligibility_text][location]["total"]),
                                                    clinic_str = CLINIC_NAME[location],
                                                    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    area_key_str = AREA_KEY[area],
                                                    eligibility = eligibility_text,
                                                    date_breakdown = breakdown_text)
                if debug:
                    print(tweet_text)
                else:
                    twitter_api.update_status(status = tweet_text)#, attachment_url = QUOTED_TWEET)

    return availability_details

def get_last_crawl():
    if os.path.isfile(CRAWLER_FILE):
        with open(CRAWLER_FILE, 'r') as verto_website_file:
            last_crawl_json = verto_website_file.read().splitlines()[-1]
        return json.loads(last_crawl_json)
    else:
        return None

def update_last_crawl(last_avail):
    with open(CRAWLER_FILE, "a") as verto_website_file:
        verto_website_file.write(json.dumps(last_avail) + '\n')

def update_open_data(availability):
    try:
        gcloud_auth = gspread.service_account(filename=SHEET_KEY_FILE)
        sheet = gcloud_auth.open_by_key(SHEET_URL_ID)
        for area, clinic_lst in AREA_CLINIC.items():
            for clinic in clinic_lst:
                worksheet = sheet.worksheet(CLINIC_NAME[clinic])
                slot_list_18 = availability["area"][area]["eligibility"]["1st dose, 18+, 'M' postal codes"][clinic]["details"]
                slot_list_12 = availability["area"][area]["eligibility"]["1st dose, age 12-17, 'M' postal codes"][clinic]["details"]
                slot_list = [availability["check_time"]]
                first_date = datetime.strptime(next(iter(slot_list_12)), "%Y-%m-%dT00:00:00.000-04:00")
                delta_days = (first_date.date() - datetime(2021, 7, 10).date()).days
                slot_list.extend([""] * delta_days * 2)
                for day, slots in slot_list_12.items():
                    slot_list.append(slots)
                    slot_list.append(slot_list_18[day])
                worksheet.append_row(slot_list, value_input_option="USER_ENTERED")
    except Exception as ex:
        log("ERROR", "fail to update open data google sheet.\n" + str(ex))
    
    return

def main(debug):
    last_availability = get_last_crawl()
    
    global driver
    driver = uc.Chrome()
    driver.minimize_window()

    checking_error = False
    availability_log = {"check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "total": 0, "area": {}}
    for area in AREA_LIST:
        availability = checker(area, last_availability["area"][area], debug)
        if availability["total"] == -1:
            checking_error = True
            break
        availability_log["total"] += availability["total"]
        availability_log["area"][area] = availability
    
    if not checking_error:
        availability_log["check_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not debug:
            twitter_api.update_profile(description = ACCOUNT_BIO + " Last checked: " + availability_log["check_time"] + ", slots left: " + str(availability_log["total"]) + ".")
        update_last_crawl(availability_log)
        update_open_data(availability_log)
    
    driver.quit()

if __name__ == "__main__":
    main(debug=False)
