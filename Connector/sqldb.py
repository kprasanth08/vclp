# -*- coding: utf-8
import os
import sqlite3


class SqlDB(object):

    def __init__(self,tag):
        # os.system('rm -rf vclp.db')
        self.db = sqlite3.connect(tag+'.db')
        self.cursor = self.db.cursor()

    def close(self):

        self.cursor.close()

    def execute(self, cmd):
        """

        :param cmd:
        :return: sql command result
        """
        return self.cursor.execute(cmd)

    def commit(self):

        return self.db.commit()
