import argparse
try:
    from natclip import client, server
except:
    from .natclip import client, server


def main():
    parser = argparse.ArgumentParser(description='用于win,macos局域网内共享剪切板, 适用于moonlight等不支持剪切板的工具', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', action='store_true', help='是否使用客户端模式')
    parser.add_argument('-i', type=str, default='192.168.150.5', help='客户端模式下的服务器ip地址')
    parser.add_argument('-p', type=int, default=48011, help='端口号')
    parser.add_argument('-s', type=float, default=0.2, help='读取剪切板间隔, 单位秒')
    parser.add_argument('--ss', type=float, default=0.4, help='客户端模式下每次访问服务端间隔, 单位秒')
    parser.add_argument('--test', action='store_true', help='服务端模式下是否输出更多测试信息')
    args, unknown = parser.parse_known_args()  # 忽略未知参数
    
    if args.c:
        client(args.i, port=args.p, s=args.s, ss=args.ss)
    else:
        server(port=args.p, s=args.s, test=args.test)


if __name__ == "__main__":
    main()
