import random
from config import dumbo_config
import math
from common.logger import Logger
from common.utils import drawLine
logger = Logger("SELL")


# ITEM_PRACE_HIGH = dumbo_config.DealInfo['ITEM_PRACE_HIGH']
ITEM_PRACE_LOW = dumbo_config.DealInfo['ITEM_PRACE_LOW']
BUYING_COUNT = dumbo_config.DealInfo['BUYING_COUNT']

def get_sell_item_list(my_item_list, LOSS, PROFIT):
    logger.info("보유 종목 청산 프로세스 시작")
    drawLine()
    sell_list_item=[]

    # 손절
    logger.info("손절 종목 검색")
    loss_sell_list = get_tick_down_item_list(my_item_list, LOSS)

    if(len(loss_sell_list)==0):
        logger.info("손절 종목 없음")
    else:
        logger.info("손절 종목 [" + str(len(loss_sell_list)) + "] 건")
        for item in loss_sell_list:
            sell_list_item.append(item)

    # 익절
    logger.info("익절 종목 검색")
    profit_list_item = get_tick_up_item_list(my_item_list, PROFIT)

    if (len(profit_list_item) == 0):
        logger.info("익절 종목 없음")
    else:
        for item in profit_list_item:
            sell_list_item.append(item)

    return sell_list_item


def get_tick_up_item_list(my_item_list, PROFIT):
    # 5% 오르면 파는 걸로
    up_items = []

    for item in my_item_list:
        '''
            item['IsuNm'] = 종목명
            item['IsuNo'] = 종목 번호
            item['SellAbleQty'] = 매도 가능 잔고 수량
            item['AvrUprc'] = 평균 단가
            item['NowPrc'] = 현재가
            item['EvalPnl'] = 평가 손익
            item['PnlRat'] = 평가 손익 비율
        '''
        if math.floor(float(item['PnlRat']) * 100) >= PROFIT:
            item['tick'] = 'up'
            up_items.append(item)
            logger.info(item)

        #temp_pnl = math.floor(float(item['PnlRat']) * 100)
        #logger.info("[Up Profit " + str(PROFIT) + "] 이익률("+item['NowPrc']+"/"+item['AvrUprc']+") : " + str(temp_pnl) + "%")

    return up_items


def get_tick_down_item_list(my_item_list, LOSS):
    # 10% 떨어지면 파는 걸로
    down_items = []

    for item in my_item_list:
        '''
            item['IsuNm'] = 종목명
            item['IsuNo'] = 종목 번호
            item['SellAbleQty'] = 매도 가능 잔고 수량
            item['AvrUprc'] = 평균 단가
            item['NowPrc'] = 현재가
            item['EvalPnl'] = 평가 손익
            item['PnlRat'] = 평가 손익 비율
        '''
        if math.floor(float(item['PnlRat']) * 100) * (-1) >= LOSS:
            item['tick'] = 'down'
            down_items.append(item)
            logger.info(item)

        #temp_pnl = math.floor(float(item['PnlRat']) * 100) * (-1)
        #logger.info("[Down " + str(LOSS) + "] 손실률("+item['NowPrc']+"/"+item['AvrUprc']+") : " + str(temp_pnl) + "%")

    return down_items