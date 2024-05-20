import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO
import time

class Awards:

    @staticmethod
    def mvp(season):
        start_time = time.time()  # Măsurarea timpului de început
        season = str(season)
        url = 'https://www.basketball-reference.com/awards/mvp.html'
        try:
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', id='mvp_NBA')
            df = pd.read_html(StringIO(str(table)))[0]
            df.columns = df.columns.droplevel(0)
            df = df[['Season', 'Player']]
            df['Season'] = df['Season'].apply(lambda x: x[:2] + x[-2:])
            mvp_data = df[df['Season'].str.contains(season)].iloc[0]
            end_time = time.time()  # Măsurarea timpului de sfârșit
            print(f"Execution time for MVP {season}: {end_time - start_time} seconds")
            return mvp_data['Player']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def all_star(season):
        start_time = time.time()  # Măsurarea timpului de început
        if season == 1999:
            print('No All Star game in the 1999 season')
            return None
        else:  
            try:
                url = f'https://www.basketball-reference.com/allstar/NBA_{season}.html'
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, 'html.parser')
                name_html = soup.find_all('a', string=re.compile('[a-z]'), href=re.compile('^/players/.+'), title=False)
                names = list(set(name.text for name in name_html))
                end_time = time.time()  # Măsurarea timpului de sfârșit
                print(f"Execution time for All-Star {season}: {end_time - start_time} seconds")
                return names
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

# Test functions
print(Awards.mvp(2022))
print(Awards.all_star(2022))
