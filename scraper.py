import requests
import pandas as pd
from bs4 import BeautifulSoup

data = []

for i in range(1,49):
    print(f'On page number => {i}')
    page = requests.get(f'https://www.letsdothis.com/gb/running-events?geolocation=false&utm_source=runners_world_gb&resultsPerPage=24&page={i}&selectedLocationName=United%20Kingdom&viewportNorthEastLat=60.9&viewportNorthEastLong=2.1&viewportSouthWestLat=49.8&viewportSouthWestLong=-8.9&sort=%7B%22date%22%3A%22asc%22%7D&sortOption=date-0')
    html = BeautifulSoup(page.content, 'html.parser')

    events = html.select('.v4_ag')

    for event in events:
        page = requests.get(f'https://www.letsdothis.com{event.get("href")}')
        html = BeautifulSoup(page.content, 'html.parser')
        
        try:
            event_date = html.select('time')[0].getText()
        except:
            event_date = None
        
        try:
            event_name = html.select('.ani_ax')[0].getText()
        except:
            event_name = None
            
        try:
            distance = html.select('.ani_anm')[0].getText()
            if 'Run' in distance:
                distance = (distance.replace('Run','')).strip()
        except:
            distance = None
        
        try:
            city = html.select('.asp_asr .asp_an')[0].getText()
        except:
            city = None
        
        print([event_date, event_name, distance, city])
        data.append([event_date, event_name, distance, city])
                            
                            
df = pd.DataFrame(data)
df.columns = ['Event Date', 'Event Name', 'Distance', 'City']
df.to_excel('running_events.xlsx', index=False, header=True)
