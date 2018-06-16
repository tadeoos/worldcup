import requests
import datetime
import dateutil.parser
import pytz
from tzlocal import get_localzone
from collections import defaultdict


def iso_to_datetime(s):
    d = dateutil.parser.parse(s)
    return d


def get_nice_date(match_date):
    return iso_to_datetime(match_date).astimezone(get_localzone()).strftime("%A, %d. %B %Y %I:%M%p")


class WorldCupData:

    def __init__(self):
        self.raw_data = self.get_worldcup_data()

    @staticmethod
    def get_worldcup_data():
        url = "https://raw.githubusercontent.com/lsv/fifa-worldcup-2018/master/data.json"
        response = requests.get(url)
        data = response.json()
        return data

    def get_key_info(self, key_, id_, attr=None):
        objects = self.raw_data[key_]
        try:
            object_dict = [obj for obj in objects if obj["id"] == id_][0]
        except IndexError:
            raise ValueError(f"There is no {key_} with id: {id_}")
        if attr:
            return object_dict[attr]
        else:
            return object_dict

    def get_team_info(self, id_, attr=None):
        return self.get_key_info("teams", id_, attr)

    def get_stadium_info(self, id_, attr=None):
        return self.get_key_info("stadiums", id_, attr)

    def all_matches(self):
        matches = []
        for key in ("groups", "knockout"):
            for stage in self.raw_data[key].keys():
                matches.extend(self.raw_data[key][stage]["matches"])
        return matches

    def get_group_matches(self, group):
        return self.raw_data["groups"][group]["matches"]

    def get_group_members(self, group):
        group_matches = self.get_group_matches(group)
        group_teams = {match["home_team"] for match in group_matches}
        assert len(group_teams) == 4
        return [self.get_team_info(team, "name") for team in group_teams]

    def calculate_group_table(self, group):
        scores = {team: defaultdict(int) for team in self.get_group_members(group)}
        matches = self.get_group_matches(group)
        for match in filter(lambda m: m['finished'] is True, matches):
            home_team = self.get_team_info(match["home_team"], "name")
            away_team = self.get_team_info(match["away_team"], "name")
            scores[home_team]['played'] += 1
            scores[away_team]['played'] += 1
            scores[home_team]['scored'] += match["home_result"]
            scores[home_team]['conceded'] += match["away_result"]
            scores[away_team]['scored'] += match["away_result"]
            scores[away_team]['conceded'] += match["home_result"]
            if match["home_result"] > match["away_result"]:
                scores[home_team]['points'] += 3
            elif match["home_result"] == match["away_result"]:
                scores[home_team]['points'] += 1
                scores[away_team]['points'] += 1
            else:
                scores[away_team]["points"] += 3
        return scores

    def get_nearest_match(self):
        systimezone = get_localzone()  # System non-DST timezone
        now = pytz.UTC.localize(datetime.datetime.now())
        nearest = None
        for match in self.all_matches():
            match_date = iso_to_datetime(match['date']).astimezone(systimezone)
            time_diff = abs(now - match_date)
            if not nearest:
                nearest = (match, time_diff)
            elif match_date > now and time_diff < nearest[1]:
                nearest = (match, time_diff)
        return nearest[0]

    def print_match(self, match):
        home_team = self.get_team_info(match["home_team"])
        away_team = self.get_team_info(match["away_team"])
        if match['finished']:
            return f"""Match #{match['name']}: {home_team['emojiString']}{home_team['name']} vs {away_team["name"]}{away_team["emojiString"]}
Result: {match['home_result']} : {match['away_result']}
Date: {get_nice_date(match["date"])}"""
        else:
            return f"""Match #{match['name']}: {home_team["name"]} vs {away_team["name"]}
When: {get_nice_date(match["date"])}
Where: {self.get_stadium_info(match["stadium"], "city")}"""

    def group_table(self, group, as_str=True, as_dict=False):
        table = self.calculate_group_table(group)
        if as_dict:
            return table
        assert as_str
        ret_str = ''
        ret_str += 'GROUP {0: <20} MP GF GA PTS\n'.format(group.upper())
        ret_str += '-' * 39
        for team, info in sorted(table.items(), key=lambda k: (k[1]['points'], k[1]['scored'] - k[1]['conceded']), reverse=1):
            ret_str += "\n{0: <26}  {1}  {2}  {3}  {4}".format(
                team, info['played'], info['scored'], info['conceded'], info['points'])
        return ret_str
