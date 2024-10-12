import logging
import time

# 로거 설정
logger = logging.getLogger('python-filebeat-logger')
logger.setLevel(logging.INFO)

# 파일 핸들러 생성
file_handler = logging.FileHandler('application.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# 예시 로그 메시지 전송
if __name__ == "__main__":
    for i in range(5):
        message = f"테스트 로그 메시지 {i+1}"
        logger.info(message)
        time.sleep(1)