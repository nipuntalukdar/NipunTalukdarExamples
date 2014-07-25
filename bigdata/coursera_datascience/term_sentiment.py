import sys
import json

def strlower(x):
    return x.lower()

def get_given_sentiments(tweet, sentiments):
    allwords = {}
    givensents = {}
    tweetwords = map(strlower, tweet.split()) 
    wordcount = len(tweetwords)
    i = 0
    while i < wordcount:
        if tweetwords[i] in sentiments:
            givensents[i] = sentiments[tweetwords[i]]
        else:
            if not tweetwords[i].replace('.','').isdigit():
                allwords[i] = tweetwords[i]
        i += 1
    return givensents,allwords
        
def compute_term_sentiment(tweettext, term_sents, sentiments):
    tweet = json.loads(tweettext)
    if u'text' not in tweet:
        return {}
    given, others = get_given_sentiments(tweet[u'text'], sentiments) 
    givenkeys = given.keys()
    otherkeys = others.keys()
    scorenew = {}
    for otherpos in otherkeys:
        thiscore = 0.0
        for pos in givenkeys:
            thiscore += float(1 - abs(pos - otherpos) / 100.0) * float(given[pos])
        if others[otherpos] in scorenew:
            scorenew[others[otherpos]]['score'] += thiscore
            scorenew[others[otherpos]]['count'] += 1
        else:
            scorenew[others[otherpos]] = {'score' : thiscore, 'count' : 1}
    return scorenew 
            
             

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


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentiments = get_sentiments(sent_file)
    term_sents = {}
    for i in tweet_file:
        newwordsents = compute_term_sentiment(i, term_sents, sentiments)
        for wordsent in newwordsents:
            if wordsent in term_sents:
                term_sents[wordsent]['score'] += newwordsents[wordsent]['score']
                term_sents[wordsent]['count'] += newwordsents[wordsent]['count']
            else:
                term_sents[wordsent] = newwordsents[wordsent]
    final_sents = {}
    for newwd in term_sents:
        final_sents[newwd] = float(term_sents[newwd]['score'] / term_sents[newwd]['count'])
    for newwd in final_sents:
        print newwd, final_sents[newwd]             
if __name__ == '__main__':
    main()

