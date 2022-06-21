# Upnext - An automated Youtube playlist builder for Chromium

Upnext is a YouTube playlist builder for the Chromium browser, which will remove old videos and add new videos to a specified playlist, based on channel subscription choices that you specify.

The main idea behind this project is for it to run as a cronjob on a Raspberry Pi, allowing you to have Youtube playlists built for you at any time of your choosing, automatically. Upnext ignores videos you have already watched throughout the day, so no need to worry about having videos you already watched getting added to the playlist.

# Requirements
- Chromium browser
- Python 3.x
- Selenium 4.x
- A Linux based system, probably. This has only been tested on Raspian (at the moment)

# Setup and Instructions
1) Download the correct ChromeDriver for your version of Chromium (if no version exists on your device already[^1]). It can be downloaded [here](https://chromedriver.chromium.org/).
2) The script **does not** require your login information. Open Chromium, log into your Youtube account, and ensure your login details are saved. Close the browser, reopen it, and go to Youtube to ensure you are still logged in.
3) Create a new playlist in your Youtube account. You can use an existing one, but it is recommeneded to keep your automation playlist separate (**OPTIONAL**) 
4) Install [Selenium](https://selenium-python.readthedocs.io/) if you do not have it already ```pip install selenium```.
5) Open upnext.py in your IDE of choice and navigate to the "# user settings" section:

   * **gc_driver** - The full location where you have your ChromeDriver saved. For example, ```/usr/lib/chromium-browser/chromedriver```
   * **gc_profile** - This is the location of your Chromium user profile. It may be located at ```/home/*your_name*/.config/chromium/```
   *  **playlist_link** - The direct link to your playlist on Youtube. It should look something like this: ```https://www.youtube.com/playlist?list=somerandomstringoflettersandnumbers```
   *  **subs_to_keep** - The list of channels you would like the script to add to your playlist. **Not** case sensitive. Ensure that the channels are separated by single quotes and a comma within the list bracket. For example: ```subs_to_keep = ['channel 1', 'channel 2', 'channel 3']```

6) Before running the script, ensure Chromium is closed.

In order to set up cronjobs and having it run automatically at specified times, I recommened checking out the plethora of cronjob resources out there (just to keep this README at a reasonable amount of text).

# Planned Updates
- Additional browser support
- Support for Windows/other distributions of Linux[^2]
- Command line interface so editing the code is not required

# Possible Issues
- Having an instance of Chromium open while the script runs will cause it to fail. Ensure to either use a different browser, or run the script when you won't be using your browser
- There isn't much error handling at the moment. If a weird issue arises you will see the Python error associated with why the script failed. Feel free to report any you run into. It will help immensly with trying to catch any and all possible errors that have not yet appeared in my testing
- Youtube code changes. If/when Youtube changes something, it may cause this script to fail. This isn't a huge concern from a development standpoint because I can always modify the script to adjust. If I fail to catch a change before you do, please report

[^1]: In some cases, you may find that ChromeDriver is already in your system files by default. If it is already on your system by default, it may be located at ```/usr/lib/chromium-browser/chromedriver```
[^2]: It may work for these platforms with or without minimal modification, I just have not tested this yet
