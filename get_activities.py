#!/usr/bin/env python3
"""
pip3 install garth requests readchar

export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>

"""
import datetime
import json
import logging
import os
import sys
import time
from getpass import getpass


import readchar
import requests
import subprocess
from garth.exc import GarthHTTPError
import http.client as http_client

requests.packages.urllib3.add_stderr_logger();
http_client.HTTPConnection.debuglevel = 1

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


def display_text(output):
    """Format API output for better readability."""

    dashed = "-" * 60
    header = f"{dashed}"
    footer = "-" * len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)

def newgarmin(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        print(
            f"Trying to login to Garmin Connect using token data from '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            garmin = Garmin(email, password)
            garmin.login()
            # Save tokens for next login
            garmin.garth.dump(tokenstore)

        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
            logger.error(err)
            return None

    return garmin


def scp_activity(file, destination):
    #p = subprocess.Popen(["scp", file, destination])
    #sts = os.waitpid(p.pid, 0)
    os.system(f"scp {file} {destination}")

def download_activities(garmin, startdate, enddate, output):
    activities = garmin.get_activities_by_date(
        startdate.isoformat(), enddate.isoformat(), "")

    # Download activities
    for activity in activities:
        activity_id = activity["activityId"]
        #if activity_id in  [19702039323,19701913985,19701854320]:
        #   continue
        activity_name = activity["activityName"]
        #display_text(activity)
        output_file = os.path.join(output, f"./activity_{str(activity_id)}.tcx")
        if not os.path.exists(output_file):
            print(
                f"garmin.download_activity({activity_id}, dl_fmt=garmin.ActivityDownloadFormat.TCX)"
            )
            tcx_data = garmin.download_activity(
                activity_id, dl_fmt=garmin.ActivityDownloadFormat.TCX
            )
            output_file = os.path.join(output, f"activity_{str(activity_id)}.tcx")
            with open(output_file, "wb") as fb:
                fb.write(tcx_data)
            print(f"Activity data downloaded to file {output_file}")
        # Both the variables would contain time
        # elapsed since EPOCH in float
        ti_m = os.path.getmtime(output_file)
        m_t = time.ctime(ti_m)
        if ti_m > datetime.datetime.combine(startdate, datetime.datetime.min.time()).timestamp():
            print(f"The file located at the path {output_file} was last modified at {m_t}")
            scp_activity(output_file, "jltryoen@ssh.cluster003.hosting.ovh.net:" + "~/www/data/tcx/" + output);
            #scp_activity(output_file, "trycoach@ssh.cluster003.hosting.ovh.net:" + "~/www/data/tcx/" + output);

# Init garmin
# Configure debug logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables if defined
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
DIRACTIVITIES = os.getenv("ACTIVITIES")
garmin = newgarmin(EMAIL, PASSWORD)
DAYS = os.getenv("DAYS") or "15"

if garmin:
    today = datetime.date.today()
    startdate = today - datetime.timedelta(days=int(DAYS))  # Select 15 days
    enddate = today
    download_activities(garmin, startdate, enddate, DIRACTIVITIES)
else:
    print("garmin is null")
        