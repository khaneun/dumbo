import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("13700")

###############################
#     CSPAQ13700 현물계좌 주식체결 내역 조회
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = True
    def OnReceiveData(self, szTrCode):
        #logger.info("CSPAQ13700 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        if str(mesageCode) != '00136':
            logger.info("CSPAQ13700 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = True

        # 임시 처리
        if str(mesageCode).lstrip() == '-21':
            XAQueryEvents.queryState = 1        # TR의 시간당 전송제한에 걸렸습니다.
            XAQueryEvents.resultCode = False

        if str(mesageCode).lstrip() == '-34': # 34 TR의 10분당 최대 전송 가능 횟수를 초과하였습니다. 이후부터는 전송가능횟수가 5배로 제한됩니다

            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

def CSPAQ13700(
        accountNo='',
        password='',
        securityNo='',
        OrdDt='',
        BnsTpCode='0',
        ExecYn='0'):

    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ13700.res")

    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "RecCnt", 0, "00001")
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "AcntNo", 0, accountNo)
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "InptPwd", 0, password)
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "OrdMktCode", 0, "00")
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "BnsTpCode", 0, BnsTpCode) # 매매구분 0: 전체 1 : 매도 2 : 매수
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "IsuNo", 0, securityNo)

    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "ExecYn", 0, ExecYn)  # 0: 전체 1: 체결 2: 미체결
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "OrdDt", 0, OrdDt)
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "SrtOrdNo2", 0, "999999999")
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "BkseqTpCode", 0, "0")
    inXAQuery.SetFieldData("CSPAQ13700InBlock1", "OrdPtnCode", 0, "00")

    succsess = inXAQuery.Request(0)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount1 = inXAQuery.GetBlockCount("CSPAQ13700OutBlock1")
    nCount2 = inXAQuery.GetBlockCount("CSPAQ13700OutBlock2")
    nCount3 = inXAQuery.GetBlockCount("CSPAQ13700OutBlock3")

    for i in range(nCount3):
        item = {}

        OrdDt           = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdDt",            i).strip() # 주문일
        MgmtBrnNo       = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MgmtBrnNo",        i).strip() # 관리지점번호
        OrdMktCode      = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdMktCode",       i).strip() # 주문시장코드
        OrdNo           = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdNo",            i).strip() # 주문번호
        OrgOrdNo        = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrgOrdNo",         i).strip() # 원주문번호
        IsuNo           = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "IsuNo",            i).strip() # 종목번호
        IsuNm           = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "IsuNm",            i).strip() # 종목명
        BnsTpCode       = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "BnsTpCode",        i).strip() # 매매구분
        BnsTpNm         = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "BnsTpNm",          i).strip() # 매매구분명
        OrdPtnCode      = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdPtnCode",       i).strip() # 주문유형코드
        OrdPtnNm        = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdPtnNm",         i).strip() # 주문유형명
        OrdTrxPtnCode   = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdTrxPtnCode",    i).strip() # 주문처리유형코드
        OrdTrxPtnNm     = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdTrxPtnNm",      i).strip() # 주문처리유형명
        MrcTpCode       = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MrcTpCode",        i).strip() # 정정취소구분
        MrcTpNm         = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MrcTpNm",          i).strip() # 정정취소구분명
        MrcQty          = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MrcQty",           i).strip() # 정정취소수량
        MrcAbleQty      = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MrcAbleQty",       i).strip() # 정정취소가능수량
        OrdQty          = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdQty",           i).strip() # 주문수량
        OrdPrc          = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdPrc",           i).strip() # 주문가격
        ExecQty         = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "ExecQty",          i).strip() # 체결수량
        ExecPrc         = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "ExecPrc",          i).strip() # 체결가
        ExecTrxTime     = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "ExecTrxTime",      i).strip() # 체결처리시각
        LastExecTime    = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "LastExecTime",     i).strip() # 최종체결시각
        OrdprcPtnCode   = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdprcPtnCode",    i).strip() # 호가유형코드
        OrdprcPtnNm     = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdprcPtnNm",      i).strip() # 호가유형명
        OrdCndiTpCode   = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdCndiTpCode",    i).strip() # 주문조건구분
        AllExecQty      = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "AllExecQty",       i).strip() # 전체체결수량
        RegCommdaCode   = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "RegCommdaCode",    i).strip() # 통신매체코드
        CommdaNm        = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "CommdaNm",         i).strip() # 통신매체명
        MbrNo           = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "MbrNo",            i).strip() # 회원번호
        RsvOrdYn        = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "RsvOrdYn",         i).strip() # 예약주문여부
        LoanDt          = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "LoanDt",           i).strip() # 대출일
        OrdTime         = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OrdTime",          i).strip() # 주문시각
        OpDrtnNo        = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OpDrtnNo",         i).strip() # 운용지시번호
        OdrrId          = inXAQuery.GetFieldData("CSPAQ13700OutBlock3", "OdrrId",           i).strip() # 주문자ID

        item['OrdDt']           = OrdDt
        item['MgmtBrnNo']       = MgmtBrnNo
        item['OrdMktCode']      = OrdMktCode
        item['OrdNo']           = OrdNo
        item['OrgOrdNo']        = OrgOrdNo
        item['IsuNo']           = IsuNo
        item['IsuNm']           = IsuNm
        item['BnsTpCode']       = BnsTpCode
        item['BnsTpNm']         = BnsTpNm
        item['OrdPtnCode']      = OrdPtnCode
        item['OrdPtnNm']        = OrdPtnNm
        item['OrdTrxPtnCode']   = OrdTrxPtnCode
        item['OrdTrxPtnNm']     = OrdTrxPtnNm
        item['MrcTpCode']       = MrcTpCode
        item['MrcTpNm']         = MrcTpNm
        item['MrcQty']          = MrcQty
        item['MrcAbleQty']      = MrcAbleQty
        item['OrdQty']          = OrdQty
        item['OrdPrc']          = OrdPrc
        item['ExecQty']         = ExecQty
        item['ExecPrc']         = ExecPrc
        item['ExecTrxTime']     = ExecTrxTime
        item['LastExecTime']    = LastExecTime
        item['OrdprcPtnCode']   = OrdprcPtnCode
        item['OrdprcPtnNm']     = OrdprcPtnNm
        item['OrdCndiTpCode']   = OrdCndiTpCode
        item['AllExecQty']      = AllExecQty
        item['RegCommdaCode']   = RegCommdaCode
        item['CommdaNm']        = CommdaNm
        item['MbrNo']           = MbrNo
        item['RsvOrdYn']        = RsvOrdYn
        item['LoanDt']          = LoanDt
        item['OrdTime']         = OrdTime
        item['OpDrtnNo']        = OpDrtnNo
        item['OdrrId']          = OdrrId

        result.append(item)

    XAQueryEvents.queryState = 0

    return XAQueryEvents.resultCode, result


def getListTradingHistory(accno,passwd):
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ13700.res")

    inXAQuery.SetFieldData( "CSPAQ13700InBlock", "accno", 0, accno )
    inXAQuery.SetFieldData("CSPAQ13700InBlock", "passwd", 0, passwd)
    # inXAQuery.SetFieldData("t0424InBlock", "prcgb", 0, prcgb)
    # inXAQuery.SetFieldData("t0424InBlock", "dangb", 0, dangb)
    succsess = inXAQuery.Request( True )

    #while XAQueryEvents.queryState == 0:
    #    pythoncom.PumpWaitingMessages()

    result = []

    nCount = inXAQuery.GetBlockCount("CSPAQ13700OutBlock3")
    for i in range(nCount):
        sunamt = inXAQuery.GetFieldData("CSPAQ13700OutBlock", "sunamt", 0)  # 추정순자산
        dtsunik = inXAQuery.GetFieldData("CSPAQ13700OutBlock", "dtsunik", 0)  # 실현손익
        mamt = inXAQuery.GetFieldData("CSPAQ13700OutBlock", "mamt", 0)  # 매입금액
        tappamt = inXAQuery.GetFieldData("CSPAQ13700OutBlock", "tappamt", 0)  # 평가금액
        tdtsunik = inXAQuery.GetFieldData("CSPAQ13700OutBlock", "tdtsunik", 0)  # 평가손익

        # 자산 = 자본 + 부채
        #     = 잔고 + (주식 + 평가금액)
        result.append(sunamt)
        result.append(tappamt)
        result.append(tdtsunik)

    XAQueryEvents.queryState = 0
    XAQueryEvents.resultCode = 0

    return result




