# (c) 2014 Laurent COUSTET <ed at zehome com>
# LICENSE: BSD

import json
import datetime


PROJECTS = {}


def seconds_to_human(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d hours %02d minutes" % (h, m)


def transform_date(strdate):
    return datetime.datetime.strptime(strdate, "%m/%d/%Y").date()


def sum_per_project(days, filter_year=None):
    for day in days:
        date = transform_date(day["date"])
        if filter_year and filter_year != date.year:
            continue
        for project in day["projects"]:
            p = PROJECTS.get(project["name"], {"total_time": 0})
            PROJECTS[project["name"]] = p
            p["total_time"] += project["total_seconds"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument(
        "--year", "-y", type=int, default=None,
        help="restrict to specified year only")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        data = json.loads(f.read())

    sum_per_project(data["days"], filter_year=args.year)
    project_names = [k for k in PROJECTS.keys()]
    project_names.sort()
    for project_name in project_names:
        p = PROJECTS[project_name]
        print("{}{}: {}.".format(
            project_name,
            args.year and " (%d)" % args.year or '',
            seconds_to_human(p["total_time"])))
