from os import system
import requests
from threading import Thread


def get_request(site):
    response = requests.get(site)
    if response.status_code == 200:
        system('start http://127.0.0.1:8000/')
        print("STARTED")


if __name__ == '__main__':
    thread_request = Thread(target=get_request, args=("http://127.0.0.1:8000/", ))
    thread_request.start()

    system('python manage.py runserver')
