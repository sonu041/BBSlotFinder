from selenium import webdriver
from datetime import datetime
import chromedriver_autoinstaller
import sys
import time
import os

def get_bb_slot(url):
    # auto-install chromedriver 
    chromedriver_autoinstaller.install() 
    
    driver = webdriver.Chrome()
    driver.get(url)
    print("Please login using OTP and then wait for a while.")
    time.sleep(60)


    while 1:
        driver.get(url)     
        time.sleep(2)
        print("Trying to find a slot!")
        try:
            driver.find_element_by_xpath("//button[@id = 'checkout']").click()

            time.sleep(5)  #driver take a few sec to update the new url
            src = driver.page_source
            if "checkout" in driver.current_url and not "Unfortunately, we do not have" in src:
                print("Found the slots!")
                for i in range(5):
                     notify("Slots Available!", "Please go and choose the slots!")
                     time.sleep(20)
        except Exception  as e:
            print("If this message pops up multiple times, please find the error and create a PR!")
            print (e)
            pass
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time, "=> No Slots found. Will retry again.")
        notify("No Slots Available!", "No Slots found. Will retry again.")
        time.sleep(600) # Retry in every 10 min.

def notify(title, text):
    if os.name == 'posix':
        os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
        os.system('say "{}"'.format(text))
    elif os.name == 'Linux':
        os.system('spd-say "{}"'.format(text))

def main():
    get_bb_slot('https://www.bigbasket.com/basket/?ver=1')

if __name__ == '__main__':
    main()