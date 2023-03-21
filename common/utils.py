import datetime
from common.logger import Logger
logger = Logger("UTIL")

DICTIONARY = {
    'sunamt'   :'추정순자산',
    'dtsunik'  :'실현손익',
    'sunamt1'  :'추정D2예수금',
    'mamt'     :'매입금액',
    'tappamt'  :'평가금액',
    'tdtsunik' :'평가손익',
    'expcode'  :'종목번호',
    'hname'    :'종목명',
    'price'    :'현재가',
    'janqty'   :'잔고수량',
    'mdposqt'  :'매도가능수량',
    'pamt'     :'평균단가',
    'appamt'   :'평가금액',
    'jangb'    :'잔고구분',
    'dtsunik'  :'실현손익',
    'sininter' :'신용이자',
    'sinamt'   :'대출금액',
    'SellAbleQty':'매도가능잔고수량',
    'IsuNm'    :'종목명',
    'IsuNo'    :'종목번호',
    'AvrUprc'  :'평균단가',
    'NowPrc'   :'현재가',
    'tqty'     : '총주문수량',
    'tcheqty'  : '총체결수량',
    'tordrem'  : '총미체결수량',
    'cmss'     : '추정수수료',
    'tamt'     : '총주문금액',
    'tmdamt'   : '총매도체결금액',
    'tmsamt'   : '총매수체결금액',
    'tax'      : '추정제세금',
    'cts_ordno': '주문번호',
    'ordno'    : '주문번호',
    'expcode'  : '종목번호',
    'medosu'   : '구분',
    'qty'      : '주문수량',
    'price0425': '주문가격',
    'cheqty'   : '체결수량',
    'cheprice' : '체결가격',
    'ordrem'   : '미체결잔량',
    'cfmqty'   : '확인수량',
    'status'   : '상태',
    'orgordno' : '원주문번호',
    'ordgb'    : '유형',
    'ordtime'  : '주문시간',
    'ordermtd' : '주문매체',
    'sysprocseq': '처리순번',
    'hogagb'   : '호가유형',
    'price10425': '현재가',
    'orggb'    : '주문구분',
    'singb'    : '신용구분',
    'loandt'   : '대출일자',
    'OrdDt'    : '주문일',
    'MgmtBrnNo': '관리지점번호',
    'OrdMktCode': '주문시장코드',
    'OrdNo'    : '주문번호',
    'OrgOrdNo' : '원주문번호',
    'IsuNo'    : '종목번호',
    'IsuNm'    : '종목명',
    'BnsTpCode': '매매구분',
    'BnsTpNm': '매매구분명',
    'OrdPtnCode': '주문유형코드',
    'OrdPtnNm': '주문유형명',
    'OrdTrxPtnCode': '주문처리유형코드',
    'OrdTrxPtnNm': '주문처리유형명',
    'MrcTpCode': '정정취소구분',
    'MrcTpNm': '정정취소구분명',
    'MrcQty': '정정취소수량',
    'MrcAbleQty': '정정취소가능수량',
    'OrdQty': '주문수량',
    'OrdPrc': '주문가격',
    'ExecQty': '체결수량',
    'ExecPrc': '체결가',
    'ExecTrxTime': '체결처리시각',
    'LastExecTime': '최종체결시각',
    'OrdprcPtnCode': '호가유형코드',
    'OrdprcPtnNm': '호가유형명',
    'OrdCndiTpCode': '주문조건구분',
    'AllExecQty': '전체체결수량',
    'RegCommdaCode': '통신매체코드',
    'CommdaNm': '통신매체명',
    'MbrNo': '회원번호',
    'RsvOrdYn': '예약주문여부',
    'LoanDt': '대출일',
    'OrdTime': '주문시각',
    'OpDrtnNo': '운용지시번호',
    'OdrrId': '주문자ID',
    'offerho1': '매도호가1',
    'offerho2': '매도호가2',
    'offerho3': '매도호가3',
    'offerrem1': '매도호가수량1',
    'offerrem2': '매도호가수량2',
    'offerrem3': '매도호가수량3',
    'bidho1': '매수호가1',
    'bidho2': '매수호가2',
    'bidho3': '매수호가3',
    'bidrem1': '매수호가수량1',
    'bidrem2': '매수호가수량2',
    'bidrem3': '매수호가수량3',
    'BrnNm' : '지점명',
    'AcntNm' : '계좌명',
    'MnyOrdAbleAmt' : '현금주문가능금액',
    'MnyoutAbleAmt' : '출금가능금액',
    'SeOrdAbleAmt' : '거래소금액',
    'KdqOrdAbleAmt' : '코스닥금액',
    'BalEvalAmt' : '잔고평가금액',
    'RcvblAmt' : '미수금액',
    'DpsastTotamt' : '예탁자산총액',
    'PnlRat' : '손익율',
    'InvstOrgAmt' : '투자원금',
    'InvstPlAmt' : '투자손익금액',
    'CrdtPldgOrdAmt' : '신용담보주문금액',
    'Dps' : '예수금',
    'SubstAmt' : '대용금액',
    'D1Dps' : 'D1예수금',
    'D2Dps' : 'D2예수금',
    'MnyrclAmt' : '현금미수금액',
    'MgnMny' : '증거금현금',
    'MgnSubst' : '증거금대용',
    'ChckAmt' : '수표금액',
    'SubstOrdAbleAmt' : '대용주문가능금액',
    'MgnRat100pctOrdAbleAmt' : '증거금률100퍼센트주문가능금액',
    'MgnRat35ordAbleAmt' : '증거금률35%주문가능금액',
    'MgnRat50ordAbleAmt' : '증거금률50%주문가능금액',
    'PrdaySellAdjstAmt' : '전일매도정산금액',
    'PrdayBuyAdjstAmt' : '전일매수정산금액',
    'CrdaySellAdjstAmt' : '금일매도정산금액',
    'CrdayBuyAdjstAmt' : '금일매수정산금액',
    'D1ovdRepayRqrdAmt' : 'D1연체변제소요금액',
    'D2ovdRepayRqrdAmt' : 'D2연체변제소요금액',
    'D1PrsmptWthdwAbleAmt' : 'D1추정인출가능금액',
    'D2PrsmptWthdwAbleAmt' : 'D2추정인출가능금액',
    'DpspdgLoanAmt' : '예탁담보대출금액',
    'Imreq' : '신용설정보증금',
    'MloanAmt' : '융자금액',
    'ChgAfPldgRat' : '변경후담보비율',
    'OrgPldgAmt' : '원담보금액',
    'SubPldgAmt' : '부담보금액',
    'RqrdPldgAmt' : '소요담보금액',
    'OrgPdlckAmt' : '원담보부족금액',
    'PdlckAmt' : '담보부족금액',
    'AddPldgMny' : '추가담보현금',
    'D1OrdAbleAmt' : 'D1주문가능금액',
    'CrdtIntdltAmt' : '신용이자미납금액',
    'EtclndAmt' : '기타대여금액',
    'NtdayPrsmptCvrgAmt' : '익일추정반대매매금액',
    'OrgPldgSumAmt' : '원담보합계금액',
    'CrdtOrdAbleAmt' : '신용주문가능금액',
    'SubPldgSumAmt' : '부담보합계금액',
    'CrdtPldgAmtMny' : '신용담보금현금',
    'CrdtPldgSubstAmt' : '신용담보대용금액',
    'AddCrdtPldgMny' : '추가신용담보현금',
    'CrdtPldgRuseAmt' : '신용담보재사용금액',
    'AddCrdtPldgSubst' : '추가신용담보대용',
    'CslLoanAmtdt1' : '매도대금담보대출금액',
    'DpslRestrcAmt' : '처분제한금액',
    'hname' : ' 종목명',
    'price' : '현재가',
    'sign' : '전일대비구분',
    'change' : '전일대비',
    'diff' : '등락율',
    'volume' : '누적거래량',
    'vol' : '회전율',
    'jnilvolume' : '전일거래량',
    'bef_diff' : '전일비',
    'shcode' : '종목코드'
}

ACOUNT = ['금액','손익','단가','이자','예수금','자산','현재가','수수료','세금']

################################
# 구분선 Print (나중에 common - common_utils.py로 이동)
################################
def drawLine(length=50, character='-'):
    line_str = ''
    for i in range(length):
        line_str += character
    logger.info(line_str)

def getDictionary(key):
    if key in DICTIONARY:
        return DICTIONARY.get(key)
    else:
        return key

def checkAccount(key):
    for word in ACOUNT:
        if str(key).endswith(word):
            return True
    return False

################################
# list 객체 Print (나중에 common - utils.py로 이동)
################################
def print_list(list, name='item'):
    idx = 1
    for item in list:
        info = ""
        for key in item.keys():
            value = item.get(key)

            if (checkAccount(getDictionary(key))):
                cv = format(float(value), ',')
                cv = "{0:<5}".format(str(cv))
                info += getDictionary(key) + "\t" + str(cv) + " 원\t | "
            else:
                #value = "{0:.4}".format(value)
                #value = "{0:>5}".format(value)
                info += getDictionary(key) + "\t" + str(value) + "\t | "
        logger.info("[" + name + " " + str(idx) + "] " + info)
        idx = idx+1

def getDateFormat(format='%Y%m%d'):
    now = datetime.datetime.now()
    formattedDate = now.strftime(format)
    return formattedDate

def getTimeCheck():
    now = datetime.datetime.now()
    msg = "금일장 중입니다. [약 " + str(int(now.hour)-9) + "시간 " + str(int(now.minute)) + "분 경과]"
    status = True

    idx = int(now.hour)*100 + int(now.minute)

    if idx < 900:
        residual = 1 if int(now.minute) > 0 else 0
        rem_min = 60 - int(now.minute) if int(now.minute) > 0 else 0
        rem_hour = (9 - int(now.hour) - residual)
        msg = "금일 장 시작 전입니다. [약 " + str(rem_hour) + "시간 " + str(rem_min) + "분 대기]"
        status = False
    elif idx > 1530:
        residual = 1 if int(now.minute) > 0 else 0
        rem_min = 60 - int(now.minute) if int(now.minute) > 0 else 0
        rem_hour = (24 - int(now.hour) - residual + 9)

        msg = "금일 장 종료되었습니다. [약 " + str(rem_hour) + "시간 " + str(rem_min) + "분 대기]"
        status = False

    return status, msg
