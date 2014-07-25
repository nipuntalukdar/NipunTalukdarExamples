import sys
import json
from operator import itemgetter
llstates = {
    (-152.2683, 61.3850): 'AK',
    (-86.8073, 32.7990): 'AL',
    (-92.3809, 34.9513): 'AR',
    (-170.7197, 14.2417): 'AS',
    (-111.3877, 33.7712): 'AZ',
    (-119.7462, 36.1700): 'CA',
    (-105.3272, 39.0646): 'CO',
    (-72.7622, 41.5834): 'CT',
    (-77.0262, 38.8964): 'DC',
    (-75.5148, 39.3498): 'DE',
    (-81.7170, 27.8333): 'FL',
    (-83.6487, 32.9866): 'GA',
    (-157.5311, 21.1098): 'HI',
    (-93.2140, 42.0046): 'IA',
    (-114.5103, 44.2394): 'ID',
    (-89.0022, 40.3363): 'IL',
    (-86.2604, 39.8647): 'IN',
    (-96.8005, 38.5111): 'KS',
    (-84.6514, 37.6690): 'KY',
    (-91.8749, 31.1801): 'LA',
    (-71.5314, 42.2373): 'MA',
    (-76.7902, 39.0724): 'MD',
    (-69.3977, 44.6074): 'ME',
    (-84.5603, 43.3504): 'MI',
    (-93.9196, 45.7326): 'MN',
    (-92.3020, 38.4623): 'MO',
    (145.5505, 14.8058): 'MP',
    (-89.6812, 32.7673): 'MS',
    (-110.3261, 46.9048): 'MT',
    (-79.8431, 35.6411): 'NC',
    (-99.7930, 47.5362): 'ND',
    (-98.2883, 41.1289): 'NE',
    (-71.5653, 43.4108): 'NH',
    (-74.5089, 40.3140): 'NJ',
    (-106.2371, 34.8375): 'NM',
    (-117.1219, 38.4199): 'NV',
    (-74.9384, 42.1497): 'NY',
    (-82.7755, 40.3736): 'OH',
    (-96.9247, 35.5376): 'OK',
    (-122.1269, 44.5672): 'OR',
    (-77.2640, 40.5773): 'PA',
    (-66.3350, 18.2766): 'PR',
    (-71.5101, 41.6772): 'RI',
    (-80.9066, 33.8191): 'SC',
    (-99.4632, 44.2853): 'SD',
    (-86.7489, 35.7449): 'TN',
    (-97.6475, 31.1060): 'TX',
    (-111.8535, 40.1135): 'UT',
    (-78.2057, 37.7680): 'VA',
    (-64.8199, 18.0001): 'VI',
    (-72.7093, 44.0407): 'VT',
    (-121.5708, 47.3917): 'WA',
    (-89.6385, 44.2563): 'WI',
    (-80.9696, 38.4680): 'WV',
    (-107.2085, 42.7475): 'WY'
}
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

statescord = {
    'AK': [-152.2683, 61.3850],
    'AL': [-86.8073, 32.7990],
    'AR': [-92.3809, 34.9513],
    'AS': [-170.7197, 14.2417],
    'AZ': [-111.3877, 33.7712],
    'CA': [-119.7462, 36.1700],
    'CO': [-105.3272, 39.0646],
    'CT': [-72.7622, 41.5834],
    'DC': [-77.0262, 38.8964],
    'DE': [-75.5148, 39.3498],
    'FL': [-81.7170, 27.8333],
    'GA': [-83.6487, 32.9866],
    'HI': [-157.5311, 21.1098],
    'IA': [-93.2140, 42.0046],
    'ID': [-114.5103, 44.2394],
    'IL': [-89.0022, 40.3363],
    'IN': [-86.2604, 39.8647],
    'KS': [-96.8005, 38.5111],
    'KY': [-84.6514, 37.6690],
    'LA': [-91.8749, 31.1801],
    'MA': [-71.5314, 42.2373],
    'MD': [-76.7902, 39.0724],
    'ME': [-69.3977, 44.6074],
    'MI': [-84.5603, 43.3504],
    'MN': [-93.9196, 45.7326],
    'MO': [-92.3020, 38.4623],
    'MP': [145.5505, 14.8058],
    'MS': [-89.6812, 32.7673],
    'MT': [-110.3261, 46.9048],
    'NC': [-79.8431, 35.6411],
    'ND': [-99.7930, 47.5362],
    'NE': [-98.2883, 41.1289],
    'NH': [-71.5653, 43.4108],
    'NJ': [-74.5089, 40.3140],
    'NM': [-106.2371, 34.8375],
    'NV': [-117.1219, 38.4199],
    'NY': [-74.9384, 42.1497],
    'OH': [-82.7755, 40.3736],
    'OK': [-96.9247, 35.5376],
    'OR': [-122.1269, 44.5672],
    'PA': [-77.2640, 40.5773],
    'PR': [-66.3350, 18.2766],
    'RI': [-71.5101, 41.6772],
    'SC': [-80.9066, 33.8191],
    'SD': [-99.4632, 44.2853],
    'TN': [-86.7489, 35.7449],
    'TX': [-97.6475, 31.1060],
    'UT': [-111.8535, 40.1135],
    'VA': [-78.2057, 37.7680],
    'VI': [-64.8199, 18.0001],
    'VT': [-72.7093, 44.0407],
    'WA': [-121.5708, 47.3917],
    'WI': [-89.6385, 44.2563],
    'WV': [-80.9696, 38.4680],
    'WY': [-107.2085, 42.7475]
}

sorted_us_state_cords = []

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
        return None,None
    if (tweet[u'lang'] is None ) or (tweet[u'lang'] != 'en') :
        return None,None
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
    return scorenew, tweet
            

def get_sorted_cords(cords):
    return sorted(cords, key=itemgetter(0,1))              

def get_sentiments(filep):
    sentiments = {}
    for line in filep:
        term, sentiment = line.split("\t")
        sentiments[term.lower()] = int(sentiment) 
    return sentiments

def get_score(text, sentiments):
    final_score = 0.0
    try:
        for word in  text.lower().split():
            if word in sentiments:
                final_score += sentiments[word]
    except KeyError:
        pass
    return final_score

def get_us_state_for_cord(cord):
    min_pos = (-10000.0, -10000.0)
    min_diff = 10000000.0
    for city_cord in sorted_us_state_cords:
        diff = abs(cord[0] - city_cord[0] + cord[1] - city_cord[1])
        if diff < min_diff:
            min_diff = diff
            min_pos = city_cord
    return llstates[min_pos]
        
    

def us_tweet(tweetjson):
    if tweetjson[u'place'] is not None:
        if tweetjson[u'place'][u'country_code'] is not None:
            if tweetjson[u'place'][u'country_code'] != 'US':
                return None 
            coordinates = tweetjson[u'place'][u'bounding_box'][u'coordinates'][0]
            thestate =  get_us_state_for_cord(coordinates)
            if thestate is not None:
                return thestate
                   
    if tweetjson[u'user'][u'location'] is not None:
        location = tweetjson[u'user'][u'location'].strip()
        for code, state in states.items():
            if location == code:
                return code
            if location.lower() == state.lower():
                return code
        for code, state in states.items():
            locparts = location.lower().split()
            if (state.lower() in locparts) or (code.lower() in locparts):
                return code 
    if tweetjson[u'geo'] is not None:
        thestate = get_us_state_for_cord(tweetjson[u'geo'][u'coordinates'])
        if thestate is not None:
            return thestate 
    if tweetjson[u'coordinates'] is not None:
        thestate = get_us_state_for_cord(tweetjson[u'coordinates'][u'coordinates'])
        if thestate is not None:
            return thestate 
    return None

def main():
    llkeys = llstates.keys()
    sorted_us_state_cords = get_sorted_cords(llkeys)
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentiments = get_sentiments(sent_file)
    sent_file.close()
    term_sents = {}
    alltweets = []
    for i in tweet_file: 
        newwordsents,tweetjson = compute_term_sentiment(i, term_sents, sentiments)
        if newwordsents is None or tweetjson is None:
            continue
        for wordsent in newwordsents:
            if wordsent in term_sents:
                term_sents[wordsent]['score'] += newwordsents[wordsent]['score']
                term_sents[wordsent]['count'] += newwordsents[wordsent]['count']
            else:
                term_sents[wordsent] = newwordsents[wordsent]
        alltweets.append(tweetjson)
    tweet_file.close()
    final_sents = {}
    for newwd in term_sents:
        final_sents[newwd] = float(term_sents[newwd]['score'] / term_sents[newwd]['count'])
    sentiments.update(final_sents)
    term_sents = None
    final_sents = None
    happy_states = {}
    for state in states:
        happy_states[state] = [0 , 0.0]
    for thetweet in alltweets:
        try:
            thestate = us_tweet(thetweet)
            if thestate is None:
                continue
            tweetsent = get_score(thetweet[u'text'], sentiments)
            happy_states[thestate][1] += tweetsent 
            happy_states[thestate][0] += 1
        except KeyError:
            pass
    happiest_score = -1000.0
    happiest_state = 'GA'
    for state in happy_states:
        if happy_states[state][0] > 0:
            this_state_score_avg = happy_states[state][1] / happy_states[state][0]
            if this_state_score_avg > happiest_score:
                happiest_score = this_state_score_avg
                happiest_state = state
    print happiest_state
         
if __name__ == '__main__':
    main()

