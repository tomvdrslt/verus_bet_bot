import argparse
import shin
import requests


# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()

sport = 'basketball_nba'
apiKey = '33567d43ad51625bd87ffa62dd57c6fe'
regions = 'us'
markets = 'h2h'
date = '2021-10-10T12:15:00Z'


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or '33567d43ad51625bd87ffa62dd57c6fe'

SPORT = 'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
#     'api_key': API_KEY
# })
#
#
# if sports_response.status_code != 200:
#     print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
#
# else:
#     print('List of in season sports:', sports_response.json())



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#/v4/sports/{SPORT}/odds-history/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}&date={DATE}
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    # 'sport': SPORT,
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
    # 'date': DATE,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

odds_dictionary = odds_json

x = 0
y = 0
sport_book_name = 'mybookieag'
print(odds_dictionary)
while x < len(odds_dictionary):

    while(odds_dictionary[x]['bookmakers'][y]['key'] != 'gtbets'):
        y+=1

    print("============")
    team_1 = str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['name'])
    team_2 = str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['name'])
    odds_1 = odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['price']
    odds_2 = odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['price']
    shin_moneyline_odds_1 = shin.calculate_implied_probabilities([odds_1, odds_2])['implied_probabilities'][0]
    shin_moneyline_odds_2 = shin.calculate_implied_probabilities([odds_1, odds_2])['implied_probabilities'][1]

    print("Bookmaker: " + str(odds_dictionary[x]['bookmakers'][y]['key']))
    print(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['name'])
    print("Decimal Odds: " + str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['price']))
    print("Shin Adjusted Odds: " + str(shin_moneyline_odds_1))
    print("VS")
    print(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['name'])
    print("Decimal Odds: " + str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['price']))
    print("Shin Adjusted Odds: " + str(shin_moneyline_odds_2))

    team_1 = str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['name'])
    team_2 = str(odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['name'])
    odds_1 = odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][0]['price']
    odds_2 = odds_dictionary[x]['bookmakers'][y]['markets'][0]['outcomes'][1]['price']
    shin_moneyline_odds_1 = shin.calculate_implied_probabilities([odds_1, odds_2])['implied_probabilities'][0]
    shin_moneyline_odds_2 = shin.calculate_implied_probabilities([odds_1, odds_2])['implied_probabilities'][1]

    y = 0
    x += 1

