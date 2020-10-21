import re
import logging
import os
import sys
import shutil
import requests
import zipfile
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from PIL import Image
import pytesseract

from win32com.client import Dispatch

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO)


def getVersionViaCom(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def getChromeVersion():
    CHROME_PATHS = [r'C:/Program Files/Google/Chrome/Application/chrome.exe',
                    r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe']
    return list(filter(None, [getVersionViaCom(p) for p in CHROME_PATHS]))[0]


def downloadFile(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    return local_filename


def unzipFile(zip_path, directory_to_extract_to='.'):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def downloadInstallChromeDriver(chrome_version, major_version, chromedriver_path):
    ROOT_URL = 'http://chromedriver.storage.googleapis.com'

    try:
        print('Auto downloading chromedriver for Chrome version %s' % chrome_version)
        r = requests.get('%s/LATEST_RELEASE_%s' % (ROOT_URL, major_version))
        r.raise_for_status()
        tarball_name = 'chromedriver_win32.zip'
        url = '%s/%s/%s' % (ROOT_URL, r.text, tarball_name)
        print('Installing chromedriver for Chrome version %s' % chrome_version)
        unzipFile(downloadFile(url))
        filename = Path('chromedriver.exe')
        if not os.path.exists(chromedriver_path):
            Path(chromedriver_path).parent.mkdir(parents=True, exist_ok=True)
            filename.rename(chromedriver_path)
        else:
            os.unlink(filename)
        if os.path.exists(tarball_name):
            os.unlink(tarball_name)
        return chromedriver_path
    except Exception as e:
        print('Error: chromedriver not found in $PATH (%s)' % e)
        sys.exit(-1)


def getChromeDriver(force=False):
    try:
        chrome_version = getChromeVersion()
        major_version = chrome_version.split('.')[0]
        chromedriver_path = './bin/chromedriver-%s.exe' % major_version
        if os.path.exists(chromedriver_path) and not force:
            return chromedriver_path
        print('Warning: chromedriver for Chrome version %s not found' % chrome_version)
        return downloadInstallChromeDriver(chrome_version, major_version, chromedriver_path)
    except Exception as e:
        print('Error: unable to detect chrome version! (%s)' % e)
        sys.exit(-1)


def getDriver(options):
    chrome_options = Options()
    chromedriver = getChromeDriver()
    if options.headless:
        chrome_options.add_argument("--headless")
    return webdriver.Chrome(
        options=chrome_options,
        executable_path=chromedriver)


def getElement(driver, selector, by=By.XPATH, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (by, selector)
        )
    )


def getClickableElement(driver, selector, by=By.XPATH, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (by, selector)
        )
    )


def selectValue(driver, selector, value, by=By.XPATH, timeout=5, retry=10):
    for round in range(retry):
        try:
            elem = getClickableElement(driver, selector, by, timeout)
            select = Select(elem)
            select.select_by_value(value)
            return select
        except:
            continue


def switchWindowTo(driver, index):
    try:
        return driver.switch_to.window(driver.window_handles[index])
    except Exception as e:
        print('Error: unable to switch to window %s' % index)
        sys.exit(-1)


def png2String(file):
    img = Image.open(file)
    img = img.convert('L')
    return pytesseract.image_to_string(img)


def png2Integer(file):
    string = png2String(file)
    return re.sub('[^\\d]', '', string)


def getCode(driver, selector, imagePath, refreshSelector='', by=By.XPATH, archive=False, timeout=5, retry=100):
    os.makedirs(os.path.dirname(imagePath), exist_ok=True)
    for count in range(retry):
        try:
            imgTag = getElement(driver, selector)
            with open(imagePath, 'wb') as file:
                file.write(imgTag.screenshot_as_png)
            if archive:
                name = os.path.splitext(imagePath)[0]
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                archivePath = '%s-%s.png' % (name, timestamp)
                shutil.copy(imagePath, archivePath)
            code = png2Integer(imagePath)
            if code:
                return code
            if refreshSelector:
                getElement(driver, refreshSelector).click()
            else:
                break
        except UnicodeEncodeError:
            continue
        except Exception as e:
            print('Error: %s' % e)
            sys.exit(-1)


def getAlert(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.alert_is_present()
        )
        return driver.switch_to.alert
    except:
        return False
