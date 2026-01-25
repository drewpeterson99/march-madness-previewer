# March Madness Previewer

## Python File Purpose

The `college_bball_data_scraper.py` script is designed to collect comprehensive college basketball statistics and power ratings from [TeamRankings.com](https://www.teamrankings.com) for March Madness analysis. It automatically scrapes data for all NCAA Division I teams and consolidates it into a single Excel file for easy analysis and bracket predictions.

## What It Does

The script collects two main categories of data:

### Power Ratings
- **Predictive Rating**: Overall team strength prediction
- **Neutral Rating**: Performance in neutral site games
- **Schedule Strength (SoS)**: Difficulty of opponents faced
- **Non-Conference Schedule Strength**: Strength of non-conference opponents
- **Luck**: How fortunate/unfortunate a team has been
- **Consistency**: How consistent a team's performance has been

### Statistics
The script collects 17 different statistical categories for each team:
- Assist-to-Turnover Ratio (and opponent)
- Close Game Win Percentage
- Effective Possession Ratio (and opponent)
- Offensive/Defensive Efficiency
- Effective Field Goal Percentage (including away games)
- Free Throw metrics
- Three-Point Percentage (and opponent)
- Offensive/Defensive Rebounding Percentage
- Possessions per Game
- Turnovers per Possession (and opponent)

## How It Works

1. **Data Collection**: The script uses pandas to read HTML tables directly from TeamRankings.com URLs
2. **Data Processing**: Team names are cleaned (removing conference abbreviations in parentheses) and data is standardized
3. **Data Merging**: All ratings and statistics are merged into a single DataFrame with teams as the index
4. **Output**: The consolidated data is exported to an Excel file (`final_output/MarchMadnessRawData.xlsx`)

## Output Format

The Excel file contains:
- **Team names** as the index (row labels)
- **Rank columns**: Ranking for each metric (e.g., `Rank_Predictive`, `Rank_AtTR`)
- **Value columns**: Actual values for each metric (e.g., `Value_Predictive`, `Value_AtTR`)
- **Special columns**: `Value_AwayEFGPct` and `Rank_AwayEFGPct` for away effective field goal percentage

## Usage

1. **Update the Season**: Before running, update the `current_season` variable at the top of the script (currently set to '2025')

2. **Run the Script in the Command Line**:
   ```bash
   python college_bball_data_scraper.py
   ```

3. **Output**: The script will generate `final_output/MarchMadnessRawData.xlsx` containing all the scraped data in a single sheet named "Data"

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
