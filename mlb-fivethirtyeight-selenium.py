import pandas as pd
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

MLB_STANDINGS_URL = 'http://mlb-standings.capplecloud.com/api'
MLB_PROJECTIONS = 'https://projects.fivethirtyeight.com/2019-mlb-predictions/'

NAME_CONVERSION_DICT = {
    'Diamondbacks': 'D-backs',
    'Dbacks': 'D-backs'
}

teams_req = requests.get(MLB_STANDINGS_URL + '/standings').json()
teams = teams_req['data']
team_dict = {}

for team in teams:
    current_team_name = team['team']['name']
    team_dict[current_team_name] = team

driver = webdriver.Chrome()

driver.get(MLB_PROJECTIONS)
team_rows = driver.find_elements_by_xpath('//*[@id="teams-table"]/tbody/tr')
for index, team_row in enumerate(team_rows, start=1):
    team_name = driver.find_element_by_xpath('//*[@id="teams-table"]/tbody/tr[' + str(index) + ']/td[1]/div/div/a').text
    team_rating = driver.find_element_by_xpath('//*[@id="teams-table"]/tbody/tr[' + str(index) + ']/td[3]').get_attribute('data-val')
    team_rating = float(team_rating)

    current_team = team_dict.get(team_name)
    if current_team is None:
        new_name = NAME_CONVERSION_DICT.get(team_name)
        current_team = team_dict.get(new_name)
        if current_team is None:
            print(team_name)
            continue

    current_team['rating'] = team_rating
    update_url = MLB_STANDINGS_URL + '/record/' + current_team['_id']
    update_req = requests.put(update_url, json=current_team)
    

driver.close()