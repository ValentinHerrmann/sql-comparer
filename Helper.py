import os
import BaseAccess as Ba
import TokenProcessing as Tp

import requests
import sqlparse

from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function, Parenthesis
from sqlparse.tokens import Keyword, DML, Name, Wildcard



def normalizeSQLQuery(query, baseDict):
    try:
        query = query.replace("\"", "'")
        parsed = sqlparse.parse(query)[0]
        parsed.tokens = [token for token in parsed.tokens if not token.is_whitespace]
    except Exception as e:
        raise Exception(f"\nSyntax-Fehler in der SQL-Abfrage.")

    formatted_query = []
    alias_map = {}

    # First pass to process FROM clause and populate alias_map
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is Keyword and token.value.upper() == 'FROM':
            formatted_query.append('FROM')
            pass
        elif isinstance(token, Identifier) and formatted_query and formatted_query[-1] == 'FROM':
            il = IdentifierList([token])
            formatted_query.append(Tp.process_from(il, alias_map, baseDict))
            Tp.process_from(il, alias_map, baseDict)
        elif isinstance(token, IdentifierList) and formatted_query and formatted_query[-1] == 'FROM':
            formatted_query.append(Tp.process_from(token, alias_map, baseDict))
            Tp.process_from(token, alias_map, baseDict)

    formatted_query = []

    # Second pass to process SELECT and WHERE clauses
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is DML and token.value.upper() == 'SELECT':
            formatted_query.append('SELECT')
        elif token.ttype is Keyword and token.value.upper() == 'FROM':
            formatted_query.append('FROM')  
        elif token.ttype is Keyword and token.value.upper() == 'GROUP BY':
            formatted_query.append('GROUP BY')
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == 'FROM':
            formatted_query.append(Tp.process_from(token, alias_map, baseDict))
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == 'GROUP BY':
            formatted_query.append(Tp.process_groupby(token, alias_map, baseDict))
        elif isinstance(token, Where):
            formatted_query.append('WHERE')
            formatted_query.append(Tp.process_where(token, alias_map, baseDict))
        elif formatted_query and formatted_query[-1] == 'SELECT' and (isinstance(token, IdentifierList) or isinstance(token, Function) or isinstance(token, Identifier)):
            if isinstance(token, Function):
                token = IdentifierList([token])
            formatted_query.append(Tp.process_select(token, alias_map, baseDict))
        else:
            formatted_query.append(str(token))

    return " ".join(formatted_query)


def findTableForColumn(data_dict, target_value, relevantTables):
    l = []
    for key, value_list in data_dict.items():
        if key.lower() in relevantTables:
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    if len(l) == 0:
        for key, value_list in data_dict.items():
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    return l


def getTableScheme(table_name: str, tableDict: dict):
    tab = tableDict[table_name]

    # Format the schema
    schema = "(" + ",".join([f"{col[0]}:{col[1]}" for col in tab]) + ")"
    return schema

def getCosetteKeyFromFile():
    try:
        with open("cosette_apikey.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "NOKEY"

def buildAndSendCosetteRequest(baseDict, sql, sol):

    err = ""
    for i in range(2):
        try:
            apiKey=getCosetteKeyFromFile()


            schema = ""
            for tab in baseDict.keys():
                schema += f"schema sch{tab}{getTableScheme(tab, baseDict)};\n"
            for tab in baseDict.keys():
                schema += f"table {tab}(sch{tab});\n"

            q1 = "query q1\n`"+sql+"`;\n"
            q2 = "query q2\n`"+sol+"`;\n"

            cosette = "-- random Kommentar\n" + schema + q1 + q2 + "verify q1 q2;\n"
            print(cosette)

            r = requests.post("https://demo.cosette.cs.washington.edu/solve",data={"api_key": apiKey, "query": cosette}, verify=False)

            print(r.text)
            return (r.json()['result'],r.text)
            #return r.json()['result']

        except Exception as e:
            err = str(e)
    return ("ERR", err)


def checkColumns(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)

    if("SELECT" in sql and "FROM" in sql):
        start = str.find(sql, "SELECT")
        end = str.find(sql, "FROM")
        submission = str.strip(sql[start:end])
        print("'"+submission+"'")

        start = str.find(sol, "SELECT")
        end = str.find(sol, "FROM")
        solution = str.strip(sol[start:end])
        print("'"+solution+"'")

        if submission == solution:
            return ""
    return "Ausgegebene Spalten sind nicht korrekt (oder nicht automatisch überprüfbar)."


def checkTables(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)

    if("SELECT" in sql and "FROM" in sql):
        endFromKeywords = ["WHERE", "GROUP", "ORDER", "LIMIT", ";"]

        start = str.find(sql, "FROM")
        end = -1


        for keyword in endFromKeywords:
            if(str.find(sql, keyword) != -1):
                end = str.find(sql, keyword)
                break
        if(end == -1):
            end = len(sql)

        submission = str.strip(sql[start:end])
        print("'"+submission+"'")

        start = str.find(sol, "FROM")
        end = -1
        
        for keyword in endFromKeywords:
            if(str.find(sol, keyword) != -1):
                end = str.find(sol, keyword)
                break
        if(end == -1):
            end = len(sol)

        solution = str.strip(sol[start:end])
        print("'"+solution+"'")

        if submission == solution:
            return ""
    return "Verwendete Tabellen sind nicht korrekt (oder nicht automatisch überprüfbar)."


def checkEquality(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)
    if(sql=='' or sol==''):
        return "\n\nSQL-Datei ist leer. Aufgabe wurde noch nicht bearbeitet."

    if(sql==sol):
        return ""

    result = buildAndSendCosetteRequest(bd, sql, sol)

    if(result[0] == "ERR"):
        return "\n\nFehler bei der automatischen Überprüfung der Abgabe. Es kann keine Aussage über die Korrektheit der Abgabe getroffen werden."
    elif(result[0] != "EQ"):
        return "\n\nDie Abgabe stimmt nicht mit der Musterlösung überein."
    return ""


