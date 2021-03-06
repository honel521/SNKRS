#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   .py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-xx-xx
Description:
"""
import logging
import os
import sys
import time

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../" % cur_dir)
from manager.spider import *
from login.login import Loginer


class Addr(object):
    """配送地址"""

    def __init__(self, username="", password="", lastname="", firstname="", province="", city="",
                 district="", detail_address="", phone_num="", ):
        """
        相关参数初始化
        :param username: 用户名
        :param password: 密码
        :param lastname: 姓
        :param firstname: 名
        :param province: 省份
        :param city: 城市
        :param district: 县城
        :param detail_address: 详细地址
        :param phone_num: 电话号码
        """
        self.username = username
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.province = province
        self.city = city
        self.district = district
        self.detail_address = detail_address
        self.phone_num = phone_num

    def login(self):
        """配置地址之前需要登陆"""
        loginer = Loginer(username=self.username, password=self.password, headless=False)
        if loginer.login(url="https://www.nike.com/cn/launch/"):
            return loginer.B

    def setting_addr(self, url):
        """
        设置配送地址
        :param url: url
        :return:
        """
        B = self.login()
        if B.get("status", "-1"):
            try:
                # 设置请求url
                B.get(url)
                # 选中设置地址
                B.wait_for_element_loaded("addresses", By.CLASS_NAME)
                elem_addresses = B.browser.find_element_by_class_name("addresses")
                B.click_elem(elem_addresses)
                # 编辑地址
                B.wait_for_element_loaded("edit-button-container", By.CLASS_NAME)
                elem_edit = B.browser.find_element_by_class_name("edit-button-container")
                B.click_elem(elem_edit)
                # 编辑姓名,注意名在前，姓在后
                B.wait_for_element_loaded("address-lastname", By.ID)
                elem_lastname = B.browser.find_element_by_id("address-lastname")
                elem_firstname = B.browser.find_element_by_id("address-firstname")
                elem_lastname.clear()
                elem_firstname.clear()
                elem_lastname.send_keys(self.lastname)
                elem_firstname.send_keys(self.firstname)
                # 编辑省份
                elem_province = B.browser.find_element_by_class_name("state-container")
                B.click_elem(elem_province)
                state_province = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper state-container container2 js-addressState']/div/ul/li")
                for one in state_province:
                    if one.text == self.province:
                        B.click_elem(one)
                # 编辑城市
                city = B.browser.find_element_by_class_name("city-container")
                B.click_elem(city)
                citys = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper city-container container1 js-addressCity']/div/ul/li")
                for one in citys:
                    if one.text == self.city:
                        B.click_elem(one)
                # 编辑县或城市
                district = B.browser.find_element_by_class_name("district-container")
                B.click_elem(district)
                districts = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper district-container container2 js-addressDistrict']/div/ul/li")
                for one in districts:
                    if one.text == self.district:
                        B.click_elem(one)
                # 编辑详细地址
                detail_address = B.browser.find_element_by_id("address-addressone")
                detail_address.clear()
                detail_address.send_keys(self.detail_address)
                # 编辑电话号码
                phonenum = B.browser.find_element_by_id("address-phonenumber")
                phonenum.clear()
                phonenum.send_keys(self.phone_num)
                # 保存设置
                save_button = B.browser.find_element_by_xpath(
                    "//button[@data-qa='my_account.settings.addresses.shipping_address.save_button']")
                save_button.click()
                # todo:这里需要验证是否保存时候一定配置成功
                B.close()
                return {"username": self.username, "status": "1", "item": "address"}
            except Exception as e:
                logging.exception(
                    "%s :(address defeat %s) %s" % (time.asctime(), self.username, str(e)))
                B.close()
                return {"username": self.username, "status": "-1", "item": "address"}


def test():
    """unittest"""
    addr = Addr(username="18404983790", password="Ljc19941108", lastname="lee", firstname="jack",
                province="黑龙江省", city="绥化市",
                district="安达市", detail_address="中国黑龙江绥化市安达市栖霞小区9栋505",
                phone_num="00000000000")
    print(addr.setting_addr(url="https://www.nike.com/cn/zh_cn/p/settings"))


if __name__ == '__main__':
    test()
