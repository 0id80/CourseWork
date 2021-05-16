from os import system
from time import sleep
from requests import get
from threading import Thread
from requests.exceptions import ConnectionError


def is_site_available(url):
    try:
        request = get(url, timeout=1)
    except ConnectionError:
        return False
    if request.status_code != 200:
        return False
    return True


def thread_checker(url):
    while not is_site_available(url):
        sleep(1)
    system(f"start {url}")


if __name__ == '__main__':
    thread_request = Thread(target=thread_checker, args=("http://127.0.0.1:8000/", ))
    thread_request.start()

    system('python manage.py runserver')
