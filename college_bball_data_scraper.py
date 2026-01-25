import pandas as pd

## INPUT THE CURRENT SEASON BELOW ##
current_season = '2025'

def scrape_ratings_url(url):
    df = pd.read_html(url)[0]
    df['Team'] = df['Team'].str.rsplit('(', n=1).str[0] #split the string once on the last "(", select the first substring
    df['Team'] = df['Team'].str[:-1] #remove last character (should be a space)
    df.set_index('Team', inplace = True)
    df = df[['Rank', 'Rating']]
    df.rename(columns={'Rating': 'Value'}, inplace = True)
    return df

def scrape_stats_url(url):
    df = pd.read_html(url)[0]
    df.set_index('Team', inplace = True)
    if(url == 'https://www.teamrankings.com/ncaa-basketball/stat/effective-field-goal-pct'):
        df = df[['Rank', current_season, 'Away']] #EFGPct is the only stat where we care about the Away value
        df.rename(columns={'Away': 'Value_AwayEFGPct'}, inplace = True)
        df['Rank_AwayEFGPct'] = df['Value_AwayEFGPct'].rank(method='min', ascending=False)
    else:
        df = df[['Rank', current_season]]
    df.rename(columns={current_season: 'Value'}, inplace = True)
    return df

# POWER RATINGS #
Predictive_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/predictive-by-other'
Neutral_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/neutral-by-other'
SoS_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/schedule-strength-by-other'
NonConSoS_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/non-conference-sos-by-other'
Luck_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/luck-by-other'
Consis_url = 'https://www.teamrankings.com/ncaa-basketball/ranking/consistency-by-other'

ratings_df = scrape_ratings_url(Predictive_url)

ratings_df = ratings_df.merge(scrape_ratings_url(Neutral_url), on=('Team'), suffixes = (None, '_Neutral'), how='outer')
ratings_df = ratings_df.merge(scrape_ratings_url(SoS_url), on=('Team'), suffixes = (None, '_SoS'), how='outer')
ratings_df = ratings_df.merge(scrape_ratings_url(NonConSoS_url), on=('Team'), suffixes = (None, '_NonConSoS'), how='outer')
ratings_df = ratings_df.merge(scrape_ratings_url(Luck_url), on=('Team'), suffixes = (None, '_Luck'), how='outer')
ratings_df = ratings_df.merge(scrape_ratings_url(Consis_url), on=('Team'), suffixes = (None, '_Consis'), how='outer')

ratings_df.rename(columns={'Rank': 'Rank_Predictive', 'Value': 'Value_Predictive'}, inplace = True) #rename based on whichever table was scraped first

# STATISTICS #
AtTR_url = 'https://www.teamrankings.com/ncaa-basketball/stat/assist--per--turnover-ratio'
oAtTR_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-assist--per--turnover-ratio'
CloseWinPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/win-pct-close-games'
EPosPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/effective-possession-ratio'
oEPosPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-effective-possession-ratio'
OEff_url = 'https://www.teamrankings.com/ncaa-basketball/stat/offensive-efficiency'
DEff_url = 'https://www.teamrankings.com/ncaa-basketball/stat/defensive-efficiency'
EFGPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/effective-field-goal-pct'
oEFGPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-effective-field-goal-pct'
FTMp100P_url = 'https://www.teamrankings.com/ncaa-basketball/stat/ftm-per-100-possessions'
oFTApP_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-free-throw-rate'
PctPtf3_url = 'https://www.teamrankings.com/ncaa-basketball/stat/percent-of-points-from-3-pointers'
_3PtPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/three-point-pct'
o3PtPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-three-point-pct'
ORPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/offensive-rebounding-pct'
DRPct_url = 'https://www.teamrankings.com/ncaa-basketball/stat/defensive-rebounding-pct'
PospG_url = 'https://www.teamrankings.com/ncaa-basketball/stat/possessions-per-game'
TOpPos_url = 'https://www.teamrankings.com/ncaa-basketball/stat/turnovers-per-possession'
oTOpPos_url = 'https://www.teamrankings.com/ncaa-basketball/stat/opponent-turnovers-per-possession'

stats_df = scrape_stats_url(AtTR_url)

stats_df = stats_df.merge(scrape_stats_url(oAtTR_url), on=('Team'), suffixes = (None, '_oAtTR'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(CloseWinPct_url), on=('Team'), suffixes = (None, '_CloseWinPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(EPosPct_url), on=('Team'), suffixes = (None, '_EPosPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(oEPosPct_url), on=('Team'), suffixes = (None, '_oEPosPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(OEff_url), on=('Team'), suffixes = (None, '_OEff'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(DEff_url), on=('Team'), suffixes = (None, '_DEff'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(EFGPct_url), on=('Team'), suffixes = (None, '_EFGPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(oEFGPct_url), on=('Team'), suffixes = (None, '_oEFGPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(FTMp100P_url), on=('Team'), suffixes = (None, '_FTMp100P'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(oFTApP_url), on=('Team'), suffixes = (None, '_oFTApP'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(PctPtf3_url), on=('Team'), suffixes = (None, '_PctPtf3'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(_3PtPct_url), on=('Team'), suffixes = (None, '_3PtPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(o3PtPct_url), on=('Team'), suffixes = (None, '_o3PtPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(ORPct_url), on=('Team'), suffixes = (None, '_ORPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(DRPct_url), on=('Team'), suffixes = (None, '_DRPct'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(PospG_url), on=('Team'), suffixes = (None, '_PospG'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(TOpPos_url), on=('Team'), suffixes = (None, '_TOpPos'), how='outer')
stats_df = stats_df.merge(scrape_stats_url(oTOpPos_url), on=('Team'), suffixes = (None, '_oTOpPos'), how='outer')

stats_df.rename(columns={'Rank': 'Rank_AtTR', 'Value': 'Value_AtTR'}, inplace = True) # rename based on whichever table was scraped first

final_df = ratings_df.merge(stats_df, on=('Team'), how='outer')
with pd.ExcelWriter('final_output/MarchMadnessRawData.xlsx') as writer:
    final_df.to_excel(writer, sheet_name = 'Data')