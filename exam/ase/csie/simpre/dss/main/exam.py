import csv
import calendar
import requests
import json
from _datetime import datetime
from bs4 import BeautifulSoup

public_acquisition_path = "eu/ro/ase/csie/simpre/dss/files/achizitii publice.csv"
date_format = '%Y-%m-%dT%H:%M:%S'
BNR_URL = 'https://www.bnr.ro/nbrfxrates.xml'


# 1.Scrieți o funcție care citește toate achizițiile publice din anul 2015 (CSV) și returnează un dicționar cu
# totalul valorii contractelor pentru fiecare județ

def public_acquisition_into_dictionary():
    acquisition_per_county = {}
    with open(public_acquisition_path, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            publication_date = row['Data Publicare']
            publication_year = datetime.strptime(publication_date, date_format).year
            county = row['Judet']
            estimated_value = float(row['Valoare Estimata'])
            if publication_year == 2015:
                if county in acquisition_per_county.keys():
                    acquisition_per_county[county] += estimated_value
                else:
                    acquisition_per_county[county] = estimated_value
            else:
                raise Exception('The year is not 2015')
    return acquisition_per_county


# 2.Elaborați o funcție care scrie într-un fișier CSV (cu următoarele coloane: Județ, Valoare Estimată)
# valorile preluate la exercițiul 1.

def estimated_cost_per_county_to_csv():
    acquisition_cost_per_county_path = "eu/ro/ase/csie/simpre/dss/files/acquisition cost per county.csv"
    with open(acquisition_cost_per_county_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Judet", "Valoare Estimata"])
        dictionary = public_acquisition_into_dictionary()
        for key, value in dictionary.items():
            writer.writerow([key, value])


estimated_cost_per_county_to_csv()


# 3.Scrieți o funcție care exportă în formatul JSON valorile totale
# ale contractelor pe fiecare lună (se folosește câmpul Data publicare).

def sum_of_values_per_month_to_json():
    acquisition_cost_per_month_json_path = "eu/ro/ase/csie/simpre/dss/files/acquisition cost per month.json"
    acquisition_per_month = {}
    with open(public_acquisition_path, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            publication_date = row['Data Publicare']
            month = datetime.strptime(publication_date, date_format).month
            formatted_month = calendar.month_name[int(month)]
            value = float(row['Valoare Estimata'])
            if formatted_month in acquisition_per_month.keys():
                acquisition_per_month[formatted_month] += value
            else:
                acquisition_per_month[formatted_month] = value
        json_obj = json.dumps(acquisition_per_month, indent=5)
        with open(acquisition_cost_per_month_json_path, "w") as json_file:
            json_file.write(json_obj)


sum_of_values_per_month_to_json()


# 4.Scrieți o funcție care să funcționeze ca un convertor valutar dintr-o monedă la alegere în RON.
# Funcția va primi ca parametri un număr real (suma de convertit) și un string (moneda).
# Această funcție va folosi cursurile expuse de BNR din ziua curentă.


# VARIANTA 1


def convert(amount: float, currency: str):
    if not isinstance(amount, (int, float)):
        raise Exception('Amount should be a number')
    response = requests.get(BNR_URL)
    if response.status_code != 200:
        raise Exception('Server error')
    soup = BeautifulSoup(response.text, 'lxml')
    rate_object = soup.find('rate', {'currency': currency})
    if not rate_object:
        raise Exception('Unknown currency')
    return amount * float(rate_object.text)


# 5.Utilizați această funcție pentru a corecta valorile de la exercițiul 2, astfel încât valoarea să fie exprimată
# întotdeauna în RON.


def formatted_public_acquisition():
    acquisition_per_county = {}
    with open(public_acquisition_path, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            publication_date = row['Data Publicare']
            publication_year = datetime.strptime(publication_date, date_format).year
            county = row['Judet']
            if publication_year == 2015:
                if row['Moneda'] != 'RON':
                    estimated_value = convert(float(row['Valoare Estimata']), row['Moneda'])
                else:
                    estimated_value = float(row['Valoare Estimata'])
                if county in acquisition_per_county.keys():
                    acquisition_per_county[county] += estimated_value
                else:
                    acquisition_per_county[county] = estimated_value
            else:
                raise Exception('The year is not 2015')
    return acquisition_per_county


def reformatted_cost_per_county():
    formatted_public_acquisition_file = "eu/ro/ase/csie/simpre/dss/files/formatted acquisition cost per county.csv"
    with open(formatted_public_acquisition_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Judet", "Valoare Estimata"])
        dictionary = formatted_public_acquisition()
        for key, value in dictionary.items():
            writer.writerow([key, value])


reformatted_cost_per_county()

# VARIANTA 2


def bnr_exchange():
    exchange = {}
    response = requests.get(BNR_URL)
    if response.status_code != 200:
        raise Exception('Server error')
    soup = BeautifulSoup(response.text, 'lxml')
    lines = soup.find_all('rate')
    for line in lines:
        exchange[line.get('currency')] = line.text
    return exchange


def bnr_exchange_to_csv():
    public_acquisition_file = "eu/ro/ase/csie/simpre/dss/files/bnr exchange.csv"
    with open(public_acquisition_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Currency", "Value"])
        dictionary = bnr_exchange()
        for key, value in dictionary.items():
            writer.writerow([key, value])


bnr_exchange_to_csv()


def convert_from_csv(amount: float, currency: str):
    bnr_exchange_file_path = 'eu/ro/ase/csie/simpre/dss/files/bnr exchange.csv'
    if not isinstance(amount, (int, float)):
        raise Exception('Amount should be a number')
    with open(bnr_exchange_file_path, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_currency = row['Currency']
            csv_value = row['Value']
            if currency == csv_currency:
                return float(amount) * float(csv_value)


def csv_formatted_public_acquisition():
    acquisition_per_county = {}
    with open(public_acquisition_path, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            publication_date = row['Data Publicare']
            publication_year = datetime.strptime(publication_date, date_format).year
            county = row['Judet']
            if publication_year == 2015:
                if row['Moneda'] != 'RON':
                    estimated_value = convert_from_csv(float(row['Valoare Estimata']), row['Moneda'])
                else:
                    estimated_value = float(row['Valoare Estimata'])
                if county in acquisition_per_county.keys():
                    acquisition_per_county[county] += estimated_value
                else:
                    acquisition_per_county[county] = estimated_value
            else:
                raise Exception('The year is not 2015')
    return acquisition_per_county


def csv_formatted_cost_per_county():
    formatted_public_acquisition_file = "eu/ro/ase/csie/simpre/dss/files/local bnr formatted acquisition cost per " \
                                         "county.csv "
    with open(formatted_public_acquisition_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Judet", "Valoare Estimata"])
        dictionary = csv_formatted_public_acquisition()
        for key, value in dictionary.items():
            writer.writerow([key, value])


csv_formatted_cost_per_county()
