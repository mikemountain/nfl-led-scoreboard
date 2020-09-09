import requests
from datetime import datetime
from utils import convert_time
import debug

API_URL = "https://api.sleeper.app/v1/league/"
# DEBUG_URL = "http://192.168.0.183:3000/matchups"

def get_matchup(team_roster_id, league_id, week, teams):
    """
        get all matchups this week and find the matchup you care about
    """
    url = '{0}{1}/matchups/{2}'.format(API_URL, league_id, week)
    # url = DEBUG_URL
    matchup_id = 0
    matchup_info = {}
    try:
        matchups = requests.get(url)
        matchups = matchups.json()
        for matchup in matchups:
            if matchup['roster_id'] == team_roster_id:
                    matchup_id = matchup['matchup_id']
                    matchup_info['matchup_id'] = matchup['matchup_id']
                    matchup_info['user_roster_id'] = team_roster_id
                    matchup_info['user_score'] = matchup['points']
                    matchup_info['user_av'] = next((item for item in teams if item['roster_id'] == team_roster_id))['avatar']
                    matchup_info['user_name'] = next((item for item in teams if item['roster_id'] == team_roster_id))['name']
            for matchup in matchups:
                if matchup['matchup_id'] == matchup_id and matchup['roster_id'] != team_roster_id:
                    matchup_info['opp_roster_id'] = matchup['roster_id']
                    matchup_info['opp_score'] = matchup['points']
                    matchup_info['opp_av'] = next((item for item in teams if item['roster_id'] == matchup['roster_id']))['avatar']
                    matchup_info['opp_name'] = next((item for item in teams if item['roster_id'] == matchup['roster_id']))['name']
        return matchup_info
    except requests.exceptions.RequestException as e:
        print("Error encountered, Can't reach Sleeper API", e)
        return matchup_info
    except IndexError:
        print("uh oh")
        return matchup_info
    except Exception as e:
        print("something bad?", e) 

def get_teams(league_id):
    users_url = '{0}{1}/users'.format(API_URL, league_id)
    rosters_url = '{0}{1}/rosters'.format(API_URL, league_id)
    user_info = []
    try:
        users = requests.get(users_url)
        users = users.json()
        for user in users:
            name = user['display_name']
            avatar = user['avatar']
            user_id = user['user_id']
            user_dict = {"name": name, "id": user_id, "avatar": avatar}
            user_info.append(user_dict)
        rosters = requests.get(rosters_url)
        rosters = rosters.json()
        for roster in rosters:
            for user in user_info:
                if user['id'] == roster['owner_id']:
                    user['roster_id'] = roster['roster_id']
                    break
        return user_info
    except requests.exceptions.RequestException:
        print("Error encountered, Can't reach Sleeper API")
        return 0
    except IndexError:
        print("something somehow ended up out of index")
        return 0

def get_roster_id(teams, user_id):
    user = next((item for item in teams if item['id'] == user_id))
    return user['roster_id']

def get_avatars(teams):
    for team in teams:
        avatar = team['avatar']
        av_url = 'https://sleepercdn.com/avatars/thumbs/{0}'.format(avatar)
        r = requests.get(av_url, stream=True)
        filename = '../logos/{0}.png'.format(avatar)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
