try:
    import pyperclip
except:
    raise NameError('缺少包, 可尝试执行: pip install pyperclip')
import threading
import time
import datetime
import socket
import traceback
import json
import struct
import sys
import copy


def clip(x, s=0.2):
    """
    不停的读取剪切板的变化
    :param x: {'text':剪切板内容,'time':剪切板内容变化的系统时间}
    :param s: float; 读取间隔, 单位秒
    :return:
    """
    while True:
        try:
            text = pyperclip.paste()
            if text != x['text']:
                x['text'] = text
                x['time'] = time.time()
                print(str(datetime.datetime.now()), '复制了%d个字符' % len(x['text']))
            time.sleep(s)
        except:
            print(str(datetime.datetime.now()), ': 访问剪切板失败(锁屏必然会产生此问题), 暂停 %d 秒后尝试!' % s * 20)
            traceback.print_exc()
            print()
            time.sleep(s * 20)


def server(port=48011, s=0.2, test=False):
    """
    :param port: int; 端口
    :param s: float; 读取剪切板间隔, 单位秒
    :param test: bool; 是否测试
    :return:
    """
    print('启动 server, 端口:', port)
    xx = {'text': pyperclip.paste(), 'time': 0}
    threading.Thread(target=clip, args=(xx, s)).start()  # 不断读取本地剪切板
    server = socket.socket()
    try:  # 解决服务重启时报address already in use
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        ...
    server.bind(('0.0.0.0', port))
    server.listen()
    while True:
        try:
            conn, addr = server.accept()
            while True:
                ret = ' '  # 不用修改是空格
                a = conn.recv(struct.unpack('i', conn.recv(4, socket.MSG_WAITALL))[0], socket.MSG_WAITALL).decode(
                    'utf-8')  # 接收client的信息
                post_dict = json.loads(a)
                if test:
                    print('接收字节数:', len(a), '; 接收内容:', post_dict)
                t = post_dict['time'] + (time.time() - post_dict['sys_time'])  # 防止系统时间差异
                if xx['text'] != post_dict['text']:  # 剪切板内容不同时
                    if t > xx['time']:  # 当客户端时间更新时
                        if post_dict['text'] is not None:  # 需要有内容
                            pyperclip.copy(post_dict['text'])
                            xx['text'] = post_dict['text']
                            xx['time'] = time.time()
                            print(str(datetime.datetime.now()), ': 从', addr, '拷贝了%d个字符' % len(xx['text']))
                    else:  # 返回给client修改
                        ret = ' ' + xx['text']
                if test:
                    print('返回内容:', ret)
                ret = ret.encode('utf-8')
                conn.send(struct.pack('i', len(ret)))  # 这个上限就是最大字符限制
                conn.send(ret)
        except KeyboardInterrupt:
            break
        except:
            print(datetime.datetime.now(), ': 将重新接收client连接, 建议重启client, 出错信息:')
            traceback.print_exc()
            print()


def client(ip, port=48011, s=0.2, ss=0.4):
    """
    :param ip: str; server 端ip
    :param port: int; 端口
    :param s: float; 读取剪切板间隔, 单位秒
    :param ss: float; 每次访问服务端间隔, 单位秒
    :return:
    """
    print('启动 client (确保先启动 server)')
    xx = {'text': pyperclip.paste(), 'time': 0}
    threading.Thread(target=clip, args=(xx, s)).start()  # 不断读取本地剪切板
    while True:
        try:
            client = socket.socket()
            client.connect((ip, port))
            while True:
                post_dict = {'sys_time': time.time()}
                xx_ = copy.deepcopy(xx)  # 防止在这个过程中改变内容
                post_dict.update(xx_)
                if post_dict['sys_time'] - post_dict['time'] > 3 * ss:  # 不用每次传输同样内容, 节省带宽, 存在没有接收到的可能
                    post_dict['text'] = None
                ret = json.dumps(post_dict).encode('utf-8')
                client.send(struct.pack('i', len(ret)))  # 这个上限就是最大字符限制
                client.send(ret)
                text = client.recv(struct.unpack('i', client.recv(4, socket.MSG_WAITALL))[0], socket.MSG_WAITALL).decode(
                    'utf-8')[1:]  # 接收server复制的内容
                if text and text != xx_['text']:
                    pyperclip.copy(text)
                    xx['text'] = text
                    xx['time'] = time.time()
                    print(str(datetime.datetime.now()), ': 从', (ip, port), '拷贝了%d个字符' % len(xx['text']))
                time.sleep(ss)
        except KeyboardInterrupt:
            break
        except:
            print(datetime.datetime.now(), ': 将重新连接server, 出错信息:')
            traceback.print_exc()
            print()
            time.sleep(ss * 10)


if __name__ == '__main__':
    port = 48011
    if len(sys.argv) == 2:
        client(ip=sys.argv[1], port=port, s=0.2, ss=0.4)
    else:
        server(port=port, s=0.2, test=False)
