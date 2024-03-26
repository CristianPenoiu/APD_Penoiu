import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO
from multiprocessing import Process, Queue
import time

class Awards:

    @staticmethod
    def mvp(season):
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
            return mvp_data['Player']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def all_star(season):
        if season == 1999:
            return None
        else:  
            try:
                url = f'https://www.basketball-reference.com/allstar/NBA_{season}.html'
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, 'html.parser')
                name_html = soup.find_all('a', string=re.compile('[a-z]'), href=re.compile('^/players/.+'), title=False) 
                names = list(set(name.text for name in name_html))
                return names
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

def process_mvp(season, output):
    start_time = time.time()  # Măsurarea timpului de început
    player = Awards.mvp(season)
    end_time = time.time()  # Măsurarea timpului de sfârșit
    output.put(f"MVP for {season}: {player} - Execution time: {end_time - start_time} seconds")

    with open('mvp_results.txt', 'a') as f:
        f.write(f"MVP for {season}: {player}\n")

def process_all_star(season, output):
    start_time = time.time()  # Măsurarea timpului de început
    players = Awards.all_star(season)
    end_time = time.time()  # Măsurarea timpului de sfârșit
    output.put(f"All-Star players for {season}:")
    if players:
        for player in players:
            output.put(player)
        df = pd.DataFrame({'Players': players})
        df.to_excel(f'all_star_{season}.xlsx', index=False)

    output.put(f"Execution time for All-Star {season}: {end_time - start_time} seconds")


if __name__ == '__main__':
    seasons = [2010, 2013, 2019]  # putem sa mai punem sezoane
    processes = []
    output = Queue()
    
    start_time_all = time.time() 
    
    for season in seasons:
        p1 = Process(target=process_mvp, args=(season, output))
        p2 = Process(target=process_all_star, args=(season, output))
        p1.start()
        p2.start()
        processes.extend([p1, p2])

        p1.join()
        p2.join()

    end_time_all = time.time()

    print("Total execution time for all processes: ", end_time_all - start_time_all)

    while not output.empty():
        print(output.get())

