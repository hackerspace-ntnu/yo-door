#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from yoapi import yo

from secret import YO_API_KEY


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

YO = yo.api(YO_API_KEY)

DOOR_API_URL = "http://hackerspace.idi.ntnu.no/api/door"
LATEST_ID_TXT = 'LATEST_ID.txt'
SLEEP_SECONDS = 60


def read_latest_id():
    with open(LATEST_ID_TXT, 'r') as f:
        return f.readline()


def write_latest_id(id_str):
    """
    If this program is stopped for some reason (e.g. reboot),
    then it will check the file when it starts up again,
    and avoid sending duplicate Yos if nothing changed during the downtime.
    """
    with open(LATEST_ID_TXT, 'w') as f:
        f.write(id_str)
        return id_str


def api_get():
    json_str = urlopen(DOOR_API_URL).read().decode("utf-8")
    data = loads(json_str)[0]
    return data


def main():
    try:
        print("Connected to api.justyo.co. {} people are subscribed!".format(YO.subscribers_count()))
    except KeyError:
        print("Error connecting to api.justyo.co. Did you remember to put YO_API_KEY in secret.py?")
        exit(1)

    try:
        latest_id = read_latest_id()
    except FileNotFoundError:
        latest_id = write_latest_id('None')

    while True:
        try:
            response = api_get()
            response_id = response['_id']
            is_open = response['isOpen']

            if response_id != latest_id:
                latest_id = write_latest_id(response_id)

                if is_open:
                    YO.yoall()
                    print("Yo!")
        except (HTTPError, URLError) as e:
            print(e)
            # TODO: better error logging?
        finally:
            sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    print("Use daemon.py to run as a daemon.")
    main()
