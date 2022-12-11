import time
import requests, bs4
import pandas as pd
import concurrent.futures
import os

MAX_THREADS = 8


def make_line(main_features):
    path = os.path.join(os.getcwd(), 'feats.txt')
    with open(path, 'r', encoding='utf-8') as featsFile:
        # featsFile = open(path, 'r')
        all_feats = featsFile.readlines()
        all_feats = [x.replace('\n', '') for x in all_feats]
        temp = dict()
        for feat in all_feats:
            if feat not in main_features.keys():
                temp[feat] = None
            else:
                temp[feat] = main_features[feat]

    # for idx, it in temp.items():
    #     print(idx, it)

    # featsFile.close()

    # print(temp)
    # df_temp = pd.DataFrame(temp.values(), temp.keys()).T
    # df = pd.concat([df, df_temp])

    return temp


def download_url(path):
    try:
        res = requests.get(path)
        res.raise_for_status()
        carSoup = bs4.BeautifulSoup(res.text, features="lxml")

        main_params = carSoup.find_all(class_='offer-params__item')

        features = dict()

        for main_param in main_params:
            text = main_param.find('span', class_='offer-params__label').text.strip()
            label = main_param.find('a', class_='offer-params__link')
            if label == None:
                label = main_param.find('div', class_='offer-params__value')
            label = label.text.strip()
            features[text] = label
            # print(text,':', label)

        extendend_params = carSoup.find_all("li", class_='parameter-feature-item')

        for extendend_param in extendend_params:
            features[extendend_param.text.strip()] = 1
            # print(extendend_param.text.strip())

        price = carSoup.find('span', class_='offer-price__number').text.strip().split()[:-1]
        price = "".join(price)
        features['Cena'] = price
        # print(price)

        currency = carSoup.find('span', class_='offer-price__currency').text.strip()
        features['Waluta'] = currency
        # print(currency)

        price_details = carSoup.find('span', class_='offer-price__details').text.strip()
        features['Szczegóły ceny'] = price_details
        # print(price_details)

        description = carSoup.find('div', class_='offer-description__description').text.strip()
        features['Opis'] = description
        # print(description)

        # print(features)
        features = make_line(features)

    except:
        return None

    time.sleep(0.25)

    return features


def download_cars(links):
    if len(links) > 0:
        cars = []
        threads = min(MAX_THREADS, len(links))
        features = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for link in links:
                # print(link)
                feature = executor.submit(download_url, link)
                features.append(feature)
                # cars.append(ans.result())

            for feature in features:
                result = feature.result()
                if result != None:
                    cars.append(result)
            # print(cars)
            print(len(cars))
        # executor.map(download_url, links)
        return pd.DataFrame(cars)
    # for link in links:
    #     site = download_url(link)
    #     cars.append(site)

    return pd.DataFrame()


def main(model, links):
    print(model, 'Wejscie')
    # t0 = time.time()
    df = download_cars(links)
    print(model, 'Wyjscie')

    # print('data/' + model + '.csv')
    # df.to_csv('data/' + model + '.csv')

    print('data/' + model + '.xlsx')
    df.to_excel('data/' + model + '.xlsx')

    # t1 = time.time()
    # print(f"Site {site} took {round(t1 - t0, 2)} seconds.")

# path = "https://www.otomoto.pl/oferta/tesla-model-x-tesla-x-plaid-model-2023-nowy-ID6EVI7D.html"
# main('path', [path])

# df = pd.read_csv('car.csv', index_col='Unnamed: 0')
# print(df)
# main('otomoto', [path, path2, path3, path5])

# print(df)
# df.to_csv('car1.csv')
