# Upnext - An automated YouTube playlist builder

**Upnext** is a YouTube playlist automation tool that:
- Removes all existing videos from a selected playlist
- Adds new, unwatched videos to a selected playlist from defined subscriptions

It's designed to run automatically (via cron or Task Scheduler), but can also be imported into your own projects.

Originally built for Chromium on a Raspberry Pi, **Upnext** now supports multiple browsers and operating systems.

## Features
- Cleans and rebuilds playlists
- Filters videos by selected channel subscriptions
- Skips videos that has already been watched
- Cross-browser support
- Works well with scheduled automation

## Requirements
- Python 3.10+
- Dependencies:
  ```pip install -r requirements.txt```

## Supported Browsers / OS
- Firefox (Windows)
- Chrome (Windows)
- Edge (Windows)
- Chromium (Linux)

## Important Information
- **Upnext** automatically detects uses the appropriate driver for your chosen browser via the Selenium package. The exception is Chromium. In order to set up Upnext with Chromium, you need to download the correct ChromeDriver for your version of Chromium (if no version exists on your device already[^1]). It can be downloaded [here](https://chromedriver.chromium.org/).
- For supported browsers it is recommended you create a new profile, specifically for use of this script. This will allow you to use the same browser at the same time the script is running. **If you attempt to run Upnext from the same profile you currently have a browser window up in, the script will not run correctly.**

## Setup
### 1. **Run once to generate settings file**

   ```python upnext.py```
   
   This creates:

   ```upnext_settings.yaml```

### 2. **Configure** ```upnext_settings.yaml```
```
browser_choice: browser name
browser_profile: /path/to/profile
edge_profile_name: Profile 1
chromium_driver: /path/to/chromedriver
playlist_link: https://www.youtube.com/playlist?list=XXXX
playlist_name: My Playlist
max_videos: 10
subs:
  - Channel One
  - Channel Two
  - Channel Three
```
**Detailed settings explanation:**
- **browser_choice:** Case insensitive. Firefox, Chrome, Edge, or Chromium
- **browser_profile:** Path to your browser profile. It is located in different locations depending on the 
   browser. For example, for Chromium it may be located at ```/home/your_name/.config/chromium/```, but FireFox it may be located at ```C:\Users\yourname\AppData\Roaming\Mozilla\Firefox\Profiles\RandomString.Profile Number```
- **edge_profile_name:** Name of your Edge profile (i.e. Profile 1, Profile 2, etc). Required for Edge only
- **chromium_driver:** Path to your chromedriver (i.e. ```/usr/lib/chromium-browser/chromedriver```). Required for Chromium only
- **playlist_link:** Full YouTube playlist URL
- **playlist_name:** Must match exactly (case sensitive)
- **max_videos:** Maximum amount of videos to add before ending script. Default = 10
- **subs:** List of channel names

### 3. **Account login setup**
This script **does not** require, see, or use your YouTube login information.
1. Open your browser and switch to your chosen browser profile (it is recommened to create a new profile, sepecifically for Upnext)
2. Log into YouTube
3. Save login credentials
4. Close browser, then re-open and confirm you are still logged into YouTube

## Usage
Run the script:

```python upnext.py```

What will happen:
1. Browser window will open with your selected browser profile
2. Videos will be removed from your defined playlist
3. Unwatched videos will be added to your playlist based on selected channel names

## Automation
As mentioned, **Upnext** works best when it is automated. You can schedule it using:
- Linux -> cron job
- Windows -> Task Scheduler

## Using as a Module
You can also import and reuse functions from **Upnext** in your own project:

```
from upnext.upnext import browser_setup, playlist_cleanup, playlist_build

browser = browser_setup(
    browser="chromium",
    profile_path="/path/to/profile/",
    chromium_driver="/path/to/chromedriver"
)

subs = ["Channel A", "Channel B"]

playlist_cleanup(browser, "https://youtube.com/playlist?list=XXXX")
playlist_build(
    browser,
    subs_to_keep=subs,
    playlist_name="My Playlist",
    max_videos=10,
    close_browser=True
)
```

## Known Issues
- There *may* be a crash when using Chromium on Raspberry PI that occurs as **Upnext** tries to access YouTube. This isn't caused by the script, but an issue with Chromium (read more about it [here](https://forums.raspberrypi.com/viewtopic.php?t=323640)). A "quick fix" is to edit your cookie settings in Settings -> Privacy -> Cookies -> Always clear cookies when windows are closed -> Add YouTube to list in this format: ```[*.]youtube.com``` and be sure to click the option that removes 3rd party cookies
- YouTube UI changes, which may break script selectors temporarily
- Sometimes (rarely), YouTube will "hang" when loading the subscription page. This may require rerunning the script

## Disclaimer
By using this script, you agree that I am not liable for any damage or action to your device/account, and you take responsibility for what may or may not happen to your device/account.

[^1]: In some cases, you may find that ChromeDriver is already in your system files by default. If it is already on your system by default, it may be located at ```/usr/lib/chromium-browser/chromedriver```
