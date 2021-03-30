import lxml.html
import requests
from collections import Counter
import pickle


# returns dict of dates to lists of games on that date
def create_games(month):
    games = requests.get('https://www.basketball-reference.com/leagues/NBA_2021_games-{}.html'.format(month))
    tree = lxml.html.fromstring(games.text)
    # list of dates
    dates_list = []
    for date in tree.cssselect('th a'):
        dates_list.append(date.text_content())
    # list of times
    times_list = []
    for time in tree.cssselect('th+ .right'):
        times_list.append(time.text_content())
    # list of teams playing
    teams_list = []
    count = 0
    teams_string = ""
    for teams in tree.cssselect('td.left a'):
        if count == 0:
            teams_string += teams.text_content()
            count += 1
        else:
            teams_string += " @ " + teams.text_content()
            count += 1
        if count == 2:
            teams_list.append(teams_string)
            count = 0
            teams_string = ""
    # combine times and teams into one string
    times_and_teams_list = []
    for i in range(len(times_list)):
        times_and_teams_list.append(times_list[i] + ": " + teams_list[i])
    # get counts of games for each date
    date_counts = dict(Counter(dates_list).items())
    # for each date, create list of games and set as value for key in dict
    index = 0
    final_dict = {}
    for date, count in date_counts.items():
        game_list = []
        for i in range(count):
            game_list.append(times_and_teams_list[index])
            index += 1
        final_dict[date] = game_list
    print(final_dict)
    return final_dict


if __name__ == "__main__":
    dec_games = create_games("december")
    jan_games = create_games("january")
    feb_games = create_games("february")
    mar_games = create_games("march")
    apr_games = create_games("april")
    may_games = create_games("may")
    # merge all months schedules into one dict
    combined_schedule = dec_games
    combined_schedule.update(jan_games)
    combined_schedule.update(feb_games)
    combined_schedule.update(mar_games)
    combined_schedule.update(apr_games)
    combined_schedule.update(may_games)
    f = open("schedule.pkl", "wb")
    pickle.dump(combined_schedule, f)
    f.close()
