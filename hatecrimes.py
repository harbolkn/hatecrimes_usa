import csv
from collections import defaultdict
import json
from math import log10, floor

TOTALS = range(3,8)

YEARS = [
            '2012',
            '2011',
            '2010',
            '2008',
            '2007',
            '2006',
            '2005',
        ]

def state_populations(year):
    temp_year = year[:3]

    populations = defaultdict(int)
    with open('static/data/census_'+temp_year+'0s.csv', 'r') as census_file:
        census = csv.reader(census_file, delimiter=',', quotechar='"')

        # This needs to change
        key = census.next()

        for row in census:
            if row[0].startswith("."):
                populations[row[0][1:].lower()] = row[key.index(year)]

    return populations


def state_totals(year):
    states = defaultdict(int)

    with open('static/data/fbi_'+year+'.csv', 'r') as crimefile:
        crimes = csv.reader(crimefile, delimiter='\t', quotechar='"')

        for row in crimes:
            if row[0] and row[4]:
                for ind in TOTALS:
                    try:
                        states[row[0].split('Total')[0].rstrip().lower()] += int(row[ind].strip("'"))
                    except:
                        states[row[0].split('Total')[0].rstrip().lower()] += 0


    return states


def state_density(year):
    states = state_totals(year)
    populations = state_populations(year)

    for s in populations:
        if s in states:
            states[s] = states[s] / float(populations[s].strip(',"').replace(",", ""))
            states[s] = round(states[s],  2 - int(floor(log10(states[s]))) - 1)

    if "outlying areas" in states:
        del states["outlying areas"]

    return states


if __name__ == '__main__':
    data = {"data": {}}
    maximum = -10000
    minimum = 1

    for year in YEARS:
        data["data"][year] = dict(state_density(year))

        temp_max = max(data["data"][year].iteritems(), key=lambda a: a[1])
        temp_min = min(data["data"][year].iteritems(), key=lambda a: a[1])

        if(temp_max > maximum):
            maximum = temp_max[1]

        if(temp_min > minimum):
            minimum = temp_min[1]

    data["data"]["min"] = minimum
    data["data"]["max"] = maximum

    fp = open("static/data/dist.json", "w")
    fp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',',': ')))
