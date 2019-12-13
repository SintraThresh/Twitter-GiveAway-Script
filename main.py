import json
import re
import time
import os
import sys

try:
    import pyfiglet
    import jsonpickle
    import pandas as pd
    import tweepy
except ImportError:
    import subprocess
    print('worked')
    subprocess.call([sys.executable, "-m", "pip", "install", 'pyfiglet'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'jsonpickle'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'pandas'])
    subprocess.call([sys.executable, "-m", "pip", "install", 'tweepy'])
    os.system('cls')

class DNPTwitterGiveawayChooser:

    def __init__(self,
                 tweet_url=None,
                 creds_file='twitter_credential.json',
                 filename='giveaway.csv',
                 contest_name='DNP3 Giveaway',
                 query_delay=0,
                 suspense_time=10,
                 choose_winner=False,
                 show_names=False,
                 autorun=True,
                 members_to_follow=['dnpthree'],
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
            #print(tweet_id)
            return self.api.get_status(tweet_id, tweet_mode='extended')
    def get_all_tweets(self, max_id=-1,max_tweets=10000000, write_file=False):
        sinceId = None
        max_id = max_id
        maxTweets = max_tweets
        split = int(self.tweet_ratio * len(self.tweet.full_text.split()))
        tweet_text = ' '.join(self.tweet.full_text.split()[:split])
        print(tweet_text)
        searchQuery = 'RT @{author} '.format(author=self.author) + self.tweet.full_text
        tweetCount = 0
        tweetsPerQry = 100
        print('[+] Retrieving all contest tweets for TWEET ID: ' + str(self.tweet_id) + '\n Tweet text: ' + str(self.tweet.full_text))
        print("[*] Downloading max {0} tweets".format(maxTweets))
        with open(self.filename,'w') as f:    
            while tweetCount < maxTweets:
                try:
                    if(max_id <= 0):
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,)
                            #print(new_tweets)
                        else:
                            new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
                    else:
                        if(not sinceId):
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id -1))
                        else:
                            new_tweets = self.api.search(q=searchQuery,count=tweetsPerQry,max_id=str(max_id - 1), since_id=sinceId)
                    if not new_tweets:
                        print("[!] No more tweets found")
                        break
                    for tweet in new_tweets:
                        self.all_tweets.append(tweet._json)
                        if write_file:
                            f.write(jsonpickle.encode(tweet._json, unpicklable=False)+'\n')
                    tweetCount += len(new_tweets)
                    time.sleep(self.query_delay)
                    print("[*] Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    print("[!] Error: "+str(e))
                    break
        print('[*] File written to %s' % self.filename)

    def get_users(self, show_names=True, from_file=False):
        users_who_retweeted = None
        print('[*] Identifying Users who Retweeted')
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
            print("[*] %s users have benn entered into the drawing" % len(users_who_retweeted))
            if show_names:
                print('[*] Showing names of contestants...')
                print(users_who_retweeted)
            return users_who_retweeted
    @staticmethod
    def name_check(series, name):
        name = str.lower(name)
        if series[series.str.contains(name)].any():
            print('%s is entered in the giveaway! :)' % name)
        else:
            print('%s is not entered in the giveaway :(' % name)
    def check_relationship(self, user_a=None, user_b=None, verbose=False):
        """
        user_a: Person you want to check is being followed
        user_b: Person who should be following
        """
        friends = self.api.show_friendship(source_screen_name=user_a, target_screen_name=user_b)
        following = friends[1].following
        if verbose:
            if following:
                print(F'{user_b} is following {user_a}!')
            else:
                print(F'{user_b} is NOT following {user_a}!')
        return following
    def remove_user(self, series, user):
        try:
            index_position = series[series == user].index[0]
            print(F'[-] {series.pop(index_position)} removed from eligible list')
        except Exception as e:
            if self.verbose:
                print(F'[!!] Error: {e}')
    def choose_winners(self):
        print("[*] Randomly selecting winner...")
        print("[*] Choosing winner(s) for {contest_name}".format(contest_name=self.contest_name))
        time.sleep(self.suspense_time)
        random_users=list(self.users.sample(self.winner_count).values)
        try:
            while len(self.winner_list) < self.winner_count:
                for user in random_users:
                    participant_eligible = False
                    for member in self.members_to_follow: #REMOVED UNNECESSARY FOR LOOP
                        if self.check_relationship(user_a=member, user_b=user, verbose=False):
                            participant_eligible=True
                        else:
                            self.check_relationship(user_a=member, user_b=user, verbose=False)
                            participant_eligible=False
                            print(F'[0xFF] {user} is not following {member} - REROLLING... F\'s')
                            self.remove_user(self.users,user)
                            random_users.remove(user)
                            new_user = self.users.sample(1).values[0]
                            print(F'[+] Adding {new_user} to eligible list and checking followers')
                            random_users.append(new_user)
                            break
                    if participant_eligible and user not in self.winner_list:
                        self.winner_list.append(user)
                        member = ','.join(self.members_to_follow[0])
                        print(F"[W {str(len(self.winner_list))}/{str(self.winner_count)}] - {user}")
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
            self.present_winner()
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

def resetKeys():
    os.remove('twitter_credential.json')
    exit()
    
def start():
    try:
        with open('twitter_credential.json','r') as p:
            credentials = json.load(p)
    except FileNotFoundError:
        with open('twitter_credential.json','w') as credentials:
            Key = input('Please enter in your key:\n')
            Key = Key.replace(' ','')
            os.system('cls')
            KeySecret = input('Please enter in your key secret:\n')
            KeySecret = KeySecret.replace(' ','')
            os.system('cls')
            Token = input('Please enter in your token:\n')
            Token = Token.replace(' ','')
            os.system('cls')
            TokenSecret = input('Please enter in your token secret:\n')
            TokenSecret = TokenSecret.replace(' ','')
            newCred = {"CONSUMER_KEY": Key,
                    "CONSUMER_SECRET": KeySecret,
                    "ACCESS_TOKEN": Token,
                    "ACCESS_SECRET": TokenSecret}
            json.dump(newCred, credentials)
            exit()
    def urlFunction():       
        url = input('Please enter in the target tweet the giveaway will be centered around (You can use /help for commands):\n')
        if url == '/help':
            print('/keys         Goes into resetting your keys.\n/clear         Clears the command prompt.\n')
            urlFunction()
        if url == '/keys':
            os.system('cls')
            resetKeys()
            exit()
        if url == '/clear':
            os.system('cls')
            exit()
        cycle = input('How many people are required to be followed in order for the contestants to be eligible?:\n')
        members_to_follow = []
        for loop in range(1, int(cycle)+1):
            followers = input('Please input the username of the person required to be followed ({}/{}):\n'.format(str(loop), str(cycle)))
            members_to_follow.append(followers)
        dnp_giveaway = DNPTwitterGiveawayChooser(tweet_url=url,
                                                choose_winner=True,
                                                winner_count=1,
                                                tweet_ratio=.95,
                                                filename='50_5.csv',
                                                autorun=True,
                                                query_delay=0,
                                                suspense_time=0,
                                                members_to_follow=members_to_follow,
                                                contest_name='Sintra')
    urlFunction()
start()
