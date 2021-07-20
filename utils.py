import tweepy
from datetime import datetime
from pytz import timezone
from config import *

# Authenticate to Twitter
twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
twitter_auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(twitter_auth)

# Util functions
def log(level, msg):
    print("[" + str(datetime.now()) + "] [" + level + "] " + msg)

def str_to_datetime(str):
    return datetime.fromisoformat(str[:-1]).replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))

def generate_request_js(url):
    script = '''
    function httpGet(theUrl)
    {
        let xmlhttp;
        
        if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        } else { // code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                return xmlhttp.responseText;
            }
        }
        xmlhttp.open("GET", theUrl, false);
        xmlhttp.setRequestHeader("accept", "application/json, text/plain, */*");
        xmlhttp.setRequestHeader("authorization", "Bearer ''' + CAPTCHA_KEY + '''");
        xmlhttp.send();
        
        return xmlhttp.response;
    }
    return httpGet("''' + url + '''");
    '''
    return script