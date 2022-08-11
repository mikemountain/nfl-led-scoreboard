import requests

URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=1 for week info (but it might return that week's info anyway)
# http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401437964 for gameID? worth it?

SEASON_TYPES = {
    1: 'pre_season',
    2: 'regular_season',
    3: 'post_season',
    4: 'off_season',
}


class API:
    # def __init__(self):
    #     self.game_ids = self.get_game_ids()

    def get_game_ids(self):
        try:
            res = requests.get(URL)
            res = res.json()
            ids = {}
            for g in res['events']:
                # clarity for now
                game_id = g['competitions'][0]['id']
                home = g['competitions'][0]['competitors'][0]['team']['abbreviation']
                away = g['competitions'][0]['competitors'][1]['team']['abbreviation']
                ids[home] = game_id
                ids[away] = game_id
            return ids
        except requests.exceptions.RequestException as e:
            print("Error encountered getting game info, can't hit ESPN api, retrying")
            return {}
        except Exception as e:
            print(e)
            return {}

    def get_game(game_id):
        try:
            res = requests.get(URL)
            res = res.json()
            for g in res['events']:
                info = g['competitions'][0]
                if info['id'] == game_id:
                    game = {'name': g['shortName'],
                            'date': g['date'],
                            'home_abbr': info['competitors'][0]['team']['abbreviation'],
                            'home_id': info['competitors'][0]['id'],
                            'home_score': int(info['competitors'][0]['score']),
                            'away_abbr': info['competitors'][1]['team']['abbreviation'],
                            'away_id': info['competitors'][1]['id'],
                            'away_score': int(info['competitors'][1]['score']),
                            'down': info.get('situation', {}).get('shortDownDistanceText'),
                            'spot': info.get('situation', {}).get('possessionText'),
                            # 'over': info['status']['type']['completed'],
                            'time': info['status']['displayClock'],
                            'quarter': info['status']['period'],
                            'redzone': info.get('situation', {}).get('isRedZone'),
                            'possession': info.get('situation', {}).get('possession'),
                            'state': info['status']['type']['state'],
                            }
                    return game
        except requests.exceptions.RequestException as e:
            return "Error encountered getting game info, can't hit ESPN api, retrying"
        except Exception as e:
            return e

    def get_week(self):
        try:
            res = requests.get(URL)
            res = res.json()
            return res['week']['number']
        except requests.exceptions.RequestException as e:
            print("Error encountered getting game info, can't hit ESPN api, retrying")
            return {}
        except Exception as e:
            print(e)
            return {}

    def get_season_type(self):
        try:
            res = requests.get(URL)
            res = res.json()
            return SEASON_TYPES[res['season']['type']]
        except requests.exceptions.RequestException as e:
            print("Error encountered getting game info, can't hit ESPN api, retrying")
            return {}
        except Exception as e:
            print(e)
            return {}
