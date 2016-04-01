#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT count(*) as num from players;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    results = c.fetchone()
    conn.close()
    num_players = results[0]
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES (%s);"
    params = (name, )
    conn = connect()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = ("SELECT * FROM standings;")
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()
    standings = results
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO matches (player1, player2, winner) VALUES (%s, %s, %s);"
    params = (winner, loser, winner)
    conn = connect()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    current_standings = playerStandings()
    pairs = []
    num_players = len(current_standings)
    c = 0
    while (c < num_players):
        player1_id = current_standings[c][0]
        player1_name = current_standings[c][1]
        player2_id = current_standings[c+1][0]
        player2_name = current_standings[c+1][1]
        pairs.append((player1_id, player1_name, player2_id, player2_name))
        c += 2
    return pairs


def roundsRequired():
    total_players = countPlayers()
    return int(math.ceil(math.log(total_players, 2)))
