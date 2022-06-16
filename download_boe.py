from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests


def get_BOE_summary_day(my_year, my_id):
    # Build URL for BOE summary
    url = 'https://www.boe.es/diario_boe/xml.php?id=BOE-S-{}-{}'.format(my_year, my_id)
    # Make request
    xml = requests.get(url).text
    xml = BeautifulSoup(xml, 'xml')
    # Get sections from the summary
    my_BOE_summary_day = []
    for seccion in xml.find_all('seccion'):
        # Get departments from the seccion
        for departamento in seccion.find_all('departamento'):
            # Get items from the department
            for item in departamento.find_all('item'):
                # Save useful values
                my_register = {
                    'AÑO': xml.find('anno').get_text(),
                    'FECHA': xml.find('fecha').get_text(),
                    'SECCION': seccion['nombre'],
                    'DEPARTAMENTO': departamento['nombre'],
                    'ID': item['id'],
                    'TITULO': item.find('titulo').get_text(),
                    'URL': item.find('urlPdf').get_text(),
                    'PAGINAS': item.find('urlPdf')['numPag']
                }
                # Add to list
                my_BOE_summary_day.append(my_register)
    # Consolidate the summary per day
    my_BOE_summary_day = pd.DataFrame(my_BOE_summary_day)
    return my_BOE_summary_day


def get_BOE_summary_year(my_year):
    my_BOE_summary_year = []
    for my_id in range(366):
        try:
            # Get BOE summary per day
            my_BOE_summary_day = get_BOE_summary_day(my_year, my_id)
            # Add to list
            my_BOE_summary_year.append(my_BOE_summary_day)
        except:
            continue
    # Consolidate the summary per year
    my_BOE_summary_year = pd.concat(my_BOE_summary_year, ignore_index=True)
    return my_BOE_summary_year


def get_BOE_summary_years(my_year_start, my_year_end):
    for my_year in range(my_year_start, my_year_end + 1):
        # Log
        print('{} start - {}'.format(my_year, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # Get
        my_BOE_summary_year = get_BOE_summary_year(my_year)
        # Save into csv
        my_BOE_summary_year.to_csv('data/{}.csv'.format(my_year), index=False)
        # Log
        print('{} end   - {}'.format(my_year, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

get_BOE_summary_years(1977, 2021)