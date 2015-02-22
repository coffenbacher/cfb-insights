import requests
import os
import json

NFL = ['San Francisco 49ers','Chicago Bears','Cincinnati Bengals','Buffalo Bills','Denver Broncos','Cleveland Browns','Tampa Bay Buccaneers','Arizona Cardinals','San Diego Chargers','Kansas City Chiefs','Indianapolis Colts','Dallas Cowboys','Miami Dolphins','Philadelphia Eagles','Atlanta Falcons','New York Giants','Jacksonville Jaguars','New York Jets','Detroit Lions','Green Bay Packers','Carolina Panthers','New England Patriots','Oakland Raiders','St.Louis Rams','Baltimore Ravens','Washington Redskins','New Orlean Saints','Seattle Seahawks','Pittsburgh Steelers','Houston Texans','Tennesse Titans','Minnesota Viking',]

def get_coach_data():
    url = 'https://rawgit.com/coffenbacher/cfb-data/master/automated/wiki/coach_tenure/coach_tenure.json'
    return json.loads(requests.get(url).content)

def get_metrics(data, humanize=True):
    m = {}
    
    # This is an approximation
    m['coverage'] = { 
        'value': calculate_coverage(data, humanize=humanize),
        'description': 'Coverage: HC, DC, OC for all 128 current FBS teams over past 75 years'
    }
    m['schools'] = len(get_schools())
    m['coaches'] = len(get_coaches(data))
    m['entries'] = len(data)
    return m

def get_schools():
    url = 'https://rawgit.com/coffenbacher/cfb-data/master/automated/wiki/team/team.json'
    known = json.loads(requests.get(url).content)
    schools = sorted(list(set([e['team'] for e in known])))
    schools.append('Unknown')
    schools.append('HS')
    schools.append('NFL')
    schools.append('Lower division CFB')
    return schools

def lookup_school(team, schools):
    try:
        return schools.index(team)
    except:
        if 'HS' in team:
            return schools.index('HS')
        elif team in NFL:
            return schools.index('NFL')
        elif 'CC' in team or 'State' in team or True:
            return schools.index('Lower division CFB')
        return schools.index('Unknown')    
    
def get_coaches(data):
    return sorted(list(set([e['name'] for e in data])))

def get_tenures(data):
    tenures = {coach: [] for coach in get_coaches(data)}
    for e in data:
        tenures[e['name']].append((e['team'], int(e['startyear']), int(e['endyear'])))
    return tenures
    
    
def get_coach_matrix(data):
    matrix = []
    schools = get_schools()
    tenures = get_tenures(data)
    
    for s in schools:
        matrix.append([0 for s in schools])
        
    for coach, tenure_list in tenures.items():
        tenure_list = sorted(tenure_list, key=lambda x: x[1])
        for i in range(len(tenure_list)):
            if len(tenure_list) > i + 1:
                origin = lookup_school(tenure_list[i][0], schools)
                destination = lookup_school(tenure_list[i+1][0], schools)
                matrix[origin][destination] += 1

    return matrix

def calculate_required_years_of_data():
    # temporary assume 128 teams for 75 years with 3 major positions
    return float(128 * 75 * 3)
    
def calculate_coverage(data, humanize=False):
    required = calculate_required_years_of_data()
    acquired = 0.0
    current_year = 2015
    for e in data:
        end = e['endyear'] if e['endyear'] else current_year
        if e['position'] in ['OC', 'DC', 'HC']: # focus on major positions
            acquired += float(end) - float(e['startyear'])
    if humanize:
        return '%s%%' % round((acquired / required) * 100, 2)
    return acquired / required

if __name__ == "__main__":
    data = get_coach_data()
    matrix = get_coach_matrix(data)