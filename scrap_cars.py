import requests, bs4
import concurrent.futures
import time
import get_advertisement
import pandas as pd


MAX_THREADS = 8

models = open('car_models.txt').readlines()
links = []


def get_cars_in_page(path, i):

    print(i, path)

    res = requests.get(path + '?page=' + str(i))
    res.raise_for_status()
    currentPage = bs4.BeautifulSoup(res.text, features='lxml')
    carlinks = currentPage.find_all('a', class_='offer-title__link', href=True)
    cnt = 0
    for x in carlinks:
        links.append(x['href'])


def scrap_model(model):
    model = model.replace('\n', '')
    path = 'https://www.otomoto.pl/osobowe/' + model
    print(path)
    try:
        res = requests.get(path)
        res.raise_for_status()

        carSoup = bs4.BeautifulSoup(res.text, features="lxml")
    except Exception:
        pass

    try:
        lastPage = int(carSoup.select('.page')[-1].text)
    except Exception:
        lastPage = 1


    threads = min(MAX_THREADS, lastPage)
    path = [path]*lastPage
    lastPage = range(1, lastPage + 1)

    links.clear()
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_cars_in_page, path, lastPage)

    get_advertisement.main(model, links)


    time.sleep(0.25)


# for model in models:
#     scrap_model(model)

filenames = ['data/'+ model.replace('\n', '') + '.csv' for model in models]

combined_csv = []
for f in filenames:
    print(f)
    try:
        combined_csv.append(pd.read_csv(f, low_memory=False))
    except Exception:
        pass
pd.concat(combined_csv).to_csv('car.csv')