from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import os
import shutil
import time
import yaml

def browser_setup(browser, profile_path):
    if browser.lower() == 'firefox':
        options = FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(profile_path)
        return webdriver.Firefox(options=options)
    
    elif browser.lower() == 'chrome':
        options = ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--user-data-dir=' + profile_path)
        return webdriver.Chrome(options=options)
    
    elif browser.lower() == 'edge':
        options = EdgeOptions()
        options.add_argument('--user-data-dir=' + profile_path)
        options.add_argument('--profile-directory=' + edge_profile_name)
        return webdriver.Edge(options=options)
    
    elif browser.lower() == 'chromium':
        options = ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--user-data-dir=' + profile_path)
        service = Service(chromium_driver)
        return webdriver.Chrome(service=service,options=options)

    else:
        raise ValueError('Invalid browser specified. Current options are "firefox", "chrome", "edge", or "chromium".')
    
upnext_folder = os.path.dirname(__file__)
settings_file = os.path.join(upnext_folder, 'upnext_settings.yaml')
template_file = os.path.join(upnext_folder, 'settings_template.yaml')

if template_file:
    if not os.path.exists(settings_file):
        try:
            shutil.copy(template_file, settings_file)
            print('upnext_settings.yaml was missing. It has now been created. You must open the new file and define the variables.')
        except FileNotFoundError:
            print('Specified template file does not exist.')
        exit()

try:
    with open(settings_file, 'r') as upnext_settings:
        settings = yaml.safe_load(upnext_settings)
except FileNotFoundError:
    print('upnext_settings.yaml not found.')
    exit()

browser_choice = settings['browser_choice']
browser_profile = settings['browser_profile']
edge_profile_name = settings['edge_profile_name']
chromium_driver = settings['chromium_driver']
playlist_link = settings['playlist_link']
subs_to_keep = settings['subs']

browser = browser_setup(browser=browser_choice, profile_path=browser_profile)

# access playlist
browser.get(playlist_link)
time.sleep(7)

# get playlist name for later reference when adding videos
# the location can change depending on browser or even window size, so multiple selectors need to be used... currently
# can possibly be improved by using a more general selector that looks for the playlist name text
selectors = [
    (By.CLASS_NAME, "yt-core-attributed-string--white-space-pre-wrap"),
    (By.CLASS_NAME, "dynamicTextViewModelH1"),
    (By.XPATH, "//div[@class='yt-page-header-view-model__scroll-container']//span[@role='text']"),
    (By.XPATH, "//*[@id='page-header']/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-dynamic-text-view-model/h1/span"),   
    (By.XPATH, "//*[@id='page-manager']/ytd-browse[1]/yt-page-header-renderer/yt-page-header-view-model/div[2]/div/div[1]/div/yt-dynamic-text-view-model/h1/span")
]

playlist_name = None
for method, value in selectors:
    try:
        element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((method, value))
        )
        if element.text:
            playlist_name = element.text
            break
    except NoSuchElementException:
        continue

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
video_elements = browser.find_elements(By.CSS_SELECTOR, 'ytd-rich-item-renderer')

# adds selected channel subscriptions to playlist
time.sleep(5)
for element in video_elements:
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.2)

    channel_names = element.find_elements(By.CSS_SELECTOR, "a.yt-core-attributed-string__link")

    for name in channel_names:    
        if name.text in subs_to_keep:
            # adds videos that haven't been watched to playlist - tries to find progress bar, if it does, skips, if not, adds to playlist
            try:
                watched_flag = element.find_element(By.CLASS_NAME, 'ytThumbnailOverlayProgressBarHostWatchedProgressBarSegment')
                print(watched_flag.text)
            except NoSuchElementException:
                hover_two = ActionChains(browser).move_to_element(name)
                hover_two.perform()
                # finds video playlist options
                WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-menu-renderer yt-icon-button, ytd-menu-renderer button, .yt-lockup-metadata-view-model__menu-button button'))).click()
                time.sleep(2)
                # add to playlist click 
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Save to playlist")]'))).click()
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

# quits
time.sleep(3)
browser.quit()
