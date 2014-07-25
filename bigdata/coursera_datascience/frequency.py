import sys
import json

def strlower(x):
    return x.lower()

def main():
    tweet_file = open(sys.argv[1])
    totalcount = 0
    frequency = {}
    for i in tweet_file:
        try:
            js = json.loads(i)
            tweet = js[u'text']
            words = map(strlower, tweet.split()) 
            rwords = [x for x in words if not x.replace('.','').isdigit()]
            totalcount += len(rwords)
            for wd in rwords:
                if wd in frequency:
                    frequency[wd] += 1
                else:
                    frequency[wd] = 1 
        except KeyError:
            pass
    for key, val in frequency.items():
        print key, float(val) / float(totalcount) 
if __name__ == '__main__':
    main()

