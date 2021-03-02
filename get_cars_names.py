import requests, bs4
import unidecode

path = 'https://www.otomoto.pl/osobowe/acura/'

res = requests.get(path)
res.raise_for_status()

carSoup = bs4.BeautifulSoup(res.text, features="lxml")

section = carSoup.find('select', title="Marka pojazdu")

models = section.find_all('option')
car_model = []

car_exceptions = {'warszawa':'marka_warszawa'}

for model in models[1:]:
    name = model.text.strip().split()[:-1]
    name = "-".join(name).lower()
    name = unidecode.unidecode(name)
    if name in car_exceptions:
        name = car_exceptions[name]
    print(name)
    car_model.append(name)

File_car_names = open('car_models.txt', 'w')
File_car_names.writelines(car + '\n' for car in car_model)
