import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print("Set path to: "+parent_dir_path)

import unittest
import BaseAccess as Ba
import Helper as He



Ba.setDBName("bayern.db")

class NormalizeQuery_test(unittest.TestCase):
    maxDiff = None

    def readFile(self,path: str):
        with open(path, 'r') as file:
            return file.read()

    def test_a01_normalize_euqiv(self):
        nr = '01'
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("tests/v2/a"+nr+".sql"),td)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)
    
    def test_a02_normalize_euqiv(self):
        nr = '02'
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("tests/v2/a"+nr+".sql"),td)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)

    def test_a03_normalize_euqiv(self):
        nr = '03'
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("tests/v2/a"+nr+".sql"),td)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)

    def test_a04_normalize_euqiv(self):
        nr = '04'
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("tests/v2/a"+nr+".sql"),td)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)

    def test_a05_normalize_euqiv(self):
        nr = '05'
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("tests/v2/a"+nr+".sql"),td)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)