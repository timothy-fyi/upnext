#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time

# user settings
gc_driver = 'CHROME_DRIVER_LOCATION'
gc_profile = 'CHROMIUM_PROFILE_LOCATION'
playlist_link = 'PLAYLIST_LINK'
playlist_name = 'EXACT PLAYLSIT NAME HERE'
subs_to_keep = ['CHANNEL', 'NAMES', 'AS', 'LIST']

# browser settings
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + gc_profile)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
ser = Service(gc_driver)
browser = webdriver.Chrome(service=ser, options=options)

# access playlist
browser.get(playlist_link)

time.sleep(7)
# get playlist name for later reference when adding videos
# have to fix below lines, supposed to automitcally return playlist name without user input
# playlist_name_element = browser.find_element(By.XPATH, '//*[@id="text"]')

videos_to_remove = browser.find_elements(By.XPATH, '//*[@id="video-title"]')
for videos in videos_to_remove:
    try:
        hover = ActionChains(browser).move_to_element(videos)
        hover.perform()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-playlist-video-renderer.style-scope:nth-child(1) > div:nth-child(3) > ytd-menu-renderer:nth-child(1)'))).click()
        time.sleep(1)
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-service-item-renderer.style-scope:nth-child(4) > tp-yt-paper-item:nth-child(1)'))).click()
        time.sleep(1)
    except ElementNotInteractableException:
        pass

# access subscription page, and add new videos to playlist
time.sleep(3)
browser.get('https://www.youtube.com/feed/subscriptions')

# identifys video elements
time.sleep(3)
video_elements = browser.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-grid-media')

time.sleep(3)
subs_to_keep = [sub.lower() for sub in subs_to_keep]
for element in video_elements:
    channel_names = element.find_elements(By.CLASS_NAME, 'style-scope ytd-channel-name')
    for name in channel_names:    
        if name.text.lower() in subs_to_keep:
            # determines if video has been watched yet
            try:                      
                watched_flag = element.find_element(By.CLASS_NAME, 'style-scope ytd-thumbnail-overlay-resume-playback-renderer')
            except NoSuchElementException:
                hover_two = ActionChains(browser).move_to_element(name)
                hover_two.perform()
                # finds video playlist options
                WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'style-scope ytd-menu-renderer'))).click()
                time.sleep(2)
                # add to playlist click
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-service-item-renderer.style-scope:nth-child(3) > tp-yt-paper-item:nth-child(1)'))).click()
                time.sleep(1)                
                # identify correct playlist
                playlist_name_path = '//*[contains(text(), "'+ playlist_name +'")]'
                # adds all elements that have playlist name text to list
                correct_playlist_check = browser.find_elements(By.XPATH, playlist_name_path)
                # try to click each item in list, if error, move to the next
                for check in correct_playlist_check:
                    time.sleep(1)
                    try:
                        check.click()
                    except (ElementClickInterceptedException, ElementNotInteractableException) as error:
                        pass
                time.sleep(4)
                # close out of menu options
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-icon.ytd-add-to-playlist-renderer'))).click()
                time.sleep(4)

time.sleep(3)
browser.quit()
