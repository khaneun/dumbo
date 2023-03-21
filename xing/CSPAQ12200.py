import win32com.client
import pythoncom
from common.logger import Logger
logger = Logger("12200")

###############################
#    현물계좌 예수금/주문가능금액/총평가 조회(API)
###############################
class XAQueryEvents:
    queryState = 0
    resultCode = True
    def OnReceiveData(self, szTrCode):
        #logger.info("CSPAQ12200 ReceiveData====>szTrCode["+str(szTrCode)+"]")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        logger.info("CSPAQ12200 ReceiveMessage====>systemError["+str(systemError)+"], mesageCode["+str(mesageCode)+"], message["+message+"]")
        XAQueryEvents.resultCode = True

        # 임시 처리
        if( str(mesageCode).lstrip() == '-21'): # 21
            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

        if ( str(mesageCode).lstrip() == '-34'):  # 34 TR의 10분당 최대 전송 가능 횟수를 초과하였습니다. 이후부터는 전송가능횟수가 5배로 제한됩니다

            XAQueryEvents.queryState = 1
            XAQueryEvents.resultCode = False

def CSPAQ12200(accountNo, password):
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\CSPAQ12200.res")

    inXAQuery.SetFieldData("CSPAQ12200InBlock1", "RecCnt",  0, "1")
    inXAQuery.SetFieldData("CSPAQ12200InBlock1", "AcntNo",  0, accountNo)
    inXAQuery.SetFieldData("CSPAQ12200InBlock1", "Pwd",     0, password)

    succsess = inXAQuery.Request(0)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount1 = inXAQuery.GetBlockCount("CSPAQ12200OutBlock1")
    nCount2 = inXAQuery.GetBlockCount("CSPAQ12200OutBlock2")

    for i in range(nCount2):
        item = {}

        RecCnt              = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "RecCnt",              i).strip()  # 레코드갯수
        BrnNm               = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "BrnNm",               i).strip()  # 지점명
        AcntNm              = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "AcntNm",              i).strip()  # 계좌명
        MnyOrdAbleAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MnyOrdAbleAmt",       i).strip()  # 현금주문가능금액
        MnyoutAbleAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MnyoutAbleAmt",       i).strip()  # 출금가능금액
        SeOrdAbleAmt        = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "SeOrdAbleAmt",        i).strip()  # 거래소금액
        KdqOrdAbleAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "KdqOrdAbleAmt",       i).strip()  # 코스닥금액
        BalEvalAmt          = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "BalEvalAmt",          i).strip()  # 잔고평가금액
        RcvblAmt            = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "RcvblAmt",            i).strip()  # 미수금액
        DpsastTotamt        = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "DpsastTotamt",        i).strip()  # 예탁자산총액
        PnlRat              = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "PnlRat",              i).strip()  # 손익율
        InvstOrgAmt         = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "InvstOrgAmt",         i).strip()  # 투자원금
        InvstPlAmt          = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "InvstPlAmt",          i).strip()  # 투자손익금액
        CrdtPldgOrdAmt      = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtPldgOrdAmt",      i).strip()  # 신용담보주문금액
        Dps                 = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "Dps",                 i).strip()  # 예수금
        SubstAmt            = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "SubstAmt",            i).strip()  # 대용금액
        D1Dps               = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D1Dps",               i).strip()  # D1예수금
        D2Dps               = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D2Dps",               i).strip()  # D2예수금
        MnyrclAmt           = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MnyrclAmt",           i).strip()  # 현금미수금액
        MgnMny              = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MgnMny",              i).strip()  # 증거금현금
        MgnSubst            = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MgnSubst",            i).strip()  # 증거금대용
        ChckAmt             = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "ChckAmt",             i).strip()  # 수표금액
        SubstOrdAbleAmt     = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "SubstOrdAbleAmt",     i).strip()  # 대용주문가능금액
        MgnRat100pctOrdAbleAmt = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MgnRat100pctOrdAbleAmt",i).strip()  # 증거금률100퍼센트주문가능금액
        MgnRat35ordAbleAmt  = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MgnRat35ordAbleAmt",  i).strip()  # 증거금률35%주문가능금액
        MgnRat50ordAbleAmt  = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MgnRat50ordAbleAmt",  i).strip()  # 증거금률50%주문가능금액
        PrdaySellAdjstAmt   = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "PrdaySellAdjstAmt",   i).strip()  # 전일매도정산금액
        PrdayBuyAdjstAmt    = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "PrdayBuyAdjstAmt",    i).strip()  # 전일매수정산금액
        CrdaySellAdjstAmt   = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdaySellAdjstAmt",   i).strip()  # 금일매도정산금액
        CrdayBuyAdjstAmt    = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdayBuyAdjstAmt",    i).strip()  # 금일매수정산금액
        D1ovdRepayRqrdAmt   = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D1ovdRepayRqrdAmt",   i).strip()  # D1연체변제소요금액
        D2ovdRepayRqrdAmt   = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D2ovdRepayRqrdAmt",   i).strip()  # D2연체변제소요금액
        D1PrsmptWthdwAbleAmt = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D1PrsmptWthdwAbleAmt",i).strip()  # D1추정인출가능금액
        D2PrsmptWthdwAbleAmt = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D2PrsmptWthdwAbleAmt",i).strip()  # D2추정인출가능금액
        DpspdgLoanAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "DpspdgLoanAmt",       i).strip()  # 예탁담보대출금액
        Imreq               = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "Imreq",               i).strip()  # 신용설정보증금
        MloanAmt            = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "MloanAmt",            i).strip()  # 융자금액
        ChgAfPldgRat        = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "ChgAfPldgRat",        i).strip()  # 변경후담보비율
        OrgPldgAmt          = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "OrgPldgAmt",          i).strip()  # 원담보금액
        SubPldgAmt          = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "SubPldgAmt",          i).strip()  # 부담보금액
        RqrdPldgAmt         = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "RqrdPldgAmt",         i).strip()  # 소요담보금액
        OrgPdlckAmt         = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "OrgPdlckAmt",         i).strip()  # 원담보부족금액
        PdlckAmt            = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "PdlckAmt",            i).strip()  # 담보부족금액
        AddPldgMny          = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "AddPldgMny",          i).strip()  # 추가담보현금
        D1OrdAbleAmt        = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "D1OrdAbleAmt",        i).strip()  # D1주문가능금액
        CrdtIntdltAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtIntdltAmt",       i).strip()  # 신용이자미납금액
        EtclndAmt           = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "EtclndAmt",           i).strip()  # 기타대여금액
        NtdayPrsmptCvrgAmt  = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "NtdayPrsmptCvrgAmt",  i).strip()  # 익일추정반대매매금액
        OrgPldgSumAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "OrgPldgSumAmt",       i).strip()  # 원담보합계금액
        CrdtOrdAbleAmt      = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtOrdAbleAmt",      i).strip()  # 신용주문가능금액
        SubPldgSumAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "SubPldgSumAmt",       i).strip()  # 부담보합계금액
        CrdtPldgAmtMny      = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtPldgAmtMny",      i).strip()  # 신용담보금현금
        CrdtPldgSubstAmt    = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtPldgSubstAmt",    i).strip()  # 신용담보대용금액
        AddCrdtPldgMny      = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "AddCrdtPldgMny",      i).strip()  # 추가신용담보현금
        CrdtPldgRuseAmt     = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CrdtPldgRuseAmt",     i).strip()  # 신용담보재사용금액
        AddCrdtPldgSubst    = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "AddCrdtPldgSubst",    i).strip()  # 추가신용담보대용
        CslLoanAmtdt1       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "CslLoanAmtdt1",       i).strip()  # 매도대금담보대출금액
        DpslRestrcAmt       = inXAQuery.GetFieldData("CSPAQ12200OutBlock2", "DpslRestrcAmt",       i).strip()  # 처분제한금액

        item['RecCnt']              = RecCnt
        item['BrnNm']               = BrnNm
        item['AcntNm']              = AcntNm
        item['MnyOrdAbleAmt']       = MnyOrdAbleAmt
        item['MnyoutAbleAmt']       = MnyoutAbleAmt
        item['SeOrdAbleAmt']        = SeOrdAbleAmt
        item['KdqOrdAbleAmt']       = KdqOrdAbleAmt
        item['BalEvalAmt']          = BalEvalAmt
        item['RcvblAmt']            = RcvblAmt
        item['DpsastTotamt']        = DpsastTotamt
        item['PnlRat']              = PnlRat
        item['InvstOrgAmt']         = InvstOrgAmt
        item['InvstPlAmt']          = InvstPlAmt
        item['CrdtPldgOrdAmt']      = CrdtPldgOrdAmt
        item['Dps']                 = Dps
        item['SubstAmt']            = SubstAmt
        item['D1Dps']               = D1Dps
        item['D2Dps']               = D2Dps
        item['MnyrclAmt']           = MnyrclAmt
        item['MgnMny']              = MgnMny
        item['MgnSubst']            = MgnSubst
        item['ChckAmt']             = ChckAmt
        item['SubstOrdAbleAmt']     = SubstOrdAbleAmt
        item['MgnRat100pctOrdAbleAmt'] = MgnRat100pctOrdAbleAmt
        item['MgnRat35ordAbleAmt']  = MgnRat35ordAbleAmt
        item['MgnRat50ordAbleAmt']  = MgnRat50ordAbleAmt
        item['PrdaySellAdjstAmt']   = PrdaySellAdjstAmt
        item['PrdayBuyAdjstAmt']    = PrdayBuyAdjstAmt
        item['CrdaySellAdjstAmt']   = CrdaySellAdjstAmt
        item['CrdayBuyAdjstAmt']    = CrdayBuyAdjstAmt
        item['D1ovdRepayRqrdAmt']   = D1ovdRepayRqrdAmt
        item['D2ovdRepayRqrdAmt']   = D2ovdRepayRqrdAmt
        item['D1PrsmptWthdwAbleAmt'] = D1PrsmptWthdwAbleAmt
        item['D2PrsmptWthdwAbleAmt'] = D2PrsmptWthdwAbleAmt
        item['DpspdgLoanAmt']       = DpspdgLoanAmt
        item['Imreq']               = Imreq
        item['MloanAmt']            = MloanAmt
        item['ChgAfPldgRat']        = ChgAfPldgRat
        item['OrgPldgAmt']          = OrgPldgAmt
        item['SubPldgAmt']          = SubPldgAmt
        item['RqrdPldgAmt']         = RqrdPldgAmt
        item['OrgPdlckAmt']         = OrgPdlckAmt
        item['PdlckAmt']            = PdlckAmt
        item['AddPldgMny']          = AddPldgMny
        item['D1OrdAbleAmt']        = D1OrdAbleAmt
        item['CrdtIntdltAmt']       = CrdtIntdltAmt
        item['EtclndAmt']           = EtclndAmt
        item['NtdayPrsmptCvrgAmt']  = NtdayPrsmptCvrgAmt
        item['OrgPldgSumAmt']       = OrgPldgSumAmt
        item['CrdtOrdAbleAmt']      = CrdtOrdAbleAmt
        item['SubPldgSumAmt']       = SubPldgSumAmt
        item['CrdtPldgAmtMny']      = CrdtPldgAmtMny
        item['CrdtPldgSubstAmt']    = CrdtPldgSubstAmt
        item['AddCrdtPldgMny']      = AddCrdtPldgMny
        item['CrdtPldgRuseAmt']     = CrdtPldgRuseAmt
        item['AddCrdtPldgSubst']    = AddCrdtPldgSubst
        item['CslLoanAmtdt1']       = CslLoanAmtdt1
        item['DpslRestrcAmt']       = DpslRestrcAmt

        result.append(item)

    XAQueryEvents.queryState = 0

    return XAQueryEvents.resultCode, result

