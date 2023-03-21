from login.login import Login, Logout
from xing.t0424 import getJanGo
from xing.t1102 import nowPrice
from config import dumbo_config
from common.logger import Logger

# 병렬처리
from concurrent.futures import ThreadPoolExecutor

from core.trading import long, short, settlement, getAssetList, getSettle, getSettleList, getLongDeal, getShortDeal
from core.getbuyitem import get_buy_item_list
from common.utils import drawLine, print_list
from core.getselltem import get_sell_item_list
from time import sleep

logger = Logger("MAIN")

################################
# 변수
################################
# ITEM_PRACE_HIGH = dumbo_config.DealInfo['ITEM_PRACE_HIGH']    # 매도 상한가
ITEM_PRACE_LOW  = dumbo_config.DealInfo['ITEM_PRACE_LOW']       # 매수 하한가
BUYING_COUNT    = dumbo_config.DealInfo['BUYING_COUNT']         # 최대 보유 종목 수 (default : 5)
SLEEP_TIME      = 2

################################
# Short
################################

################################
# Short
################################
def short_deal(result, user_account, user_pass, sellItem):
    ################################
    # 변수 설정
    ################################
    marketPrice = sellItem['price']  # 현재가
    amount = int(sellItem['mdposqt'])  # 매도 가능 수량
    security_name = sellItem['hname']  # 종목명
    security_code = "A" + sellItem['expcode']  # 종목 코드 (A prefix)
    security_inform = "[" + str(security_name) + "(" + str(security_code) + ")" + "] "

    drawLine(character='$')

    # 매수 호가 조회
    status, now, longPrice, longAmount = getLongDeal(security_name, sellItem['expcode'])
    if (status):
        logger.info(
            security_name + " 현재가 " + str(now['now']) + "원 - 매수 호가 " + str(longPrice['p1']) + "[" + str(
                longAmount['a1']) + "] / " + str(longPrice['p2']) + "[" + str(
                longAmount['a2']) + "] /" + str(longPrice['p3']) + "[" + str(longAmount['a3']) + "]")

    # 매물 최고가로 매도
    marketPrice = longPrice['p1']

    drawLine(character='$')

    if amount > 0:
        ################################
        # 매도 주문
        ################################
        result.append(
            short(
                accountNo=user_account,
                password=user_pass,
                securityName=security_name,
                securityCode=security_code,
                longAmount=amount,
                longPrice=marketPrice
            ))
        ################################
        # 매도 대기
        ################################
        sleep(SLEEP_TIME)
        logger.info(security_inform + "매도 주문")
    else:
        logger.info(security_inform + "매도 대기 중인 종목입니다. 매도 채결을 대기합니다.")

    ################################
    # 미체결 종목 처리
    # 10회 미체결시 해당 종목/물량 취소 처리
    ################################
    settlement(user_account=user_account,
               password=user_pass,
               security_code=security_code,
               security_name=security_name,
               type='1',  # 매매구분 1 : 매도
               ExecYn='2')  # 매매구분 2 : 미체결

################################
# 긴급 청산 프로토콜
################################
def exit_process(POC=1):

    drawLine(character='=')
    logger.info("긴급 청산 프로토콜 시작")
    drawLine(character='=')
    user_account, user_pass = Login()

    TOTAL = POC

    while(POC > 0):
        # [t0424]
        _, my_item_list = getJanGo(user_account, user_pass)
        item_count = len(my_item_list)
        result = []

        if item_count > 0:
            # 매도 호출
            # 잔고 재 조회 할 필요없음 미수거래 안할 예정
            # 팔면 2일이 지나서 내 잔고가 되었을때 사야함.
            logger.info(str(len(my_item_list)) + "개 종목 청산 시작")
            print_list(my_item_list)

            ################################
            # 종목 갯수만큼 Thread 생성
            ################################
            pool_executor = ThreadPoolExecutor(int(item_count))

            for sellItem in my_item_list:
                #logger.info("분산 처리 시작")
                #pool = pool_executor.map(short_deal, result, user_account, user_pass, sellItem)
                short_deal(result, user_account, user_pass, sellItem)

        else:
            drawLine(character='=')
            logger.info("청산 대상 포트폴리오 없음")
            drawLine(character='=')
            break

        POC -= 1

        drawLine(character='+')
        logger.info("긴급 청산 프로토콜 총 " + str(TOTAL - POC) + "번 반복하였습니다. ")
        drawLine(character='+')

    drawLine(character='=')
    logger.info("긴급 청산 프로토콜 종료")
    drawLine(character='=')
    sleep(1)

def getAsset():
    user_account, user_pass = Login()
    drawLine()

    # CSPAQ12300 잔고 조회,  내가 보유한 종목 조회
    # amt 현금 주문 가능 금액
    amt, minus_amt, my_item_list = getAssetList(user_account, user_pass)
    drawLine()

# CSPAQ13700
def getSettleL(type='0', ExecYn='0'):
    user_account, user_pass = Login()
    drawLine()
    result = getSettleList(user_account, user_pass, BnsTpCode=type, ExecYn=ExecYn)
    print_list(result)
    drawLine()

################################
# 기본 프로세스
################################
def process(LOSS, PROFIT, POC=1):
    # 로그인
    user_account, user_pass = Login()
    drawLine()
    TOTAL = POC

    while(POC > 0):

        # CSPAQ12300 잔고 조회,  내가 보유한 종목 조회
        # amt 현금 주문 가능 금액
        amt, minus_amt, my_item_list = getAssetList(user_account, user_pass)
        drawLine()

        # 변수 초기화
        amt = 1000000
        holdItemCount = len(my_item_list);  # 보유한 종목 갯수

        ################################
        # Step 1. 매도
        ################################
        if (len(my_item_list) > 0):

            ################################
            # 매도 대상 검색
            ################################
            sellItemList = get_sell_item_list(my_item_list, LOSS, PROFIT)
            drawLine()
            result = []

            if len(sellItemList) > 0:
                # 매도 호출
                # 잔고 재 조회 할 필요없음 미수거래 안할 예정
                # 팔면 2일이 지나서 내 잔고가 되었을때 사야함.
                logger.info("종목 청산 수행")
                print_list(sellItemList)

                for sellItem in sellItemList:
                    # 시세가이기 때문에 추후 호가로 변경 필요
                    # ※시세가인 경우 물량이 없으면 거래가 이루어지지 않음
                    amount          = sellItem['SellAbleQty']
                    marketPrice     = sellItem['NowPrc']
                    security_code   = sellItem['IsuNo']
                    security_name   = sellItem['IsuNm']
                    security_inform = "[" + str(security_code) + "(" + str(security_name) + ")" + "] "

                    # 매수 호가 조회
                    status, now, longPrice, longAmount = getLongDeal(security_name, str(sellItem['IsuNo']).replace('A',''))
                    if (status):
                        logger.info(
                            security_name + " 현재가 " + str(now['now']) + "원 - 매수 호가 " + str(longPrice['p1']) + "[" + str(
                                longAmount['a1']) + "] / " + str(longPrice['p2']) + "[" + str(
                                longAmount['a2']) + "] /" + str(longPrice['p3']) + "[" + str(longAmount['a3']) + "]")

                    # 매물 최고가로 매도
                    marketPrice = int(longPrice['p1'])

                    if int(amount) > 0:

                        ################################
                        # 매도 주문
                        ################################
                        result.append(
                            short(
                                accountNo=user_account,
                                password=user_pass,
                                securityName=security_name,
                                securityCode=security_code,
                                longAmount=amount,
                                longPrice=marketPrice
                            ))
                        sleep(SLEEP_TIME)

                        logger.info(security_inform + str(marketPrice) + "원/" + str(amount)+"주 매도")

                    else:
                        logger.info("매도 대기 중인 종목입니다.")

                    ################################
                    # 미체결 종목 처리
                    # 10회 미체결시 해당 종목/물량 취소 처리
                    ################################
                    settlement(user_account=user_account,
                               password=user_pass,
                               security_code=security_code,
                               security_name=security_name,
                               type='1',  # 매매구분 1 : 매도
                               ExecYn='2')  # 매매구분 2 : 미체결
            else:
                logger.info("청산 대상 없음")
                drawLine()

        else:
            logger.info("현재 구성된 포트폴리오 없음")

        ################################
        # Step 2. 매수
        ################################
        if holdItemCount < BUYING_COUNT:
            logger.info("포트폴리오 구성 시작 [" + str(holdItemCount) +"/" + str(BUYING_COUNT) + "]")
            drawLine()
            ################################
            # 매수 대상 종목 검색
            ################################
            buyItemList = get_buy_item_list(amt, my_item_list, holdItemCount)
            drawLine()
            logger.info("추가 매수 대상 검색 종목 수 " + str(len(buyItemList)))
            result = []

            for buyItem in buyItemList:
                # 시세가이기 때문에 추후 호가로 변경 필요
                # ※시세가인 경우 물량이 없으면 거래가 이루어지지 않음
                amount          = buyItem['count']
                security_code   = "A" + buyItem['item_code']
                security_name   = buyItem['item_name']
                marketPrice     = nowPrice(str(buyItem['item_code']))['price']
                security_inform = "[" + str(security_name) + "(" + str(security_code) + ")" + "] "

                # 매도 호가 조회
                status, now, shortPrice, shortAmount = getLongDeal(security_name, buyItem['item_code'])
                if (status):
                    logger.info(
                        security_name + " 현재가 " + str(now['now']) + "원 - 매수 호가 " + str(shortPrice['p1']) + "[" + str(
                            shortAmount['a1']) + "] / " + str(shortPrice['p2']) + "[" + str(
                            shortAmount['a2']) + "] /" + str(shortPrice['p3']) + "[" + str(shortAmount['a3']) + "]")

                # 매물 최저가로 매수
                marketPrice = int(shortPrice['p1'])

                ################################
                # 매수 주문
                ################################
                logger.info("===========================================")
                result.append(
                    long(
                        accountNo=user_account,
                        password=user_pass,
                        securityName=security_name,
                        securityCode=security_code,
                        longAmount=amount,
                        longPrice=marketPrice))
                sleep(SLEEP_TIME)
                logger.info("===========================================")

                ################################
                # 미체결 종목 처리
                # 10회 미체결시 해당 종목/물량 취소 처리
                ################################
                settlement(user_account=user_account,
                           password=user_pass,
                           security_code=security_code,
                           security_name=security_name,
                           type='2',    # 매매구분 2 : 매수
                           ExecYn='2')  # 매매구분 2 : 미체결

        POC -= 1

        drawLine(character='+')
        logger.info("기본 프로토콜 총 " + str(TOTAL-POC) + "번 반복하였습니다. ")
        drawLine(character='+')

    drawLine(character='=')
    logger.info("기본 프로세스를 종료합니다.")
    getAssetList(user_account, user_pass)
    drawLine(character='=')
    sleep(1)

if __name__ == "__main__":

    # 전략
    POC = 999
    LOSS = 10
    PROFIT = 5
    EXIT = True

    if(EXIT):
        # 긴급 청산 프로토콜
        exit_process(POC)
    else:
        #getAsset()
        #getSettleL(1, 2)
        process(LOSS, PROFIT, POC)
