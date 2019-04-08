# -*- coding:utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# 如需使用 chromedriver 导入此模块
# from selenium.webdriver.chrome.options import Options


class TBLogin(object):
    """淘宝登陆"""
    def __init__(self):
        self.browser = self.__init_browser()
        self.wait = WebDriverWait(self.browser, 10)
        # 输入用户名和密码
        self.username = 'xxxxxxxxxx'
        self.password = 'xxxxxxxxxx'

    def __init_browser(self):  # 初始化浏览器驱动
        # 使用 chromedriver
        # options = Options()
        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        # options.add_argument('--ignore-ssl-errors=true')
        # options.add_argument('--proxy-server=http://127.0.0.1:8080')
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.browser = webdriver.Chrome(options=options)

        # 使用 geckodriver
        profile = webdriver.FirefoxProfile()
        # 启用 https 代理
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.ssl', '127.0.0.1')
        profile.set_preference('network.proxy.ssl_port', 8080)
        profile.update_preferences()
        # 添加下面两个参数防止 SSL 报错，参考自：https://www.guru99.com/ssl-certificate-error-handling-selenium.html#2
        profile.accept_untrusted_certs = True
        profile.assume_untrusted_cert_issuer = False
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.maximize_window()
        return self.browser

    def send_key(self):  # 输入用户名和密码
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_username_1')))
        username.clear()
        username.send_keys(self.username)
        time.sleep(random.uniform(1.2, 2))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_password_1')))
        password.click()
        password.clear()
        password.send_keys(self.password)
        # 判断是否出现滑块
        if self.browser.find_element_by_id('nocaptcha').get_attribute('style') == 'display: block;':
            try:
                self.move_slider()
            except:
                print('滑块已拖动至最右边')
        time.sleep(random.uniform(1.2, 2))
        login_button = self.wait.until(EC.presence_of_element_located((By.ID, 'J_SubmitStatic')))
        login_button.click()

    def move_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.ID, 'nc_1_n1z')))
        action = ActionChains(self.browser)
        action.click_and_hold(slider).perform()
        # 滑块轨迹，此处为人工提取的轨迹，相关js脚本存放在 track.js 文件中，需根据实际情况做出调整
        track_list = [4, 19, 28, 37, 44, 64, 61, 20]
        for track in track_list:
            action.move_by_offset(xoffset=track, yoffset=0).perform()
            # 重定义 action 可使轨迹拖动停顿感降低
            action = ActionChains(self.browser)
        action.release().perform()
        time.sleep(random.uniform(0.6, 1))
        self.check_slider_ok()

    def check_slider_ok(self):  # 验证滑块是否通过
        check_flag = self.browser.find_element_by_id('nc_1_n1z').get_attribute('class')
        if 'btn_ok' in check_flag:
            print('验证通过')
            return None
        else:
            refresh_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="nc-lang-cnt"]/a')))
            refresh_btn.click()
            time.sleep(random.uniform(0.4, 0.6))
            self.move_slider()
            return self.check_slider_ok()

    def check_login_ok(self):  # 验证登陆是否成功
        try:
            nickname = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="site-nav-login-info-nick "]')))
            print('用户 [{}] 登陆成功'.format(nickname.text))
            return None
        except:
            print('登陆失败，正在重试...')
            self.send_key()
            return self.check_login_ok()

    def login(self):  # 登陆
        self.browser.get('https://login.taobao.com/member/login.jhtml')
        change_login_met = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="密码登录"]')))
        change_login_met.click()
        self.send_key()
        self.check_login_ok()

    def get_cookies(self):  # 获得登陆后的cookies,保存为字典
        cookies = self.browser.get_cookies()
        # 格式化 cookies 为字典
        item = {}
        for cookie in cookies:
            item[cookie['name']] = cookie['value']
        return item


if __name__ == '__main__':
    tb = TBLogin()
    tb.login()

