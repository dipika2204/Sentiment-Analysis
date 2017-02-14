import json
import collections
import pprint as pp
No_of_tweet=0;
No_of_nontweet=0;
No_of_hashtags=0;
text_of_tweet = []
text_array= []
sentiment= {}
data = []
hashtags=[]
hash={}
sortedhash={}
topthree={}
trendin={}
hash_senti={}
#positive_negative_sentiments_file
afinnfile = open("AFINN-96.txt")
scores = {} # initialize an empty dictionary
for line in afinnfile:
  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  scores[term] = int(score)  # Convert the score to an integer.


#my file operations
fname = raw_input("Enter file name: ")
with open(fname) as f:
    for line in f:
        data.append(json.loads(line))
        numLines=len(data) 
        #print numLines       
print "No of Objects of twitter in my Json file: ",len(data),"\n"
for tweet in data:
    if tweet.get('created_at'):
        No_of_tweet=No_of_tweet+1           
        
        if tweet.get('text'):
            text_of_tweet=tweet['text'].encode('utf-8')
            text_array=text_of_tweet.split(" ")
            senti=0
            for posneg in text_array:
                if posneg.decode('utf-8').lower() in scores.keys():
                    senti=senti+ int(scores[posneg.encode('utf-8').lower()])     
        if tweet.get('entities'):
            if tweet['entities']['hashtags'] != []:
                hashtags=tweet['entities']['hashtags']
                No_of_hashtags=No_of_hashtags+1
                #print hashtags
                for hashing in hashtags:
                    if(hashing['text'].encode('utf-8') in hash.keys()):
                       hash[hashing['text'].encode('utf-8')]+=1 
                    else:
                        hash[hashing['text'].encode('utf-8')]=1                        
                    if(hashing['text'].encode('utf-8') in sentiment.keys()):
                       sentiment[hashing['text'].encode('utf-8')]=sentiment[hashing['text'].encode('utf-8')]+senti
                    else:
                        sentiment[hashing['text'].encode('utf-8')]=senti                       
            #print text_array
        
    else:
        No_of_nontweet=No_of_nontweet+1
        #print 'No Tweet' 


for tag in hash:
    hash_senti[tag]=float(sentiment[tag])/float(hash[tag])

#print hash_senti
print "No of Tweets in the file:",No_of_tweet,"\n"
print "No of non-tweets in the file:",No_of_nontweet,"\n"
print "No of Tweets having Hashtags:",No_of_hashtags,"\n"
print "Most popular Hashtags:"
for key, value in sorted(hash.iteritems(), key=lambda (k,v): (v,k),reverse=True)[:10]:
    print key,value
    trendin[key]=hash_senti[key]
    #print (key,value,hash_senti[key])
print "\nSentiments of popular Hashtags: "
pp.pprint (trendin)

for key, value in sorted(trendin.iteritems(), key=lambda (k,v): (v,k),reverse=True)[:1]:
    print "\nPositive sentiment of",key,"is:",value,"\n"

for key, value in sorted(trendin.iteritems(), key=lambda (k,v): (v,k),reverse=True)[9:10]:
    print "\nNegative sentiment of",key,"is:",value,"\n"

