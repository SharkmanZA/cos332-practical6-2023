import socket
from datetime import datetime, timedelta

HOST, PORT = '127.0.0.1', 1025
DAY = '30'
MONTH = '04'

DAYS =  [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def find_all_dates():
    list = []
    with open('days.txt', 'r') as f:
        f.seek(0)
        dates = f.readlines()
        for date in dates:
            parts =  date.split(' ')
            dates = parts[0].split('/')
            day   = dates[0]
            month = dates[1]
            event = parts[1]
            result = calculate(day, month)

            if result: list.append(event.strip())

    return list
#Multiply days by n-1 months then add current days and view if within buffer
def calculate(day, month):
    dayI = int(day)
    monthI = int(month)
    currDay = int(DAY)
    currMonth = int(MONTH)

    currDays = 0
    for i in range (currMonth-1):
        currDays += DAYS[i]
    currDays += currDay

    predictedDays = 0
    for i in range (monthI-1):
        predictedDays += DAYS[i]
    predictedDays += dayI
    return True if ((predictedDays - currDays <= 6 and predictedDays - currDays > 0) or (currDays - predictedDays <= 6 and currDays - predictedDays > 0)) else False


def send_email(events):
    if len(events) == 0:
        return
    

    
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((HOST,PORT))

    # my_socket.send(b'HELO jake@gmail.com\r\n')
    # response = my_socket.recv(1024)
    # print(response.decode())

    SENDER = 'jake@gmail.com'
    RECEIVER = 'mailhog@example.com'

    USERNAME = 'user'
    PASS = 'pass'

    for i in range (2):
        MSG = 'From: ' + SENDER + '\r\nTO: ' + RECEIVER + '\r\nSubject: Upcoming Event\r\nCustom Header: Jake\r\n\r\n' +  events[i]  + ' is soon!' + '\r\n.\r\n'
        
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((HOST,PORT))

        my_socket.send(('HELO ' + SENDER + '\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(('AUTH LOGIN\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send((USERNAME + '\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send((PASS + '\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(('MAIL FROM:<' + SENDER + '>\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(('RCPT TO:<' + RECEIVER +'>\r\n').encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(b'DATA\r\n')
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(MSG.encode())
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.send(b'QUIT\r\n')
        response = my_socket.recv(1024)
        print(response.decode())

        my_socket.close()


    return

def main():
    nearby_events = find_all_dates()
    print('\033[92m===========================================')
    print('Upcoming events: ')
    print('===========================================\033[0m')
    print('\r\n')
    print(nearby_events)
    print('\r\n')
    print('\033[92m===========================================')
    print('Email Protocols: ')
    print('===========================================\033[0m')
    print('\r\n')
    send_email(nearby_events)
    print('\033[92m===========================================\033[0m')

    return


if __name__ == '__main__':
    main()


# BONUS MARKS:
# 1. Custom Headers
# 2. SMTP Auth