import pandas as pd
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

def to_sql(df):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        df.insert(0, 'id', range(1, 1 + len(df)))  # Add an id column to the DataFrame
        df.columns = ['id', 'block', 'name', 'desc', 'credits', 'requisites', 'repeatable', 'lastTaught', 'level', 'breadth', 'grad', 'lns', 'ethnic', 'honors', 'genEd', 'workplace', 'foreignLang']
        df.to_sql('Course', conn, if_exists='replace')
    except Exception as e:
        print("An error occurred while converting DataFrame to SQL:", e)
    finally:
        conn.close()
    return None


def main():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        df = pd.read_csv('classes.csv')
        print("DataFrame Head:")
        print(df.head())  # Print the first few rows of DataFrame for inspection
        to_sql(df)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()
