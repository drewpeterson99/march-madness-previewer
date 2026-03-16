# March Madness Previewer

## Python File Purpose

The `college_bball_data_scraper.py` script is designed to collect comprehensive college basketball statistics and power ratings from [TeamRankings.com](https://www.teamrankings.com) for March Madness analysis. It automatically scrapes data for all NCAA Division I teams and consolidates it into a single Excel file for easy analysis and bracket predictions.

## What It Does

The script collects two main categories of data:

### Tempo-Free Power Ratings (as calculated by TeamRankings.com)
- **Predictive Rating**: Overall/net team strength
- **Neutral Rating**: Rating in neutral site games
- **Opponent Rating**: Rating/strength of opponents faced
- **Non-Conference Opponent Rating**: Strength of non-conference opponents
- **Luck Rating**: How fortunate/unfortunate a team has been relative to the model's prediction (i.e. the residual)
- **2H Rating**: Rating in the second half
- **Last 10 Rating**: Rating in the team's most recent 10 games played

### Statistics
The script collects 22 different statistics for each team:
- Points Per Game (and opponent's)
- Free Throw %
- Free Throw Rate (and opponent's)
- Floor % (and opponent's)
- Assist-to-Turnover Ratio (and opponent's)
- Close Game Win Percentage
- Offensive & Defensive Efficiency
- Effective FG % (and opponent's)
- Away Effective FG %
- % of Points from 3
- 3 Point % (and opponent's)
- Offensive & Defensive Rebounding %
- Pace (Possessions per Game)
- Turnover % (and opponent's)

Note that the traditional "Four Factors" of basketball team performance that are used to build predictive models such as KenPom are eFG%, TO%, OReb% and FTRate as outlined [here](https://kenpom.com/blog/four-factors/)

## How It Works

1. **Data Collection**: The script uses pandas to read HTML tables directly from TeamRankings.com URLs
2. **Data Processing**: Team names are cleaned (removing conference abbreviations in parentheses) and data is standardized
3. **Data Merging**: All ratings and statistics are merged into a single DataFrame with teams as the index
4. **Output**: The consolidated data is exported to an Excel file (`final_output/AggregatedTeamData.xlsx`)

## Output Format

The Excel file contains:
- **Team names** as the index (row labels)
- **Rank columns**: Ranking for each metric (e.g., `Rank_EFG%`, `Rank_ORb%`)
- **Value columns**: Actual values for each metric (e.g., `Value_EFG%`, `Value_ORb%`)

## Usage

1. **Update the Season**: Before running, update the `current_season` variable at the top of the script (currently set to '2025')

2. **Run the Script in the Command Line**:
   ```bash
   py college_bball_data_scraper.py
   ```

3. **Output**: The script will generate `final_output/AggregatedTeamData.xlsx` containing all the scraped data in a single sheet named "Data"

4. **Final March Madness Preview**: Paste the script's output into the "TeamRankings Data" tab of the `final_output/March Madness Preview` file and follow the instructions in the file's README

## Requirements

- Python 3.x
- pandas
- openpyxl (for Excel file writing)
- lxml or html5lib (for HTML parsing)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Other Notes

- The script requires an active internet connection to scrape data from TeamRankings.com
- Data is scraped in real-time, so results will reflect the most current statistics available
- The `final_output/` directory must exist before running the script (or the script will need to be modified to create it)