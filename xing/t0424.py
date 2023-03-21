import win32com.client
import pythoncom
from common.utils import drawLine
from common.logger import Logger
logger = Logger("0424")

###############################
# 잔고 조회 TR
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = True
    def OnReceiveData(self, szTrCode):
        #logger.info("[" + str(szTrCode) +"] ReceiveData")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("[t0424] ReceiveMessage : systemError["+str(systemError)+"] mesageCode["+str(mesageCode)+"] message["+message+"]")
        #XAQueryEvents.resultCode = mesageCode

        # 임시 처리
        if (str(mesageCode).lstrip() == '-21'):  # 21
            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

        if (str(mesageCode).lstrip() == '-34'):  # 34 TR의 10분당 최대 전송 가능 횟수를 초과하였습니다. 이후부터는 전송가능횟수가 5배로 제한됩니다

            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

def getJanGo(accountNo,password):
    inXAQuery   = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t0424.res")
    inblock     = "t0424InBlock"
    outBlock    = "t0424OutBlock"
    outBlock1   = "t0424OutBlock1"

    inXAQuery.SetFieldData(inblock, "accno",    0, accountNo)
    inXAQuery.SetFieldData(inblock, "passwd",   0, password)

    # inXAQuery.SetFieldData("t0424InBlock", "prcgb", 0, prcgb)
    # inXAQuery.SetFieldData("t0424InBlock", "dangb", 0, dangb)
    succsess = inXAQuery.Request( True )

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    myAsset = []

    nCount  = inXAQuery.GetBlockCount(outBlock)
    nCount1 = inXAQuery.GetBlockCount(outBlock1)

    ################################
    # 자산 조회
    ################################
    for i in range(nCount):
        item = {}
        sunamt      = inXAQuery.GetFieldData(outBlock, "sunamt",    i)   # 추정순자산
        dtsunik     = inXAQuery.GetFieldData(outBlock, "dtsunik",   i)   # 실현손익
        sunamt1     = inXAQuery.GetFieldData(outBlock, "sunamt1",   i)   # 추정 D2 예수금

        mamt        = inXAQuery.GetFieldData(outBlock, "mamt",      i)   # 매입금액
        tappamt     = inXAQuery.GetFieldData(outBlock, "tappamt",   i)   # 평가금액
        tdtsunik    = inXAQuery.GetFieldData(outBlock, "tdtsunik",  i)   # 평가손익

        item['sunamt']  = sunamt
        item['dtsunik'] = dtsunik
        item['sunamt1'] = sunamt1
        item['mamt']    = mamt
        item['tappamt'] = tappamt
        item['tdtsunik']= tdtsunik

        myAsset.append(item)

    mySecurity = []

    ################################
    # 보유 종목 조회
    ################################
    for i in range(nCount1):
        item = {}
        expcode     = inXAQuery.GetFieldData(outBlock1, "expcode",  i)  # 종목번호
        hname       = inXAQuery.GetFieldData(outBlock1, "hname",    i)  # 종목명
        price       = inXAQuery.GetFieldData(outBlock1, "price",    i)  # 현재가
        janqty      = inXAQuery.GetFieldData(outBlock1, "janqty",   i)  # 잔고수량
        mdposqt     = inXAQuery.GetFieldData(outBlock1, "mdposqt",  i)  # 매도가능수량
        pamt        = inXAQuery.GetFieldData(outBlock1, "pamt",     i)  # 평균단가
        appamt      = inXAQuery.GetFieldData(outBlock1, "appamt",   i)  # 평가금액

        # 현재는 덜 중요한 변수
        jangb       = inXAQuery.GetFieldData(outBlock1, "jangb",    i)  # 잔고구분
        dtsunik     = inXAQuery.GetFieldData(outBlock1, "dtsunik",  i)  # 평균손익
        sininter    = inXAQuery.GetFieldData(outBlock1, "sininter", i)  # 신용이자
        mamt        = inXAQuery.GetFieldData(outBlock1, "mamt",     i)  # 매입금액
        sinamt      = inXAQuery.GetFieldData(outBlock1, "sinamt",   i)  # 대출금액

        item['hname']       = hname;
        item['expcode']     = expcode;
        item['price']       = price;
        item['janqty']      = janqty;
        item['mdposqt']     = mdposqt;
        item['pamt']        = pamt;
        item['appamt']      = appamt;

        item['jangb']       = jangb;
        item['dtsunik']     = dtsunik;
        item['sininter']    = sininter;
        item['mamt']        = mamt;
        item['sinamt']      = sinamt;

        mySecurity.append(item)

    XAQueryEvents.queryState = 0

    return myAsset, mySecurity




