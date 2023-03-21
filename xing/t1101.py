import win32com.client
import pythoncom
from common.logger import Logger

logger = Logger("1101")


###############################
#     호가 정보 조회 TR
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0

    def OnReceiveData(self, szTrCode):
        #logger.info("t1101 ReceiveData====>szTrCode[" + str(szTrCode) + "]")
        XAQueryEvents.queryState = 1

    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t1101 ReceiveMessage====>systemError[" + str(systemError) + "], mesageCode[" + str(
            mesageCode) + "], message[" + message + "]")
        XAQueryEvents.resultCode = mesageCode

def t1101(
        shcode = ''
    ):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1101.res")

    inXAQuery.SetFieldData("t1101InBlock", "shcode", 0, shcode)
    succsess = inXAQuery.Request(True)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    nCount = inXAQuery.GetBlockCount("t1101OutBlock")
    result = []

    for i in range(nCount):
        item = {}

        hname       = inXAQuery.GetFieldData("t1101OutBlock", "hname",      i).strip()  # 한글명
        price       = inXAQuery.GetFieldData("t1101OutBlock", "price",      i).strip()  # 현재가
        offerho1    = inXAQuery.GetFieldData("t1101OutBlock", "offerho1",   i).strip()  # 매도호가1
        offerho2    = inXAQuery.GetFieldData("t1101OutBlock", "offerho2",   i).strip()  # 매도호가2
        offerho3    = inXAQuery.GetFieldData("t1101OutBlock", "offerho3",   i).strip()  # 매도호가3
        offerrem1   = inXAQuery.GetFieldData("t1101OutBlock", "offerrem1",  i).strip()  # 매도호가수량1
        offerrem2   = inXAQuery.GetFieldData("t1101OutBlock", "offerrem2",  i).strip()  # 매도호가수량2
        offerrem3   = inXAQuery.GetFieldData("t1101OutBlock", "offerrem3",  i).strip()  # 매도호가수량3
        bidho1      = inXAQuery.GetFieldData("t1101OutBlock", "bidho1",     i).strip()  # 매수호가1
        bidho2      = inXAQuery.GetFieldData("t1101OutBlock", "bidho2",     i).strip()  # 매수호가2
        bidho3      = inXAQuery.GetFieldData("t1101OutBlock", "bidho3",     i).strip()  # 매수호가3
        bidrem1     = inXAQuery.GetFieldData("t1101OutBlock", "bidrem1",    i).strip()  # 매수호가수량1
        bidrem2     = inXAQuery.GetFieldData("t1101OutBlock", "bidrem2",    i).strip()  # 매수호가수량2
        bidrem3     = inXAQuery.GetFieldData("t1101OutBlock", "bidrem3",    i).strip()  # 매수호가수량3

        item['hname'] = hname
        item['price'] = price
        item['offerho1'] = offerho1
        item['offerho2'] = offerho2
        item['offerho3'] = offerho3
        item['offerrem1'] = offerrem1
        item['offerrem2'] = offerrem2
        item['offerrem3'] = offerrem3
        item['bidho1'] = bidho1
        item['bidho2'] = bidho2
        item['bidho3'] = bidho3
        item['bidrem1'] = bidrem1
        item['bidrem2'] = bidrem2
        item['bidrem3'] = bidrem3

        result.append(item)

    XAQueryEvents.queryState = 0

    return result