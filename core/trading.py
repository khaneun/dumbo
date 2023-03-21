from common.utils import drawLine
from config import dumbo_config
from time import sleep
from xing.CSPAQ12200 import CSPAQ12200
from xing.CSPAQ12300 import CSPAQ12300
from xing.CSPAT00600 import CSPAT00600
from xing.CSPAQ13700 import CSPAQ13700
from xing.CSPAT00800 import CSPAT00800
from xing.t1101 import t1101
from xing.t0425 import getSettlement
from common.logger import Logger
from common.utils import print_list, getDateFormat
logger = Logger("TRAD")


# ITEM_PRACE_HIGH = dumbo_config.DealInfo['ITEM_PRACE_HIGH']
ITEM_PRACE_LOW  = dumbo_config.DealInfo['ITEM_PRACE_LOW']
BUYING_COUNT    = dumbo_config.DealInfo['BUYING_COUNT']
SETTLE_TIMER    = 5
SETTLE_RETRY    = 3

################################
# 매수
################################
def long(
        accountNo='',
        password='',
        securityName='',
        securityCode='',
        longAmount='',
        longPrice='',
        longShrotType = '2',    # 매매구분 (1 : 매도 2 : 매수)
        priceType = '00',
        creditTransCode = '000',
        OrderConditionType = '0' # 주문조건 (0 : 없음, 1: IOC, 2: FOK)
    ):
    ###############################
    # 호가 유형
    # 00 : 지정가
    # 03 : 시장가
    # 05 : 조건부지정가
    # 06 : 최유리지정가
    # 07 : 최우선지정가
    # 61 : 장개시전시간외종가
    # 81 : 시간외종가
    # 82 : 시간외단일가가
    ###############################
    security_inform = "[" + str(securityName) + "(" + str(securityCode) + ")" + "] "
    logger.info(security_inform + str(longPrice) + "원 " + str(longAmount) + "주 매수")
    return CSPAT00600(accountNo, password, securityCode, longAmount, longPrice, longShrotType, priceType, creditTransCode, OrderConditionType)

################################
# 매도
################################
def short(
        accountNo='',
        password='',
        securityName='',
        securityCode='',
        longAmount='',
        longPrice='',
        longShrotType = '1', # 매매구분 (1 : 매도 2 : 매수)
        priceType = '00',
        creditTransCode = '000',
        OrderConditionType = '0' # 주문조건 (0 : 없음, 1: IOC, 2: FOK)
    ):
    ###############################
    # 호가(priceType) 유형
    ###############################
    # 00 : 지정가
    # 03 : 시장가
    # 05 : 조건부지정가
    # 06 : 최유리지정가
    # 07 : 최우선지정가
    # 61 : 장개시전시간외종가
    # 81 : 시간외종가
    # 82 : 시간외단일가가
    ###############################
    security_inform = "[" + str(securityName) + "(" + str(securityCode) + ")" + "] "
    logger.info(security_inform + str(longPrice) + "원/" + str(longAmount) + "주 매도")

    return CSPAT00600(accountNo, password, securityCode, longAmount, longPrice, longShrotType, priceType, creditTransCode, OrderConditionType)

################################
# 주문 취소
################################
def cancelOrder(
        OrgOrdNo = '',
        accountNo = '',
        password = '',
        securityNo = '',
        OrdQty = '0'):

    return CSPAT00800(OrgOrdNo=OrgOrdNo, accountNo=accountNo, password=password, securityNo=securityNo, OrdQty=OrdQty)

def getSettle(user_account, password, security_code=''):
    return getSettlement(user_account, password, security_code)

################################
# 가격 조정 정책
################################
def adjustPrice(type, security_name, security_code):
    drawLine(character='=')

    title = "전체"
    price = -1

    if type == '1':
        title = "매도"
        # 매수 호가 조회
        status, now, longPrice, longAmount = getLongDeal(security_name, str(security_code).replace('A', ''))
        if (status):
            logger.info(
                security_name + " 현재가 " + str(now['now']) + "원 - 매수 호가 " + str(longPrice['p1']) + "[" + str(
                    longAmount['a1']) + "] / " + str(longPrice['p2']) + "[" + str(
                    longAmount['a2']) + "] /" + str(longPrice['p3']) + "[" + str(longAmount['a3']) + "]")

        # 매물 최고가로 매도
        price = int(longPrice['p1'])

    elif type == '2':
        title = "매수"
        # 매수 호가 조회
        status, now, longPrice, longAmount = getLongDeal(security_name, str(security_code).replace('A', ''))
        if (status):
            logger.info(
                security_name + " 현재가 " + str(now['now']) + "원 - 매수 호가 " + str(longPrice['p1']) + "[" + str(
                    longAmount['a1']) + "] / " + str(longPrice['p2']) + "[" + str(
                    longAmount['a2']) + "] /" + str(longPrice['p3']) + "[" + str(longAmount['a3']) + "]")

        # 매물 최고가로 매도
        price = int(longPrice['p1'])

    return title, price

################################
# 체결 완료 처리
################################
def settlement(user_account, password, security_code, security_name, type, ExecYn):

    title, price = adjustPrice(
        type=type,
        security_name=security_name,
        security_code=security_code)

    status, result = getSettleListBySecurity(user_account, password, security_code, type, ExecYn)

    idx = 1
    rePrice = True
    while(len(result)!=0):
        exit = True
        # 잔고 조회
        while (exit):
            sleep(SETTLE_TIMER)
            status, result = getSettleListBySecurity(user_account, password, security_code, type, ExecYn)
            status = (status & False)
            exit = status

        logger.info("[" + str(security_name) + "(" + str(security_code) + ")] " + str(title) + " 체결 대기 " + str(idx) + "/" + str(SETTLE_RETRY))

        if(len(result)==0):
            logger.info("거래가 체결되었습니다.")
            continue

        if(idx >= SETTLE_RETRY):

            temp = result[0]
            OrgOrdNo = temp['OrdNo']
            ExecQty = temp['ExecQty']
            OrdQty = int(temp['MrcAbleQty'])
            cancelOrder(OrgOrdNo, user_account, password, security_code, OrdQty)

            if (rePrice):
                logger.info(str(title) + " 가격을 조정하여 재시도 합니다.")
                title = "매수 조정"
                idx = 0
                rePrice = False

                if type == 1:   # 매도
                    short(
                        accountNo=user_account,
                        password=password,
                        securityName=security_name,
                        securityCode=security_code,
                        longAmount=OrdQty,
                        longPrice=price
                    )
                elif type == 2: # 매수
                    long(
                        accountNo=user_account,
                        password=password,
                        securityName=security_name,
                        securityCode=security_code,
                        longAmount=OrdQty,
                        longPrice=price
                    )
            else:
                logger.info("[" + str(security_name) + "(" + str(security_code) + ")] " + title + " 주문[" + OrgOrdNo + "]에 실패하여 " + str(OrdQty) + "건 취소합니다.")
                break

        idx += 1

def getSettleList(user_account, user_pass, BnsTpCode='0', ExecYn='0'):
    return CSPAQ13700(accountNo=user_account, password=user_pass, OrdDt=str(getDateFormat()), BnsTpCode=BnsTpCode, ExecYn=ExecYn)

def getSettleListBySecurity(user_account, user_pass, security_code, BnsTpCode='0', ExecYn='0'):
    return CSPAQ13700(accountNo=user_account, password=user_pass, OrdDt=str(getDateFormat()), BnsTpCode=BnsTpCode, securityNo=security_code, ExecYn=ExecYn)

################################
# 매수 호가 조회
################################
def getLongDeal(security_name, security_code):
    now = {}
    price = {}
    amount = {}

    result = t1101(security_code)
    if len(result) == 0:
        logger.info(security_name + " 매수 호가 정보가 없습니다.")
        return False, -1,-1,-1
    else:
        now['now'] = result[0]['price']
        price['p1'] = result[0]['bidho1']
        price['p2'] = result[0]['bidho2']
        price['p3'] = result[0]['bidho3']
        amount['a1'] = result[0]['bidrem1']
        amount['a2'] = result[0]['bidrem2']
        amount['a3'] = result[0]['bidrem3']

        return True, now, price, amount

################################
# 매도 호가 조회
################################
def getShortDeal(security_name, security_code):
    now = {}
    price = {}
    amount = {}

    result = t1101(security_code)
    if len(result) == 0:
        logger.info(security_name + " 매도 호가 정보가 없습니다.")
        return False, -1,-1,-1
    else:
        now['now'] = result[0]['price']
        price['p1'] = result[0]['offerho1']
        price['p2'] = result[0]['offerho2']
        price['p3'] = result[0]['offerho3']
        amount['a1'] = result[0]['offerrem1']
        amount['a2'] = result[0]['offerrem2']
        amount['a3'] = result[0]['offerrem3']

        return True, now, price, amount

################################
# 잔고 조회 CSPAQ12200
################################
def getCapital(user_account, user_pass):

    status, result = CSPAQ12200(user_account, user_pass)
    size = len(result)

    logger.info("잔고 조회 건수 [" + str(size) + "]")

    #logger.info(result)
    #print_list(result)

    if(status):
        stat = result[0]
        amt = float(stat['MnyoutAbleAmt'])
        minus_amt = float(stat['RcvblAmt'])

        drawLine(character='=')
        logger.info("요약 정보")
        drawLine(character='=')
        logger.info("잔고 " + str(format(amt, ',')) + "원 (현금 출금 가능 금액) - 미수 거래 금액 " + str(format(minus_amt, ',')) + " 원")
        drawLine()

        return status, stat
    else:
        return status, result


################################
# 잔고 조회 CSPAQ12300
################################
def getSecurity(user_account, user_pass):

    my_item_list = CSPAQ12300(user_account, user_pass)

    if len(my_item_list) > 0:
        logger.info("보유 종목 리스트")
        print_list(my_item_list)
        return True, my_item_list
    else:
        logger.info("보유 종목 없음")
        return False, my_item_list

