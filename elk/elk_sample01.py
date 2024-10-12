import socket
import json
import time

# Logstash
HOST = '192.168.0.37'
PORT = 5044


# 로그 메시지 생성 함수
def send_log(message, level='INFO'):
    log_data = {
        "message": message,
        "level": level,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    log_json = json.dumps(log_data)
    log_json += '\n'  # json_lines codec을 위해 개행 추가

    # TCP 소켓 생성 및 Logstash로 로그 전송
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(log_json.encode('utf-8'))


if __name__ == "__main__":
    for i in range(5):
        message = f"테스트 로그 메시지 {i+1}"
        send_log(message)
        time.sleep(1)
        print('test')