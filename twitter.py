#########################################
##### Name: Jing Cao                #####
##### Uniqname: jingcao             #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests
import secrets  # file that contains your OAuth credentials

HYDRO_FILE = "hydroxychloroquine.json"
COVID_19_RS = "relevant_account_timeline.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
               client_secret=client_secret,
               resource_owner_key=access_token,
               resource_owner_secret=access_token_secret)


def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache(file_name):
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(file_name, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, file_name):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(file_name, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    #TODO Implement function
    param_strings = []
    for k in params:
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + '_' + '_'.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    #TODO Implement function
    request = requests.get(baseurl, params=params, auth=oauth)
    result = request.json()
    # print(result)
    return result


def make_request_with_cache_hashtag(baseurl, hashtag, count, file_name, lang='en'):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        A string of value for params
    count:
        The number of tweets to return per page, up to a maximum of 100.
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function
    params = {'q': hashtag, 'count': count, 'lang': lang}
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        return CACHE_DICT[request_key]
    else:
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT, file_name)
        return CACHE_DICT[request_key]


def make_request_with_cache_user_timeline(timeline_url, screen_name, count, file_name, max_id=None):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        A string of value for params
    count:
        The number of tweets to return per page, up to a maximum of 100.
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function
    params = {'screen_name': screen_name, 'count': count, 'max_id': max_id}
    request_key = construct_unique_key(timeline_url, params)
    if request_key in CACHE_DICT.keys():
        return CACHE_DICT[request_key]
    else:
        CACHE_DICT[request_key] = make_request(timeline_url, params)
        save_cache(CACHE_DICT, file_name)
        return CACHE_DICT[request_key]


if __name__ == "__main__":
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()


    # baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    # hashtag = "#hydroxychloroquine"
    # count = 100
    # file_name = HYDRO_FILE

    timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    screen_names = ['covid_19_RS', 'ResearchGate',
                    'CarolineYLChen', 'nature', 'XihongLin', 'barabasi', 'uTobian', 'JamesTodaroMD', 'trvrb', 'EBRheum', '_MiguelHernan', 'ProfMattFox', 'LudoWaltman', 'MKittlesonMD', 'Jeffsparks', 'oilcanoyler', 'trishgreenhalgh', 'peripatetical', 'DrDenaGrayson', 'DrTedros', 'WHO', 'CDCgov', 'NIH', 'OIGatHHS', 'WFSJ', 'rheum_covid', 'The Lancet']
    count = 200
    file_name = COVID_19_RS
    # max_id = 1245258800749256705

    CACHE_DICT = open_cache(file_name)

    # tweet_data = make_request_with_cache_hashtag(baseurl, hashtag, count, file_name)
    for screen_name in screen_names:
        tweet_data = make_request_with_cache_user_timeline(timeline_url, screen_name, count, file_name)
    
    # print(len(tweet_data))
