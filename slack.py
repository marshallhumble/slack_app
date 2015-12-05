#!/usr/bin/env python

import requests
import calendar
from datetime import datetime, timedelta
from settings import token, domain, user, time, pretty


def delete_my_files():
    while 1:
        files_list_url = 'https://slack.com/api/files.list'
        date = str(calendar.timegm((datetime.now() + timedelta(-time)).utctimetuple()))
        data = {"token": token, "ts_to": date, "user": user}
        response = requests.post(files_list_url, data=data)
        if len(response.json()["files"]) == 0:
            break
        for f in response.json()["files"]:
            print("Deleting file " + f["name"] + "...")
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            delete_url = "https://" + domain + ".slack.com/api/files.delete?t=" + timestamp
            requests.post(delete_url, data={
                "token": token,
                "file": f["id"],
                "set_active": "true",
                "_attempts": "1"})
    print("DONE!")


if __name__ == '__main__':
    delete_my_files()
