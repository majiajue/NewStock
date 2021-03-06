# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2
import datetime
import time

@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, w_x_position= -1, kline_type=StockConfig.kline_type_week, min_item=80):
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
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < min_item:
            continue

        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        low = kline[:, 4].astype(np.float)
        sma5, sma10, sma20, sma30, sma60= StockIndicator.sma(kline, 5, 10, 20, 30, 60)
        cjl = StockIndicator.cjl(kline)
        add = False
        if close[x_position] > sma5[x_position] > sma10[x_position]:
                #and close[x_position] > sma20[x_position] and sma5[x_position] > sma20[x_position]
            if close[x_position] > np.max(close[x_position - 10: x_position]):
                add = False
                # 趋势
                count = 0
                while count < 4:
                    if StockFilter2.is_jx(sma5, sma10, x_position - count):

                        add = True
                        break
                    count += 1


        if add:
            max_exceed = 5
            while close[x_position] > np.max(close[x_position - max_exceed : x_position]):
                max_exceed+=1
                if max_exceed > 200:
                    break

            stock.max_exceed=max_exceed
        if add:
            print(stock)
            result.append(stock)

    return result


def get_stock_list(x_position):
    stock_list = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    stock_list += select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    # stock_list = []
    #
    # stock_list1 = select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    # stock_list2 = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    # for x in stock_list1:
    #     if x not in stock_list:
    #         stock_list.append(x)
    # for x in stock_list2:
    #     if x not in stock_list:
    #         stock_list.append(x)
    #
    return stock_list


def delete_invalid_record():
    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code = data[0]
                target_sma = 0 if data[2].strip() == '' else int(data[2])
                target_price = 0 if data[3].strip() == '' else float(data[3])
                kline = StockIO.get_kline(stock_code, StockConfig.kline_type_day)
                close = kline[:, -2].astype(np.float)
                sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
                if target_sma == 0 and target_price == 0:
                    if sma5[-1] < sma10[-1] and sma5[-1] < sma20[-1] or close[-1] < sma20[-1]:
                        continue
                f.write(line)
            else:
                f.write(line)


def toTDX():
    stock_code_list = []
    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code_list.append(data[0])
    with open('{}/{}.txt'.format(StockConfig.path_track, 'today_sma'), mode='w', encoding='utf-8') as f:
        for stock_code in stock_code_list:
            f.write("{}\n".format(stock_code))



if __name__ == '__main__':
    for position in range(-3, 0):
        position = position
        #position = StockIndicator.position('2017-12-15', stock_code='601398')
        date = 'yyyy-mm-dd'
        stock_list_1 = get_stock_list(position)
        stock_list_2 = get_stock_list(position - 1)
        stock_list_3 = get_stock_list(position - 2)
        stock_list_4 = get_stock_list(position - 3)


        stock_list = [x for x in stock_list_1 if x not in (stock_list_2 + stock_list_3 + stock_list_4)]
        stock_list = sorted(stock_list, key=lambda stock: stock.max_exceed, reverse=True)
        print(stock_list)
        print(len(stock_list))



        stock_code_list = []
        with open('data/track/2_sma_track.txt', mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith("#") and not '\n' == line:
                    data = line.strip('\n').split(',')
                    stock_code_list.append(data[0])


        with open('data/track/2_sma_track.txt', mode='a', encoding='utf-8') as f:
            f.write('\n#{}\n'.format(date))
            for key in stock_list:
                if key.stock_code not in stock_code_list:
                    f.write('{:>6},{: >5},{:>2},{:>2},{:>5},{:>5}, , ,\n'.format(key.stock_code, key.stock_name, '', '', '00.00', '00.00'))


        with open('data/track/today.txt', mode='w', encoding='utf-8') as f:
            for key in stock_list:
                if key.stock_code not in stock_code_list:
                    f.write("{}\n".format(key.stock_code))


    delete_invalid_record()

    #toTDX()



