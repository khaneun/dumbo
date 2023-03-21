import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("00800")

###############################
# CSPAT00800 현물계좌 주문 취소
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("CSPAT00800 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("CSPAT00800 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode

def CSPAT00800(
        OrgOrdNo='',
        accountNo='',
        password='',
        securityNo='',
        OrdQty='0'):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00800.res")

    inXAQuery.SetFieldData("CSPAT00800InBlock1", "OrgOrdNo",    0, OrgOrdNo)
    inXAQuery.SetFieldData("CSPAT00800InBlock1", "AcntNo",      0, accountNo)
    inXAQuery.SetFieldData("CSPAT00800InBlock1", "InptPwd",     0, password)
    inXAQuery.SetFieldData("CSPAT00800InBlock1", "IsuNo",       0, securityNo)
    inXAQuery.SetFieldData("CSPAT00800InBlock1", "OrdQty",      0, OrdQty)

    succsess = inXAQuery.Request(True)

    #while XAQueryEvents.queryState == 0:
    #    pythoncom.PumpWaitingMessages()

    result = []
    nCount1 = inXAQuery.GetBlockCount("CSPAT00800OutBlock1")
    nCount2 = inXAQuery.GetBlockCount("CSPAT00800OutBlock2")

