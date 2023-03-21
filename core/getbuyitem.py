import random
from config import dumbo_config

from xing.t1452 import t1452
from xing.t8436 import t8436
from common.utils import drawLine
import math
from common.logger import Logger
logger = Logger("PICK")
###############################
#     주식종목 조회 TR
###############################

################################
# 변수
################################
# ITEM_PRACE_HIGH = dumbo_config.DealInfo['ITEM_PRACE_HIGH']    # 매도 상한가
ITEM_PRACE_LOW  = dumbo_config.DealInfo['ITEM_PRACE_LOW']       # 매수 하한가
BUYING_COUNT    = dumbo_config.DealInfo['BUYING_COUNT']         # 최대 보유 종목 수

################################
# 종목 고르는 방법
################################
def getPickingMethod(allItemList):
    item = random.choice(allItemList)
    return item

def itemList(type=0):

    item_list = []
    ################################
    # 시장 Ordering
    ################################
    # 0 전종목
    # 1 거래량

    if(type==0):
        # 전종목
        item_list = t8436("2")

    elif(type==1):
        # 거래량 기준 40종목 선정
        item_list = t1452(
            gubun='0',  # 구분        0:전체  1:코스피  2:코스닥
            jnilgubun='1',  # 전일구분     1:당일  2:전일
            sdiff='',  # 시작등락율
            ediff='',  # 종료등락율
            jc_num='',  # 대상제외
            sprice='',  # 시작가격
            eprice='',  # 종료가격
            volume='',  # 거래량
            idx=''  # IDX
        )
    return item_list

def get_buy_item_list(amt, my_item_codes, holdCount, type=0):
    title = "전종목"
    if (type == 0):
        title = "전종목"
    elif (type == 1):
        title = "거래량 상위 40 종목"

    logger.info("시장 [" + str(title) + "] 종목 조회")
    allItemList = itemList(type)
    logger.info("시장 [" + str(title) + "] 종목수 : " + str(len(allItemList)))
    drawLine()
    logger.info("매수 대상 종목 조회")
    ################################
    # 임시 변수
    ################################
    buyingList = [];    # 구매 목록
    calAmt = amt;       # 구매 가능 자본
    count = 0;          #

    buyingTargetCount = BUYING_COUNT - holdCount
    logger.info("추가 구매 가능 종목수 : " + str(buyingTargetCount) + " [현보유 현황 : " + str(holdCount) + "/" + str(BUYING_COUNT) + "]")
    itemHighPrice = amt / buyingTargetCount
    logger.info("종목 당 평균 구매 가능 금액  : " + str(format(float(itemHighPrice),',')) + "원")

    ################################
    # 조건 : 구매 자본이 없거나, 포트폴리오 추가 가능한 종목수 초과시
    ################################
    while calAmt > 0 and count < buyingTargetCount:

        '''
            item['item_code'] = shcode
            item['item_name'] = hname
            item['up_price'] = uplmtprice
            item['down_price'] = dnlmtprice
            item['reperence_price'] = recprice
            item['closing_price'] = jnilclose
        '''
        item = getPickingMethod(allItemList)
        itemPrice = int(item['reperence_price'])

        # 중복 종목 제거
        if item['item_code'] in my_item_codes:
            continue;

        # 조건 : 종목 최소 매수 가격 이상, 구매 가능 자산 이하
        # itemPrice     매수 종목 가격
        # itemHighPrice 구매 가능 자산
        if itemPrice >= ITEM_PRACE_LOW and itemPrice <= itemHighPrice:

            itemCount = math.floor(itemHighPrice / itemPrice)

            # logger.info("종목 별 구매 가능 count : " + str(itemCount))
            calAmt = calAmt - (itemPrice * itemCount)
            # logger.info("계산후 남은 금액 " + str(calAmt))

            if (calAmt > 0):
                item['count'] = itemCount
                buyingList.append(item)
                count = count + 1

        else:
            continue;

    return buyingList
