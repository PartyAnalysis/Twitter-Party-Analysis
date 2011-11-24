# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import tweepy
import MySQLdb
import textwrap

db = MySQLdb.Connect(charset='utf8', init_command='SET NAMES UTF8', host="localhost", user="root", passwd="", db="twitter")
cur = db.cursor()

f = open('tweets.txt','w')

ConsumerKey = ''
ConsumerSecret = ''
AccessToken = ''
AccessTokenSecret = ''

auth1 = tweepy.auth.OAuthHandler(ConsumerKey, ConsumerSecret)
auth1.set_access_token(AccessToken, AccessTokenSecret)
#api = tweepy.API(auth1)

class CustomStreamListener(tweepy.StreamListener):
    status_wrapper = textwrap.TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    f = open('tweets.txt','w')
    db = MySQLdb.Connect(host="localhost", user="root", passwd="", db="twitter")
    def on_status(self, status):
        try:
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
            print self.status_wrapper.fill(status.text)

            print >> f, '-' * 60 + '\n %s \n %s \n' % (status.author.screen_name, status.created_at)
            #print >> f, self.status_wrapper.fill(status.text)
            print >> f, self.status_wrapper.fill(status.text.encode('utf-8'))
            
            #jaunas rindas
            #newtext =  status.text
           # newtext.encode('utf-8')
            

            q = 'INSERT INTO tweetz (`date`, `text`, `tweet_id`) VALUES (NOW(), %s, %s)'


            cur.execute(q, (status.text, status.id))
            #cur.execute(q, (newtext, status.id)) 

            db.commit()
           
        except Exception, e:
            pass
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True
    

l = CustomStreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l, secure='secure')   



setTerms = [

'puolue',
'partei',
'šalis',
'strona',
'Partei',
'partito',
'parti',
#'party',
'ballīte',
'juovuksissa',
'täisjoonud',
'pasigėręs',
'zalany',
'trunken',
'brillo',
'ivre',
'pālī',
'berusad',
'beruset',
'humalassa',
'purjus',
'girtas',
'pijany',
'betrunken',
'ubriaco',
#'bu',
#'drunk',
'piedzēries',
'baksmälla',
'bakrus',
'krapula',
'pohmelus',
'pagirios',
'kac',
'Kater',
'Una notte da leoni',
'gueule de bois',
'hangover',
'pohas',
'kohmelo',
'liekana',
'kociokwik',
'Katzenjammer',
'pohains'

]
streamer.filter(None, setTerms)
