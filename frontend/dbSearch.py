import pandas as pd
import numpy as np
import sqlite3

def search_db(search_term, creds, requirements, breadths, genEds, class_level):
    conn = sqlite3.connect('../data/classes.db')
    crsr = conn.cursor()

    # Default values if no filters are provided
    if len(creds) == 0:
        creds = [1, 2, 3, 4, 5, 6, 7, 8]
    else:
        creds = [int(i) for i in creds]

    if not class_level:
        class_level = [0, 1, 2]  # Assuming 0=ELEM, 1=INTER, 2=ADV
    else:
        for i in range(len(class_level)):
            if class_level[i] == 'ELEM':
                class_level[i] = 1
            elif class_level[i] == 'INTER':
                class_level[i] = 2
            elif class_level[i] == 'ADV':
                class_level[i] = 3

    # Base query
    query = 'SELECT Course.*, gradeDists.* FROM Course LEFT JOIN gradeDists ON Course.block = gradeDists.block WHERE 1=1'  # Always true condition for easy appending
    params = []

    # Add search term if provided
    if search_term:
        query += ' AND (Course.block LIKE ? OR Course.desc LIKE ?)'
        params.extend([f"%{search_term}%", f"%{search_term}%"])

    # Add filters dynamically based on available data
    if creds:
        query += ' AND Course.credits IN ({})'.format(','.join('?' for _ in creds))
        params.extend(creds)

    if class_level:
        query += ' AND Course.level IN ({})'.format(','.join('?' for _ in class_level))
        params.extend(class_level)

    requirementsDict = {'L&S': 'lns', 'ETHNIC': 'ethnic', 'HONORS': 'honors', 'GENED': 'genEd', 'WORKPLACE': 'workplace', 'FOREIGN': 'foreignLang'}
    if requirements:
        for req in requirements:
            query += f' AND Course.{requirementsDict[req]} = 1'

    breadthDict = {'BIO': 'Biological Science', 'HUM': 'Humanities', 'PHY': 'Physical Science', 'SOC': 'Social Science', 'NAT': 'Natural Science', 'LIT': 'Literature'}
    if breadths:
        for breadth in breadths:
            query += f' AND Course.breadth = "{breadthDict[breadth]}"'

    genEdDict = {'COMM A': 1, 'COMM B': 2, 'QR-A': 1, 'QR-B': 2}
    if genEds:
        for genEd in genEds:
            query += f' AND Course.genEd = {genEdDict[genEd]}'

    crsr.execute(query, params)
    rows = crsr.fetchall()
    conn.close()

    if len(rows) > 500:
        return rows[:500]
    return rows


def getData(name):
    conn = sqlite3.connect('../data/classes.db')
    query = f'SELECT Course.*, gradeDists.* FROM Course LEFT JOIN gradeDists ON Course.block = gradeDists.block WHERE Course.block = "{name}"'
    crsr = conn.cursor()
    crsr.execute(query)
    row = crsr.fetchall()
    print(row)
    conn.close()
    return row