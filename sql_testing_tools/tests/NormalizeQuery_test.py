import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print("Set path to: "+parent_dir_path)

import unittest
import BaseAccess as Ba
import Helper as He

Ba.setDBName("sql_testing_tools/databases/bayern.db")

class NormalizeQuery_test(unittest.TestCase):
    maxDiff = None

    def readFile(self,path: str):
        with open(path, 'r') as file:
            return file.read()

    def helper(self, nr:str):
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("sql_testing_tools/tests/v1/a"+nr+".sql"),td)
        q2 = He.normalizeSQLQuery(self.readFile("sql_testing_tools/tests/v2/a"+nr+".sql"),td)
        if q1 != q1:
            self.fail("\n" + q1 + "\n" + q1)
        if q2 != q2:
            self.fail("\n" + q2 + "\n" + q2)
        if q1 != q2:
            self.fail("\n" + q1 + "\n" + q2)


    def test_a01_oneCondition(self):
        nr = '01'
        self.helper(nr)
    

    def test_a02_oneOR(self):
        nr = '02'
        self.helper(nr)


    def test_a03_twoOR(self):
        nr = '03'
        self.helper(nr)


    def test_a04_twoOR_withBrackets(self):
        nr = '04'
        self.helper(nr)


    def test_a05_twoOR_withWithoutBrackets(self):
        nr = '05'
        self.helper(nr)


    def test_a06_AND_inBrackets_OR_outside(self):
        nr = '06'
        self.helper(nr)


    def test_a07_AND_inOutsideBrackets_OR_outside(self):
        nr = '07'
        self.helper(nr)


    def test_a08_OR_inBrackets_AND_outside(self):
        nr = '08'
        self.helper(nr)


    def test_a09_GROUP_CountSumAvg(self):
        nr = '09'
        self.helper(nr)


    def test_a10_GROUP_twoCols(self):
        nr = '10'
        self.helper(nr)
            

    def test_a11_BUG(self):
        nr = '11'
        self.helper(nr)
            

    def test_a12_BUG(self):
        nr = '12'
        self.helper(nr)
            

    def test_a13_BUG(self):
        nr = '13'
        self.helper(nr)
            

    def test_a14_BUG(self):
        nr = '14'
        self.helper(nr)


    def test_a15_ORDER_BY(self):
        nr = '15'
        self.helper(nr)


    def test_a16_LIMIT(self):
        nr = '16'
        self.helper(nr)


    def test_a17_LIKE(self):
        nr = '17'
        self.helper(nr)


    def test_a18_Semicolon(self):
        nr='18'
        self.helper(nr)