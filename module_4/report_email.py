#!/usr/bin/env python3
import datetime
import emails
import reports
import os


def create_paragraoh(path):
    """ Create paragraph for reports.generate_report function. """
    records = []
    for filename in os.listdir(path):
        with open(path + filename, "r") as f:
            lines_names = ["name", "weight"]
            lines = f.read().splitlines()[:2]
            record = dict(zip(lines_names, lines))
            for key, value in record.items():
                records.append(key+": "+value+"<br/>")
            records.append("<br/>")
    return "".join(records)


if __name__ == "__main__":
    # generate report
    now = datetime.datetime.now()
    # TODO Processed Update on March 11,2020
    title = "Processed Update "+now.strftime('%D')
    descriptions_path = os.getcwd() + "/supplier-data/descriptions/"
    pdf_path = "/tmp/processed.pdf"
    paragraph = create_paragraoh(descriptions_path)
    reports.generate_report(pdf_path, title, paragraph)

    # create message and send it
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
    message = emails.generate(sender, receiver, subject, body, pdf_path)
    emails.send(message)
