from functools import partial
from flask import Flask
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import pdb
import pprint
import itertools
from collections import defaultdict
import jsonpickle

server = Flask(__name__)

@server.route("/")
def hello():
    oauth2 = OAuth2(None, None, from_file="credentials.json")
    #    if not oauth.token_is_valid():
#        oauth.refresh_access_token()
    pp = pprint.PrettyPrinter(indent=2)
    gm = yfa.Game(oauth2, 'nhl')
    league = gm.to_league('403.l.21811')
    all_matchups = league.matchups()['fantasy_content']['league']
    matchups = league.matchups()['fantasy_content']['league'].pop()['scoreboard']['0']['matchups']
    count = int(league.matchups()['fantasy_content']['league'].pop()['scoreboard']['0']['matchups']['count'])
    stats = []
    for x in range(count):
        team_0 = matchups[str(x)]['matchup']['0']['teams']['0']['team']
        team_1 = matchups[str(x)]['matchup']['0']['teams']['1']['team']
        team_key_0 = team_0[0][0]['team_key']
        team_key_1 = team_1[0][0]['team_key']
        team_stats_0 = team_0[1]['team_stats']['stats']
        team_stats_1 = team_1[1]['team_stats']['stats']
        to_stats_0 = partial(to_stats, team_key_0)
        to_stats_1 = partial(to_stats, team_key_1)
        stats += list(map(to_stats_0, team_stats_0))
        stats += list(map(to_stats_1, team_stats_1))
    groups = defaultdict(list)
    for stat in stats:
        groups[stat.stat].append(stat)
    for key in groups:
        groups[key].sort(key=lambda stat: stat.value * stat.sortDirection())
    return str(jsonpickle.encode(RotisserieWeek(groups)))

def to_stats(team_key, stats_dict):
    return Stat(team_key, stats_dict['stat']['stat_id'], stats_dict['stat']['value'])

class Stat():
    def __init__(self, team_id, stat, value):
        self.team_id = team_id
        self._stat = stat
        self.value = value

    @property
    def stat(self):
        try:
            return int(self._stat)
        except:
            return float(self._stat)

    def sortDirection(self):
        if(self.stat == '23'):
            return -1
        else:
            return 1

class RotisserieWeek():
    def __init__(self, ordered_stats):
        self.ordered_stats = ordered_stats

    def create_points_map(self, stat):
        stat_list = ordered_stats[stat]
        max_points = len(stat_list)
        current_value = None

