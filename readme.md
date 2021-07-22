实现windows、macos或及其之间的剪切板共享, 可用于moonlight串流等等.

# 教程

1. 安装 python 3 和 pip (自行解决);

2. 打开终端运行(两台电脑都需要): pip install natclip

3. 启动服务端: python -c "import natclip as n; n.server()"

4. 启动客户端: python -c "import natclip as n; n.client('这里填服务端的ip地址')"

5. 防火墙放行tcp端口(默认端口48011)

6. 通过服务端再启动客户端连接另一个服务端可以实现多台电脑的共享剪切板

