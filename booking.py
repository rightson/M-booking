#!/usr/bin/env python3
import sys
import argparse
from chrome_utils import (
    getDriver, selectValue, getElement, switchWindowTo, getCode, getAlert,
    getChromeVersion, getChromeDriver
)


def listTreadmill(options):
    ROOT_URL = 'https://hrwebapps.mediatek.inc/sport/SP'

    driver = getDriver(options)
    driver.get('%s/index_orderlist.aspx' % ROOT_URL)
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlPlace"]', '新竹E棟')
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlSportType"]', '跑步')
    getElement(driver, '//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]', timeout=20).click()
    input('Press Enter to continue')
    driver.quit()


def bookTreadmill(options):
    ROOT_URL = 'https://hrwebapps.mediatek.inc/sport/SP'

    driver = getDriver(options)
    driver.get('%s/index_order.aspx' % ROOT_URL)
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlPlace"]', '新竹E棟')
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlSportType"]', '跑步')
    getElement(driver, '//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]', timeout=20).click()

    try:
        choice = ('//*[@id="ctl00_ContentPlaceHolder1_ShowData"]/tbody' +
                  '/tr[%s]/td[%s]/a' % (options.row + 1, options.column + 1))
        getElement(driver, choice).click()
    except Exception as e:
        print('Unable to book selected slot (%s)' % str(e))
        sys.exit(-1)

    switchWindowTo(driver, 1)

    code = getCode(driver, '//*[@id="Imgchkcode"]', './images/code.png', '//*[@id="btnRefresh"]', archive=True)
    getElement(driver, '//*[@id="txtVali"]').send_keys(code)
    getElement(driver, '//*[@id="btnOK"]').click()

    alert = getAlert(driver)
    if alert:
        text = alert.text
        alert.accept()
        switchWindowTo(driver, 0)
        print(text)
        input('Press Enter to continue')
        driver.quit()
    else:
        switchWindowTo(driver, 0)
        print('Successfully booked!')
        listTreadmill(options)


def listMassage(options):
    ROOT_URL = 'https://hrwebapps.mediatek.inc/massage/MS'

    driver = getDriver(options)
    driver.get('%s/index_date.aspx' % ROOT_URL)
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlWorkPlace"]', '新竹E棟')
    if options.page == 2:
        getElement(driver, '//*[@id="ctl00_ContentPlaceHolder1_btnNext"]').click()
    input('Press Enter to continue')
    driver.quit()


def bookMassage(options):
    ROOT_URL = 'https://hrwebapps.mediatek.inc/massage/MS'

    driver = getDriver(options)
    driver.get('%s/index_date.aspx' % ROOT_URL)
    selectValue(driver, '//*[@id="ctl00_ContentPlaceHolder1_ddlWorkPlace"]', '新竹E棟')
    if options.page == 2:
        getElement(driver, '//*[@id="ctl00_ContentPlaceHolder1_btnNext"]').click()

    try:
        choice = ('//*[@id="ctl00_ContentPlaceHolder1_tc_%s_%s"]/span[%s]/a' %
                  (options.column, options.row, options.page))
        getElement(driver, choice).click()
    except Exception as e:
        print('Unable to book selected slot (%s)' % str(e))
        sys.exit(-1)

    switchWindowTo(driver, 1)

    code = getCode(driver, '//*[@id="Imgchkcode"]', './images/code.png', '//*[@id="btnRefresh"]', archive=True)
    getElement(driver, '//*[@id="txtVali"]').send_keys(code)
    getElement(driver, '//*[@id="btnOK"]').click()

    alert = getAlert(driver)
    if alert:
        text = alert.text
        alert.accept()
        switchWindowTo(driver, 0)
        print(text)
        input('Press Enter to continue')
    else:
        switchWindowTo(driver, 0)
        print('Successfully booked!')
        listMassage(options)
    input('Press Enter to continue')
    driver.quit()


if __name__ == '__main__':
    name = 'Booking Utility'
    version = 'Version 1.0.0'
    parser = argparse.ArgumentParser(description='%s (%s)' % (name, version))
    parser.add_argument('-t', '--treadmill', action='store_true', help='Book treadmill')
    parser.add_argument('-m', '--massage', action='store_true', help='Book massage')
    parser.add_argument('-l', '--listOnly', action='store_true', help='List order list only')
    parser.add_argument('-p', '--page', default=2, help='Sub page number (default=2) for massage')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('-r', '--row', type=int, default=1)
    parser.add_argument('-c', '--column', type=int, default=4)
    parser.add_argument('--chromeVersion', action='store_true', help='Show chrome version')
    parser.add_argument('--installChromeDriver', action='store_true', help='Install chromedriver')
    args = parser.parse_args()

    if args.installChromeDriver:
        getChromeDriver(force=True)
        sys.exit(0)

    elif args.treadmill:
        if args.listOnly:
            listTreadmill(args)
        else:
            bookTreadmill(args)

    elif args.massage:
        if args.listOnly:
            listMassage(args)
        else:
            bookMassage(args)

    elif args.chromeVersion:
        print(getChromeVersion())

    else:
        parser.print_help()
