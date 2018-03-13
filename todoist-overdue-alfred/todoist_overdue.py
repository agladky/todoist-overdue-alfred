# -*- coding: utf-8 -*-

u"""Moves all overdue tasks to today in Todoist by token API"""

import sys
import os.path

sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

import argparse
import pytz

from todoist import TodoistAPI
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse


def today_actions(todoist_api):
    try:
        overdue_items = todoist_api.query(['overdue'])
        _fail_if_contains_errors(overdue_items)
        overdue_items = overdue_items[0]['data']
        for overdue_item in overdue_items:
            item = todoist_api.items.get(overdue_item['id'])
            item_due_date = parse(item['item']['due_date_utc'])
            delta = datetime.now().replace(tzinfo=pytz.utc).date() - item_due_date.date()
            item_today_date = item_due_date + timedelta(days=delta.days)
            todoist_api.items.update(overdue_item['id'], due_date_utc=item_today_date.strftime('%Y-%m-%dT%H:%M:%S'))
        todoist_api.commit()
    except:
        print "Error in accessing API. Try to regenerate token."
        sys.exit(1)


def _fail_if_contains_errors(items):
    if isinstance(items, dict) and (items.get('error_code') == 400 or items.get('error_code') == 401):
        print "Invalid token. Set another in workflow."
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moving overdue tasks for today in todoist")
    parser.add_argument("-t", "--token", help="Todoist API token", nargs='?')
    args = parser.parse_args()

    token = args.token
    if token is None:
        print "Token is not specified. Set another in workflow."
        sys.exit(1)

    api = TodoistAPI(token)
    today_actions(api)
    print "Tasks successfully moved"
