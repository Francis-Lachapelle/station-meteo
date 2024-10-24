import sqlite3
from common_utils import error_handler
import pandas as pd

@error_handler
def connect_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    return conn, cursor


@error_handler
def create_tables():
    conn, cursor = connect_db()
    
    # Create a table for storing temperature and humidity logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL, 
            device TEXT
        )
    ''') 

    # Create the table for storing daily means if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_means (
            date TEXT PRIMARY KEY,
            mean_temperature REAL,
            mean_humidity REAL
        )
    ''')

    # Create a table to store metadata like the last processed date
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Initialize the last processed date to NULL if it doesn't exist
    cursor.execute('''
        INSERT OR IGNORE INTO metadata (key, value) VALUES ('last_processed_date', NULL)
    ''') 
    conn.commit()
    conn.close()

@error_handler  
def get_last_processed_date():
    conn, cursor = connect_db()
    
    cursor.execute('''
        SELECT value FROM metadata WHERE key = 'last_processed_date'
    ''')
    
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return pd.to_datetime(result[0])  # Return as a datetime object
    else:
        return None

@error_handler  
def update_last_processed_date(last_date, conn, cursor):
    
    
    cursor.execute('''
        UPDATE metadata SET value = ? WHERE key = 'last_processed_date'
    ''', (last_date.strftime('%Y-%m-%d'),))


@error_handler  
def compute_and_save_daily_means():
    print('Computing and saving daily means for new data...')
    
    last_processed_date = get_last_processed_date()

    # Query logs only for unprocessed days
    query = '''
        SELECT timestamp, temperature, humidity FROM logs
    '''
    if last_processed_date:
        query += " WHERE timestamp > '{}'".format(last_processed_date)
    
    print(" WHERE timestamp > '{}'".format(last_processed_date))
    conn, cursor = connect_db()
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print('No new data to process.')
        return

    # Unpack the data into separate lists
    timestamps = [row[0] for row in rows]
    temperatures = [row[1] for row in rows]
    humidities = [row[2] for row in rows]
    
    # Create a DataFrame
    data = pd.DataFrame({
        'timestamp': pd.to_datetime(timestamps, format='%Y-%m-%d %H:%M:%S'),
        'temperature': temperatures,
        'humidity': humidities
    })
    print(data)
    # Extract the date and group by date
    data['date'] = data['timestamp'].dt.date
    daily_means = data.groupby('date').mean()
    
    # Insert or replace daily means into the daily_means table
    for date, row in daily_means.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO daily_means (date, mean_temperature, mean_humidity)
            VALUES (?, ?, ?)
        ''', (str(date), row['temperature'], row['humidity']))

    # Update last processed date
    last_date = daily_means.index[-1]  # The last processed date
    update_last_processed_date(last_date, conn, cursor)

    conn.commit()
    conn.close()
    
    print('Daily means saved up to {}.'.format(last_date))

@error_handler  
def insert_log(timestamp, temperature, humidity, device):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO logs (timestamp, temperature, humidity, device) 
        VALUES (?, ?, ?, ?)
    ''', (timestamp, temperature, humidity, device))
    conn.commit()
    conn.close()

@error_handler  
def get_data():
    conn, cursor = connect_db()
    cursor.execute('''
        SELECT timestamp, temperature, humidity FROM logs
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
    