from mpi4py import MPI
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
            return f"MVP for {season}: {mvp_data['Player']} - Execution time: {end_time - start_time} seconds"
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def all_star(season):
        start_time = time.time()  # Măsurarea timpului de început
        if season == 1999:
            return 'No All Star game in the 1999 season'
        else:  
            try:
                url = f'https://www.basketball-reference.com/allstar/NBA_{season}.html'
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, 'html.parser')
                name_html = soup.find_all('a', string=re.compile('[a-z]'), href=re.compile('^/players/.+'), title=False)
                names = list(set(name.text for name in name_html))
                end_time = time.time()  # Măsurarea timpului de sfârșit
                return f"All-Star players for {season}: {', '.join(names)} - Execution time: {end_time - start_time} seconds"
            except Exception as e:
                return f"An error occurred: {e}"

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    seasons = [2022]  # Add more seasons if needed

    if rank < len(seasons) * 2:
        season_index = rank // 2
        if rank % 2 == 0:
            result = Awards.mvp(seasons[season_index])
        else:
            result = Awards.all_star(seasons[season_index])
        print(f"Process {rank}: {result}")

if __name__ == '__main__':
    main()
