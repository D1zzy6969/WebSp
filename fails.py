import requests
from bs4 import BeautifulSoup

class Movie:
    def __init__(self, rank, title, weekend_gross, total_gross, weeks, distributor):
        self.rank = rank
        self.title = title
        self.weekend_gross = weekend_gross
        self.total_gross = total_gross
        self.weeks = weeks
        self.distributor = distributor

    def __str__(self):
        return f"{self.rank:<5} {self.title:<40} {self.weekend_gross:<15} {self.total_gross:<15} {self.weeks:<6} {self.distributor}"

url = "https://www.the-numbers.com/weekend-box-office-chart"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Something failed: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all("table")
if len(tables) < 2:
    print("Not enough tables found.")
    exit()

table = tables[1]
rows = table.find_all("tr")[1:]  
movies = []

rank = 1
for row in rows:
    cols = row.find_all("td")
    if len(cols) < 11:
        continue

    title = cols[2].text.strip()
    distributor = cols[3].text.strip()
    weekend_gross = cols[4].text.strip()
    total_gross = cols[9].text.strip()
    weeks = cols[10].text.strip()

    movie = Movie(rank, title, weekend_gross, total_gross, weeks, distributor)
    movies.append(movie)

    rank += 1
    if rank > 10:
        break

print(f"{'Rank':<5} {'Movie':<40} {'Weekend Gross':<15} {'Total Gross':<15} {'Weeks':<6} {'Distributor'}")
print("-" * 102)
for movie in movies:
    print(movie)
