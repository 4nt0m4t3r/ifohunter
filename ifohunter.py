from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from PIL import Image
import imagehash
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from pyvirtualdisplay import Display
from core.config import INSTAGRAM_PASSWORD,INSTAGRAM_USERNAME
import logging
import os
import instaloader



def get_followees(profile):
    followee_list = []

    for followee in profile.get_followees():
        followee_list.append(followee.username)
        
    return followee_list

def get_followers_not_followed(profile):
    followers_list = []
    followee_list = get_followees(profile)

    for follower in profile.get_followers():
        #if follower.username not in followee_list:
        followers_list.append(follower.username)    
    return followers_list



def connect_browser():
    logging.info("Connecting to browser")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    browser = webdriver.Chrome(options=options)
    return browser


    
    
def login(browser):
    try:
        logging.info("Logging in to instagram")
        browser.get('https://www.instagram.com/')
        logging.info("Opened Browser")
        time.sleep(3)
        try:
            browser.find_element_by_xpath("//button[contains(.,'Accept')]").click()
        
        except:
            pass
        finally:

            username = browser.find_element_by_name('username')
            time.sleep(3)
            username.send_keys(INSTAGRAM_USERNAME)
            password = browser.find_element_by_name('password')
            password.send_keys(INSTAGRAM_PASSWORD)


            browser.find_element_by_xpath("//button[@type='submit']").click()
            time.sleep(10)
            
            element = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._2dbep.qNELH")))
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='cmbtv']/button[@type='button']").click()
            time.sleep(2)

            #find_elements_by_css_selector
            browser.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()
            time.sleep(2)
    except Exception as e:
        logging.info(e)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('screenshots/error.png') # saves new cropped image
        exit()
    
    
def follow_non_followed(followers_list,browser):
    try:

        
        for account in followers_list:
            browser.get("https://www.instagram.com/"+account+"/")
            time.sleep(2)
            try:
                browser.find_element_by_xpath("//button[contains(.,'Follow Back')]").click()
            except:
                pass
            finally:
                time.sleep(2)
                
        
    except Exception as e:
        logging.info(e)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('screenshots/error.png') # saves new cropped image
        exit()


    
def send_message(browser,exchange_name,account):
    try:
        logging.info("Sending message")
        
        browser.get("https://www.instagram.com/"+account+"/")
        time.sleep(2)
        browser.find_element_by_xpath("//button[contains(.,'Message')]").click()
        time.sleep(2)
        
        browser.find_element_by_xpath("//textarea").send_keys("new IFO at "+exchange_name)
        browser.find_element_by_xpath("//button[contains(.,'Send')]").click()
    except Exception as e:
        logging.info(e)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('screenshots/error.png') # saves new cropped image
        exit()
        
    
    
def send_image(browser,exchange_name):
    logging.info("Sending image")
    browser.find_element_by_xpath("//input[@class='tb_sK']").send_keys(ROOT_DIR+"/screenshots/"+exchange_name+".png")
    logging.info("Sent")
    
    

    
def send_notif_by_Instagram(exchange_name,account,browser):
    try:

        send_message(browser,exchange_name,account)
        send_image(browser,exchange_name)
        time.sleep(2)

    except Exception as e:
        logging.info(e)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('screenshots/error.png') # saves new cropped image
        exit()
    


def compare_screenshots():
    logging.info("Comparing screenshots")
    browser = connect_browser()
    
    try:
    
        with open("exchanges.txt") as fp:
            urls = fp.readlines()
        for website in urls:

            exchange_name=website.split(".")[0]
            logging.info(website)
            
            browser.get("https://"+website)
            time.sleep(10)

            
            hash_previous = imagehash.average_hash(Image.open("screenshots/"+exchange_name+".png"))

            
                
            png = browser.get_screenshot_as_png()
            im = Image.open(BytesIO(png))

            
            

            
            hash_new = imagehash.average_hash(im)
            logging.info(hash_new)
            logging.info(hash_previous)
            if(hash_previous!=hash_new):
                im.save('screenshots/'+exchange_name+'.png') # saves new cropped image
                browser.quit()
                return exchange_name
                
            
        browser.quit()
        return None
    except Exception as e:
        logging.info(e)
        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('screenshots/error.png') # saves new cropped image
        exit()
    

if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    L = instaloader.Instaloader()


    logging.basicConfig( level=logging.INFO)

    L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)  # (login)
    #if you get an error while logging in check this out: https://github.com/instaloader/instaloader/issues/929
    #L.load_session_from_file('username', filename='/home_directory/.config/instaloader/session-...')

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, INSTAGRAM_USERNAME)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    logging.info("Sleeping for 1 minute...")
    time.sleep(60)
    browser=connect_browser() 
    login(browser)
    
    followers_list = get_followers_not_followed(profile)
    follow_non_followed(followers_list,browser)
    

    exchange = compare_screenshots()
    if exchange is not None:
        followees_list = get_followees(profile)
        for account in followees_list:
            send_notif_by_Instagram(exchange,account,browser)
        browser.quit() 
    else:
        browser.quit()
        exit()
        



