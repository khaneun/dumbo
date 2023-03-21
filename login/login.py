import win32com.client
import pythoncom
from time import sleep
from config import dumbo_config
from common.logger import Logger
logger = Logger("LOGN")

class XASessionEvents:
    logInState = 0
    def OnLogin(self, code, msg):
        logger.info("OnLogin method is called [CODE " + str(code) + "] [MGS " + str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = 1

    def OnLogout(self):
        logger.info("OnLogout method is called")

    def OnDisconnect(self):
        logger.info("OnDisconnect method is called")

#접속할 서버정보와 본인의 계좌정보 셋팅~
env = dumbo_config.DUMBO['ENV']

if env == "demo":
    HOST= dumbo_config.DemoLogin["HOST"]
    PORT = dumbo_config.DemoLogin["PORT"]
    USER_ID = dumbo_config.DemoLogin["USER_ID"]
    USER_PWD = dumbo_config.DemoLogin["USER_PWD"]
    CERTIFICATE_PWD = dumbo_config.DemoLogin["CERTIFICATE_PWD"]
    ACCOUNT_PWD = dumbo_config.DemoLogin["ACCOUNT_PWD"]
    SERVER_TYPE = dumbo_config.DemoLogin["SERVER_TYPE"]
else:
    HOST = dumbo_config.RealLogin["HOST"]
    PORT = dumbo_config.RealLogin["PORT"]
    USER_ID = dumbo_config.RealLogin["USER_ID"]
    USER_PWD = dumbo_config.RealLogin["USER_PWD"]
    CERTIFICATE_PWD = dumbo_config.RealLogin["CERTIFICATE_PWD"]
    ACCOUNT_PWD = dumbo_config.RealLogin["ACCOUNT_PWD"]
    SERVER_TYPE = dumbo_config.RealLogin["SERVER_TYPE"]


inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)

def Logout():
    logger.info("Logout 합니다.")
    inXASession.Logout()
    inXASession.DisconnectServer()

def Login():

    if(inXASession.IsConnected()):
        inXASession.Logout()
        inXASession.DisconnectServer()

    result = inXASession.ConnectServer(HOST, PORT)

    inXASession.Login(USER_ID, USER_PWD, CERTIFICATE_PWD, SERVER_TYPE, 0)

    while XASessionEvents.logInState == 0:
        pythoncom.PumpWaitingMessages()

    if env == "demo":
        user_account = inXASession.GetAccountList(0)  # 모의서버일 경우 선물,주식 둘다
    else:
        user_account = inXASession.GetAccountList(1)
        # 나의 리얼계좌는 두번째꺼 사용
        # 0 : 20143559401
        # 1 : 20336283401

    logger.info("계좌번호===>"+str(user_account))
    return user_account, ACCOUNT_PWD