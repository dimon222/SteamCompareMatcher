from requests import get
import io
from difflib import SequenceMatcher
import ujson
import os
import re

input_file = 'input.log'
result_file = 'result.log'
account_name = "*****"
token = "*****"
steamid = "*****"

#url = "http://steamcommunity.com/id/{0}/games/?tab=all&xml=1".format(account_name)
url = None
mode = 2 # appid is mode 1, name is mode 2

if mode == 2:
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json&include_appinfo=1".format(token, steamid)
    response = get(url)
    tree = ujson.loads(response.text)
    list_of_games = [re.sub('/( *\[[^)]*\] *)|( *\([^)]*\) *)|\=.*|\:|\-|\–|\\|\/|\™|\®| |\'|\.|\?|\!/g', '', single_item['name'].lower()) for single_item in tree['response']['games']]
elif mode == 1:
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json".format(token, steamid)
    response = get(url)
    tree = ujson.loads(response.text)
    list_of_games = [single_item['appid'] for single_item in tree['response']['games']]

del tree
del response

result = io.open(result_file, 'w', encoding='utf8')
to_process = io.open(input_file, 'r', encoding='utf8')

for line in to_process:
    line = line.strip()
    if mode == 2:
        filtered_name = re.sub('/( *\[[^)]*\] *)|( *\([^)]*\) *)|\=.*|\:|\-|\–|\\|\/|\™|\®| |\'|\.|\?|\!/g', '', line.lower())
        if filtered_name not in list_of_games:
            found_match = False
            for game in list_of_games:
                if SequenceMatcher(None, filtered_name, game).ratio() > 0.8:
                    found_match = True
                    break

            if found_match is False:
                result.write(line + "\n")
                #result.flush()
                #os.fsync(result.fileno())
    elif mode == 1:
        if int(line) not in list_of_games:
            result.write(line + "\n")
            #result.flush()
            #os.fsync(result.fileno())


result.close()
to_process.close()

