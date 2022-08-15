
import requests
from bs4 import BeautifulSoup

from database import connection as db_connection
from database.schema import Course as DB_Course
from database.schema import EventType as DB_EventType
from database.schema import Tournament as DB_Tournament

from data_sources import courses
from data_sources import the_open


def init_event_and_courses_data():
    session = db_connection.get_db_session()
    
    try:
        open_event_type_exists = session.query(DB_EventType).filter(name = 'The Open').first()
        if not open_event_type_exists:
            open_event_type = DB_EventType(
                name = 'The Open'
            )
            session.add(open_event_type)

        for course in courses.COURSES:
            db_course_exists = session.query(DB_Course).filter(name = course.name).first()
            if db_course_exists:
                continue

            db_course = DB_Course(
                name = course.name
            )
            session.add(db_course)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f'Failed to save to DB: {e}')

    finally:
        session.close()


def pull_open_data(open_event):
    
    page = requests.get(open_event['url'])

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='leaderboard')
    leaderboard_rows = results.find_all('div', 'final-leaderboard__row')
    
    # The Open Leaderboard slots are as following:
    # Player Name | Place | Rd1 | Rd2 | Rd3 | Rd4 | Total
    print('')
    print(f'**** The Open - {open_event["year"]} ****')
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
    init_event_and_courses_data()
    for event in the_open.THE_OPEN_DATA:
        pull_event_data(event)


def run_data_init():
    pull_the_open_data()


if __name__ == '__main__':
   pull_the_open_data()
