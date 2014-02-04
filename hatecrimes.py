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

def populations(year):
    temp_year = year[:3]

    population = defaultdict(int)
    with open('static/data/census_'+temp_year+'0s.csv', 'r') as census_file:
        census = csv.reader(census_file, delimiter=',', quotechar='"')

        # This needs to change
        key = census.next()

        for row in census:
            if row[0].startswith("."):
                population[row[0][1:].lower()] = int(row[key.index(year)].replace(',', ''))

    return population


def crimes(year):
    crimes = defaultdict(int)

    with open('static/data/fbi_'+year+'.csv', 'r') as crimefile:
        c_file = csv.reader(crimefile, delimiter='\t', quotechar='"')

        for i, row in enumerate(c_file):
            state_ind=0; total_ind=4
            if i > 1:
                row = row[0].strip("'").split(",")
                crimes[row[state_ind].lower()] = int(row[total_ind])

    return crimes

def coverages(year):
    coverage = defaultdict(int)

    with open('static/data/fbi_'+year+'.csv', 'r') as crimefile:
        c_file = csv.reader(crimefile, delimiter='\t', quotechar='"')

        for i, row in enumerate(c_file):
            state_ind=0; cov_ind=2;

            if i > 1:
                row = row[0].strip("'").split(",")

                try:
                    coverage[row[state_ind].lower()] = int(row[cov_ind])
                except:
                    coverage[row[state_ind].lower()] = 0

    return coverage

def state_density(year):
    crime = crimes(year)
    coverage = coverages(year)
    population = populations(year)

    for s in population:
        if s in crime and s in coverage:
            if coverage[s] != 0:
                crime[s] = round((float(population[s])/ coverage[s])*crime[s]) / population[s]
            else:
                crime[s] = crime[s] / float(population[s])

##            crime[s] = round(crime[s],  2 - int(floor(log10(crime[s]))) - 1)

    return crime


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
