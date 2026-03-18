import os
import shutil
import time
import yaml
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
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


def load_yaml(file: str, template: str | None = None) -> dict | None:
    """Load a YAML file or create a YAML file from a template.

    This function attempts to load a YAML file from the specified path.
    If the file does not exist and a template path is provided,
    it will copy the template file to the specified path.
    If the file exists, it will load and return the contents as a dictionary.

    Args:
        file (str): Path to the YAML file to load.
        template (str | None): Path to a template YAML file to copy if the specified file does not exist. Defaults to None.

    Returns:
        Dict: Returns a dictionary of the loaded YAML file.
    """
    if template:
        if not os.path.exists(file):
            try:
                shutil.copy(template, file)
                print("Specified file missing. A new one has been created.")
            except FileNotFoundError:
                print("Specified template file does not exist.")
    try:
        with open(file, "r") as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        print("File not found. Please check path.")


def browser_setup(
    browser: str,
    profile_path: str,
    edge_profile_name: str | None = None,
    chromium_driver: str | None = None,
) -> WebDriver:
    """Create and configure a Selenium WebDriver instance for the specified browser.

    This function initializes a WebDriver for Firefox, Chrome, Edge, or Chromium,
    applying the appropriate profile directory and browser-specific options. For
    Chromium, a custom driver path needs to be provided.

    Args:
        browser (str): Browser name (Firefox, Chrome, Edge, or Chromium).
        profile_path (str): Path to the browser's user profile directory.
        edge_profile_name (str | None): Name of the Edge profile to use. Required only for Edge use.
        chromium_driver (str | None): Path to the Chromium driver executable. Required only for Chromium use.

    Returns:
        WebDriver: Returns a WebDriver instance for the specified browser.
    """
    if browser.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(profile_path)
        return webdriver.Firefox(options=options)

    elif browser.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--user-data-dir=" + profile_path)
        return webdriver.Chrome(options=options)

    elif browser.lower() == "edge":
        options = EdgeOptions()
        options.add_argument("--user-data-dir=" + profile_path)
        options.add_argument("--profile-directory=" + edge_profile_name)
        return webdriver.Edge(options=options)

    elif browser.lower() == "chromium":
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--user-data-dir=" + profile_path)
        service = Service(chromium_driver)
        return webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError(
            'Invalid browser specified. Current options are "firefox", "chrome", "edge", or "chromium".'
        )


def playlist_cleanup(browser: WebDriver) -> None:
    """Clean up a YouTube playlist by removing all videos within it.

    This function removes all videos from a YouTube playlist by iterating through
    the videos in the playlist and using Selenium to interact with the browser.
    It locates the video options menu for each video, clicks it, and selects the
    option to remove the video from the playlist. It continues this process
    until all videos have been removed.

    Args:
        browser (WebDriver): Selenium WebDriver instance to interact with the browser.

    Returns:
        None
    """
    videos_to_remove = browser.find_elements(By.XPATH, '//*[@id="video-title"]')
    for videos in videos_to_remove:
        try:
            hover = ActionChains(browser).move_to_element(videos)
            hover.perform()
            WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "ytd-playlist-video-renderer.style-scope:nth-child(1) > div:nth-child(3) > ytd-menu-renderer:nth-child(1)",
                    )
                )
            ).click()
            time.sleep(1)
            WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "ytd-menu-service-item-renderer.style-scope:nth-child(4) > tp-yt-paper-item:nth-child(1)",
                    )
                )
            ).click()
            time.sleep(1)
        except ElementNotInteractableException:
            pass


def playlist_build(
    browser: WebDriver, subs_to_keep: list[str], playlist_name: str, max_videos: int
) -> None:
    """Build a YouTube playlist by adding unwatched videos from specified channel subscriptions.

    This function scans the YouTube subscription feed using
    a Selenium WebDriver instance. It checks whether the video's
    channel name matches one of the channels in `subs_to_keep`. If the video
    has not been watched (determined by the absence of the progress bar), the
    function will open the video options menu, select "Save to playlist", and add it to
    the playlist specified. It continues until `max_videos` is reached
    or all visible videos have been gone through (if set to None).

    Args:
        browser (WebDriver): Selenium WebDriver instance to interact with the browser.
        subs_to_keep (list): List of channel names to use when building the playlist. Only videos from these channels will be added.
        playlist_name (str): Name of the playlist to add videos to. Case sensitive.
        max_videos (int): Maximum number of videos to add to the playlist. If None, will continue until the end of the subscription feed is reached.

    Returns:
        None
    """
    videos_added = 0

    video_elements = browser.find_elements(By.CSS_SELECTOR, "ytd-rich-item-renderer")

    # adds selected channel subscriptions to playlist
    time.sleep(5)

    for element in video_elements:
        if max_videos is None or videos_added < max_videos:
            browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            time.sleep(0.2)

            channel_names = element.find_elements(
                By.CSS_SELECTOR, "a.yt-core-attributed-string__link"
            )

            for name in channel_names:
                if name.text in subs_to_keep:
                    # adds videos that haven't been watched to playlist - tries to find progress bar, if it does, skips, if not, adds to playlist
                    try:
                        watched_flag = element.find_element(
                            By.CLASS_NAME,
                            "ytThumbnailOverlayProgressBarHostWatchedProgressBarSegment",
                        )
                        print(watched_flag.text)
                    except NoSuchElementException:

                        hover_two = ActionChains(browser).move_to_element(name)
                        hover_two.perform()
                        # finds video playlist options
                        WebDriverWait(element, 20).until(
                            EC.element_to_be_clickable(
                                (
                                    By.CSS_SELECTOR,
                                    "ytd-menu-renderer yt-icon-button, ytd-menu-renderer button, .yt-lockup-metadata-view-model__menu-button button",
                                )
                            )
                        ).click()
                        time.sleep(2)
                        # add to playlist click
                        WebDriverWait(browser, 20).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    '//span[contains(text(), "Save to playlist")]',
                                )
                            )
                        ).click()
                        time.sleep(1)
                        # identify correct playlist
                        playlist_name_path = (
                            '//*[contains(text(), "' + playlist_name + '")]'
                        )
                        # adds all elements that have playlist name text to list
                        correct_playlist_check = browser.find_elements(
                            By.XPATH, playlist_name_path
                        )
                        # try to click each item in list, if error, move to the next
                        for check in correct_playlist_check:
                            time.sleep(1)
                            try:
                                check.click()
                                videos_added += 1
                            except (
                                ElementClickInterceptedException,
                                ElementNotInteractableException,
                            ) as error:
                                pass
                        time.sleep(4)

    print("Playlist build complete. Total videos added: " + str(videos_added))


def main():
    upnext_folder = os.path.dirname(__file__)
    settings_file = os.path.join(upnext_folder, "upnext_settings.yaml")
    template_file = os.path.join(upnext_folder, "settings_template.yaml")

    settings = load_yaml(settings_file, template_file)

    required_keys = ["browser_choice", "playlist_link", "playlist_name", "subs"]

    if any(settings.get(key) is None for key in required_keys):
        print(
            "Error: Missing required settings. Please check your upnext_settings.yaml file."
        )
        exit()
    else:
        browser_choice = settings["browser_choice"]
        browser_profile = settings["browser_profile"]
        edge_profile_name = settings["edge_profile_name"]
        chromium_driver = settings["chromium_driver"]
        playlist_link = settings["playlist_link"]
        playlist_name = settings["playlist_name"]
        subs_to_keep = settings["subs"]
        max_videos = settings["max_videos"]

        browser = browser_setup(
            browser=browser_choice,
            profile_path=browser_profile,
            edge_profile_name=edge_profile_name,
            chromium_driver=chromium_driver,
        )

        try:
            # access playlist
            print("Accessing playlist...")
            browser.get(playlist_link)
            time.sleep(7)

            print("Cleaning up playlist...")
            playlist_cleanup(browser)
            time.sleep(3)

            print("Adding videos to playlist...")
            browser.get("https://www.youtube.com/feed/subscriptions")
            time.sleep(5)

            playlist_build(browser, subs_to_keep, playlist_name, max_videos)
            time.sleep(3)
        finally:
            print("Closing browser...")
            browser.quit()


if __name__ == "__main__":
    main()
