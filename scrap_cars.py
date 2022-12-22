import requests, bs4
import concurrent.futures
import time
import get_advertisement
import pandas as pd
import os


MAX_THREADS = 8
path = os.path.join(os.getcwd(), 'car_models.txt')
models = open(path, 'r', encoding='utf-8').readlines()
links = []


def get_cars_in_page(path, i):

    print(i, path)

    res = requests.get(path + '?page=' + str(i))
    res.raise_for_status()
    currentPage = bs4.BeautifulSoup(res.text, features='lxml')
    carlinks = currentPage.find('main', attrs={'data-testid': 'search-results'})
    cnt = 0
    for x in carlinks.find_all('article'): # [:10]: TODO
        x = x.find('a', href=True)
        links.append(x['href'])
        # print(x['href'])


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
        lastPage = int(carSoup.find_all('a', class_='ooa-xdlax9 ekxs86z0')[-1].text)
    except Exception:
        lastPage = 1

    #lastPage = 1 TODO
    lastPage = min(lastPage, 500)

    print("Liczba podstron modelu = ", lastPage)
    threads = min(MAX_THREADS, lastPage)
    path = [path]*lastPage
    lastPage = range(1, lastPage + 1)

    links.clear()
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_cars_in_page, path, lastPage)

    get_advertisement.main(model, links)


    time.sleep(0.25)


for model in models:
    scrap_model(model)

# csv_filenames = ['data/'+ model.replace('\n', '') + '.csv' for model in models]
xlsx_filenames = ['data/'+ model.replace('\n', '') + '.xlsx' for model in models]

combined_df = []
for f in xlsx_filenames:
    print(f)
    try:
        # combined_df.append(pd.read_csv(f, low_memory=False, index_col='Unnamed: 0'))
        combined_df.append(pd.read_excel(f, index_col='Unnamed: 0'))
    except Exception:
        pass

df_all = pd.concat(combined_df, ignore_index=True)
df_all.to_excel('car.xlsx', index=False)
# df_all.to_csv('car.csv', index=False)
# pd.concat(combined_csv, ignore_index = True).to_pickle('data/car.pickle')