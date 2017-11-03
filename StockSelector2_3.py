# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2

@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, min_item=10):
    """
    均线选股法
    :param stock_list:
    :param kline_type:
    :param avg:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except:
            continue
        if kline.shape[0] < min_item:
            continue
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        vb = StockIndicator.vibration(kline)
        if sma5[x_position] < sma10[x_position] < sma20[x_position]:
            if close[x_position] > sma5[x_position]:
                if vb[x_position] > 5:
                    print(stock)
                    result.append(stock)

    return result


if __name__ == '__main__':
    result={}
    # for x in range(-10, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_week)
    #     print(stock_list)
    #
    #     for stock in stock_list:
    #         result[stock] = result.get(stock, 0) + 1
    #
    # with open('{}/{}'.format(StockConfig.path_stock, 'wsma10'), 'w', encoding='utf-8') as f:
    #     for key in result:
    #         if result[key] >= 7:
    #             f.write("{},{}\n".format(key.stock_code, key.stock_name))
    #
    # print(sorted(result.items(), key=lambda d: d[1], reverse=True))
    date = '2017-10-09'
    position = StockIndicator.position(date, '000001')
    stock_list = select(StockIO.get_stock('sza'), x_position=-1)
    stock_list2 = select(StockIO.get_stock('sha'), x_position=-1)
    stock_list = stock_list + stock_list2
    print(len(stock_list))
    with open('C:/Users/panha/Desktop/xgfx/1002.txt', mode='w', encoding='utf-8') as f:
        for key in stock_list:
            f.write("{}\n".format(key.stock_code))



