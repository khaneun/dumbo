import win32com.client
import pythoncom
from config import dumbo_config
from common.logger import Logger
logger = Logger("8436")

###############################
#     주식종목 조회 TR
###############################

# ITEM_PRACE_HIGH = dumbo_config.DealInfo['ITEM_PRACE_HIGH']
ITEM_PRACE_LOW = dumbo_config.DealInfo['ITEM_PRACE_LOW']
BUYING_COUNT = dumbo_config.DealInfo['BUYING_COUNT']
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("t8436 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t8436 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode

def t8436(gubun):
    '''

    :param gubun:
    :param amt: 구매가능금액
    :return:
    '''
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8436.res")
    inBlock = "t8436InBlock"
    outBlock = "t8436OutBlock"

    inXAQuery.SetFieldData( inBlock, "gubun", 0, gubun )
    succsess = inXAQuery.Request( True )

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    allItemList = [];

    nCount = inXAQuery.GetBlockCount(outBlock)
    for i in range(nCount):
        item={}
        shcode      = inXAQuery.GetFieldData(outBlock, "shcode",        i)  # 종목코드
        hname       = inXAQuery.GetFieldData(outBlock, "hname",         i)  # 종목명
        uplmtprice  = inXAQuery.GetFieldData(outBlock, "uplmtprice",    i)  # 상한가
        dnlmtprice  = inXAQuery.GetFieldData(outBlock, "dnlmtprice",    i)  # 하한가
        recprice    = inXAQuery.GetFieldData(outBlock, "recprice",      i)  # 기준가
        jnilclose   = inXAQuery.GetFieldData(outBlock, "jnilclose",     i)  # 전일기준가

        item['item_code'] = shcode
        item['item_name'] = hname
        item['up_price'] = uplmtprice
        item['down_price'] = dnlmtprice
        item['reperence_price'] = recprice
        item['closing_price'] = jnilclose

        allItemList.append(item)

    XAQueryEvents.queryState = 0
    XAQueryEvents.resultCode = 0

    return allItemList




