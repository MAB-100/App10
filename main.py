import requests
import selectorlib
import time
import sqlite3


URL = "http://programmer100.pythonanywhere.com/tours/"


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

conn = sqlite3.connect("data.db")
def scrape(url):
    """scarpe the web provided the url"""        
    response = requests.get(URL)
    source = response.text
    return source


def extract(source):
    """extract the data from the source"""
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)["tours"]
    return value


def send_email(data):
    print("Email sent")


def save_data(data):
    try:
        with open("extracted_data.txt","a") as file:
            file.write(data + "\n")
            print("Data saved")
    except Exception as e:
        print(e)

def read_data():
    try:
        with open("extracted_data.txt","r") as file:
            data = file.read()
            return data
    except Exception as e:
        print(e)

def read_from_db(extracted_data):
    row = extracted_data.split(",")
    row = [i.strip() for i in row]
    band, city , date = row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date))
    rows = cursor.fetchall()
    cursor.close() 
    return rows

def save_to_db(data):
    try:
        row = extracted_data.split(",")
        row = [i.strip() for i in row]
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS events (band TEXT, city TEXT, date TEXT)")
        cursor.execute("INSERT INTO events  VALUES (?,?,?)", row)
        conn.commit()
        cursor.close()
        print("Data saved to db")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    while True:
        source = scrape(URL)
        extracted_data = extract(source)
        if extracted_data != "No upcoming tours":
            print(extracted_data)
            # exitisting_data = read_data()
            exitisting_data = read_from_db(extracted_data)
            if not exitisting_data:
            #    save_data(extracted_data)
                save_to_db(extracted_data)
                send_email(extracted_data)
        time.sleep(2)