# -*- coding = utf-8 -*-
# @Time : 2023/5/12 13:46
# @Author : Lowry
# @File : main
# @Software : PyCharm

import sys
import socket
import attention

HOST = '127.0.0.1'
PORT = 12012


def get_args():
    """
    get arguments from terminal
    example: ./main.py libxml[argv1] xmllint[argv2]

    :return: project & PUT
    """
    project = sys.argv[1]       # directory name of project
    out = sys.argv[2]           # abs path of out directory
    return project, out


def main():
    print('begin py mode')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    project, out = get_args()
    print(f"{project} is the tested project")
    print(f"out: {out}")
    path = './programs/' + project + '/out/queue/'
    # path = out + '/queue/'
    print('connected by MLFuzz execution module ' + str(addr))
    attention.selection(path=path, project=project)
    conn.sendall(b"start")
    print("send success")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            print(f'connected, sign is {data}')
            attention.selection(path=path, project=project)
            print('generate complete')
            conn.sendall(b"yesss")            # send to BaSFuzz
    conn.close()


if __name__ == '__main__':
    main()
