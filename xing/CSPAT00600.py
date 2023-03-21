import win32com.client
import pythoncom
import inspect, os, sys
from common.logger import Logger
logger = Logger("00600")

###############################
#     현물 주문
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = 0
    def OnReceiveData(self, szTrCode):
        #logger.info("CSPAT00600 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("CSPAT00600 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = mesageCode

def outBlock3():
    return 0

def CSPAT00600(accno,password,
               securityCode,
               securityAmount,
               securityPrice,
               longShrotType,
               priceType,
               creditTransCode,
               OrderConditionType):
    ###############################
    # 변수 설명
    # accno             :   계좌번호
    # password          :   계좌 비밀번호
    # securityCode      :   종목 코드
    # securityAmount    :   수량
    # securityPrice     :   가격
    # longShrotType     :   매매구분 (1 : 매도 2 : 매수)
    # priceType         :   호가 구분 코드
    # creditTransCode   :   신용 거래 코드
    # OrderConditionType:   주문 조건 코드
    ###############################
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    INBLOCK1 = "%sInBlock1" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    OUTBLOCK2 = "%sOutBlock2" % MYNAME
    RESFILE = "C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res"

    # print(MYNAME, RESFILE)

    inXAQuery.LoadFromResFile(RESFILE)
    inXAQuery.SetFieldData(INBLOCK1, "AcntNo", 0, accno)
    inXAQuery.SetFieldData(INBLOCK1, "InptPwd", 0, password)
    inXAQuery.SetFieldData(INBLOCK1, "IsuNo", 0, securityCode)
    inXAQuery.SetFieldData(INBLOCK1, "OrdQty", 0, securityAmount)
    inXAQuery.SetFieldData(INBLOCK1, "OrdPrc", 0, securityPrice)
    inXAQuery.SetFieldData(INBLOCK1, "BnsTpCode", 0, longShrotType)
    inXAQuery.SetFieldData(INBLOCK1, "OrdprcPtnCode", 0, priceType)
    inXAQuery.SetFieldData(INBLOCK1, "MgntrnCode", 0, creditTransCode)
    # query.SetFieldData(INBLOCK1, "LoanDt", 0, 대출일)
    inXAQuery.SetFieldData(INBLOCK1, "OrdCndiTpCode", 0, OrderConditionType)
    inXAQuery.Request(0)

    # 응답에 대한 처리 로직 필요
    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()
    #print(XAQueryEvents.queryState)

    result1 = []
    result2 = []

    nCount1 = inXAQuery.GetBlockCount("CSPAT00600OutBlock1")
    nCount2 = inXAQuery.GetBlockCount("CSPAT00600OutBlock2")

    for i in range(nCount1):
        item = {}

        result1.append(item)

    for i in range(nCount2):
        item = {}

        RecCnt      = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "RecCnt",       i).strip()  # 레코드갯수
        OrdNo       = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "OrdNo",        i).strip()  # 주문번호
        OrdTime     = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "OrdTime",      i).strip()  # 주문시각
        OrdMktCode  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "OrdMktCode",   i).strip()  # 주문시장코드
        OrdPtnCode  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "OrdPtnCode",   i).strip()  # 주문유형코드
        ShtnIsuNo   = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "ShtnIsuNo",    i).strip()  # 단축종목번호
        MgempNo     = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "MgempNo",      i).strip()  # 관리사원번호
        OrdAmt      = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "OrdAmt",       i).strip()  # 주문금액
        SpareOrdNo  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "SpareOrdNo",   i).strip()  # 예비주문번호
        CvrgSeqno   = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "CvrgSeqno",    i).strip()  # 반대매매일련번호
        RsvOrdNo    = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "RsvOrdNo",     i).strip()  # 예약주문번호
        SpotOrdQty  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "SpotOrdQty",   i).strip()  # 실물주문수량
        RuseOrdQty  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "RuseOrdQty",   i).strip()  # 재사용주문수량
        MnyOrdAmt   = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "MnyOrdAmt",    i).strip()  # 현금주문금액
        SubstOrdAmt = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "SubstOrdAmt",  i).strip()  # 대용주문금액
        RuseOrdAmt  = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "RuseOrdAmt",   i).strip()  # 재사용주문금액
        AcntNm      = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "AcntNm",       i).strip()  # 계좌명
        IsuNm       = inXAQuery.GetFieldData("CSPAT00600OutBlock2", "IsuNm",        i).strip()  # 종목명

        item['RecCnt']      = RecCnt
        item['OrdNo']       = OrdNo
        item['OrdTime']     = OrdTime
        item['OrdMktCode']  = OrdMktCode
        item['OrdPtnCode']  = OrdPtnCode
        item['ShtnIsuNo']   = ShtnIsuNo
        item['MgempNo']     = MgempNo
        item['OrdAmt']      = OrdAmt
        item['SpareOrdNo']  = SpareOrdNo
        item['CvrgSeqno']   = CvrgSeqno
        item['RsvOrdNo']    = RsvOrdNo
        item['SpotOrdQty']  = SpotOrdQty
        item['RuseOrdQty']  = RuseOrdQty
        item['MnyOrdAmt']   = MnyOrdAmt
        item['SubstOrdAmt'] = SubstOrdAmt
        item['RuseOrdAmt']  = RuseOrdAmt
        item['AcntNm']      = AcntNm
        item['IsuNm']       = IsuNm

        result2.append(item)


    return result2