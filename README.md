# TaoBaoLogin
selenium + Firefox + mitmproxy 模拟淘宝登陆

## 实现原理
通过 mitmproxy 拦截响应，修改特征值，防止 selenium 被识别。然后使用 selenium 模拟登陆淘宝。<br>
基本上不会出现验证码，验证码可自动识别，但这一块效率没做测试。

## 文件说明
- login.py:  主程序，登陆淘宝，处理验证并获取cookies。
- script.py:  mitmproxy 脚本，截获响应并修改 selenium 特征值，防止被检测。
- track.js:  获取滑块验证吗人工轨迹。

## 版本信息
selenium (3.13.0)

mitmproxy (4.0.4)

Firefox (66.0.2)

geckodriver (0.24.0)

## 启动
首先说明一下，之所以不用 chromedriver 的原因是淘宝对 chromedriver 的检测太严，即使屏蔽了特征值 webdriver，<br>
但只要调用相关的事件方法，还是会被检测出来，导致出现验证码并且不让通过验证。

### 首先启动 mitmproxy 开启代理：
```
mitmdump -s script.py
```
默认端口为8080，可 -p 指定

### 启动主程序
```
python login.py
```

### 获取人工轨迹
这个是如果滑块过不了的话，可以重新采集一下轨迹列表<br>
脚本文件：track.js<br>
文件内有注释这里就不写了
