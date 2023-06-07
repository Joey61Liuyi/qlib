# -*- coding: utf-8 -*-
# @Time    : 2023/6/6 20:22
# @Author  : LIU YI


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':


    price_train = pd.read_csv('./train/price_train.csv')
    price_test = pd.read_csv('./test/price_test.csv')
    price = pd.concat([price_train, price_test], ignore_index=True)
    del price_train
    del price_test
    scaler = StandardScaler()
    factor_file = {}
    factor_names = ['factor1', 'factor2', 'factor3', 'factor4', 'factor5']
    for factor in factor_names:
        train_file  = pd.read_csv('./train/'+ factor+'_train.csv')
        test_file = pd.read_csv('./test/'+ factor+'_test.csv')
        factor_file[factor] = pd.concat([train_file, test_file], ignore_index=True)
        factor_file[factor] = factor_file[factor].rename(columns = {'Unnamed: 0': 'date'})
        df_without_date = factor_file[factor].iloc[:, 1:]
        df_standardized = pd.DataFrame(scaler.fit_transform(df_without_date), columns=factor_file[factor].columns[1:], index=factor_file[factor].index)
        df_combined = pd.concat([factor_file[factor][['date']], df_standardized], axis=1)
        factor_file[factor] = df_combined
        del train_file
        del test_file


    column_name = {
        'TRADE_DT': 'date',
        'S_DQ_ADJCLOSE': 'close',
        'S_DQ_ADJHIGH': 'high',
        'S_DQ_ADJLOW': 'low',
        'S_DQ_ADJOPEN': 'open',
        'S_DQ_AMOUNT': 'amount',
        'S_DQ_VOLUME': 'volume',
        'S_INFO_WINDCODE': 'stock'
    }
    price = price.rename(columns=column_name)
    price['date'] = pd.to_datetime(price['date'], format='%Y%m%d')
    price['date'] = price['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    value_counts = dict(price['stock'].value_counts())
    total_dates = max(value_counts.values())
    to_be_deleted = []

    for one in value_counts:
        if value_counts[one] != total_dates:
            to_be_deleted.append(one)
    for one in to_be_deleted:
        del value_counts[one]

    object_stocks = list(value_counts.keys())


    for stock in object_stocks:
        if stock in factor_file['factor1'].columns:
            stock_data = price[price['stock'] == stock]
            stock_data = stock_data.drop('stock', axis = 1)
            for factor in factor_file:
                factor_data = factor_file[factor]
                tep = factor_data[['date', stock]]
                tep = tep.rename(columns = {stock: factor})
                stock_data = pd.merge(stock_data, tep, on='date')
            stock_data.to_csv('./processed_std_data/{}.csv'.format(stock), index = False)
            print(str(object_stocks.index(stock))+'/'+str(len(object_stocks)))
        else:
            print(str(object_stocks.index(stock)) + '/' + str(len(object_stocks)))

