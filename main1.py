"""A gaming system contains the following fields
game_id, player_id, played_date, points

1. Generate random synthetic data for the above fields with following constraints:
Number of games: 5
Number of players in each game: 75 to 125 (Note: same player can be repeated multiple times on different dates but on the same date. Meaning, same player shouldn't play on the same date but can play on different dates)
played_date: All games should have played in the month of August 2021 but not on Tuesdays
points: The point for each player should be in the range of 75 to 200 only

2. Once the above random synthetic data is created then store the results in a CSV file
3. Read the above CSV file and perform the following aggregations:
Find out the top 5 players by points in each of the games and display the results (game_id, player_id, total_points)
Find out the bottom 5 players by points in each of the games and display the results (game_id, player_id, total_points)
Find out the top 5 players in each game whose total points in a game is greater than the average of all players points of that game (hint: if average points of all players in game 1 is 90 then find out all the top 5 players whose points are greater than 90)
Find out top 5 players in each game by their total points for each week (hint: list 5 players in game 1 with top scores between Aug 1st - Augt 7th)
Find out top 5 players in each game by their total points bi-weekly - every 2 weeks (hint: list 5 players in game 1 with top scores between Aug 1st - Augt 14th)

4. Create a proper project structure for the above problem statement, indent the code properly, add comments to the code, perform all git operations on the code (git clone, add, commit, fetch, pull, etc). Each of the above requirements should be an individual commit to the github
"""
import pandas as pd
from calendar import monthrange
from datetime import datetime
from random import randint

test_game_map = []
game_id_list = [1, 2, 3, 4, 5]
random_game_player_map = dict()
year = 2021
month = 8
start_day, num_days = monthrange(year, month)   #returns start day and 31 days in aug

# create list of dates considered
def get_date_list(skip_day=1):
    datelist = []
    for day in range(1, num_days + 1):      #1 to 31
        date = datetime(year, month, day)
        # Skip Tuesday
        if date.weekday() != skip_day:
            datelist.append(f'{year}-{month}-{day}')
    return datelist

#date and game id for each player
def get_game_date_map():
    df_list = []
    # 0 - Monday .... 6 - Sunday
    datelist = get_date_list(skip_day=1)
    for game_id in game_id_list:
        for _date in datelist:
            num_players = randint(75, 125)
            for j in range(num_players):
                df_list.append({
                    "game_id": game_id,
                    "played_date": _date
                })
    return df_list


if __name__ == '__main__':
    test_game_map = get_game_date_map()
    sorted_test_game_map = sorted(test_game_map, key=lambda x: int(x["played_date"].split("-")[-1]))
    #print(sorted_test_game_map)
    date_player_map = {}
    player_id_list = []
    for test_map in sorted_test_game_map:
        if test_map["played_date"] not in date_player_map:
            player_id_list = list(range(1, len(sorted_test_game_map)))
            date_player_map[test_map["played_date"]] = []

        #check if same player again on same date
        player_id = player_id_list.pop(0)
        while player_id in date_player_map[test_map["played_date"]]:
            player_id_list.append(player_id)
            player_id = player_id_list.pop(0)
        date_player_map[test_map["played_date"]].append(player_id)
        test_map.update(
            {
                "player_id": player_id,
                "points": randint(75, 200)
            }
        )
#print(sorted_test_game_map)
df = pd.DataFrame(test_game_map)
df.to_csv("data.csv")
