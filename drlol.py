#!/usr/bin/python3

import configparser
from datetime import timedelta
import requests
import requests_cache
import json
from collections import OrderedDict

config = configparser.ConfigParser()
config.read("drlol.conf")
username = config['drlol']['username']
password = config['drlol']['password']
cache_time = timedelta(seconds=int(config['drlol']['cache_time']))

requests_cache.install_cache('drlol', backend='sqlite', allowable_methods=('GET', 'POST'), expire_after=cache_time)

login_url = 'https://F67D.playfabapi.com/Client/LoginWithPlayFab'
login_headers = {
  'Host': 'F67D.playfabapi.com',
  'User-Agent': 'UnityPlayer/5.4.0f3 (http://unity3d.com)',
  'Accept': '*/*',
  'Accept-Encoding': 'identity',
  'Content-Type': 'application/json',
  'X-PlayFabSDK': 'UnitySDK-2.5.160815',
  'X-ReportErrorAsSuccess': 'true',
  'X-Unity-Version': '5.4.0f3'
}
# if we don't order these, caching doesn't work as python dicts have aribtrary order
login_headers = OrderedDict(sorted(login_headers.items()))
login_payload = {
  'TitleId': 'F67D',
  'Username': username,
  'Password': password,
  'InfoRequestParameters': 'null'
}
login_payload = OrderedDict(sorted(login_payload.items()))

r = requests.post(login_url, headers=login_headers, data=json.dumps(login_payload))
r = r.json()
session_ticket = r['data']['SessionTicket']

leaderboard_url = 'https://F67D.playfabapi.com/Client/GetLeaderBoard'
leaderboard_headers = {
  'Host': 'F67D.playfabapi.com',
  'Content-Type': 'application/json',
  'X-Authorization': session_ticket,
  'X-PlayFabSDK': 'UnitySDK-2.5.160815',
  'X-ReportErrorAsSuccess': 'true',
  'X-Unity-Version': '5.4.0f3'
}
leaderboard_headers = OrderedDict(sorted(leaderboard_headers.items()))
# anything over 99 gives back an error ¯\_(ツ)_/¯
leaderboard_payload = {
  'StatisticName': 'SP.RC.miami-lights.race.TotalTime',
  'StartPosition': 0,
  'MaxResultsCount': 99
}
leaderboard_payload = OrderedDict(sorted(leaderboard_payload.items()))

r = requests.post(leaderboard_url, headers=leaderboard_headers, data=json.dumps(leaderboard_payload))
cached = r.from_cache
r = r.json()

print("Content-Type: application/json")
print()

print(r)

