# Command and control servers in social media

Script is a proof of concept how to control your machine by using social media platforms.

# Description and usage

Script has following functions:

- **history** - (Re)Tweet #history, like photo on Instagram with 'history' in description or wrote 'history' to Telegram bot to delete your browser history (works only for Firefox).
- **mac** - (Re)Tweet #mac, like photo in Instagram with 'mac' in description or wrote 'mac' to Telegram bot to get MAC address.
- **location** - (Re)Tweet #location, like photo in Instagram with 'location' in description or wrote 'location' to Telegram bot in order to obtain last SSID(s) and IP from ipify.org.
- **update** - (Re)Tweet #update, like photo in Instagram with 'update' in description or wrote 'update' to Telegram bot to get keywords from youtube comments.

**Script can be highly customized:**

You can choose social site which will be used, by default it uses:

- Instagram
- Twitter
- Youtube
- Telegram

`pip install InstagramAPI tweepy telegram`

and for each one, you need API key beside Instagram, which uses username and password.

**Keywords (history, mac, location, update) can be changed to something more fancy or stealthy.**

Comments from Youtube are retrieved based on startswith() function and first letters of each consecutive word from hardcoded video.

Code is commented very well, so you shouldn't have problem with integrating it to your project.

Tested on Win7 and Win10.

![Alt Text](https://i.imgur.com/oIc1rk8.gif)

![Alt Text](https://i.imgur.com/hXy1Mu0.gif)

![Alt Text](https://i.imgur.com/P1TjAE1.png)

**I am not responsible for what you will do with this, be cautious.**

Questions? Contact: [@PoszerzHoryzont](https://twitter.com/@PoszerzHoryzont)
