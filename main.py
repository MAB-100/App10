import requests
import selectorlib
import time


URL = "http://programmer100.pythonanywhere.com/tours/"


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


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

if __name__ == "__main__":
    while True:
        source = scrape(URL)
        extracted_data = extract(source)
        if extracted_data != "No upcoming tours":
            print(extracted_data)
            exitisting_data = read_data()
            if extracted_data not in exitisting_data:
                save_data(extracted_data)
                send_email(extracted_data)
        time.sleep(3)