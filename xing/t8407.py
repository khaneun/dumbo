import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("8407")

###############################
#     주식 멀티 현재가 조회
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("t8436 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t8436 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode



def listJongMok(gubun):
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8436.res")

    inXAQuery.SetFieldData( "t8436InBlock", "gubun", 0, gubun )
    succsess = inXAQuery.Request( True )

    #while XAQueryEvents.queryState == 0:
    #    pythoncom.PumpWaitingMessages()

    result = []

    nCount = inXAQuery.GetBlockCount("t8436OutBlock")
    for i in range(nCount):
        shcode = inXAQuery.GetFieldData("t8436OutBlock", "shcode", i)  # 종목코드
        hname = inXAQuery.GetFieldData("t8436OutBlock", "hname", i)  # 종목명
        uplmtprice = inXAQuery.GetFieldData("t8436OutBlock", "uplmtprice", i)  # 상한가
        dnlmtprice = inXAQuery.GetFieldData("t8436OutBlock", "dnlmtprice", i)  # 하한가
        recprice = inXAQuery.GetFieldData("t8436OutBlock", "recprice", i)  # 기준가
        jnilclose = inXAQuery.GetFieldData("t8436OutBlock", "jnilclose", i)  # 기준가



        result.append(shcode)
        result.append(hname)
        result.append(uplmtprice)
        result.append(dnlmtprice)
        result.append(recprice)
        result.append(jnilclose)


    XAQueryEvents.queryState = 0
    XAQueryEvents.resultCode = 0

    return result




