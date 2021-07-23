import pyperclip
import threading
import time
import datetime
import requests
from flask import Flask, request
import logging


def clip(x, s=0.1):
    """
    不停的读取剪切板的变化
    :param x: {'text':剪切板内容,'time':剪切板内容变化的系统时间}
    :param s: float; 读取间隔, 单位秒
    :return:
    """
    while True:
        text = pyperclip.paste()
        if text != x['text']:
            x['text'] = text
            x['time'] = time.time()
        time.sleep(s)


def server(port=48011, s=0.1):
    """
    :param port: int; 端口
    :param s: float; 读取剪切板间隔, 单位秒
    :return:
    """
    app = Flask(__name__)
    # app.logger.setLevel(logging.ERROR)
    xx = {'text': pyperclip.paste(), 'time': 0}
    threading.Thread(target=clip, args=(xx, s)).start()  # 不断读取本地剪切板

    @app.route('/clip', methods=['POST'])
    def route():
        post_dict = dict(request.form)
        post_dict['time'] = float(post_dict['time'])
        post_dict['sys_time'] = float(post_dict['sys_time'])
        t = post_dict['time'] + (time.time() - post_dict['sys_time'])  # 防止系统时间差异
        if xx['text'] != post_dict['text']:  # 剪切板内容不同时
            if t > xx['time']:  # 当客户端时间更新
                pyperclip.copy(post_dict['text'])
                xx['text'] = post_dict['text']
                xx['time'] = time.time()
                print(str(datetime.datetime.now()), ': 拷贝了%d个字符' % len(xx['text']))
            else:
                return xx['text']
        return ''

    app.run(host='0.0.0.0', port=port, debug=False)


def client(ip, port=48011, s=0.1, ss=0.2):
    """
    :param ip: str; server 端ip
    :param port: int; 端口
    :param s: float; 读取剪切板间隔, 单位秒
    :param ss: float; 访问服务端间隔, 单位秒
    :return:
    """
    xx = {'text': pyperclip.paste(), 'time': 0}
    threading.Thread(target=clip, args=(xx, s)).start()  # 不断读取本地剪切板
    while True:
        post_dict = {'sys_time': time.time()}
        post_dict.update(xx)
        text = requests.post('http://%s:%d/clip' % (ip, port), post_dict).text
        if text and text != xx['text']:
            pyperclip.copy(text)
            xx['text'] = text
            xx['time'] = time.time()
            print(str(datetime.datetime.now()), ': 拷贝了%d个字符' % len(xx['text']))
        time.sleep(ss)


if __name__ == '__main__':
    ip = '192.168.150.6'
    port = 48011
    try:
        requests.post('http://%s:%d' % (ip, port))
        client(ip=ip, port=port, s=0.1, ss=1)
    except:
        server(port=port, s=0.1)
