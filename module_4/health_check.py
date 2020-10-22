#!/usr/bin/env python3

import psutil
import shutil
import os

import emails


subjects = {
    "CPU": "Error - CPU usage is over 80%",
    "DISK": "Error - Available disk space is less than 20%",
    "RAM": "Error - Available memory is less than 500MB",
    "NETWORK": "Error - localhost cannot be resolved to 127.0.0.1"
}


def check_system():
    # Report an error if CPU usage is over 80%
    if psutil.cpu_percent(60) > 80:
        send_email(subjects['CPU'])
    # Report an error if available disk space is lower than 20%
    if psutil.disk_usage('/').percent > 80:
        send_email(subjects['DISK'])
    # Report an error if available memory is less than 500MB
    if psutil.virtual_memory().free < 524288000:  # 500 x 1024 x 1024 (500MB)
        send_email(subjects['RAM'])
    # Report an error if the hostname "localhost" cannot be resolved to "127.0.0.1"
    if psutil.net_if_addrs()["lo"][0].address != '127.0.0.1':
        send_email(subjects['NETWORK'])


def send_email(subject):
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    body = "Please check your system and resolve the issue as soon as possible."
    message = emails.generate_error_report(
        sender, receiver, subject, body)
    emails.send(message)


if __name__ == "__main__":
    check_system()
