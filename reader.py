#!/usr/bin/env python
# coding: UTF-8

import csv
import os
from datetime import datetime, timedelta, date
import MySQLdb

class Reader:
    mysql_conn = ""
    csv_name = ""
    hostname = "localhost"
    username = "root"
    password = ""
    database = "laravel_expense"
    columns = ""

    def __init__(self, csv, columns):
        self.csv_name = csv
        self.columns = columns

    def __connect_db(self):
        self.mysql_conn = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database)

    def __generate_sql(self):
        if not os.path.isfile(self.csv_name):
            raise Exception('You must set a valid csv!')

        with open(self.csv_name) as csv_data:
            csv_file = csv.reader(csv_data, delimiter=',')
            values = self.__generateValues(csv_file)

        query = 'INSERT INTO expenses (' + self.__generateColumns() + ') VALUES (' + self.__bindValues() + ');'

        return query, values

    def __generateValues(self, csv_file):
        values = []

        for row in csv_file:
            value = (1, (date.today() - timedelta(days=120)).isoformat(), (date.today() + timedelta(days=30)).isoformat(), '', 1, 1, 1, 1, row[2], '', 1, datetime.today().isoformat())
            values.append(value)
        
        return values
        
    def __generateColumns(self):
        if self.columns == '' or self.columns == False:
            raise Exception('You must set a valid columns!') 

        return ', '.join(map(str, self.columns))

    def __bindValues(self):
        binds = []

        for row in self.columns:
            binds.append("%s")

        return ', '.join(map(str, binds))

    def execute(self):
        generated_sql = self.__generate_sql()

        self.__connect_db()

        cursor = self.mysql_conn.cursor()
        cursor.executemany(generated_sql[0], generated_sql[1])

        self.mysql_conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        print('Query is done...Affected rows: {}'.format(affected_rows))
