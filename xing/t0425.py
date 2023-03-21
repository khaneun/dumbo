import win32com.client
import pythoncom
import inspect
from common.logger import Logger
logger = Logger("0425")

###############################
#    주식체결/미체결 TR
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("t0425 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t0425 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode

def getJanGo(
        accno,
        passwd,
        expcode='',
        chegb='0',
        medosu='0',
        sortgb='2',
        cts_ordno=''):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t0425.res")
    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    inXAQuery.SetFieldData(INBLOCK, "accno", 0, accno)
    inXAQuery.SetFieldData(INBLOCK, "passwd", 0, passwd)
    inXAQuery.SetFieldData(INBLOCK, "expcode", 0, expcode)
    inXAQuery.SetFieldData(INBLOCK, "chegb", 0, chegb)
    inXAQuery.SetFieldData(INBLOCK, "medosu", 0, medosu)
    inXAQuery.SetFieldData(INBLOCK, "sortgb", 0, sortgb)
    inXAQuery.SetFieldData(INBLOCK, "cts_ordno", 0, cts_ordno)

    # inXAQuery.SetFieldData("t0425InBlock", "prcgb", 0, prcgb)
    # inXAQuery.SetFieldData("t0425InBlock", "dangb", 0, dangb)
    succsess = inXAQuery.Request( True )

    #while XAQueryEvents.queryState == 0:
    #    pythoncom.PumpWaitingMessages()

    result = []

    nCount = inXAQuery.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        sunamt = inXAQuery.GetFieldData(OUTBLOCK, "sunamt", 0)  # 추정순자산
        dtsunik = inXAQuery.GetFieldData(OUTBLOCK, "dtsunik", 0)  # 실현손익
        mamt = inXAQuery.GetFieldData(OUTBLOCK, "mamt", 0)  # 매입금액
        tappamt = inXAQuery.GetFieldData(OUTBLOCK, "tappamt", 0)  # 평가금액
        tdtsunik = inXAQuery.GetFieldData(OUTBLOCK, "tdtsunik", 0)  # 평가손익

        # 자산 = 자본 + 부채
        #     = 잔고 + (주식 + 평가금액)
        result.append(sunamt)
        result.append(tappamt)
        result.append(tdtsunik)


    XAQueryEvents.queryState = 0
    XAQueryEvents.resultCode = 0

    return result


def getSettlement(
        accountNo='',   # 계좌번호
        password='',    # 비밀번호
        securityCode='',# 종목번호
        doneYN='0',     # 체결구분
        longShort='0',  # 매매구분
        order='2',      # 정렬순서
        orderNo=''):    # 주문번호

    '''
    주식 체결/미체결
    '''
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t0425.res")

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "t0425InBlock"
    INBLOCK1 = "t0425InBlock1"
    OUTBLOCK = "t0425OutBlock"
    OUTBLOCK1 = "t0425OutBlock1"
    OUTBLOCK2 = "t0425OutBlock2"

    inXAQuery.SetFieldData(INBLOCK, "accno", 0, accountNo)
    inXAQuery.SetFieldData(INBLOCK, "passwd", 0, password)
    inXAQuery.SetFieldData(INBLOCK, "expcode", 0, securityCode)
    inXAQuery.SetFieldData(INBLOCK, "chegb", 0, doneYN)
    #inXAQuery.SetFieldData(INBLOCK, "medosu", 0, longShort)
    #inXAQuery.SetFieldData(INBLOCK, "sortgb", 0, order)
    #inXAQuery.SetFieldData(INBLOCK, "cts_ordno", 0, orderNo)
    inXAQuery.Request(0)

    #while XAQueryEvents.queryState == False:
    #    pythoncom.PumpWaitingMessages()

    result = []
    nCount = inXAQuery.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        item = {}
        tqty        = int(inXAQuery.GetFieldData(OUTBLOCK, "tqty", i).strip())      #총주문수량
        tcheqty     = int(inXAQuery.GetFieldData(OUTBLOCK, "tcheqty", i).strip())   #총체결수량
        tordrem     = int(inXAQuery.GetFieldData(OUTBLOCK, "tordrem", i).strip())   #총미체결수량
        cmss        = int(inXAQuery.GetFieldData(OUTBLOCK, "cmss", i).strip())      #추정수수료
        tamt        = int(inXAQuery.GetFieldData(OUTBLOCK, "tamt", i).strip())      #총주문금액
        tmdamt      = int(inXAQuery.GetFieldData(OUTBLOCK, "tmdamt", i).strip())    #총매도체결금액
        tmsamt      = int(inXAQuery.GetFieldData(OUTBLOCK, "tmsamt", i).strip())    #총매수체결금액
        tax         = int(inXAQuery.GetFieldData(OUTBLOCK, "tax", i).strip())       #추정제세금
        cts_ordno   = inXAQuery.GetFieldData(OUTBLOCK, "cts_ordno", i).strip()      #주문번호

        item['tqty']    = tqty
        item['tcheqty'] = tcheqty
        item['tordrem'] = tordrem
        item['cmss']    = cmss
        item['tamt']    = tamt
        item['tmdamt']  = tmdamt
        item['tmsamt']  = tmsamt
        item['tax']     = tax
        item['cts_ordno'] = cts_ordno

        result.append(item)

    result1 = []
    nCount1 = inXAQuery.GetBlockCount(OUTBLOCK1)

    for i in range(nCount1):
        item = {}
        ordno       = int(inXAQuery.GetFieldData(OUTBLOCK1, "ordno", i).strip())    #주문번호
        expcode     = inXAQuery.GetFieldData(OUTBLOCK1, "expcode", i).strip()       #종목번호
        medosu      = inXAQuery.GetFieldData(OUTBLOCK1, "medosu", i).strip()        #구분
        qty         = int(inXAQuery.GetFieldData(OUTBLOCK1, "qty", i).strip())      #주문수량
        price0425   = int(inXAQuery.GetFieldData(OUTBLOCK1, "price", i).strip())    #주문가격
        cheqty      = int(inXAQuery.GetFieldData(OUTBLOCK1, "cheqty", i).strip())   #체결수량
        cheprice    = int(inXAQuery.GetFieldData(OUTBLOCK1, "cheprice", i).strip()) #체결가격
        ordrem      = int(inXAQuery.GetFieldData(OUTBLOCK1, "ordrem", i).strip())   #미체결잔량
        cfmqty      = int(inXAQuery.GetFieldData(OUTBLOCK1, "cfmqty", i).strip())   #확인수량
        status      = inXAQuery.GetFieldData(OUTBLOCK1, "status", i).strip()        #상태
        orgordno    = int(inXAQuery.GetFieldData(OUTBLOCK1, "orgordno", i).strip()) #원주문번호
        ordgb       = inXAQuery.GetFieldData(OUTBLOCK1, "ordgb", i).strip()         #유형
        ordtime     = inXAQuery.GetFieldData(OUTBLOCK1, "ordtime", i).strip()       #주문시간
        ordermtd    = inXAQuery.GetFieldData(OUTBLOCK1, "ordermtd", i).strip()      #주문매체
        sysprocseq  = int(inXAQuery.GetFieldData(OUTBLOCK1, "sysprocseq", i).strip())#처리순번
        hogagb      = inXAQuery.GetFieldData(OUTBLOCK1, "hogagb", i).strip()        #호가유형
        price10425  = int(inXAQuery.GetFieldData(OUTBLOCK1, "price1", i).strip())   #현재가
        orggb       = inXAQuery.GetFieldData(OUTBLOCK1, "orggb", i).strip()         #주문구분
        singb       = inXAQuery.GetFieldData(OUTBLOCK1, "singb", i).strip()         #신용구분
        loandt      = inXAQuery.GetFieldData(OUTBLOCK1, "loandt", i).strip()        #대출일자

        item['ordno']       = ordno
        item['expcode']     = expcode
        item['medosu']      = medosu
        item['qty']         = qty
        item['price0425']   = price0425
        item['cheqty']      = cheqty
        item['cheprice']    = cheprice
        item['ordrem']      = ordrem
        item['cfmqty']      = cfmqty
        item['status']      = status
        item['orgordno']    = orgordno
        item['ordgb']       = ordgb
        item['ordtime']     = ordtime
        item['ordermtd']    = ordermtd
        item['sysprocseq']  = sysprocseq
        item['hogagb']      = hogagb
        item['price10425']  = price10425
        item['orggb']       = orggb
        item['singb']       = singb
        item['loandt']      = loandt

        result1.append(item)


    XAQueryEvents.queryState = False

    return result, result1




