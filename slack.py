#!/usr/bin/env python

import requests
import calendar
from datetime import datetime, timedelta
from settings import _token, _domain, _user, _time, _pretty


if __name__ == '__main__':
    while 1:
        files_list_url = 'https://slack.com/api/files.list'
        date = str(calendar.timegm((datetime.now() + timedelta(-_time)).utctimetuple()))
        data = {"token": _token, "ts_to": date, "user": _user}
        response = requests.post(files_list_url, data=data)
        if len(response.json()["files"]) == 0:
            break
        for f in response.json()["files"]:
            print("Deleting file " + f["name"] + "...")
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            delete_url = "https://" + _domain + ".slack.com/api/files.delete?t=" + timestamp
            requests.post(delete_url, data={
                "token": _token, 
                "file": f["id"], 
                "set_active": "true", 
                "_attempts": "1"})
    print("DONE!")
