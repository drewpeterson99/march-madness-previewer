import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context # Global fix to bypass certificate verification

##################### INPUTS #####################
current_season = '2025' # should be the year the season began, but verify on the TeamRankings website
base_url = 'https://www.teamrankings.com/ncaa-basketball'
stats_url_path = '/stat'
ratings_url_path = '/ranking'

stats_urls = {
    'PPG':'/points-per-game',
    'OppPPG':'/opponent-points-per-game',
    'FT%':'/free-throw-pct',
    'FTRate':'/fta-per-fga',
    'OppFTRate':'/opponent-fta-per-fga',
    'Floor%':'/floor-percentage',
    'OppFloor%':'/opponent-floor-percentage',
    'APerTO':'/assist--per--turnover-ratio',
    'OppAPerTO':'/opponent-assist--per--turnover-ratio',
    'CloseWin%':'/win-pct-close-games',
    'OEff':'/offensive-efficiency',
    'DEff':'/defensive-efficiency',
    'EFG%':'/effective-field-goal-pct',
    'OppEFG%':'/opponent-effective-field-goal-pct',
    '%PtsFrom3':'/percent-of-points-from-3-pointers',
    '3Pt%':'/three-point-pct',
    'Opp3Pt%':'/opponent-three-point-pct',
    'ORb%':'/offensive-rebounding-pct',
    'DRb%':'/defensive-rebounding-pct',
    'Pace':'/possessions-per-game',
    'TO%':'/turnovers-per-possession',
    'OppTO%':'/opponent-turnovers-per-possession'
}

stats_to_include_away_values = ['EFG%']

ratings_urls = {
    'PredictRating':'/predictive-by-other',
    'NeutralRating':'/neutral-by-other',
    'OppRating':'/schedule-strength-by-other',
    'OppRatingNonCon':'/non-conference-sos-by-other',
    'LuckRating':'/luck-by-other',
    '2HRating':'/second-half-by-other',
    'Last10Rating':'/last-10-games-by-other'
}
##################################################

def validate_num_types(value:str):
    """
    Convert a percentage value to a decimal.
    If the value contains a '%' sign, strips it and divides by 100.
    Otherwise, converts to float as-is.
    
    Examples:
        "54.6%" -> 0.546
        "12.5" -> 12.5
    """
    value_str = str(value)
    if '--' in value_str:
        return 'n/a'
    elif '%' in value_str:
        return float(value_str.replace('%', '')) / 100
    else:
        return float(value)

def scrape_ratings_url(stat_name:str, url:str):
    print('Scraping ' + url)
    df = pd.read_html(url)[0]
    df['Team'] = df['Team'].str.rsplit('(', n=1).str[0] # split the string once on the last "(", select the first substring
    df['Team'] = df['Team'].str[:-1] # remove last character (should be a space)
    df.set_index('Team', inplace = True)
    df = df[['Rank', 'Rating']]
    df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    df['Rating'] = df['Rating'].apply(validate_num_types)

    suffix = '_' + stat_name
    df = df.rename(columns={'Rank':('Rank'+suffix), 'Rating':('Value'+suffix)})
    return df

def scrape_stats_url(stat_name:str, url:str):
    print('Scraping ' + url)
    df = pd.read_html(url)[0]
    df.set_index('Team', inplace = True)
    if(stat_name in stats_to_include_away_values):
        df = df[['Rank', current_season, 'Away']]
        df['Away'] = df['Away'].apply(validate_num_types)
        df = df.rename(columns={'Away':('Value_Away'+stat_name)})
        df[('Rank_Away'+stat_name)] = df[('Value_Away'+stat_name)].rank(method='min', ascending=False)
    else:
        df = df[['Rank', current_season]]
    df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    df[current_season] = df[current_season].apply(validate_num_types)

    suffix = '_' + stat_name
    df = df.rename(columns={'Rank':('Rank'+suffix), current_season:('Value'+suffix)})
    return df

# POWER RATINGS #
ratings_df = pd.DataFrame()
for key, value in ratings_urls.items():
    full_url = base_url + ratings_url_path + value
    if ratings_df.empty:
        ratings_df = scrape_ratings_url(key, full_url)
    else:
        ratings_df = ratings_df.merge(scrape_ratings_url(key, full_url), on=('Team'), how='outer')

# STATISTICS #
stats_df = pd.DataFrame()
for key, value in stats_urls.items():
    full_url = base_url + stats_url_path + value
    if stats_df.empty:
        stats_df = scrape_stats_url(key, full_url)
    else:
        stats_df = stats_df.merge(scrape_stats_url(key, full_url), on=('Team'), how='outer')

final_df = ratings_df.merge(stats_df, on=('Team'), how='outer')
final_df = final_df.sort_values(by='Rank_PredictRating', ascending=True)
with pd.ExcelWriter('final_output/AggregatedTeamData.xlsx') as writer:
    final_df.to_excel(writer, sheet_name = 'Data')