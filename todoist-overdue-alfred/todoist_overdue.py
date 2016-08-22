# -*- coding: utf-8 -*-
import sys
from todoist import TodoistAPI
from datetime import datetime
from datetime import timedelta
from os.path import expanduser
from dateutil.parser import parse
import argparse
import pytz
import ConfigParser


def today_actions(todoist_api):
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


def _fail_if_contains_errors(items):
    if isinstance(items, dict) and items.get('error_code') == 400:
        sys.exit("Access for the current token is denied. Please set another token with -t argument.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moving overdue tasks for today in todoist")
    parser.add_argument("-t", "--token", help="Todoist API token")
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read(expanduser('~') + "/.todoist")

    token = args.token
    if token is None:
        token = config.get('Global', 'TokenAPI') if config.has_option('Global', 'TokenAPI') else sys.exit(
            "Please, set a todoist token with -t argument")
    else:
        if not config.has_section('Global'):
            config.add_section('Global')
        config.set('Global', 'TokenAPI', token)
        with open(expanduser('~') + "/.todoist", 'w') as configfile:
            config.write(configfile)

    api = TodoistAPI(token)
    today_actions(api)
    print("Tasks successfully moved")
