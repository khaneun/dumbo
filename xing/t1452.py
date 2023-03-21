import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("1452")

###############################
# 거래량 상위 종목 조회
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("t1452 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("t1452 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode

def t1452(
    gubun = '0',        # 구분        0:전체  1:코스피  2:코스닥
    jnilgubun = '1',    # 전일구분     1:당일  2:전일
    sdiff = '',         # 시작등락율
    ediff = '',         # 종료등락율
    jc_num = '',        # 대상제외
    sprice = '',        # 시작가격
    eprice = '',        # 종료가격
    volume = '',        # 거래량
    idx = ''            # IDX
    ):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1452.res")

    ###############################
    # gubun
    # 0 : 전체
    # 1 : 코스피
    # 2 : 코스닥
    ###############################
    inXAQuery.SetFieldData("t1452InBlock", "gubun",     0, gubun)
    inXAQuery.SetFieldData("t1452InBlock", "jnilgubun", 0, jnilgubun)
    succsess = inXAQuery.Request(True)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    nCount = inXAQuery.GetBlockCount("t1452OutBlock1")

    result = []
    for i in range(nCount):
        item = {}
        hname       = inXAQuery.GetFieldData("t1452OutBlock1", "hname",    i).strip()  # 종목명
        price       = inXAQuery.GetFieldData("t1452OutBlock1", "price",    i).strip()  # 현재가
        sign        = inXAQuery.GetFieldData("t1452OutBlock1", "sign",     i).strip()  # 전일대비구분
        change      = inXAQuery.GetFieldData("t1452OutBlock1", "change",   i).strip()  # 전일대비
        diff        = inXAQuery.GetFieldData("t1452OutBlock1", "diff",     i).strip()  # 등락율
        volume      = inXAQuery.GetFieldData("t1452OutBlock1", "volume",   i).strip()  # 누적거래량
        vol         = inXAQuery.GetFieldData("t1452OutBlock1", "vol",      i).strip()  # 회전율
        jnilvolume  = inXAQuery.GetFieldData("t1452OutBlock1", "jnilvolume", i).strip()  # 전일거래량
        bef_diff    = inXAQuery.GetFieldData("t1452OutBlock1", "bef_diff", i).strip()  # 전일비
        shcode      = inXAQuery.GetFieldData("t1452OutBlock1", "shcode",   i).strip()  # 종목코드

        item['hname']       = hname
        item['price']       = price
        item['sign']        = sign
        item['change']      = change
        item['diff']        = diff
        item['volume']      = volume
        item['vol']         = vol
        item['jnilvolume']  = jnilvolume
        item['bef_diff']    = bef_diff
        item['shcode']      = shcode
        item['item_code']   = shcode
        item['item_name']   = hname
        item['reperence_price'] = price

        result.append(item)

    XAQueryEvents.queryState = 0

    return result