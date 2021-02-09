import psycopg2
import json

"""
Blue Onion Labs
Take Home Technical Test
Author: Clay Brimm 
2/9/2021
"""

def main():
    print('Welcome to starlink.py!')
    print('Parsing JSON File: starlink_historical_data.json...')
    starlink_data = parse_json() 
    print('Parsing Complete!')
    starlink_sql(starlink_data)

# Function that parses json file and creates an array of the relevent fields 
# this function is not entirely necessary but it could be useful if incoming data changed or was a stream.
def parse_json():
    relevant_fields = []
    with open('./starlink_historical_data.json') as f:
        data = json.load(f)
    for i in data:
        satellite_id = i['id']
        creation_date = i['spaceTrack']['CREATION_DATE']
        latitude = i['latitude']
        longitude = i['longitude']
        entry_arr = [creation_date, satellite_id, latitude, longitude]
        relevant_fields.append(entry_arr)
    return relevant_fields

# Function accepts an array and inserts data to starlink table
def starlink_sql(data_arr):
    #postgres connection fields
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="admin123")

    cur = conn.cursor()

    #SQL statements to create starlink table and upload data
    starlink_create_sql = 'CREATE TABLE starlink (id serial PRIMARY KEY, creation_date TIMESTAMP, satellite_id VARCHAR(50), longitude INT, latitude INT);'
    insert_sql = 'INSERT INTO starlink (creation_date, satellite_id, latitude, longitude) VALUES (%s, %s, %s, %s)'

    # Create starlink table
    print('Creating starlink table...')
    cur.execute(starlink_create_sql)
    conn.commit()
    print('starlink table created!')

    # Iterate through data array and attempt to execute the insert statement
    print('Inserting data to starlink table...')
    for entry in data_arr:
        try:
            data = (entry[0], entry[1], entry[2], entry[3])
            cur.execute(insert_sql, data)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
    conn.commit()

    cur.close()
    print('Insert Complete!')

if __name__ == "__main__":
    main()
