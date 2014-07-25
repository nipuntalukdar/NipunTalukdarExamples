import sys
import json



def main():
    tweet_file = open(sys.argv[1])
    hashtags = {}
    counttags = {}
    for i in tweet_file:
        tweetj = json.loads(i)
        if u'entities' not in tweetj:
            continue
        for tag in tweetj[u'entities'][u'hashtags'] :
            tagtext = tag[u'text'].lower()
            if tagtext in hashtags:
                hashtags[tagtext] += 1
            else:
                hashtags[tagtext] = 1
            currentcount = hashtags[tagtext]
            if currentcount > 1:
                counttags[currentcount - 1].remove(tagtext)
                if not counttags[currentcount - 1]:
                    del counttags[currentcount - 1]
            if currentcount not in counttags:
                counttags[currentcount] = set()
            counttags[currentcount].add(tagtext) 
    tweet_file.close()
    tagprinted = 0
    for count in reversed(counttags.keys()):
        for tag in counttags[count]:
            print tag,count
            tagprinted += 1
            if tagprinted == 10:
                break
        if tagprinted == 10:
            break
if __name__ == '__main__':
    main()

