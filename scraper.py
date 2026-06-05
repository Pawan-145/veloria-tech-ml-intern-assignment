import csv
import time
import requests
from bs4 import BeautifulSoup

# Start from your verified match code and let Python hunt backwards automatically
START_CODE = 2598

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

match_rows = []
current_code = START_CODE

print("Starting fully automated Head-to-Head hunt.")
print("This will check codes sequentially backward until 10 India vs Australia matches are found...\n")

# Keep looping indefinitely until our dataset reaches exactly 10 rows
while len(match_rows) < 10:
    url = f"http://www.howstat.com/cricket/Statistics/Matches/MatchScorecard.asp?MatchCode={current_code}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        # If a page doesn't exist or errors out, just skip it and keep moving backward
        if res.status_code != 200:
            current_code -= 1
            continue
            
        soup = BeautifulSoup(res.text, "html.parser")
        
        team1_elem = soup.find("td", class_="ScorecardCountry2")
        team2_elem = soup.find("td", class_="ScorecardCountry1")
        
        # If it's an empty page or alternative layout, skip it
        if not team1_elem or not team2_elem:
            current_code -= 1
            continue
            
        # Clean the team text strings
        team1 = team1_elem.text.strip().split('\n')[0].split('&')[0].strip()
        team2 = team2_elem.text.strip().split('\n')[0].split('&')[0].strip()
        
        # AUTOMATIC FILTER: Match must be strictly India vs Australia
        playing_teams = [team1, team2]
        if "India" in playing_teams and "Australia" in playing_teams:
            # We found one! Extract the details
            match_date, venue, result = "N/A", "International Ground", "Match Completed"
            header_cells = soup.find_all("td", class_="ScorecardHeader")
            header_data = [cell.text.strip() for cell in header_cells]
            
            if len(header_data) >= 4:
                venue = header_data[1].replace('\n', ' ').strip()
                match_date = header_data[2].strip()
                result = header_data[3].strip()

            # Find the top batsman milestones
            top_scorer, highest_score = "N/A", 0
            player_cells = soup.find_all("td", class_="ScorecardPlayer")
            
            for cell in player_cells:
                player_name = cell.text.strip()
                row = cell.find_parent("tr")
                if row:
                    score_element = row.find("b")
                    if score_element and score_element.text.strip().isdigit():
                        runs = int(score_element.text.strip())
                        if runs > highest_score:
                            highest_score = runs
                            top_scorer = player_name
                                    
            score_text = str(highest_score) if highest_score > 0 else "N/A"

            # Save the clean row
            match_rows.append([match_date, team1, team2, venue, result, top_scorer, score_text])
            
            print(f"[MATCH {len(match_rows)}/10] Found at Code {current_code}: {team1} vs {team2} ({match_date})")
            
            # Politeness delay so we don't spam the server
            time.sleep(1)
        else:
            # This prints a minor log so you know the script is working through the background pages
            if current_code % 10 == 0:
                print(f"...checking code {current_code} (Other match: {team1} vs {team2})...")

    except Exception as e:
        # If a single page hits a network snag, ignore it and keep moving backward
        pass
        
    # Subtract 1 from the code to check the previous match on the next loop iteration
    current_code -= 1

# Define file headers
csv_headers = ["Match Date", "Team 1 Name", "Team 2 Name", "Venue", "Match Result", "Top Scorer", "Score"]

# Automatically compile rows to CSV format
with open("match_data2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(match_rows)

print("\nSuccess! The scraper tracked backwards completely on its own.")
print("Check 'match_data2.csv' for your perfect 10-row head-to-head dataset.")