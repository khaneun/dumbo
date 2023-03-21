import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("00700")

###############################
# CSPAT00700 현물계좌 주문 정정
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

def CSPAT00700(
        OrgOrdNo = '',          # 원주문번호
        AcntNo = '',            # 계좌번호
        InptPwd = '',           # 입력비밀번호
        IsuNo = '',             # 종목번호
        OrdQty = '',            # 주문 수량
        OrdprcPtnCode = '',     # 호가유형코드
        OrdCndiTpCode = '',     # 주문조건구분
        OrdPrc = ''             # 주문가
    ):
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAT00700.res")

    inXAQuery.SetFieldData("CSPAT00700InBlock1", "OrgOrdNo", 0, OrgOrdNo)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "AcntNo", 0, AcntNo)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "InptPwd", 0, InptPwd)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "IsuNo", 0, IsuNo)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "OrdQty", 0, OrdQty)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "OrdprcPtnCode", 0, OrdprcPtnCode)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "OrdCndiTpCode", 0, OrdCndiTpCode)
    inXAQuery.SetFieldData("CSPAT00700InBlock1", "OrdPrc", 0, OrdPrc)

    return 0