import sqlite3
import math

# Create and/or connect to the SQLite database
conn = sqlite3.connect('Task11_final.db')
c = conn.cursor()

# Create a table to store city data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        city_name TEXT PRIMARY KEY,
        latitude REAL,
        longitude REAL
    )
''')

def get_coordinates(city):
    c.execute('SELECT latitude, longitude FROM cities WHERE city_name = ?', (city,))
    data = c.fetchone()
    if data is None:
        latitude = float(input(f'Enter the latitude for {city}: '))
        longitude = float(input(f'Enter the longitude for {city}: '))
        c.execute('INSERT INTO cities (city_name, latitude, longitude) VALUES (?, ?, ?)', (city, latitude, longitude))
        conn.commit()
        return latitude, longitude
    return data

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def calculate_distance(city1, city2):
    lat1, lon1 = get_coordinates(city1)
    lat2, lon2 = get_coordinates(city2)
    distance = haversine(lat1, lon1, lat2, lon2)
    return distance

def main():
    city1 = input('Enter the first city name: ')
    city2 = input('Enter the second city name: ')
    distance = calculate_distance(city1, city2)
    print(f'The distance between {city1} and {city2} is {distance:.2f} kilometers.')

if __name__ == '__main__':
    main()

# Close the connection
conn.close()