# -*- coding: utf-8 -*-
import logging.handlers
import os
from datetime import date

class Setting:

    """로거 세팅 클래스
        ::
            Setting.LEVEL = logging.INFO # INFO 이상만 로그를 작성
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_date= date.today()
    current_file = os.path.basename(__file__)
    current_file_name = current_file[:-3]  # xxxx.py
    FILENAME = 'myDumboLog2-{}-{}'.format(current_file_name,current_date)

    # 로그 저장할 폴더 생성
    log_dir = '{}/logs'.format(current_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    LEVEL = logging.DEBUG
    #FILENAME = "myDumbo.log"
    MAX_BYTES = 5000 * 1024 * 1024
    BACKUP_COUNT = 10
    FORMAT = "%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s"
    LOG_FILEPATH=os.path.join(log_dir, FILENAME)

def Logger(name):
    """파일 로그 클래스
        :param name: 로그 이름
        :type name: str
        :return: 로거 인스턴스
        ::
            logger = Logger(__name__)
            logger.info('info 입니다')
    """

    # 로거 & 포매터 & 핸들러 생성
    logger = logging.getLogger(name)
    formatter = logging.Formatter(Setting.FORMAT)
    streamHandler = logging.StreamHandler()
    fileHandler = logging.handlers.TimedRotatingFileHandler(
        filename=Setting.LOG_FILEPATH,
        when='midnight',
        backupCount=Setting.BACKUP_COUNT)

    # 핸들러 & 포매터 결합
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 로거 & 핸들러 결합
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    # 로거 레벨 설정
    logger.setLevel(Setting.LEVEL)

    return logger


