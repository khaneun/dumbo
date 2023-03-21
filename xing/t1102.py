import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("1102")

###############################
#     현재가 조회 TR
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("t1102 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t1102 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode


def nowPrice(shcode):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1102.res")

    inXAQuery.SetFieldData( "t1102InBlock", "shcode", 0, shcode )
    succsess = inXAQuery.Request( True )

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    result = {}

    nCount = inXAQuery.GetBlockCount("t1102OutBlock")
    for i in range(nCount):

        shcode      = inXAQuery.GetFieldData("t1102OutBlock", "shcode", 0)  # 종목코드
        hname       = inXAQuery.GetFieldData("t1102OutBlock", "hname", 0)  # 종목명
        price       = inXAQuery.GetFieldData("t1102OutBlock", "price", 0)  # 현재가
        rate        = inXAQuery.GetFieldData("t1102OutBlock", "diff", 0)  # 등락율
        high52w     = inXAQuery.GetFieldData("t1102OutBlock", "high52w", 0)  # 52주최고가
        high52wdate = inXAQuery.GetFieldData("t1102OutBlock", "high52wdate", 0)  # 52주최고가일자
        volume      = inXAQuery.GetFieldData("t1102OutBlock", "volume", 0)  # 누적거래량
        open        = inXAQuery.GetFieldData("t1102OutBlock", "open", 0)  # 시가

        result['price'] = price
        #result.append({"price", price})
        #result.append({"rate", rate})
        #result.append({"open", open})


    XAQueryEvents.queryState = 0
    XAQueryEvents.resultCode = 0

    return result




