#! python3
# InternetSpeed.py - Checks my Comcast internet speed and posts to Twitter if below a threshold.

import speedtest
import tweepy
import json

# Initialize Twitter function

def authenticate_twitter(c_key, c_secret, a_token, a_secret):
    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_secret)
    return tweepy.API(auth)


def main():
    # Open configuration file
    with open('config_file.json') as fh:
        config = json.load(fh)
        
    download_speed = config["download_speed"]
    threshold = config["speed_threshold"]
    isp_twitter = config["isp_twitter"]

    # Twitter setup
    twitter_api = authenticate_twitter(
        config["consumer_key"], config["consumer_secret"],
        config["access_token"], config["access_token_secret"]
    )

    # Call speedtester API to get your current internet speed
    speedtester = speedtest.Speedtest()
    speedtester.get_best_server()

    # Transform your speed from B/s to MB/s and round it to 2 decimal places.
    d_speed = round(speedtester.download() / (1024 ** 2), 2)

    # Tweet to your ISP if your speed is below a threshold, otherwise just tell you your speed.
    if d_speed < download_speed - threshold:
        twitter_api.update_status("{} why is my download speed {} MB/s when I pay for {} MB/s? "
                                  "Fix it please!".format(isp_twitter, d_speed, download_speed))
        print("Tweet sent. Your speed is {}".format(d_speed))

    else:
        print("Your speed is {} MB/s. No tweet sent.".format(d_speed))


main()
