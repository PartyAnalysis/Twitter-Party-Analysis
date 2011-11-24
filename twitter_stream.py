import tweepy
import mysql.connector
import re

#Datubāzes inicializācija
HOST = "localhost"
USER = "grupa6"
PASSWORD = "Eehoh6oh"
DATABASE = "grupa6"

db = mysql.connector.Connect(host = HOST, user = USER, password = PASSWORD, database = DATABASE)
cur = db.cursor()

#Twitter OAuth inicializācija
ConsumerKey = ''
ConsumerSecret = ''
AccessToken = ''
AccessTokenSecret = ''

auth1 = tweepy.auth.OAuthHandler(ConsumerKey, ConsumerSecret)
auth1.set_access_token(AccessToken, AccessTokenSecret)

#Atslēgas vārdu veidošana
cur.execute ("""select foursq_id, name, twitter from venues""")
result = []
columns = tuple([d[0] for d in cur.description])
for row in cur:
  result.append(dict(zip(columns, row)))
k = [] #Keywords
for i in result:
    if i['twitter'] != None and len(i['twitter'].split()) == 1:
        k.append(i['twitter'].encode('utf8'))
db.commit()

#Noskaidro pēc kura atslēgas vārda atrasts tvīts
reg = re.compile(r'(?i)\b(?:%s)\b' % '|'.join(k))

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
                res = reg.search(status.text)
                if res != None:
                    q = 'INSERT INTO tweets (`tweet_id`, date, `screen_name`, `text`, `keyword`) VALUES (%s, NOW(), %s, %s, %s)'
                    cur.execute(q, (status.id, status.author.screen_name, status.text, res.group(0),))
                    db.commit()
        except Exception, e:
            pass
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

#Pieslēdzamies Twitter Streaming API
l = CustomStreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l, secure=True)   

#Strīma filtra uzstādīšana 
setTerms = k
streamer.filter(None, setTerms)
