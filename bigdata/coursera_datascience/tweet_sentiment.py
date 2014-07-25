import sys
import json


def get_sentiments(filep):
    sentiments = {}
    for line in filep:
        term, sentiment = line.split("\t")
        sentiments[term.lower()] = int(sentiment) 
    return sentiments

def get_score(jsonline, sentiments):
    final_score = 0
    this_tweet = json.loads(jsonline)
    try:
        for word in  this_tweet[u'text'].split():
            if word in sentiments:
                final_score += sentiments[word]
    except KeyError:
        pass
    return final_score

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentiments = get_sentiments(sent_file)
    keys = sentiments.keys()
    final_scores = []
    for i in tweet_file:
        this_score = get_score(i, sentiments)
        final_scores.append(this_score)
    for score in final_scores:
        print score
if __name__ == '__main__':
    main()
