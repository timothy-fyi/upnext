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
import json
import yaml

with open('/home/pi/upnext_settings.yaml', 'r') as upnext_settings:
    settings = yaml.safe_load(upnext_settings)

# user settings
gc_driver = settings['gc_driver']
gc_profile = settings['gc_profile']
playlist_link = settings['playlist_link']
playlist_name = settings['playlist_name']
subs_to_keep = settings['subs']

# browswer settings
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
# playlist_name = playlist_name_element.text

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
time.sleep(5)
video_elements = browser.find_elements(By.CSS_SELECTOR, 'ytd-rich-item-renderer, ytd-grid-video-renderer, ytd-video-renderer')

# adds selected channel subscriptions to playlist
time.sleep(5)
for element in video_elements:
    channel_names = element.find_elements(By.CSS_SELECTOR, 'a.yt-core-attributed-string__link')

    for name in channel_names:    
        if name.text in subs_to_keep:
            try:        
                watched_flag = element.find_element(By.CLASS_NAME, 'ytThumbnailOverlayProgressBarHostWatchedProgressBarSegment')
            # adds videos that haven't been watched to playlist
            except NoSuchElementException:
                hover_two = ActionChains(browser).move_to_element(name)
                hover_two.perform()
                # finds video playlist options
                WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-renderer yt-icon-button, ytd-menu-renderer button, .yt-lockup-metadata-view-model__menu-button button'))).click()
                time.sleep(2)
                # add to playlist click 
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-list-item-view-model.yt-list-item-view-model:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)'))).click()
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
                # close out of menu options -> possibly obsolete with recent Youtube update
                # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-icon.ytd-add-to-playlist-renderer'))).click()
                # time.sleep(4)

# quits
time.sleep(3)
browser.quit()
