import pandas as pd
import numpy as np
import sqlite3

def search_db(search_term, creds, requirements, breadths, genEds, class_level):
    conn = sqlite3.connect('../data/classes.db')
    crsr = conn.cursor()

    # Default values if no filters are provided
    if not creds:
        creds = [1, 2, 3, 4, 5, 6, 7, 8]
    else:
        creds = [int(i) for i in creds]

    if not class_level:
        class_level = [1, 2, 3]  # Assuming 1=ELEM, 2=INTER, 3=ADV
    else:
        for i in range(len(class_level)):
            if class_level[i] == 'ELEM':
                class_level[i] = 1
            elif class_level[i] == 'INTER':
                class_level[i] = 2
            elif class_level[i] == 'ADV':
                class_level[i] = 3

    # Normalize search term to remove spaces and make it case insensitive
    if search_term:
        normalized_search_term = search_term.replace(' ', '').lower()
    else:
        normalized_search_term = " "
        search_term = " "


    # Mapping for abbreviations
    abbreviation_mapping = {
        'cs': 'COMP SCI',

        # Add more abbreviations as needed
    }

    # Expand the search term if it matches an abbreviation
    expanded_search_term = search_term
    for abbrev, full_name in abbreviation_mapping.items():
        if normalized_search_term.startswith(abbrev):
            expanded_search_term = search_term.upper().replace(abbrev.upper(), full_name, 1)
            break

    print("Normalized search term:", normalized_search_term)

    # Base query
    query = '''
    SELECT Course.*, gradeDists.*,
    (CASE
        WHEN LOWER(REPLACE(Course.block, " ", "")) LIKE ? THEN 10
        ELSE 0
    END +
     CASE
        WHEN LOWER(Course.desc) LIKE ? THEN 5
        ELSE 0
    END +
     CASE
        WHEN Course.block LIKE ? THEN 7
        ELSE 0
    END) AS relevance_score
    FROM Course
    LEFT JOIN gradeDists ON Course.block = gradeDists.block
    WHERE 1=1
    '''

    params = [f"%{normalized_search_term}%", f"%{search_term.lower()}%", f"%{expanded_search_term}%"]

    # Add credit filters
    if creds:
        query += ' AND Course.min_credits <= ? AND Course.max_credits >= ?'
        print("Max creds:", max(creds), "Min creds:", min(creds))
        params.extend([max(creds), min(creds)])

    # Add class level filters
    if class_level:
        query += ' AND Course.level IN ({})'.format(','.join('?' for _ in class_level))
        print("Class level:", class_level)
        params.extend(class_level)

    # Add requirement filters
    requirementsDict = {'L&S': 'lns', 'ETHNIC': 'ethnic', 'HONORS': 'honors', 'GENED': 'genEd', 'WORKPLACE': 'workplace', 'FOREIGN': 'foreignLang'}
    if requirements:
        for req in requirements:
            print("Requirement:", req)
            query += f' AND Course.{requirementsDict[req]} = 1'

    # Add breadth filters
    breadthDict = {'BIO': 'Biological Science', 'HUM': 'Humanities', 'PHY': 'Physical Science', 'SOC': 'Social Science', 'NAT': 'Natural Science', 'LIT': 'Literature'}
    if breadths:
        query += ' AND (' + ' OR '.join([f'Course.breadth = ?' for _ in breadths]) + ')'
        print("Breadths:", breadths)
        params.extend([breadthDict[breadth] for breadth in breadths])

    # Add genEd filters
    genEdDict = {'COMM A': 1, 'COMM B': 2, 'QR-A': 1, 'QR-B': 2}
    if genEds:
        print("GenEds:", genEds)
        query += ' AND (' + ' OR '.join([f'Course.genEd = ?' for _ in genEds]) + ')'
        params.extend([genEdDict[genEd] for genEd in genEds])

    # Ensure only courses with a relevance_score > 0 are included
    query += ' AND relevance_score > 0'
    # Order by relevance score
    query += ' ORDER BY relevance_score DESC'
    print(query)
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
    print(len(row[0]))
    conn.close()
    return row