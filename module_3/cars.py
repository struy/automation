#!/usr/bin/env python3

import json
import locale
import operator
import os
import sys

import emails
import reports


def load_data(filename):
    """Loads the contents of filename as a JSON file."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def format_car(car):
    """Given a car dictionary, returns a nicely formatted name."""
    return "{} {} ({})".format(
        car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
    """Analyzes the data, looking for maximums.

    Returns a list of lines that summarize the information.
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    max_revenue = {"revenue": 0}
    max_total_sales = {"total_sales": 0}
    popular_year = {}

    for item in data:
        # Calculate the revenue generated by this model (price * total_sales)
        # We need to convert the price from "$1234.56" to 1234.56
        item_price = locale.atof(item["price"].strip("$"))
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item
        # max sales
        if item['total_sales'] > max_total_sales["total_sales"]:
            max_total_sales = item
        car_year = item['car']['car_year']
        popular_year[car_year] = popular_year.get(
            car_year, 0)+item['total_sales']
    # most popular car_year
    max_popular_year = max(popular_year.items(), key=operator.itemgetter(1))

    summary = [
        "The {} generated the most revenue: ${}".format(
            format_car(max_revenue["car"]), max_revenue["revenue"]),
        "The {} had the most sales: {}".format(
            format_car(max_total_sales["car"]), max_total_sales["total_sales"]),
        "The most popular year was {} with {} sales.".format(
            max_popular_year[0], max_popular_year[1]),
    ]

    return summary


def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists."""
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append([item["id"], format_car(
            item["car"]), item["price"], item["total_sales"]])
    return table_data


def main(argv):
    """Process the JSON data and generate a full report out of it."""
    data = load_data("car_sales.json")
    summary = process_data(data)
    print(summary)

    table_data = cars_dict_to_table(data)
    reports.generate("/tmp/cars.pdf", "Sales summary for last month",
                     "<br/>".join(summary), table_data)

    #  send the PDF report as an email attachment
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    subject = "Sales summary for last month"
    body = "\n".join(summary)
    message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
    emails.send(message)


if __name__ == "__main__":
    main(sys.argv)


# As optional challenges, you could try some of the following functionalities:

# Sort the list of cars in the PDF by total sales.
# table_data[1:].sort(key=lambda i: i[3])


# Create a pie chart for the total sales of each car made.

# Create a bar chart showing total sales for the top 10 best selling
#  vehicles using the ReportLab Diagra library. Put the vehicle name on the X-axis
#  and total revenue (remember, price * total sales!) along the Y-axis.
