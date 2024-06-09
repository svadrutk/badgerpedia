import pandas as pd
import numpy as np
import psycopg2
import os

if 'DATABASE_URL' in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    DATABASE_URL = "postgres://ub9r9h2ch1dkdd:p8acce4f8f0a55498479c89b9c6dda4fbd6ca3cb921638eb34ced5c624678bba6@ec2-52-204-68-34.compute-1.amazonaws.com:5432/d3v3v0c0h5hlvq"

def search_db(search_term, creds, requirements, breadths, genEds, class_level):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require') # Connect to the database
    crsr = conn.cursor()

    # Default values if no filters are provided
    if not creds:
        creds = [1, 2, 3, 4, 5, 6, 7, 8]
    else:
        creds = [int(i) for i in creds]

    if not class_level:
        class_level = [0, 1, 2, 3]  # Assuming 1=ELEM, 2=INTER, 3=ADV
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

    # Base query
    subquery = '''
    SELECT classes.*, grades.*,
    (CASE
        WHEN LOWER(REPLACE(classes.block, ' ', '')) LIKE %s THEN 10
        ELSE 0
    END +
     CASE
        WHEN LOWER(classes.description) LIKE %s THEN 5
        ELSE 0
    END +
     CASE
        WHEN classes.block LIKE %s THEN 7
        ELSE 0
    END) AS relevance_score
    FROM classes
    LEFT JOIN grades ON classes.block = grades.block
    WHERE 1=1
    '''

    params = [f"%{normalized_search_term}%", f"%{search_term.lower()}%", f"%{expanded_search_term}%"]

    print("Search term:", search_term)
    print("Normalized search term:", normalized_search_term)
    print("Expanded search term:", expanded_search_term)

    # Add credit filters
    if creds:
        subquery += ' AND classes.min_credits <= %s AND classes.max_credits >= %s'
        print("Max creds:", max(creds), "Min creds:", min(creds))
        params.extend([max(creds), min(creds)])
    else:
        print("No credit filters")

    # Add class level filters
    if class_level:
        placeholders = ', '.join(['%s'] * len(class_level))
        subquery += f' AND classes.level IN ({placeholders})'
        print("Class level:", class_level)
        params.extend(class_level)
    else:
        print("No class level filt ers")

    # Add requirement filters
    requirementsDict = {'L&S': 'lns', 'ETHNIC': 'ethnic', 'HONORS': 'honors', 'GENED': 'genEd', 'WORKPLACE': 'workplace', 'FOREIGN': 'foreignLang'}
    if requirements:
        for req in requirements:
            print("Requirement:", req)
            subquery += f' AND classes.{requirementsDict[req]} = 1'
    else:
        print("No requirement filters")

    # Add breadth filters
    breadthDict = {'BIO': 'Biological Science', 'HUM': 'Humanities', 'PHY': 'Physical Science', 'SOC': 'Social Science', 'NAT': 'Natural Science', 'LIT': 'Literature'}
    if breadths:
        breadth_placeholders = ' OR '.join(['classes.breadth = %s' for _ in breadths])
        subquery += f' AND ({breadth_placeholders})'
        print("Breadths:", breadths)
        params.extend([breadthDict[breadth] for breadth in breadths])
    else:
        print("No breadth filters")

    # Add genEd filters
    genEdDict = {'COMM A': 1, 'COMM B': 2, 'QR-A': 1, 'QR-B': 2}
    if genEds:
        print("GenEds:", genEds)
        genEd_placeholders = ' OR '.join(['classes.genEd = %s' for _ in genEds])
        subquery += f' AND ({genEd_placeholders})'
        params.extend([genEdDict[genEd] for genEd in genEds])
    else:
        print("No genEd filters")

    # Ensure only classes with a relevance_score > 0 are included in the outer query
    final_query = f'''
    SELECT * FROM ({subquery}) subquery
    WHERE relevance_score > 0
    ORDER BY relevance_score DESC
    '''
    crsr.execute(final_query, params)
    rows = crsr.fetchall()
    conn.close()

    if len(rows) > 500:
        return rows[:500]
    return rows


# Function to get data for a specific class
def getData(name):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    query = f'SELECT classes.*, grades.* FROM classes LEFT JOIN grades ON classes.block = grades.block WHERE classes.block = \'{name}\''
    crsr = conn.cursor()
    crsr.execute(query)
    row = crsr.fetchall()
    print(row)
    print(len(row[0]))
    conn.close()
    return row