import requests
import psycopg2
import os

# Constants
API_TOKEN = '192214970a684cd68488a22e5fa80a34'
BASE_URL = 'https://api.madgrades.com/v1'
DATABASE_URL = os.environ['DATABASE_URL']

# Headers for authentication
headers = {
    'Authorization': f'Token token={API_TOKEN}'
}

# Function to search for a course
def search_course(query):
    url = f'{BASE_URL}/courses'
    params = {
        'query': query,
        'sort': 'relevance'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Function to get detailed course information
def get_course_details(uuid):
    url = f'{BASE_URL}/courses/{uuid}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to pull grade distribution based on course query
def pull_grade_distribution(course_query):
    # Search for the course
    search_results = search_course(course_query)
    if search_results['results']:
        course_uuid = search_results['results'][0]['uuid']  # Assuming the first result is the desired course
        course_details = get_course_details(course_uuid)
        gradesURL = course_details['gradesUrl'] # URL to get grade distribution
        response = requests.get(gradesURL, headers=headers, params={'format': 'json'}).json()
        return response["cumulative"]
    return None


def add_grades_to_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades")
    # Fetch all classes from the Course table
    cursor.execute("SELECT block FROM classes")
    classes = cursor.fetchall()

    # Iterate over each class
    for course in classes:
        course_block = course[0]

        # Get the grade distribution for the current class
        grade_distribution = pull_grade_distribution(course_block)

        print('Inserting grade distribution for:', course_block)
        print(grade_distribution)
        # Insert grade distribution data into the grades table
        if grade_distribution:
            # Assuming grade_distribution is a dictionary
            cursor.execute("INSERT INTO grades (block, total, aCount, abCount, bCount, bcCount, cCount, dCount, fCount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (course_block, grade_distribution['total'], grade_distribution['aCount'], grade_distribution['abCount'],
                            grade_distribution['bCount'], grade_distribution['bcCount'], grade_distribution['cCount'],
                            grade_distribution['dCount'], grade_distribution['fCount']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def convert_to_letters():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    rows = cursor.fetchall()
    # calculate gpa
    for row in rows:
        total = row[2]
        a = row[3]
        ab = row[4]
        b = row[5]
        bc = row[6]
        c = row[7]
        d = row[8]
        f = row[9]
        if total == 0 or a + ab + b + bc + c + d + f == 0:
            cursor.execute("UPDATE grades SET letter = ? WHERE block = ?", ('N/A', row[1]))
            conn.commit()
            continue
        gpa = (4 * a + 3.5 * ab + 3 * b + 2.5 * bc + 2 * c + 1 * d) / (a + ab + b + bc + c + d + f)
        if gpa >= 3.5:
            letter = 'A'
        elif gpa >= 3:
            letter = 'B'
        elif gpa >= 2.5:
            letter = 'BC'
        elif gpa >= 2:
            letter = 'C'
        elif gpa >= 1:
            letter = 'D'
        else:
            letter = 'F'
        print("GPA for", row[1], "is", gpa, "which is equivalent to", letter)
        cursor.execute("UPDATE grades SET letter = ? WHERE block = ?", (letter, row[1]))
        conn.commit()
    conn.close()


def transfer_credits_to_range():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    crsr = conn.cursor()

    # Add min_credits and max_credits columns
    crsr.execute('ALTER TABLE Course ADD COLUMN min_credits INTEGER')
    crsr.execute('ALTER TABLE Course ADD COLUMN max_credits INTEGER')

    # Update min_credits and max_credits based on credits column
    crsr.execute('SELECT rowid, credits FROM Course')
    rows = crsr.fetchall()
    for row in rows:
        rowid, credits = row
        if '-' in credits:
            min_credits, max_credits = map(int, credits.split('-'))
        else:
            min_credits = max_credits = int(credits)
        print(f'Updating min_credits and max_credits for rowid {rowid} to {min_credits} and {max_credits}')
        crsr.execute('UPDATE Course SET min_credits = ?, max_credits = ? WHERE rowid = ?', (min_credits, max_credits, rowid))

    conn.commit()
    conn.close()

# Call the function
transfer_credits_to_range()
