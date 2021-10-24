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
            return conn
        except Error as e:
            error(e)

        return conn

    def sql_stash( self, sql_query , sql_values=None ):
        conn = self.create_connection()

        try:
            c = conn.cursor()
            c.execute( sql_query , sql_values )
        except Error as e:
            error(e)

        conn.commit()
        conn.close()

    def db_init(self):
        # create_sql = []
        # create_sql.append( """ PRAGMA foreign_keys = ON; """ )
        self.sql_stash( """ PRAGMA foreign_keys = ON; """ )

        ## AGENTS
        self.sql_stash(""" CREATE TABLE IF NOT EXISTS agents (
        agent_name TEXT PRIMARY KEY, \
        listener_name TEXT, \
        remote_ip TEXT, \
        hostname TEXT, \
        beacon_type TEXT, \
        enc_key TEXT); """)

        # # TESTING
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS testing (
        # target TEXT, \
        # linkedin_link TEXT); """ )

        # ## EMPLOYEES
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS employees ( \
        # comp_link TEXT, \
        # name TEXT, \
        # position TEXT, \
        # prof_link TEXT PRIMARY KEY, \
        # prof_pic TEXT, \
        # email TEXT, \
        # FOREIGN KEY ( comp_link ) REFERENCES testing ( linkedin_link ) ); """)

        # ## EMPLOYEES
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS potential_employees ( \
        # comp_link TEXT, \
        # name TEXT, \
        # position TEXT, \
        # prof_link TEXT, \
        # prof_pic TEXT, \
        # email TEXT, \
        # FOREIGN KEY ( comp_link ) REFERENCES testing ( linkedin_link ) ); """)

        # ## EMPLOYEES
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS hidden_employees ( \
        # comp_link TEXT, \
        # position TEXT, \
        # prof_pic TEXT, \
        # FOREIGN KEY ( comp_link ) REFERENCES testing ( linkedin_link ) ); """)

        # # SUBDOMAINS
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS subdomains ( \
        # domain TEXT NOT NULL, \
        # subdomain TEXT NOT NULL PRIMARY KEY, \
        # FOREIGN KEY ( domain ) REFERENCES testing ( target ) ); """ )

        # # WHOIS
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS whois ( \
        # hostname TEXT NOT NULL, \
        # ip TEXT NOT NULL, \
        # FOREIGN KEY ( ip ) REFERENCES server_info ( ip ), \
        # FOREIGN KEY ( hostname ) REFERENCES subdomains ( subdomain ) ); """ )

        # # SERVER INFO
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS server_info ( \
        # ip TEXT NOT NULL PRIMARY KEY, \
        # asn TEXT, \
        # organization TEXT, \
        # coordinate TEXT, \
        # isp TEXT, \
        # FOREIGN KEY ( asn ) REFERENCES asn_info ( asn ) ); """ )

        # # SERVICES
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS services ( \
        # ip TEXT NOT NULL, \
        # port TEXT NOT NULL, \
        # service TEXT NOT NULL, \
        # FOREIGN KEY ( ip ) REFERENCES server_info ( ip ) ); """ )

        # # ASN INFO
        # create_sql.append( """ CREATE TABLE IF NOT EXISTS asn_info ( \
        # asn TEXT NOT NULL PRIMARY KEY, \
        # country TEXT NOT NULL, \
        # registry TEXT NOT NULL, \
        # cidr TEXT NOT NULL, \
        # description TEXT, \
        # registration_date TEXT NOT NULL ); """ )

        ### MODIFY!!
        # for query in create_sql:
        #     self.sql_stash( query )

        ################# sometimes linkedin sometime domain, sometomes both
        # if 'linkedin' in target:
        #     self.sql_stash( 'INSERT INTO testing( linkedin_link ) VALUES( ? )', (target,) )
        # else:
        #     self.sql_stash( 'INSERT INTO testing( target ) VALUES( ? )', (target,) )

    def get_column( self, table, column, compT=None, compS=None, grB=None ):
        conn = self.create_connection()

        try:
            c = conn.cursor()
            if compT and compS:
                c.execute( f'SELECT {column} FROM {table} WHERE {compT} = ?' , ( compS, ) )
            elif grB:
                c.execute( f'SELECT {column} FROM {table} GROUP BY {grB}' )
            else:
                c.execute( f'SELECT DISTINCT {column} FROM {table}' )
            result = c.fetchall()
        except Error as e:
            error(e)
            result = []

        conn.close()
        if compS or compT or grB:
            return result if result else []
        else:
            return [r[0] if result else [] for r in result]