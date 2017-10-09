#!/usr/bin/python
import sys
import MySQLdb


class MyDbInfo(object):
    def __init__(self, db_host='127.0.0.1', db_user='root', db_pass='root', port=3306, db='mydb'):
        self._host = db_host
        self._user = db_user
        self._password = db_pass
        self._db_port = port
        self._db = db
        self._relations = {}
        self._table_heights = {}
        try:
            self._con = MySQLdb.Connection(
                host=self._host,
                user=self._user,
                passwd=self._password,
                port=self._db_port,
                db=self._db
            )
            self._cursor = self._con.cursor()
            self._cursor.execute("show tables")
            data = self._cursor.fetchall()
            self._tables = [t[0] for t in data]
        except Exception as e:
            print e
            sys.exit(1)
    
    def get_relations(self):
        if self._relations:
            return
        stmt = "select  table_name,column_name,referenced_table_name,referenced_column_name from\
        information_schema.key_column_usage where referenced_table_name is not null  and\
        table_schema='{}' and table_name='{}'";
        for t in self._tables:
            self._relations[t] = {'referredby' : set(), 'referring' : set()}
        for t in self._tables:
            stmt_sub = stmt.format(self._db, t)
            self._cursor.execute(stmt_sub)
            data = self._cursor.fetchall()
            if len(data) == 0:
                continue
            for d in data:
                self._relations[t]['referring'].add(d[2])
                self._relations[d[2]]['referredby'].add(t)

    def print_leaf_tables(self):
        if not self._relations:
            self.get_relations()
        for t in self._relations:
            if not self._relations[t]['referring']:
                print t

    def print_relations(self):
        if not self._relations:
            self.get_relations()
        print self._relations


    def show_tables(self):
        print self._tables

    def get_heights(self):
        if not self._table_heights:
            for t in self._tables:
                self.height_table(t)


    def height_table(self, table):
        if table not in self._relations:
            return -1
        if table in self._table_heights:
            return self._table_heights[table]
        if not self._relations[table]['referring']:
            return 0
        heights = [self.height_table(t) for t in self._relations[table]['referring']\
                if t != table]
        retval = 1
        if heights:
            retval = 1 + max(heights)
        self._table_heights[table] = retval
        return retval

    def print_table_heights(self):
        if not self._table_heights:
            self.get_heights()
        print self._table_heights

    def _get_table_down(self, table, plist):
        if not self._relations[table]['referring']:
            out = ""
            if plist:
                out += ", ".join(plist)
            out += ", " +  table
            print out
        else:
            plist.append(table)
            for t in self._relations[table]['referring']:
                if t == table:
                    if len(self._relations[table]['referring']) == 1:
                        print ', '.join(plist)   
                    continue
                self._get_table_down(t, plist)
            plist.pop()

    def get_table_down_path(self, table):
        if table not in self._tables:
            return ""
        self._get_table_down(table, [])


    def get_related_table_groups(self, table, table_groups):
        if table in table_groups:
            return
        table_groups.add(table)
        for t in self._relations[table]['referring']:
            self.get_related_table_groups(t, table_groups)
    
    
if __name__ == '__main__':
    mydb = MyDbInfo(db_user='root', db_pass='root', port=3306)
    mydb.get_relations()
    mydb.print_leaf_tables()
    mydb.print_relations()
    mydb.print_table_heights()
