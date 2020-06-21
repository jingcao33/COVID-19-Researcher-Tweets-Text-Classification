import csv
import json

timeline_list = []
hydro_list = []
timeline_json = 'relevant_account_timeline.json'
hydro_json = 'hydroxychloroquine.json'
with open(timeline_json, 'r') as cache_file:
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    for key in cache_dict.keys():
        timeline_list += cache_dict[key]


with open(hydro_json, 'r') as cache_file:
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    for key in cache_dict.keys():
        hydro_list += cache_dict[key]['statuses']
    

timeline_csv = 'relevant_account_timeline.csv'
hydro_csv = 'hydroxychloroquine.csv'

with open(timeline_csv, 'w', newline='') as csvfile:
    fieldnames = ['id', 'url', 'user_name', 'screen_name', 'text', 'label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    # print(cache_list[1])
    for post in timeline_list:
        if type(post) is str:
            print(post)
            pass
        else:
            post_id = post['id_str']
            try:
                url = post['entities']['urls'][0]['url']
            except:
                url = ''
            user_name = post['user']['name']
            screen_name = post['user']['screen_name']
            text = post['text']
            label = None
            writer.writerow({'id': post_id, 'url': url, 'user_name': user_name,
                            'screen_name': screen_name, 'text': text, 'label': label})
        

with open(hydro_csv, 'w', newline='') as csvfile:
    fieldnames = ['id', 'url', 'user_name', 'screen_name', 'text', 'label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    # print(cache_list[1])
    for post in hydro_list:
        if type(post) is str:
            print(post)
            pass
        else:
            post_id = post['id_str']
            try:
                url = post['entities']['urls'][0]['url']
            except:
                url = ''
            user_name = post['user']['name']
            screen_name = post['user']['screen_name']
            text = post['text']
            label = None
            writer.writerow({'id': post_id, 'url': url, 'user_name': user_name,
                            'screen_name': screen_name, 'text': text, 'label': label})
        
