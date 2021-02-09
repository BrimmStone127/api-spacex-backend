import psycopg2
import json

def main():
    print('Welcome to starlink.py')
    print('Parsing JSON File: starlink_historical_data.json...')
    starlink_data = parse_json()
    print('Parsing Complete.')
    sql_insert(starlink_data)

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
    #print(relevant_fields)
    return relevant_fields
        
def sql_insert(data_arr):

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="admin123")

    cur = conn.cursor()
    insert_sql = 'INSERT INTO starlink (creation_date, satellite_id, latitude, longitude) VALUES (%s, %s, %s, %s)'

    for entry in data_arr:
        try:
            data = (entry[0], entry[1], entry[2], entry[3])
            cur.execute(insert_sql, data)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
    conn.commit()

if __name__ == "__main__":
    main()