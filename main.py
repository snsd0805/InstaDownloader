import requests
import os
import time
import json
from tqdm import tqdm
import sys

header = {
        # 'x-ig-app-id': 'You should find IG App ID on the browser',
        'x-ig-app-id': '936619743392459',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

def getLinks(username: str):
    print("Get images' links...'")

    # find this user's total media counts
    # progress bar
    response = requests.get("https://www.instagram.com/api/v1/users/web_profile_info/?username="+username, headers=header)
    progress = tqdm(total=json.loads(response.text)['data']['user']['edge_owner_to_timeline_media']['count'])               # media counts

    url = "https://www.instagram.com/api/v1/feed/user/{}/username/?count=15".format(username)
    links = []

    # get pictures' links
    load_count = 0
    flag = True
    while flag:
        # We should use "next_max_id" to requests the next group of medias
        # But we will not have "next_max_id" in the first requst
        if load_count == 0:
            response = requests.get(url, headers=header)
            url += "&max_id={}"
        else:
            response = requests.get(url.format(data['next_max_id']), headers=header)

        # get links from responded JSON
        data = json.loads(response.text)
        for item in data['items']:
            if 'carousel_media' in item:
                code = item['code']
                
                # if the picture exist, break this loop and return links that have images haven't been downloaded
                if os.path.isfile("images/{}/{}_0".format(username, code)):
                    flag = False
                    break
                for index, image in enumerate(item['carousel_media']):
                    link = image['image_versions2']['candidates'][0]['url']
                    links.append((link, "{}_{}".format(code, index)))
            else:
                link = item['image_versions2']['candidates'][0]['url']
                code = item['code']
                if os.path.isfile("images/{}/{}".format(username, code)):
                    flag = False
                    break
                links.append((link, code))

        # update progress bar
        progress.update(data['num_results'])

        # check whether need to break
        if data['more_available'] == False:
            break

        load_count += 1
        time.sleep(0.2)

    if not flag:
        print("Only need to get {} images".format(len(links)))

    return links

def checkDir(username: str):
    if not os.path.isdir('images'):
        os.mkdir('images')
    if not os.path.isdir('images/'+username):
        os.mkdir('images/'+username)

def downloadImages(username, links: list):
    print("download images...")
    progress = tqdm(total=len(links))
    for link in links:
        response = requests.get(link[0])
        with open('images/{}/{}'.format(username, link[1]), 'wb') as fp:
            fp.write(response.content)
        progress.update(1)
        time.sleep(0.5)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [username]")
    else:
        username = sys.argv[1]
        checkDir(username)
        downloadImages( username, getLinks(username) )
