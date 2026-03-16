# Upnext - An automated YouTube playlist builder

**Upnext** is an automated YouTube playlist builder that will remove old videos (if any) and add new videos to a specified playlist, based on channel subscription choices that you specify. It ignores videos you have already watched, so no need to worry about having videos you already watched getting added back to the playlist. This can be set up to run on a schedule (probably the best use for it), meaning, you can have YouTube playlists built for you at any time of your choosing, ready to go whenever.

**Upnext** started as a YouTube playlist builder for the Chromium browser, with the main idea being it would run as a cronjob on a Raspberry Pi. However, it has since transformed to work across multiple browsers and multiple operating systems.

# Compatible Browsers / OS
- FireFox (Widnows)
- Chrome (Windows)
- Edge (windows)
- Chromium (Linux)

# Basic Setup and Instructions
1) Upnext now automatically detects and downloads the appropriate driver for your chosen browser via the Selenium package. The exception is Chromium. In order to set up Upnext with Chromium, you need to download the correct ChromeDriver for your version of Chromium (if no version exists on your device already[^1]). It can be downloaded [here](https://chromedriver.chromium.org/).
2) For supported browsers (like FireFox), it is recommended you create a new profile, specifically for use of this script. This will allow you to use the same browser at the same time the script is running. If you attempt to run Upnext from the same profile you currently have a browser window up in, the script will not run correctly.
3) The script **does not** require your login information. Open your browser, switch to the Profile you created for Upnext (if you did), log into your YouTube account, and ensure your login details are saved. Close the browser, reopen it, and go to YouTube to ensure you are still logged in. Once confirmed, close your browser once again.
4) Create a new playlist in your YouTube account. You can use an existing one, but it is recommeneded to keep your automation playlist separate. 
5) Run upnext.py once to generate your "upnext_settings.yaml" file. Once done, open it up and update your settings:

   * **browser_choice** - Your chosen browser, contingent upon compatibility (see above). Case insensitive.
   * **browswer_profile** - This is the location of your browser user profile. It is located in different locations depending on the 
   browser. For example, for Chromium it may be located at ```/home/your_name/.config/chromium/```, but FireFox it may be located at ```C:\Users\yourname\AppData\Roaming\Mozilla\Firefox\Profiles\RandomString.Profile Number```
   * **edge_profile** - Required if using Edge browser. The name of your profile (i.e. Profile 1, Profile 2, etc)
   * **chromium_driver** - The full location where you have your ChromeDriver saved. For example, ```/usr/lib/chromium-browser/chromedriver```
   *  **playlist_link** - The direct link to your playlist on YouTube. It should look something like this: ```https://www.youtube.com/playlist?list=somerandomstringoflettersandnumbers```
   *  **subs** - The list of channels you would like the script to add to your playlist. **Not** case sensitive. Ensure that the channels are separated by a new line with a dash. For example: 
   ```
   subs:
   - Channel 1
   - Channel 2
   - Channel 3
   ```

If you want Upnext to run on a schedule, I recommened creating a cronjob (if using Linux) or utilizing Task Scheduler (if using Windows). 

# Issues out of my control
- There *may* be a crash when using Chromium on Raspberry PI (but also on any platform) that occurs as Upnext tries to access YouTube. This isn't caused by the script, but an issue with Chromium (read more about it [here](https://forums.raspberrypi.com/viewtopic.php?t=323640)). A "quick fix" is to edit your cookie settings in Settings -> Privacy -> Cookies -> Always clear cookies when windows are closed -> Add YouTube to list in this format: ```[*.]youtube.com``` and be sure to click the option that removes 3rd party cookies as well
- YouTube code changes. If/when YouTube changes something, it may cause this script to fail. This isn't a huge concern from a development standpoint because I can always modify the script to adjust. If I fail to catch a change before you do, please report

# Disclaimer
By using this script, you agree that I am not liable for any damage or action to your device/account, and you take responsibility for what may or may not happen to your device/account.

[^1]: In some cases, you may find that ChromeDriver is already in your system files by default. If it is already on your system by default, it may be located at ```/usr/lib/chromium-browser/chromedriver```
