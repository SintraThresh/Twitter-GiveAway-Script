import json
import re
import time
import sys

try:
    import pyfiglet
    import jsonpickle
    import pandas as pd
    import tweepy
except ImportError:
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", 'pyfiglet'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'jsonpickle'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'pandas'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'tweepy'])

class TwitterGiveawayChooser:

    def __init__(self,
                 tweet_url=None,
                 creds_file='twitter_credential.json',
                 filename='giveaway.csv',
                 contest_name='',
                 query_delay=0,
                 suspense_time=10,
                 choose_winner=False,
                 show_names=False,
                 autorun=True,
                 members_to_follow=[''],
                 verbose=False,
                 tweet_ratio=.95,
                 wait_on_rate_limit=False,
                 winner_count=1):
        self.user = None
        self.creds = json.load(open(creds_file))
        self.auth = tweepy.OAuthHandler(self.creds['CONSUMER_KEY'],self.creds['CONSUMER_SECRET'])
        self.auth.set_access_token(self.creds['ACCESS_TOKEN'], self.creds['ACCESS_SECRET'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit = wait_on_rate_limit)
        self.filename = filename
        self.tweet_id = None
        self.suspense_time= suspense_time
        self.query_delay = query_delay
        self.choose_winner = choose_winner
        self.contest_name = contest_name
        self.winner_count = winner_count
        self.show_names = show_names
        self.users = None
        self.members_to_follow = members_to_follow
        self.winner_list = []
        self.all_tweets = []
        self.verbose = verbose
        self.tweet_ratio = tweet_ratio
        self.final_df = None
        if tweet_url:
            try:
                self.tweet_id = self.id_from_url(tweet_url)
            except Exception as e:
                print(F'Could not process URL: {e}')
        if self.tweet_id:
            self.tweet = self.get_tweet_text_by_id(int(self.tweet_id))
            self.author = self.tweet.author.screen_name
        if autorun:
            self.get_all_tweets_and_contest_users()
    def id_from_url(self, url):
        digit = re.search('[\d+]{10,}', url)
        if digit:
            return digit.group(0)
    def get_tweet_text_by_id(self, tweet_id=None):
        if tweet_id:
            return self.api.get_status(tweet_id, tweet_mode='extended')
    def get_all_tweets(self, max_id=-1,max_tweets=10000000, write_file=False):
        sinceId = None
        max_id = max_id
        maxTweets = max_tweets
        searchQuery = F'RT @{self.author} '+ self.tweet.full_text
        tweetCount = 0
        tweetsPerQry = 100
        with open(self.filename,'w') as f:
            while tweetCount < maxTweets:
                try:
                    if(max_id <= 0):
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry)
                        else:
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
                    else:
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id -1))
                        else:
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id - 1), since_id=sinceId)
                    if not new_tweets:
                        break
                    for tweet in new_tweets:
                        self.all_tweets.append(tweet._json)
                        if write_file:
                            f.write(jsonpickle.encode(tweet._json, unpicklable=False)+'\n')
                    tweetCount += len(new_tweets)
                    print(F'Tweets: {tweetCount}')
                    time.sleep(self.query_delay)
                    max_id = new_tweets[-1].id
                except:
                    half_tweet = int(len(self.tweet.full_text)/2)
                    searchQuery = F'RT @{self.author} '+ self.tweet.full_text[0:half_tweet]
                    if(max_id <= 0):
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry)
                        else:
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
                    else:
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id -1))
                        else:
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id - 1), since_id=sinceId)
                    if not new_tweets:
                        break
                    for tweet in new_tweets:
                        self.all_tweets.append(tweet._json)
                        if write_file:
                            f.write(jsonpickle.encode(tweet._json, unpicklable=False)+'\n')
                    tweetCount += len(new_tweets)
                    print(F'Tweets: {tweetCount}')
                    time.sleep(self.query_delay)
                    max_id = new_tweets[-1].id
                    break

    def get_users(self, show_names=True, from_file=False):
        users_who_retweeted = None       #Responsible for the list of all participants
        if from_file:
            retweets = pd.read_json(self.filename, lines=True)
            parsed_users = pd.concat([pd.DataFrame(x) for x in retweets.user], sort=False)
            users_who_retweeted = parsed_users.reset_index()['screen_name'].drop_duplicates()
        if self.all_tweets:
            df = pd.concat([x for x in pd.DataFrame(self.all_tweets).user.apply(pd.DataFrame)], sort=False)
            users_who_retweeted = df.reset_index()['screen_name'].drop_duplicates()
            self.final_df = df
        if users_who_retweeted.any():
            users_who_retweeted.reset_index(drop=True, inplace=True)
            return users_who_retweeted
    @staticmethod
    def name_check(series, name):
        name = str.lower(name)
    def check_relationship(self, user_a=None, user_b=None, verbose=False):
        """
        user_a: Person you want to check is being followed
        user_b: Person who should be following
        """
        friends = self.api.show_friendship(source_screen_name=user_a, target_screen_name=user_b)
        following = friends[1].following
        return following
    def remove_user(self, series, user):
        try:
            index_position = series[series == user].index[0]
        except:
            pass
    def choose_winners(self):
        time.sleep(self.suspense_time)
        random_users=list(self.users.sample(self.winner_count).values)
        try:
            while len(self.winner_list) < self.winner_count:
                for user in random_users:
                    participant_eligible = False
                    if len(self.members_to_follow) != 0:
                        for member in self.members_to_follow: #REMOVED UNNECESSARY FOR LOOP
                            if self.check_relationship(user_a=member, user_b=user, verbose=False):
                                participant_eligible=True
                            else:
                                self.check_relationship(user_a=member, user_b=user, verbose=False)
                                participant_eligible=False
                                random_users.remove(user)
                                new_user = self.users.sample(1).values[0]
                                random_users.append(new_user)
                                break
                        if participant_eligible and user not in self.winner_list:
                            self.winner_list.append(user)
                            member = ','.join(self.members_to_follow[0])
                    else:
                        participant_eligible = True
                        self.winner_list.append(user)
        except Exception as e:
            print(F'[!] No more users to choose from {e}')
            pass
    def present_winner(self):
        if self.winner_list:
            print(F'{len(self.winner_list)} winners identified')
            winners = [pyfiglet.figlet_format(x) for x in self.winner_list]
            twittwer_handles = ['Twitter: https://www.twitter.com/'+x for x in self.winner_list]
            final_winners= zip(winners, twittwer_handles)
            for user, twittwer_handles in final_winners:
                print(user), print(twittwer_handles)
            print('Twitter handles:'+','.join(['@'+x for x in self.winner_list]))
            print("-" * 60 + "\n")
        else:
            print('[!!] No eligible users!')
    def get_all_tweets_and_contest_users(self, file_exists=False):
        self.get_all_tweets()
        self.users = self.get_users(show_names=self.show_names)
        if self.choose_winner:
            self.choose_winners()
        return
    def retrieve_video_url(self):
        """Retrieves video URL - make sure to set process to False"""
        highest_bitrate = 0
        video_url = None
        for vid_url in self.tweet._json['extended_entities']['media']:
            for vid_info in vid_url['video_info']['variants']:
                if 'bitrate' in vid_info:
                    if vid_info['bitrate'] > highest_bitrate:
                        highest_bitrate = int(vid_info['bitrate'])
                        video_url = vid_info['url']
        if video_url:
            return video_url

def GStart(tweetlink, followers, winCount):
    try:
        url = tweetlink
        members_to_follow = followers
        winCount = int(winCount)
        Tgiveaway = TwitterGiveawayChooser(tweet_url=url,
                                    choose_winner=True,
                                    winner_count=winCount,
                                    tweet_ratio=.95,
                                    filename='50_5.csv',
                                    autorun=True,
                                    query_delay=0,
                                    suspense_time=0,
                                    members_to_follow=members_to_follow,
                                    contest_name='')
        return Tgiveaway.winner_list
    except Exception as p:
        print(p)
        if str(p) == "[{'code': 144, 'message': 'No status found with that ID.'}]" or str(p) == "'TwitterGiveawayChooser' object has no attribute 'author'":
            return '|tweet|'
        if str(p) == "[{'code': 32, 'message': 'Could not authenticate you.'}]":
            return '|keys|'
        if str(p) == "'NoneType' object has no attribute 'any'":
            return '|rate|'
        else:
            return '|Error|'

