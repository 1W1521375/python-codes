#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import socket
import multiprocessing
import threading


HOST = '192.168.70.142'
PORT = 37564
list_IP = []


def search_socket(client_address):
    for i in range(len(list_IP)):
        if list_IP[i][1] == client_address:
            return i


# send
def mes_send(client_address, mes):
    sent_message = mes
    while True:
        num = search_socket(client_address)
        # sent_len = clientsocket.send(sent_message)
        sent_len = list_IP[num][0].send(sent_message)
        if sent_len == len(sent_message):
            break
        sent_message = sent_message[sent_len:]


def read_sig(client_address):
    f = open('sig.txt', 'r')
    bl = []
    line = f.readline().strip()
    while line:
        m = [(line)]
        bl.append(m)
        line = f.readline().strip()
    f.close()
    print('bl:{}\n'.format(bl))
    fl = sig_check(client_address, bl)
    print('fl:{}\n'.format(fl))
    return fl


def sig_check(address, black_li):
    client_ip = address.split(".")
    for b in black_li:
        b1 = b[0].split(".")
        for i in range(4):
            if client_ip[i] != b1[i]:
                break
        else:
            return 0
    else:
        return 1


def mes(message, client_address, flag):
    cliok = (client_address + ':').encode("UTF-8")
    errmsg = ('error:' + client_address + '\n').encode("UTF-8")
    print(cliok,errmsg)
    if flag == 1:
        sent_message = cliok + message
        mes_send(client_address, sent_message)
        mes_send(list_IP[0][1], sent_message)
    else:
        mes_send(client_address, errmsg)
    print('Send: {0} to {1}'.format(message, client_address))


def worker_thread(serversocket):
    """クライアントとの接続を処理するハンドラ (スレッド)"""
    while True:
        # クライアントからの接続を待ち受ける (接続されるまでブロックする)
        # ワーカースレッド同士でクライアントからの接続を奪い合う
        clientsocket, (client_address, client_port) = serversocket.accept()
        flag = read_sig(client_address)
        list_IP.append([clientsocket, client_address, client_port])
        print('New client: {0}:{1}'.format(client_address, client_port))
        print(list_IP)
        while True:
            try:
                message = clientsocket.recv(1024)
                print('Recv: {0} from {1}:{2}'.
                    format(message, client_address, client_port))
            except OSError:
                break
            if len(message) == 0:
                break
            print(clientsocket)
            mes(message, client_address, flag)
        clientsocket.close()
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


def worker_process(serversocket):
    NUMBER_OF_THREADS = 10
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread, args=(serversocket, ))
        thread.start()
    while True:
        # ワーカープロセスのメインスレッドは遊ばせておく
        time.sleep(1)


def main():
    print('start')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    host = HOST
    port = PORT
    serversocket.bind((host, port))
    serversocket.listen(128)
    NUMBER_OF_PROCESSES = multiprocessing.cpu_count()
    for _ in range(NUMBER_OF_PROCESSES):
        process = multiprocessing.Process(target=worker_process,
                                          args=(serversocket, ))
        process.daemon = True
        process.start()
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
