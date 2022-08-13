
import requests
from bs4 import BeautifulSoup

from database import connection as db_connection
from database.schema import EventType as DB_EventType
from database.schema import Tournament as DB_Tournament

from data_sources import the_open


def pull_data(data_source):
    page = requests.get(data_source['url'])

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='leaderboard')
    leaderboard_rows = results.find_all('div', 'final-leaderboard__row')
    
    # The Open Leaderboard slots are as following:
    # Player Name | Place | Rd1 | Rd2 | Rd3 | Rd4 | Total
    print('')
    print(f'**** The Open - {data_source["year"]} ****')
    for row in leaderboard_rows:
        player_info = row.find_all('div', 'final-leaderboard__content')
        
        player_name_slot = player_info[0].find('a', class_='final-leaderboard__content-name')
        if not player_name_slot:
            player_name_slot = player_info[0].find('div', class_='final-leaderboard__content-name')
        
        if not player_name_slot:
            continue

        player_name = player_name_slot.text.strip()
        place = player_info[1].text.strip()
        rd_1 = player_info[2].text.strip()
        rd_2 = player_info[3].text.strip()
        rd_3 = player_info[4].text.strip()
        rd_4 = player_info[5].text.strip()
        total = player_info[6].text.strip()

        print(f'Player Name: {player_name}')
        print(f'Place: {place}')
        print(f'Rd1: {rd_1}')
        print(f'Rd2: {rd_2}')
        print(f'Rd3: {rd_3}')
        print(f'Rd4: {rd_4}')
        print(f'Total: {total}')
        print('**********************')
        
    print('')


def pull_the_open_data():
    # # URL = 'https://www.theopen.com/previous-opens/1st-open-prestwick-1860/'
    # # URL = 'https://www.theopen.com/previous-opens/2nd-open-prestwick-1861/'
    # URL = 'https://www.theopen.com/previous-opens/138th-open-turnberry-2009/'
    
    for data_source in the_open.THE_OPEN_DATA:
        pull_data(data_source)
    
# def save_to_rds(tournament_id):
#     session = db_connection.get_db_session()

#     try:
#         tournament = session.squery(DB_Tournament).filter(id == tournament_id).first()

#     except Exception as e:
#         session.rollback()
#         print(f'Failed to save to rds: {e}')

#     finally:
#         session.close()


def run_data_init():
    pull_the_open_data()


if __name__ == '__main__':
   pull_the_open_data()
