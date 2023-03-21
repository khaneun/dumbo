import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("12300")

###############################
#    현물계좌 잔고내역 조회
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = True
    def OnReceiveData(self, szTrCode):
        #logger.info("CSPAQ12300 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        if str(mesageCode) != '00136':
            logger.info("CSPAQ12300 ReceiveMessage====>systemError[" + str(systemError) + "], mesageCode[" + str(mesageCode) + "], message[" + message + "]")
        XAQueryEvents.resultCode = True

        # 임시 처리
        if( str(mesageCode).lstrip() == '-21'): # 21
            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

        if ( str(mesageCode).lstrip() == '-34'):  # 34 TR의 10분당 최대 전송 가능 횟수를 초과하였습니다. 이후부터는 전송가능횟수가 5배로 제한됩니다

            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

def CSPAQ12300(accno,passwd):
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ12300.res")

    MnyOrdAbleAmt = -1
    RcvblAmt = -1

    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "RecCnt",  0, "1")
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "AcntNo",  0, accno)
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "Pwd",     0, passwd)

    # 실서버 추가 변수
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "BalCreTp",        0, "0")
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "CmsnAppTpCode",   0, "0")
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "D2balBaseQryTp",  0, "1")
    inXAQuery.SetFieldData("CSPAQ12300InBlock1", "UprcTpCode",      0, "0")

    succsess = inXAQuery.Request(0)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount1 = inXAQuery.GetBlockCount("CSPAQ12300OutBlock1")
    nCount2 = inXAQuery.GetBlockCount("CSPAQ12300OutBlock2")
    nCount3 = inXAQuery.GetBlockCount("CSPAQ12300OutBlock3") # 종목 리스트

    for i in range(nCount1):
        AcntNo = inXAQuery.GetFieldData("CSPAQ12300OutBlock1", "AcntNo", 0)

    for i in range(nCount2):
        if AcntNo == accno:
            RecCnt          = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "RecCnt",           i) # 레코드 갯수
            BrnNm           = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "BrnNm",            i) # 지점명
            AcntNm          = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "AcntNm",           i) # 계좌명
            MnyoutAbleAmt   = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "MnyoutAbleAmt",    i) # 출금 가능 금액
            MnyOrdAbleAmt   = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "MnyOrdAbleAmt",    i) # 현금 주문 가능 금액
            RcvblAmt        = inXAQuery.GetFieldData("CSPAQ12300OutBlock2", "RcvblAmt",         i) # 미수 금액
        # 자산 = 자본 + 부채
        #     = 잔고 + (주식 + 평가금액)

    itemList = [];
    for i in range(nCount3):
        item_temp={};
        IsuNm           = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "IsuNm",    i)      # 종목명
        IsuNo           = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "IsuNo",    i)      # 종목 번호
        #BalQty          = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "BalQty",  i)      # 잔고 수량
        SellAbleQty     = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "SellAbleQty", i)   # 매도 가능 잔고 수량
        AvrUprc         = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "AvrUprc",  i)      # 평균 단가
        NowPrc          = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "NowPrc",   i)      # 현재가
        EvalPnl         = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "EvalPnl",  i)      # 평가 손익
        PnlRat          = inXAQuery.GetFieldData("CSPAQ12300OutBlock3", "PnlRat",   i)      # 평가 손익 비율

        item_temp["IsuNm"] = IsuNm;
        item_temp["IsuNo"] = IsuNo;

        #item_temp["BalQty"] = BalQty;
        item_temp["SellAbleQty"] = SellAbleQty;
        item_temp["AvrUprc"] = AvrUprc;
        item_temp["NowPrc"] = NowPrc;
        item_temp["EvalPnl"] = EvalPnl;
        item_temp["PnlRat"] = PnlRat;

        itemList.append(item_temp)

    XAQueryEvents.queryState = 0

    return itemList



