
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class EventType(Base):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self) -> str:
        return f'<Event Type: {self.id} - {self.name}>'


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    established = Column(Integer)
    designed_by = Column(String(255))
    location = Column(String(255))
    coordinates = Column(String(255))

    def __repr__(self) -> str:
        return f'<Course: {self.id} - {self.name}>'


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    nickname = Column(String(255))
    born = Column(Date)
    died = Column(Date)
    nationality = Column(String(255))

    def __repr__(self) -> str:
        return f'<Player: {self.id} - {self.last_name}, {self.first_name}>'


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    event_type_id = Column(Integer, ForeignKey('event_types.id'))
    event_type = relationship('EventType', back_populates='tournaments')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='tournaments')
    number_of_players = Column(Integer)
    date_round_1 = Column(Date)
    date_round_2 = Column(Date)
    date_round_3 = Column(Date)
    date_round_4 = Column(Date)

    def __repr__(self) -> str:
        return f'<Tournament: {self.id}>'
    

class TournamentPlayerResult(Base):
    __tablename__ = 'tournament_player_results'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    tournament = relationship('Tournament', back_populates='tournament_player_results')
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player', back_populates='tournament_player_results')
    finish = Column(Integer)
    score_round_1 = Column(Integer)
    score_round_2 = Column(Integer)
    score_round_3 = Column(Integer)
    score_round_4 = Column(Integer)
    score_total = Column(Integer)
    amature = Column(Boolean)
    champion = Column(Boolean)
    winnings = Column(Integer)

    def __repr__(self) -> str:
        return f'<Tournament Player Result: {self.tournament_id} - {self.player_id} - {self.id}>'


EventType.tournaments = relationship('Tournament', order_by = Tournament.id, back_populates = 'event_type')
Course.tournaments = relationship('Tournament', order_by = Tournament.id, back_populates = 'course')
Tournament.tournament_player_results = relationship('TournamentPlayerResult', order_by = TournamentPlayerResult.id, back_populates = 'tournament')
Player.tournament_player_results = relationship('TournamentPlayerResult', order_by = TournamentPlayerResult.id, back_populates = 'player')
