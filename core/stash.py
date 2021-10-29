from os import path
from core.logger import *
from datetime import datetime
from sqlite3 import Error, connect

class Stash :

    def __init__(self, db_name):
        self.db_file = db_name

    def create_connection( self ):
        conn = None
        try:
            conn = connect( self.db_file )
            conn.row_factory = lambda cursor, row: row[0]
            return conn
        except Error as e:
            error(e)

        return conn

    def sql_stash( self, sql_query , sql_values=None ):
        conn = self.create_connection()

        try:
            c = conn.cursor()
            if sql_values != None:
            	c.execute(sql_query , sql_values)
            else:
            	c.execute(sql_query)
        except Error as e:
            error(e)

        conn.commit()
        conn.close()

    def db_init(self):
        self.sql_stash( """ PRAGMA foreign_keys = ON; """ )

        ## AGENTS
        self.sql_stash(""" CREATE TABLE IF NOT EXISTS agents (
        agent_name TEXT PRIMARY KEY, \
        listener_name TEXT, \
        remote_ip TEXT, \
        hostname TEXT, \
        beacon_type TEXT, \
        enc_key TEXT); """)

        self.sql_stash(""" CREATE TABLE IF NOT EXISTS commands (
        agent_name TEXT, \
        enc_command TEXT); """)

        self.sql_stash(""" CREATE TABLE IF NOT EXISTS commands_history (
        agent_name TEXT, \
        clear_command TEXT, \
        clear_out TEXT); """)

    def get_task( self, agent):
        conn = self.create_connection()
        try:
            c = conn.cursor()
            c.execute( 'SELECT enc_command FROM commands WHERE agent_name = ?' , ( agent, ) )
            result = c.fetchall()
        except Error as e:
            error(e)
            result = []

        conn.close()
        return result

    def del_commands(self, agent):
        conn = self.create_connection()
        try:
            c = conn.cursor()
            c.execute( 'DELETE FROM commands WHERE agent_name = ?' , ( agent, ) )
            conn.commit()
        except Error as e:
            error(e)

        conn.close()