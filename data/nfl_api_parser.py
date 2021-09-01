import requests
import datetime
import time as t
from utils import convert_time

URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# def get_game(team_name):
#     for i in range(5):
#         try:
#             res = requests.get(URL)
#             res = res.json()
#             for g in res['events']:
#                 if team_name in g['shortName']:
#                     info = g['competitions'][0]
#                     game = {'name': g['shortName'], 'date': g['date'],
#                             'hometeam': info['competitors'][0]['team']['abbreviation'], 'homeid': info['competitors'][0]['id'], 'homescore': int(info['competitors'][0]['score']),
#                             'awayteam': info['competitors'][1]['team']['abbreviation'], 'awayid': info['competitors'][1]['id'], 'awayscore': int(info['competitors'][1]['score']),
#                             'down': info.get('situation', {}).get('shortDownDistanceText'), 'spot': info.get('situation', {}).get('possessionText'),
#                             'time': info['status']['displayClock'], 'quarter': info['status']['period'], 'over': info['status']['type']['completed'],
#                             'redzone': info.get('situation', {}).get('isRedZone'), 'possession': info.get('situation', {}).get('possession'), 'state': info['status']['type']['state']}
#                     return game
#         except requests.exceptions.RequestException as e:
#             print("Error encountered getting game info, can't hit ESPN api, retrying")
#             if i < 4:
#                 t.sleep(1)
#                 continue
#             else:
#                 print("Can't hit ESPN api after multiple retries, dying ", e)
#         except Exception as e:
#             print("something bad?", e)

def get_all_games():
    # for i in range(5):
    try:
        res = requests.get(URL)
        res = res.json()
        games = []
        # i = 0
        for g in res['events']:
            info = g['competitions'][0]
            game = {'name': g['shortName'], 'date': g['date'],
                    'hometeam': info['competitors'][0]['team']['abbreviation'], 'homeid': info['competitors'][0]['id'], 'homescore': int(info['competitors'][0]['score']),
                    'awayteam': info['competitors'][1]['team']['abbreviation'], 'awayid': info['competitors'][1]['id'], 'awayscore': int(info['competitors'][1]['score']),
                    'down': info.get('situation', {}).get('shortDownDistanceText'), 'spot': info.get('situation', {}).get('possessionText'),
                    'time': info['status']['displayClock'], 'quarter': info['status']['period'], 'over': info['status']['type']['completed'],
                    'redzone': info.get('situation', {}).get('isRedZone'), 'possession': info.get('situation', {}).get('possession'), 'state': info['status']['type']['state']}
            games.append(game)
            # i += 1
        return games
    except requests.exceptions.RequestException as e:
        print("Error encountered getting game info, can't hit ESPN api, retrying")
        # if i < 4:
        #     t.sleep(1)
        #     continue
        # else:
        #     print("Can't hit ESPN api after multiple retries, dying ", e)
    except Exception as e:
        print("something bad?", e)

# def which_game(games, fav_team):
#     # check for fav team first
#     for game in games:
#         if games[game]['hometeam'] == fav_team or games[game]['awayteam'] == fav_team:
#             return games[game]
#     # games should be sorted by date, earliest to latest
#     for game in games:
#         # testing purposes
#         # if games[game]['state'] == 'post':
#         #     return games[game]
#         if games[game]['state'] == 'in':
#             return games[game]
#         if games[game]['state'] == 'pre':
#             return games[game]
#         if games[game]['state'] == 'post':
#             return games[game]
#     return None

# def is_playoffs():
#     try:
#         res = requests.get(URL)
#         res = res.json()
#         return res['season']['type'] == 3
#     except requests.exceptions.RequestException:
#         print("Error encountered getting game info, can't hit ESPN api")
#     except Exception as e:
#         print("something bad?", e)