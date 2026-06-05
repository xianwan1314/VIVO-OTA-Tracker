#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
import subprocess
import tempfile
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox, QProgressBar,
                             QComboBox, QScrollArea, QCheckBox)
from PyQt5.QtCore import QProcess, Qt, QSize
from PyQt5.QtGui import QClipboard, QIcon, QPixmap

# 应用版本号
APP_VERSION = "V1.0.0_Release_mytiantian"


def resource_path(relative_path):
    """获取资源文件的绝对路径（兼容 PyInstaller 打包模式）

    PyInstaller --onefile 模式会将资源解压到 sys._MEIPASS 临时目录，
    此函数确保无论开发模式还是打包模式都能正确找到资源文件。
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# Vivo 设备型号数据库 (来源: MobileModels/vivo_cn.md)
DEVICE_DATABASE = {
    "NEX 系列": [
        {"model": "vivo NEX 双屏版", "codename": "PD1821", "model_sw_ver": "V1821A"},
        {"model": "vivo NEX 双屏版 移动全网通", "codename": "PD1821", "model_sw_ver": "V1821T"},
        {"model": "vivo NEX 3", "codename": "PD1923", "model_sw_ver": "V1923A"},
        {"model": "vivo NEX 3 移动全网通", "codename": "PD1923", "model_sw_ver": "V1923T"},
        {"model": "vivo NEX 3 5G", "codename": "PD1924", "model_sw_ver": "V1924A"},
        {"model": "vivo NEX 3 5G 移动全网通", "codename": "PD1924", "model_sw_ver": "V1924T"},
        {"model": "vivo NEX 3S 5G", "codename": "PD1950", "model_sw_ver": "V1950A"},
    ],
    "X 系列": [
        {"model": "vivo X21s", "codename": "PD1814", "model_sw_ver": "V1814A"},
        {"model": "vivo X21s 移动全网通", "codename": "PD1814", "model_sw_ver": "V1814T"},
        {"model": "vivo X23", "codename": "PD1809", "model_sw_ver": "V1809A"},
        {"model": "vivo X23 移动全网通", "codename": "PD1809", "model_sw_ver": "V1809T"},
        {"model": "vivo X23 幻彩版", "codename": "PD1816", "model_sw_ver": "V1816A"},
        {"model": "vivo X23 幻彩版 移动全网通", "codename": "PD1816", "model_sw_ver": "V1816T"},
        {"model": "vivo X27 (8+256)", "codename": "PD1829", "model_sw_ver": "V1829A"},
        {"model": "vivo X27 (8+256) 移动全网通", "codename": "PD1829", "model_sw_ver": "V1829T"},
        {"model": "vivo X27 (8+128)", "codename": "PD1838", "model_sw_ver": "V1838A"},
        {"model": "vivo X27 (8+128) 移动全网通", "codename": "PD1838", "model_sw_ver": "V1838T"},
        {"model": "vivo X27 Pro", "codename": "PD1836", "model_sw_ver": "V1836A"},
        {"model": "vivo X27 Pro 移动全网通", "codename": "PD1836", "model_sw_ver": "V1836T"},
        {"model": "vivo X30 5G", "codename": "PD1938C", "model_sw_ver": "V1938CA"},
        {"model": "vivo X30 5G 移动全网通", "codename": "PD1938C", "model_sw_ver": "V1938CT"},
        {"model": "vivo X30 Pro 5G", "codename": "PD1938", "model_sw_ver": "V1938A"},
        {"model": "vivo X30 Pro 5G 移动全网通", "codename": "PD1938", "model_sw_ver": "V1938T"},
        {"model": "vivo X50", "codename": "PD2001", "model_sw_ver": "V2001A"},
        {"model": "vivo X50 Pro", "codename": "PD2005", "model_sw_ver": "V2005A"},
        {"model": "vivo X50 Pro+", "codename": "PD2011", "model_sw_ver": "V2011A"},
        {"model": "vivo X60", "codename": "PD2046", "model_sw_ver": "V2046A"},
        {"model": "vivo X60 曲屏版", "codename": "PD2059", "model_sw_ver": "V2059A"},
        {"model": "vivo X60t", "codename": "PD2085", "model_sw_ver": "V2085A"},
        {"model": "vivo X60 Pro", "codename": "PD2047", "model_sw_ver": "V2047A"},
        {"model": "vivo X60t Pro", "codename": "PD2120", "model_sw_ver": "V2120A"},
        {"model": "vivo X60 Pro+", "codename": "PD2056", "model_sw_ver": "V2056A"},
        {"model": "vivo X60t Pro+", "codename": "PD2056", "model_sw_ver": "V2056A"},
        {"model": "vivo X70", "codename": "PD2133", "model_sw_ver": "V2133A"},
        {"model": "vivo X70t", "codename": "PD2132", "model_sw_ver": "V2132A"},
        {"model": "vivo X70 Pro", "codename": "PD2134", "model_sw_ver": "V2134A"},
        {"model": "vivo X70 Pro+", "codename": "PD2145", "model_sw_ver": "V2145A"},
        {"model": "vivo X Fold", "codename": "PD2178", "model_sw_ver": "V2178A"},
        {"model": "vivo X Note", "codename": "PD2170", "model_sw_ver": "V2170A"},
        {"model": "vivo X80", "codename": "PD2183", "model_sw_ver": "V2183A"},
        {"model": "vivo X80 Pro", "codename": "PD2185", "model_sw_ver": "V2185A"},
        {"model": "vivo X80 Pro 天玑9000版", "codename": "PD2186", "model_sw_ver": "V2186A"},
        {"model": "vivo X Fold+", "codename": "PD2229", "model_sw_ver": "V2229A"},
        {"model": "vivo X90", "codename": "PD2241", "model_sw_ver": "V2241A"},
        {"model": "vivo X90s", "codename": "PD2241", "model_sw_ver": "V2241HA"},
        {"model": "vivo X90 Pro", "codename": "PD2242", "model_sw_ver": "V2242A"},
        {"model": "vivo X90 Pro+", "codename": "PD2227", "model_sw_ver": "V2227A"},
        {"model": "vivo X Fold2", "codename": "PD2266", "model_sw_ver": "V2266A"},
        {"model": "vivo X Flip", "codename": "PD2256", "model_sw_ver": "V2256A"},
        {"model": "vivo X100", "codename": "PD2309", "model_sw_ver": "V2309A"},
        {"model": "vivo X100 Pro", "codename": "PD2324", "model_sw_ver": "V2324A"},
        {"model": "vivo X Fold3", "codename": "PD2303", "model_sw_ver": "V2303A"},
        {"model": "vivo X Fold3 Pro", "codename": "PD2337", "model_sw_ver": "V2337A"},
        {"model": "vivo X100s", "codename": "PD2359", "model_sw_ver": "V2359A"},
        {"model": "vivo X100s Pro", "codename": "PD2324", "model_sw_ver": "V2324HA"},
        {"model": "vivo X100 Ultra", "codename": "PD2366", "model_sw_ver": "V2366GA"},
        {"model": "vivo X100 Ultra 卫星通信版", "codename": "PD2366", "model_sw_ver": "V2366HA"},
        {"model": "vivo X200", "codename": "PD2415", "model_sw_ver": "V2415A"},
        {"model": "vivo X200 Pro", "codename": "PD2405", "model_sw_ver": "V2405A"},
        {"model": "vivo X200 Pro 卫星通信版", "codename": "PD2405", "model_sw_ver": "V2405DA"},
        {"model": "vivo X200 Pro mini", "codename": "PD2419", "model_sw_ver": "V2419A"},
        {"model": "vivo X200s", "codename": "PD2458", "model_sw_ver": "V2458A"},
        {"model": "vivo X200 Ultra", "codename": "PD2454", "model_sw_ver": "V2454A"},
        {"model": "vivo X200 Ultra 卫星通信版", "codename": "PD2454", "model_sw_ver": "V2454DA"},
        {"model": "vivo X Fold5", "codename": "PD2436", "model_sw_ver": "V2436A"},
        {"model": "vivo X300", "codename": "PD2509", "model_sw_ver": "V2509A"},
        {"model": "vivo X300 Pro", "codename": "PD2502", "model_sw_ver": "V2502A"},
        {"model": "vivo X300 Pro 卫星通信版", "codename": "PD2502", "model_sw_ver": "V2502DA"},
        {"model": "vivo X300s", "codename": "PD2548", "model_sw_ver": "V2548A"},
        {"model": "vivo X300 Ultra", "codename": "PD2547", "model_sw_ver": "V2547A"},
        {"model": "vivo X300 Ultra 卫星通信版", "codename": "PD2547", "model_sw_ver": "V2547DA"},
    ],
    "S 系列": [
        {"model": "vivo S1", "codename": "PD1831", "model_sw_ver": "V1831A"},
        {"model": "vivo S1 移动全网通", "codename": "PD1831", "model_sw_ver": "V1831T"},
        {"model": "vivo S1 Pro", "codename": "PD1832", "model_sw_ver": "V1832A"},
        {"model": "vivo S1 Pro 移动全网通", "codename": "PD1832", "model_sw_ver": "V1832T"},
        {"model": "vivo S5", "codename": "PD1932", "model_sw_ver": "V1932A"},
        {"model": "vivo S5 移动全网通", "codename": "PD1932", "model_sw_ver": "V1932T"},
        {"model": "vivo S6", "codename": "PD1962", "model_sw_ver": "V1962A"},
        {"model": "vivo S7", "codename": "PD2020", "model_sw_ver": "V2020A"},
        {"model": "vivo S7 (V2020CA)", "codename": "PD2020", "model_sw_ver": "V2020CA"},
        {"model": "vivo S7t", "codename": "PD2080", "model_sw_ver": "V2080A"},
        {"model": "vivo S7e", "codename": "PD2031", "model_sw_ver": "V2031A"},
        {"model": "vivo S7e 活力版", "codename": "PD2031EA", "model_sw_ver": "V2031EA"},
        {"model": "vivo S9", "codename": "PD2072", "model_sw_ver": "V2072A"},
        {"model": "vivo S9e", "codename": "PD2048", "model_sw_ver": "V2048A"},
        {"model": "vivo S10", "codename": "PD2121", "model_sw_ver": "V2121A"},
        {"model": "vivo S10 Pro", "codename": "PD2121", "model_sw_ver": "V2121A"},
        {"model": "vivo S10e", "codename": "PD2130", "model_sw_ver": "V2130A"},
        {"model": "vivo S12", "codename": "PD2162", "model_sw_ver": "V2162A"},
        {"model": "vivo S12 Pro", "codename": "PD2163", "model_sw_ver": "V2163A"},
        {"model": "vivo S15", "codename": "PD2203", "model_sw_ver": "V2203A"},
        {"model": "vivo S15 Pro", "codename": "PD2207", "model_sw_ver": "V2207A"},
        {"model": "vivo S15e", "codename": "PD2190", "model_sw_ver": "V2190A"},
        {"model": "vivo S16", "codename": "PD2244", "model_sw_ver": "V2244A"},
        {"model": "vivo S16 Pro", "codename": "PD2245", "model_sw_ver": "V2245A"},
        {"model": "vivo S16e", "codename": "PD2239", "model_sw_ver": "V2239A"},
        {"model": "vivo S17", "codename": "PD2283", "model_sw_ver": "V2283A"},
        {"model": "vivo S17t", "codename": "PD2282", "model_sw_ver": "V2282A"},
        {"model": "vivo S17 Pro", "codename": "PD2284", "model_sw_ver": "V2284A"},
        {"model": "vivo S17e", "codename": "PD2285", "model_sw_ver": "V2285A"},
        {"model": "vivo S18", "codename": "PD2323", "model_sw_ver": "V2323A"},
        {"model": "vivo S18 Pro", "codename": "PD2344", "model_sw_ver": "V2344A"},
        {"model": "vivo S18e", "codename": "PD2334", "model_sw_ver": "V2334A"},
        {"model": "vivo S19", "codename": "PD2364", "model_sw_ver": "V2364A"},
        {"model": "vivo S19 Pro", "codename": "PD2362", "model_sw_ver": "V2362A"},
        {"model": "vivo S20", "codename": "PD2429", "model_sw_ver": "V2429A"},
        {"model": "vivo S20 Pro", "codename": "PD2430", "model_sw_ver": "V2430A"},
        {"model": "vivo S30", "codename": "PD2464", "model_sw_ver": "V2464A"},
        {"model": "vivo S30 Pro mini", "codename": "PD2465", "model_sw_ver": "V2465A"},
        {"model": "vivo S50", "codename": "PD2528", "model_sw_ver": "V2528A"},
        {"model": "vivo S50 Pro mini", "codename": "PD2527", "model_sw_ver": "V2527A"},
        {"model": "vivo S60", "codename": "PD2571", "model_sw_ver": "V2571A"},
        {"model": "vivo S60 元气版", "codename": "PD2572", "model_sw_ver": "V2572A"},
    ],
    "Y 系列": [
        {"model": "vivo Y3", "codename": "PD1901", "model_sw_ver": "V1901A"},
        {"model": "vivo Y3 移动全网通", "codename": "PD1901", "model_sw_ver": "V1901T"},
        {"model": "vivo Y3 标准版", "codename": "PD1930", "model_sw_ver": "V1930A"},
        {"model": "vivo Y3 标准版 移动全网通", "codename": "PD1930", "model_sw_ver": "V1930T"},
        {"model": "vivo Y3s", "codename": "PD1901", "model_sw_ver": "V1901A"},
        {"model": "vivo Y3s 移动全网通", "codename": "PD1901", "model_sw_ver": "V1901T"},
        {"model": "vivo Y5s", "codename": "PD1934", "model_sw_ver": "V1934A"},
        {"model": "vivo Y5s 移动全网通", "codename": "PD1934", "model_sw_ver": "V1934T"},
        {"model": "vivo Y7s", "codename": "PD1913", "model_sw_ver": "V1913A"},
        {"model": "vivo Y7s 移动全网通", "codename": "PD1913", "model_sw_ver": "V1913T"},
        {"model": "vivo Y9s", "codename": "PD1945", "model_sw_ver": "V1945A"},
        {"model": "vivo Y9s 移动全网通", "codename": "PD1945", "model_sw_ver": "V1945T"},
        {"model": "vivo Y10", "codename": "PD2140", "model_sw_ver": "V2140A"},
        {"model": "vivo Y10 (t1 版)", "codename": "PD2168", "model_sw_ver": "V2168A"},
        {"model": "vivo Y10 (t2 版)", "codename": "PD2180", "model_sw_ver": "V2180A"},
        {"model": "vivo Y11", "codename": "PD2236", "model_sw_ver": "V2236A"},
        {"model": "vivo Y12", "codename": "PD2317", "model_sw_ver": "V2317A"},
        {"model": "vivo Y30", "codename": "PD2034", "model_sw_ver": "V2034A"},
        {"model": "vivo Y30 标准版", "codename": "PD2036", "model_sw_ver": "V2036A"},
        {"model": "vivo Y30 2021", "codename": "PD2099", "model_sw_ver": "V2099A"},
        {"model": "vivo Y30 活力版", "codename": "PD2066", "model_sw_ver": "V2066A"},
        {"model": "vivo Y30g", "codename": "PD2066B", "model_sw_ver": "V2066BA"},
        {"model": "vivo Y31s 5G", "codename": "PD2054", "model_sw_ver": "V2054A"},
        {"model": "vivo Y31s 标准版 5G", "codename": "PD2068", "model_sw_ver": "V2068A"},
        {"model": "vivo Y31s (t1 版) 5G", "codename": "PD2068", "model_sw_ver": "V2068A"},
        {"model": "vivo Y31s (t2 版) 5G", "codename": "PD2092", "model_sw_ver": "V2054A"},
        {"model": "vivo Y32", "codename": "PD2158", "model_sw_ver": "V2158A"},
        {"model": "vivo Y32t (P70)", "codename": "PD2168", "model_sw_ver": "V2168A"},
        {"model": "vivo Y32t (骁龙680)", "codename": "PD2180", "model_sw_ver": "V2180A"},
        {"model": "vivo Y33s 5G", "codename": "PD2166", "model_sw_ver": "V2166A"},
        {"model": "vivo Y33e 5G", "codename": "PD2166", "model_sw_ver": "V2166A"},
        {"model": "vivo Y33t", "codename": "PD2317", "model_sw_ver": "V2317A"},
        {"model": "vivo Y35 5G", "codename": "PD2230", "model_sw_ver": "V2230A"},
        {"model": "vivo Y35+ 5G", "codename": "PD2279", "model_sw_ver": "V2279A"},
        {"model": "vivo Y36 5G", "codename": "PD2318", "model_sw_ver": "V2318A"},
        {"model": "vivo Y36t", "codename": "PD2327", "model_sw_ver": "V2327A"},
        {"model": "vivo Y36c 5G", "codename": "PD2357", "model_sw_ver": "V2357A"},
        {"model": "vivo Y37 5G", "codename": "PD2357", "model_sw_ver": "V2357A"},
        {"model": "vivo Y37m 5G", "codename": "PD2357", "model_sw_ver": "V2357EA"},
        {"model": "vivo Y37 Pro 5G", "codename": "PD2354", "model_sw_ver": "V2354A"},
        {"model": "vivo Y37c", "codename": "PD2442", "model_sw_ver": "V2442A"},
        {"model": "vivo Y50", "codename": "PD1965", "model_sw_ver": "V1965A"},
        {"model": "vivo Y50t", "codename": "PD2023", "model_sw_ver": "V2023EA"},
        {"model": "vivo Y37t 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y37+ 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y50 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y50i 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y50e 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y50s 5G", "codename": "PD2443", "model_sw_ver": "V2443A"},
        {"model": "vivo Y50m 5G", "codename": "PD2443", "model_sw_ver": "V2443BA"},
        {"model": "vivo Y50c 5G", "codename": "PD2443", "model_sw_ver": "V2443BA"},
        {"model": "vivo Y51s 5G", "codename": "PD2019", "model_sw_ver": "V2002A"},
        {"model": "vivo Y52s 5G", "codename": "PD2057", "model_sw_ver": "V2057A"},
        {"model": "vivo Y52s (t1 版) 5G", "codename": "PD2106", "model_sw_ver": "V2054A"},
        {"model": "vivo Y52t 5G", "codename": "PD2166", "model_sw_ver": "V2166A"},
        {"model": "vivo Y53s 5G", "codename": "PD2111", "model_sw_ver": "V2111A"},
        {"model": "vivo Y53s (t1 版) 5G", "codename": "PD2069", "model_sw_ver": "V2069A"},
        {"model": "vivo Y53s (t2 版) 5G", "codename": "PD2123", "model_sw_ver": "V2123A"},
        {"model": "vivo Y53s NFC版 5G", "codename": "PD2069", "model_sw_ver": "V2069A"},
        {"model": "vivo Y53t 5G", "codename": "PD2230", "model_sw_ver": "V2230A"},
        {"model": "vivo Y54s 5G", "codename": "PD2045", "model_sw_ver": "V2045A"},
        {"model": "vivo Y55s 5G", "codename": "PD2164", "model_sw_ver": "V2164A"},
        {"model": "vivo Y55t 5G", "codename": "PD2279", "model_sw_ver": "V2279A"},
        {"model": "vivo Y60 5G", "codename": "PD2559", "model_sw_ver": "V2559A"},
        {"model": "vivo Y6t 5G", "codename": "PD2559", "model_sw_ver": "V2559A"},
        {"model": "vivo Y60m 5G", "codename": "PD2559", "model_sw_ver": "V2559BA"},
        {"model": "vivo Y6m", "codename": "PD2532", "model_sw_ver": "V2532BA"},
        {"model": "vivo Y70s 5G", "codename": "PD2002", "model_sw_ver": "V2002A"},
        {"model": "vivo Y70t 5G", "codename": "PD2019", "model_sw_ver": "V2002A"},
        {"model": "vivo Y71s", "codename": "PD1731C", "model_sw_ver": "V1731CA"},
        {"model": "vivo Y71t 5G", "codename": "PD2102", "model_sw_ver": "V2102A"},
        {"model": "vivo Y72t 5G", "codename": "PD2164", "model_sw_ver": "V2164A"},
        {"model": "vivo Y73", "codename": "PD1731C", "model_sw_ver": "V1731CA"},
        {"model": "vivo Y73s 5G", "codename": "PD2031", "model_sw_ver": "V2031A"},
        {"model": "vivo Y73t 5G", "codename": "PD2164U", "model_sw_ver": "V2164PA"},
        {"model": "vivo Y74s 5G", "codename": "PD2009", "model_sw_ver": "V2009A"},
        {"model": "vivo Y75s 5G", "codename": "PD2069", "model_sw_ver": "V2069BA"},
        {"model": "vivo Y76s 5G", "codename": "PD2156", "model_sw_ver": "V2156A"},
        {"model": "vivo Y76s (t1 版) 5G", "codename": "PD2156U", "model_sw_ver": "V2156FA"},
        {"model": "vivo Y77 5G", "codename": "PD2219", "model_sw_ver": "V2219A"},
        {"model": "vivo Y77e 5G", "codename": "PD2224", "model_sw_ver": "V2166BA"},
        {"model": "vivo Y77t 5G", "codename": "PD2278", "model_sw_ver": "V2278A"},
        {"model": "vivo Y78 5G", "codename": "PD2278", "model_sw_ver": "V2278A"},
        {"model": "vivo Y78m 5G", "codename": "PD2278", "model_sw_ver": "V2278A"},
        {"model": "vivo Y78+ 5G", "codename": "PD2271", "model_sw_ver": "V2271A"},
        {"model": "vivo Y78 (t1) 5G", "codename": "PD2279", "model_sw_ver": "V2279A"},
        {"model": "vivo Y78m (t1) 5G", "codename": "PD2279", "model_sw_ver": "V2279A"},
        {"model": "vivo Y78t 5G", "codename": "PD2312", "model_sw_ver": "V2312BA"},
        {"model": "vivo Y81", "codename": "PD1732", "model_sw_ver": "V1732A"},
        {"model": "vivo Y81 移动全网通", "codename": "PD1732", "model_sw_ver": "V1732T"},
        {"model": "vivo Y81s", "codename": "PD1732", "model_sw_ver": "V1732A"},
        {"model": "vivo Y81s 移动全网通", "codename": "PD1732", "model_sw_ver": "V1732T"},
        {"model": "vivo Y89", "codename": "PD1730E", "model_sw_ver": "V1730EA"},
        {"model": "vivo Y91", "codename": "PD1818C", "model_sw_ver": "V1818CA"},
        {"model": "vivo Y91 移动全网通", "codename": "PD1818C", "model_sw_ver": "V1818CT"},
        {"model": "vivo Y93", "codename": "PD1818", "model_sw_ver": "V1818A"},
        {"model": "vivo Y93 移动全网通", "codename": "PD1818", "model_sw_ver": "V1818T"},
        {"model": "vivo Y93 标准版", "codename": "PD1818B", "model_sw_ver": "V1818BA"},
        {"model": "vivo Y93 标准版 (V1818CA)", "codename": "PD1818B", "model_sw_ver": "V1818CA"},
        {"model": "vivo Y93 标准版 移动全网通", "codename": "PD1818B", "model_sw_ver": "V1818CT"},
        {"model": "vivo Y93s", "codename": "PD1818C", "model_sw_ver": "V1818CA"},
        {"model": "vivo Y93s 移动全网通", "codename": "PD1818C", "model_sw_ver": "V1818CT"},
        {"model": "vivo Y97", "codename": "PD1813", "model_sw_ver": "V1813A"},
        {"model": "vivo Y97 移动全网通", "codename": "PD1813", "model_sw_ver": "V1813T"},
        {"model": "vivo Y100 5G", "codename": "PD2313", "model_sw_ver": "V2313A"},
        {"model": "vivo Y100t 5G", "codename": "PD2314", "model_sw_ver": "V2314DA"},
        {"model": "vivo Y100i 5G", "codename": "PD2279", "model_sw_ver": "V2279A"},
        {"model": "vivo Y100i 长续航版 5G", "codename": "PD2312", "model_sw_ver": "V2312BA"},
        {"model": "vivo Y100+ 5G", "codename": "PD2354", "model_sw_ver": "V2354A"},
        {"model": "vivo Y200i 5G", "codename": "PD2354", "model_sw_ver": "V2354A"},
        {"model": "vivo Y200+ 5G", "codename": "PD2354", "model_sw_ver": "V2354A"},
        {"model": "vivo Y200 5G", "codename": "PD2343", "model_sw_ver": "V2343A"},
        {"model": "vivo Y200 GT 5G", "codename": "PD2361", "model_sw_ver": "V2361GA"},
        {"model": "vivo Y200 Pro 企业定制版", "codename": "PD2361", "model_sw_ver": "V2361GA"},
        {"model": "vivo Y200t 5G", "codename": "PD2353", "model_sw_ver": "V2353DA"},
        {"model": "vivo Y300 5G", "codename": "PD2435", "model_sw_ver": "V2435A"},
        {"model": "vivo Y300c", "codename": "PD2435", "model_sw_ver": "V2435A"},
        {"model": "vivo Y300i 5G", "codename": "PD2444", "model_sw_ver": "V2444A"},
        {"model": "vivo Y300 Pro", "codename": "PD2410", "model_sw_ver": "V2410A"},
        {"model": "vivo Y300 Pro+", "codename": "PD2456", "model_sw_ver": "V2456A"},
        {"model": "vivo Y300t", "codename": "PD2445D", "model_sw_ver": "V2445EA"},
        {"model": "vivo Y300+", "codename": "PD2445D", "model_sw_ver": "V2445EA"},
        {"model": "vivo Y300 GT", "codename": "PD2452", "model_sw_ver": "V2452GA"},
        {"model": "vivo Y500", "codename": "PD2506", "model_sw_ver": "V2506A"},
        {"model": "vivo Y500 Pro", "codename": "PD2516", "model_sw_ver": "V2516A"},
        {"model": "vivo Y500i", "codename": "PD2531", "model_sw_ver": "V2531A"},
        {"model": "vivo Y500s", "codename": "PD2531", "model_sw_ver": "V2531A"},
        {"model": "vivo Y6", "codename": "PD2531", "model_sw_ver": "V2531A"},
        {"model": "vivo Y600 Pro", "codename": "PD2561", "model_sw_ver": "V2561A"},
        {"model": "vivo Y600 Turbo", "codename": "PD2553", "model_sw_ver": "V2553A"},
    ],
    "T 系列": [
        {"model": "vivo T1", "codename": "PD2115", "model_sw_ver": "V2115A"},
        {"model": "vivo T1x", "codename": "PD2123", "model_sw_ver": "V2123A"},
        {"model": "vivo T2", "codename": "PD2199", "model_sw_ver": "V2199GA"},
        {"model": "vivo T2x", "codename": "PD2188", "model_sw_ver": "V2188A"},
    ],
    "Z 系列": [
        {"model": "vivo Z1", "codename": "PD1730C", "model_sw_ver": "V1801A0"},
        {"model": "vivo Z1i", "codename": "PD1730D", "model_sw_ver": "V1730DA"},
        {"model": "vivo Z1i 移动全网通", "codename": "PD1730D", "model_sw_ver": "V1730DT"},
        {"model": "vivo Z1 青春版", "codename": "PD1730E", "model_sw_ver": "V1730EA"},
        {"model": "vivo Z3 (骁龙670)", "codename": "PD1813B", "model_sw_ver": "V1813BA"},
        {"model": "vivo Z3 (骁龙710)", "codename": "PD1813B", "model_sw_ver": "V1813BT"},
        {"model": "vivo Z3i", "codename": "PD1813", "model_sw_ver": "V1813A"},
        {"model": "vivo Z3i 移动全网通", "codename": "PD1813", "model_sw_ver": "V1813T"},
        {"model": "vivo Z3i 标准版", "codename": "PD1813", "model_sw_ver": "V1813A"},
        {"model": "vivo Z3i 标准版 移动全网通", "codename": "PD1813", "model_sw_ver": "V1813T"},
        {"model": "vivo Z3x", "codename": "PD1730G", "model_sw_ver": "V1730GA"},
        {"model": "vivo Z5", "codename": "PD1921", "model_sw_ver": "V1921A"},
        {"model": "vivo Z5 移动全网通", "codename": "PD1921", "model_sw_ver": "V1921T"},
        {"model": "vivo Z5x", "codename": "PD1911", "model_sw_ver": "V1911A"},
        {"model": "vivo Z5x 移动全网通", "codename": "PD1911", "model_sw_ver": "V1919A"},
        {"model": "vivo Z5x 712版", "codename": "PD1990", "model_sw_ver": "V1990A"},
        {"model": "vivo Z5i", "codename": "PD1941", "model_sw_ver": "V1941A"},
        {"model": "vivo Z5i 移动全网通", "codename": "PD1941", "model_sw_ver": "V1941T"},
        {"model": "vivo Z6 5G", "codename": "PD1963", "model_sw_ver": "V1963A"},
    ],
    "U 系列": [
        {"model": "vivo U1", "codename": "PD1818", "model_sw_ver": "V1818A"},
        {"model": "vivo U3", "codename": "PD1941", "model_sw_ver": "V1941A"},
        {"model": "vivo U3 移动全网通", "codename": "PD1941", "model_sw_ver": "V1941T"},
        {"model": "vivo U3x", "codename": "PD1928", "model_sw_ver": "V1928A"},
        {"model": "vivo U3x 移动全网通", "codename": "PD1928", "model_sw_ver": "V1928T"},
    ],
    "G 系列": [
        {"model": "vivo G1", "codename": "PD1962B", "model_sw_ver": "V1962BA"},
        {"model": "vivo G2", "codename": "PD2318", "model_sw_ver": "V2318A"},
        {"model": "vivo G3", "codename": "PD2443", "model_sw_ver": "V2443A"},
    ],
    "iQOO 旗舰系列": [
        {"model": "iQOO (6+128)", "codename": "PD1824", "model_sw_ver": "V1824BA"},
        {"model": "iQOO (8/12GB)", "codename": "PD1824", "model_sw_ver": "V1824A"},
        {"model": "iQOO Pro", "codename": "PD1922", "model_sw_ver": "V1922A"},
        {"model": "iQOO Pro 移动全网通", "codename": "PD1922", "model_sw_ver": "V1922T"},
        {"model": "iQOO Pro 5G", "codename": "PD1916", "model_sw_ver": "V1916A"},
        {"model": "iQOO Pro 5G 移动全网通", "codename": "PD1916", "model_sw_ver": "V1916T"},
        {"model": "iQOO 3", "codename": "PD1955", "model_sw_ver": "V1955A"},
        {"model": "iQOO 5", "codename": "PD2024", "model_sw_ver": "V2024A"},
        {"model": "iQOO 5 Pro", "codename": "PD2025", "model_sw_ver": "V2025A"},
        {"model": "iQOO 7", "codename": "PD2049", "model_sw_ver": "V2049A"},
        {"model": "iQOO 8", "codename": "PD2136", "model_sw_ver": "V2136A"},
        {"model": "iQOO 8 Pro", "codename": "PD2141", "model_sw_ver": "V2141A"},
        {"model": "iQOO 9", "codename": "PD2171", "model_sw_ver": "V2171A"},
        {"model": "iQOO 9 Pro", "codename": "PD2172", "model_sw_ver": "V2172A"},
        {"model": "iQOO 10", "codename": "PD2217", "model_sw_ver": "V2217A"},
        {"model": "iQOO 10 Pro", "codename": "PD2218", "model_sw_ver": "V2218A"},
        {"model": "iQOO 11", "codename": "PD2243", "model_sw_ver": "V2243A"},
        {"model": "iQOO 11 Pro", "codename": "PD2254", "model_sw_ver": "V2254A"},
        {"model": "iQOO 11S", "codename": "PD2304", "model_sw_ver": "V2304A"},
        {"model": "iQOO 12", "codename": "PD2307", "model_sw_ver": "V2307A"},
        {"model": "iQOO 12 Pro", "codename": "PD2329", "model_sw_ver": "V2329A"},
        {"model": "iQOO 13", "codename": "PD2408", "model_sw_ver": "V2408A"},
        {"model": "iQOO 15", "codename": "PD2505", "model_sw_ver": "V2505A"},
        {"model": "iQOO 15 Ultra", "codename": "PD2546", "model_sw_ver": "V2546A"},
        {"model": "iQOO 15T", "codename": "PD2564", "model_sw_ver": "V2564A"},
    ],
    "iQOO Neo 系列": [
        {"model": "iQOO Neo", "codename": "PD1914", "model_sw_ver": "V1914A"},
        {"model": "iQOO Neo 移动全网通", "codename": "PD1914", "model_sw_ver": "V1914T"},
        {"model": "iQOO Neo 855版", "codename": "PD1936", "model_sw_ver": "V1936A"},
        {"model": "iQOO Neo 855版 移动全网通", "codename": "PD1936", "model_sw_ver": "V1936T"},
        {"model": "iQOO Neo 855竞速版", "codename": "PD1936", "model_sw_ver": "V1936AL"},
        {"model": "iQOO Neo 855竞速版 移动全网通", "codename": "PD1936", "model_sw_ver": "V1936TL"},
        {"model": "iQOO Neo3", "codename": "PD1981", "model_sw_ver": "V1981A"},
        {"model": "iQOO Neo5", "codename": "PD2055", "model_sw_ver": "V2055A"},
        {"model": "iQOO Neo5 活力版", "codename": "PD2118", "model_sw_ver": "V2118A"},
        {"model": "iQOO Neo5S", "codename": "PD2154", "model_sw_ver": "V2154A"},
        {"model": "iQOO Neo5 SE", "codename": "PD2157", "model_sw_ver": "V2157A"},
        {"model": "iQOO Neo6", "codename": "PD2196", "model_sw_ver": "V2196A"},
        {"model": "iQOO Neo6 SE", "codename": "PD2199", "model_sw_ver": "V2199A"},
        {"model": "iQOO Neo7", "codename": "PD2231", "model_sw_ver": "V2231A"},
        {"model": "iQOO Neo7 竞速版", "codename": "PD2232", "model_sw_ver": "V2232A"},
        {"model": "iQOO Neo7 SE", "codename": "PD2238", "model_sw_ver": "V2238A"},
        {"model": "iQOO Neo8", "codename": "PD2301", "model_sw_ver": "V2301A"},
        {"model": "iQOO Neo8 Pro", "codename": "PD2302", "model_sw_ver": "V2302A"},
        {"model": "iQOO Neo9", "codename": "PD2338", "model_sw_ver": "V2338A"},
        {"model": "iQOO Neo9 Pro", "codename": "PD2339", "model_sw_ver": "V2339A"},
        {"model": "iQOO Neo9S Pro", "codename": "PD2339", "model_sw_ver": "V2339FA"},
        {"model": "iQOO Neo9S Pro+", "codename": "PD2403", "model_sw_ver": "V2403A"},
        {"model": "iQOO Neo10", "codename": "PD2425", "model_sw_ver": "V2425A"},
        {"model": "iQOO Neo10 Pro", "codename": "PD2426", "model_sw_ver": "V2426A"},
        {"model": "iQOO Neo10 Pro+", "codename": "PD2463", "model_sw_ver": "V2463A"},
        {"model": "iQOO Neo11", "codename": "PD2520", "model_sw_ver": "V2520A"},
    ],
    "iQOO Z 系列": [
        {"model": "iQOO Z1", "codename": "PD1986", "model_sw_ver": "V1986A"},
        {"model": "iQOO Z1x", "codename": "PD2012", "model_sw_ver": "V2012A"},
        {"model": "iQOO Z3", "codename": "PD2073", "model_sw_ver": "V2073A"},
        {"model": "iQOO Z5", "codename": "PD2148", "model_sw_ver": "V2148A"},
        {"model": "iQOO Z5x", "codename": "PD2131", "model_sw_ver": "V2131A"},
        {"model": "iQOO Z6", "codename": "PD2220", "model_sw_ver": "V2220A"},
        {"model": "iQOO Z6 活力版", "codename": "PD2220", "model_sw_ver": "V2220A"},
        {"model": "iQOO Z6x", "codename": "PD2164U", "model_sw_ver": "V2164KA"},
        {"model": "iQOO Z7", "codename": "PD2270", "model_sw_ver": "V2270A"},
        {"model": "iQOO Z7x", "codename": "PD2272", "model_sw_ver": "V2272A"},
        {"model": "iQOO Z7i", "codename": "PD2230", "model_sw_ver": "V2230EA"},
        {"model": "iQOO Z8", "codename": "PD2314", "model_sw_ver": "V2314A"},
        {"model": "iQOO Z8x", "codename": "PD2312", "model_sw_ver": "V2312A"},
        {"model": "iQOO Z9", "codename": "PD2361", "model_sw_ver": "V2361A"},
        {"model": "iQOO Z9 Turbo", "codename": "PD2352", "model_sw_ver": "V2352A"},
        {"model": "iQOO Z9 Turbo 长续航版", "codename": "PD2352G", "model_sw_ver": "V2352GA"},
        {"model": "iQOO Z9 Turbo+", "codename": "PD2417", "model_sw_ver": "V2417A"},
        {"model": "iQOO Z9x", "codename": "PD2353", "model_sw_ver": "V2353A"},
        {"model": "iQOO Z10 Turbo", "codename": "PD2452", "model_sw_ver": "V2452A"},
        {"model": "iQOO Z10 Turbo Pro", "codename": "PD2453", "model_sw_ver": "V2453A"},
        {"model": "iQOO Z10 Turbo+", "codename": "PD2507", "model_sw_ver": "V2507A"},
        {"model": "iQOO Z10x", "codename": "PD2445", "model_sw_ver": "V2445A"},
        {"model": "iQOO Z11 Turbo", "codename": "PD2536", "model_sw_ver": "V2536A"},
        {"model": "iQOO Z11", "codename": "PD2551", "model_sw_ver": "V2551A"},
        {"model": "iQOO Z11x", "codename": "PD2532", "model_sw_ver": "V2532A"},
    ],
    "iQOO U 系列": [
        {"model": "iQOO U1", "codename": "PD2023", "model_sw_ver": "V2023A"},
        {"model": "iQOO U1x", "codename": "PD2065", "model_sw_ver": "V2065A"},
        {"model": "iQOO U3 5G", "codename": "PD2061", "model_sw_ver": "V2061A"},
        {"model": "iQOO U3x 5G", "codename": "PD2106", "model_sw_ver": "V2106A"},
        {"model": "iQOO U3x 标准版", "codename": "PD2143", "model_sw_ver": "V2143A"},
        {"model": "iQOO U5 5G", "codename": "PD2165", "model_sw_ver": "V2165A"},
        {"model": "iQOO U5x", "codename": "PD2180G", "model_sw_ver": "V2180GA"},
        {"model": "iQOO U5e 5G", "codename": "PD2197", "model_sw_ver": "V2197A"},
    ],
    "平板电脑": [
        {"model": "vivo Pad", "codename": "DPD2106", "model_sw_ver": "PA2170"},
        {"model": "vivo Pad2", "codename": "DPD2221", "model_sw_ver": "PA2373"},
        {"model": "vivo Pad Air", "codename": "DPD2305", "model_sw_ver": "PA2353"},
        {"model": "vivo Pad3", "codename": "DPD2345", "model_sw_ver": "PA2455"},
        {"model": "vivo Pad3 Pro", "codename": "DPD2329", "model_sw_ver": "PA2473"},
        {"model": "vivo Pad5", "codename": "DPD2437", "model_sw_ver": "PA2553"},
        {"model": "vivo Pad5 Pro", "codename": "DPD2429", "model_sw_ver": "PA2573"},
        {"model": "vivo Pad5e", "codename": "DPD2345", "model_sw_ver": "PA2535"},
        {"model": "vivo Pad SE", "codename": "DPD2424", "model_sw_ver": "PA2511"},
        {"model": "vivo Pad6 Pro", "codename": "DPD2540", "model_sw_ver": "PA2671"},
        {"model": "iQOO Pad", "codename": "DPD2307", "model_sw_ver": "iPA2375"},
        {"model": "iQOO Pad Air", "codename": "DPD2305", "model_sw_ver": "iPA2451"},
        {"model": "iQOO Pad2", "codename": "DPD2345", "model_sw_ver": "iPA2453"},
        {"model": "iQOO Pad2 Pro", "codename": "DPD2329", "model_sw_ver": "iPA2475"},
        {"model": "iQOO Pad5", "codename": "DPD2437", "model_sw_ver": "iPA2556"},
        {"model": "iQOO Pad5 Pro", "codename": "DPD2438", "model_sw_ver": "iPA2575"},
        {"model": "iQOO Pad5e", "codename": "DPD2345", "model_sw_ver": "iPA2537"},
        {"model": "iQOO Pad6 Pro", "codename": "DPD2540", "model_sw_ver": "iPA2673"},
    ],
    "穿戴设备": [
        {"model": "vivo WATCH 42mm", "codename": "WA2052", "model_sw_ver": "WA2052"},
        {"model": "vivo WATCH 46mm", "codename": "WA2056", "model_sw_ver": "WA2056"},
        {"model": "vivo WATCH 2 eSIM版", "codename": "WA2156A", "model_sw_ver": "WA2156A"},
        {"model": "vivo WATCH 3 eSIM版", "codename": "WA2356A", "model_sw_ver": "WA2356A"},
        {"model": "vivo WATCH 3 蓝牙版", "codename": "WA2356C", "model_sw_ver": "WA2356C"},
        {"model": "vivo WATCH GT eSIM版", "codename": "WA2456A", "model_sw_ver": "WA2456A"},
        {"model": "vivo WATCH GT 蓝牙版", "codename": "WA2456C", "model_sw_ver": "WA2456C"},
        {"model": "vivo WATCH 5 蓝牙版", "codename": "WA2556A", "model_sw_ver": "WA2556A"},
        {"model": "vivo WATCH 5 eSIM版", "codename": "WA2556B", "model_sw_ver": "WA2556B"},
        {"model": "vivo WATCH GT 2 蓝牙版", "codename": "WA2536A", "model_sw_ver": "WA2536A"},
        {"model": "vivo WATCH GT 2 eSIM版", "codename": "WA2536B", "model_sw_ver": "WA2536B"},
        {"model": "iQOO WATCH eSIM版", "codename": "iWA2356A", "model_sw_ver": "iWA2356A"},
        {"model": "iQOO WATCH 蓝牙版", "codename": "iWA2356C", "model_sw_ver": "iWA2356C"},
        {"model": "iQOO WATCH GT eSIM版", "codename": "iWA2456A", "model_sw_ver": "iWA2456A"},
        {"model": "iQOO WATCH GT 蓝牙版", "codename": "iWA2456C", "model_sw_ver": "iWA2456C"},
        {"model": "iQOO WATCH 5 蓝牙版", "codename": "iWA2556A", "model_sw_ver": "iWA2556A"},
        {"model": "iQOO WATCH 5 eSIM版", "codename": "iWA2556B", "model_sw_ver": "iWA2556B"},
        {"model": "iQOO WATCH GT 2 蓝牙版", "codename": "iWA2536A", "model_sw_ver": "iWA2536A"},
        {"model": "iQOO WATCH GT 2 eSIM版", "codename": "iWA2536C", "model_sw_ver": "iWA2536C"},
    ],
}


# ── 主题配置 ──────────────────────────────────────────
THEMES = {
    'light': {
        'name': '浅色',
        'app_bg': '#f0f2f5',
        'card_bg': '#ffffff',
        'text': '#1a1a2e',
        'text_secondary': '#666680',
        'accent': '#4a90d9',
        'accent_hover': '#357abd',
        'border': '#dde1e6',
        'log_bg': '#ffffff',
        'log_text': '#1a1a2e',
        'btn_bg': '#e8ecf1',
        'btn_text': '#1a1a2e',
        'btn_hover': '#dde1e6',
        'btn_primary_bg': '#4a90d9',
        'btn_primary_hover': '#357abd',
        'btn_primary_text': '#ffffff',
        'btn_success_bg': '#52c41a',
        'btn_success_hover': '#45a615',
        'btn_success_text': '#ffffff',
        'input_bg': '#ffffff',
        'input_text': '#1a1a2e',
        'input_border': '#d0d5dd',
        'input_focus': '#4a90d9',
        'group_title': '#4a90d9',
        'progress_bg': '#e8ecf1',
        'progress_chunk': '#4a90d9',
        'scrollbar_bg': '#e8ecf1',
        'scrollbar_thumb': '#c0c4cc',
        'shadow': 'rgba(0,0,0,0.06)',
    },
    'dark': {
        'name': '深色',
        'app_bg': '#0f0f1a',
        'card_bg': '#1a1a2e',
        'text': '#e4e6eb',
        'text_secondary': '#b0b3b8',
        'accent': '#5b9bd5',
        'accent_hover': '#4a8ac4',
        'border': '#2d2d44',
        'log_bg': '#1a1a2e',
        'log_text': '#e4e6eb',
        'btn_bg': '#2a2a44',
        'btn_text': '#e4e6eb',
        'btn_hover': '#35355a',
        'btn_primary_bg': '#5b9bd5',
        'btn_primary_hover': '#4a8ac4',
        'btn_primary_text': '#ffffff',
        'btn_success_bg': '#45a615',
        'btn_success_hover': '#3a8e11',
        'btn_success_text': '#ffffff',
        'input_bg': '#252540',
        'input_text': '#e4e6eb',
        'input_border': '#3d3d5c',
        'input_focus': '#5b9bd5',
        'group_title': '#5b9bd5',
        'progress_bg': '#2a2a44',
        'progress_chunk': '#5b9bd5',
        'scrollbar_bg': '#1a1a2e',
        'scrollbar_thumb': '#3d3d5c',
        'shadow': 'rgba(0,0,0,0.30)',
    }
}

# ── 多语言翻译 ────────────────────────────────────────
TR = {
    # 窗口
    'window_title':       {'zh': f'Vivo Ota Tracker By mytiantian {APP_VERSION}', 'en': f'Vivo Ota Tracker By mytiantian {APP_VERSION}'},
    # 分组标题
    'device_model_select': {'zh': '设备型号选择', 'en': 'Device Model'},
    'config_params':      {'zh': '配置参数', 'en': 'Configuration'},
    # 标签
    'series':       {'zh': '系列', 'en': 'Series'},
    'model':        {'zh': '型号', 'en': 'Model'},
    'model_sw_ver_label': {'zh': '项目代号', 'en': 'Project Code'},
    'device_model_label': {'zh': '入网型号', 'en': 'Network Model'},
    'sw_version_label':   {'zh': '系统软件版本', 'en': 'System Version'},
    'android_ver_label':  {'zh': '底层安卓版本', 'en': 'Android Version'},
    # 占位符
    'model_sw_ver_ph':  {'zh': '软件型号，例如 PD2408', 'en': 'Software model, e.g. PD2408'},
    'device_model_ph':  {'zh': '设备型号，例如 V2408A', 'en': 'Device model, e.g. V2408A'},
    'sw_version_ph':    {'zh': '系统版本号，例如 16.1.16.5.W10', 'en': 'System version, e.g. 16.1.16.5.W10'},
    'android_ver_ph':   {'zh': '安卓版本，例如 16', 'en': 'Android version, e.g. 16'},
    # 提示
    'model_sw_ver_tip': {'zh': '软件型号，例如 PD2408', 'en': 'Software model, e.g. PD2408'},
    'device_model_tip': {'zh': '设备型号，例如 V2408A', 'en': 'Device model, e.g. V2408A'},
    'sw_version_tip':   {'zh': '系统版本号，例如 16.1.16.5.W10', 'en': 'System version, e.g. 16.1.16.5.W10'},
    'android_ver_tip':  {'zh': '安卓版本，例如 16（13=OriginOS3, 14=OriginOS4, 15=OriginOS5, 16=OriginOS6）',
                          'en': 'Android version, e.g. 16 (13=OriginOS3, 14=OriginOS4, 15=OriginOS5, 16=OriginOS6)'},
    # 按钮
    'start_get_link':  {'zh': '开始获取链接', 'en': 'Get Download Link'},
    'verbose_mode':    {'zh': '详细日志模式', 'en': 'Verbose Log'},
    'verbose_tip':     {'zh': '勾选后显示完整日志输出，不勾选仅显示简洁结果',
                         'en': 'Show full log output when checked, concise result otherwise'},
    'copy_clipboard':  {'zh': '一键复制到剪贴板', 'en': 'Copy to Clipboard'},
    'theme_toggle':    {'zh': '切换深色模式', 'en': 'Toggle Light Mode'},
    'lang_toggle':     {'zh': 'EN', 'en': '中'},
    'lang_tip':        {'zh': '切换为英文', 'en': 'Switch to Chinese'},
    # 消息弹窗
    'warn_fill_all':   {'zh': '请填写所有参数后再开始获取链接！\n\n- 项目代号\n- 入网型号\n- 系统软件版本\n- 底层安卓版本（需为数字）',
                         'en': 'Please fill in all parameters before getting the link!\n\n- Project Code\n- Network Model\n- System Version\n- Android Version (digits only)'},
    'no_result_to_copy': {'zh': '没有可复制的结果，请先运行查询。', 'en': 'No result to copy. Please run a query first.'},
    'copied':       {'zh': '已复制到剪贴板！', 'en': 'Copied to clipboard!'},
    'error_title':  {'zh': '错误', 'en': 'Error'},
    'warn_title':   {'zh': '警告', 'en': 'Warning'},
    'success_title': {'zh': '成功', 'en': 'Success'},
    'info_title':   {'zh': '提示', 'en': 'Info'},
    # 运行状态
    'please_wait':  {'zh': '正在执行中，请稍等……', 'en': 'Running, please wait...'},
    'step_running': {'zh': '[Step 1/1] 正在运行 VivoOtaTracker...', 'en': '[Step 1/1] Running VivoOtaTracker...'},
    'exec_cmd':     {'zh': '执行命令', 'en': 'Command'},
    'error_exec_fail': {'zh': '执行失败！错误码', 'en': 'Execution failed! Exit code'},
    'error_no_java': {'zh': '未找到 Java 运行时环境', 'en': 'Java runtime not found'},
    'done':         {'zh': '[完成] OTA Tracker 运行结束！', 'en': '[Done] OTA Tracker finished!'},
    'ota_banner':   {'zh': 'OTA 更新信息', 'en': 'OTA Update Info'},
    # 结果字段
    'device_type_field': {'zh': '设备类型', 'en': 'Device Type'},
    'device_model_field': {'zh': '设备型号', 'en': 'Device Model'},
    'android_ver_field':  {'zh': 'Android版本', 'en': 'Android Ver'},
    'sw_ver_field':       {'zh': '软件版本', 'en': 'SW Version'},
    'file_size_field':    {'zh': '软件包大小', 'en': 'Package Size'},
    'download_url_field': {'zh': '下载链接', 'en': 'Download URL'},
    # 设备类型中文
    'phone_cn':  {'zh': '手机', 'en': 'Phone'},
    'tablet_cn': {'zh': '平板', 'en': 'Tablet'},
    # 底部标签
    'credit_text': {
        'zh': '图形化制作基于 <b>PyQt5</b> | GUI作者: <b>酷安@mytiantian_是天天吖</b> | 原项目作者: <b>酷安@桜酱没有未来</b><br>'
              '原项目: ',
        'en': 'GUI built with <b>PyQt5</b> | GUI Author: <b>CoolAPK@mytiantian</b> | Original Author: <b>CoolAPK@桜酱没有未来</b><br>'
              'Original: ',
    },
}

def t(key, lang='zh'):
    """获取翻译文本"""
    entry = TR.get(key, {})
    return entry.get(lang, key)

# ── 通用样式表生成器 ──────────────────────────────────
def make_stylesheet(theme):
    """根据主题生成全局 QSS"""
    return f"""
    QMainWindow {{
        background-color: {theme['app_bg']};
    }}
    QWidget {{
        color: {theme['text']};
        font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    }}
    QGroupBox {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 10px;
        margin-top: 14px;
        padding: 18px 14px 10px 14px;
        font-weight: bold;
        font-size: 13px;
        color: {theme['group_title']};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 8px;
        color: {theme['group_title']};
    }}
    QLabel {{
        color: {theme['text']};
        background: transparent;
    }}
    QLineEdit {{
        background-color: {theme['input_bg']};
        color: {theme['input_text']};
        border: 1.5px solid {theme['input_border']};
        border-radius: 8px;
        padding: 7px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus {{
        border-color: {theme['input_focus']};
    }}
    QPushButton {{
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 500;
        background-color: {theme['btn_bg']};
        color: {theme['btn_text']};
    }}
    QPushButton:hover {{
        background-color: {theme['btn_hover']};
    }}
    QPushButton:pressed {{
        background-color: {theme['border']};
    }}
    QPushButton:disabled {{
        opacity: 0.45;
    }}
    QPushButton#runBtn {{
        background-color: {theme['btn_primary_bg']};
        color: {theme['btn_primary_text']};
        font-weight: bold;
    }}
    QPushButton#runBtn:hover {{
        background-color: {theme['btn_primary_hover']};
    }}
    QPushButton#copyBtn {{
        background-color: {theme['btn_success_bg']};
        color: {theme['btn_success_text']};
        font-weight: bold;
        border-radius: 8px;
    }}
    QPushButton#copyBtn:hover {{
        background-color: {theme['btn_success_hover']};
    }}
    QPushButton#iconBtn {{
        background: transparent;
        border: 1.5px solid {theme['border']};
        border-radius: 8px;
        padding: 6px 14px;
        font-weight: bold;
        font-size: 12px;
        color: {theme['text_secondary']};
    }}
    QPushButton#iconBtn:hover {{
        background-color: {theme['btn_hover']};
        color: {theme['text']};
    }}
    QComboBox {{
        background-color: {theme['input_bg']};
        color: {theme['input_text']};
        border: 1.5px solid {theme['input_border']};
        border-radius: 8px;
        padding: 7px 12px;
        font-size: 13px;
    }}
    QComboBox:hover {{
        border-color: {theme['input_focus']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {theme['card_bg']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        selection-background-color: {theme['accent']};
        border-radius: 4px;
    }}
    QCheckBox {{
        color: {theme['text_secondary']};
        spacing: 6px;
        font-size: 12px;
    }}
    QCheckBox::indicator {{
        width: 16px; height: 16px;
        border: 1.5px solid {theme['input_border']};
        border-radius: 4px;
        background: {theme['input_bg']};
    }}
    QCheckBox::indicator:checked {{
        background: {theme['accent']};
        border-color: {theme['accent']};
    }}
    QProgressBar {{
        border: none;
        border-radius: 6px;
        background-color: {theme['progress_bg']};
        height: 6px;
        text-align: center;
        font-size: 11px;
    }}
    QProgressBar::chunk {{
        background-color: {theme['progress_chunk']};
        border-radius: 6px;
    }}
    QTextEdit {{
        background-color: {theme['log_bg']};
        color: {theme['log_text']};
        border: 1.5px solid {theme['border']};
        border-radius: 10px;
        padding: 12px;
        font-family: "Cascadia Code", "Consolas", "Microsoft YaHei", monospace;
        font-size: 12px;
    }}
    QScrollBar:vertical {{
        background: {theme['scrollbar_bg']};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {theme['scrollbar_thumb']};
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QMessageBox {{
        background-color: {theme['card_bg']};
    }}
    QMessageBox QLabel {{
        color: {theme['text']};
        font-size: 13px;
    }}
    QMessageBox QPushButton {{
        background-color: {theme['btn_primary_bg']};
        color: {theme['btn_primary_text']};
        border-radius: 6px;
        padding: 6px 20px;
        font-weight: bold;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {theme['btn_primary_hover']};
    }}
    """


class VivoOtaTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'zh'
        self.theme = 'light'
        self.setWindowTitle(t('window_title', self.lang))
        self.setGeometry(100, 100, 920, 680)
        
        # 设置主窗口图标（使用 resource_path 兼容打包模式）
        icon_path = resource_path("assets/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            # 同时设置 QApplication 级图标（Windows 任务栏依赖此设置）
            QApplication.instance().setWindowIcon(QIcon(icon_path))
        
        # 配置文件路径（持久化到用户目录，避免临时目录只读问题）
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        self.config_dir = os.path.join(appdata, 'VivoOtaTracker')
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, 'config.json')
        
        # 初始化变量
        self.current_config = {
            'DEVICE_TYPE': 'phone',
            'MODEL_SW_VER': '',
            'DEVICE_MODEL': '',
            'SW_VERSION': '',
            'ANDROID_VER': ''
        }
        
        # 状态标志
        self.current_stage = None  # 'compile' 或 'run'
        self.raw_output = ""  # 收集原始输出，用于简洁模式解析
        self.last_result_text = ""  # 缓存最后一次的简洁结果，用于复制
        
        self.init_ui()
        # 不再加载保存的配置，选型号后直接可运行
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(10)
        
        # ── 标题栏：Logo + 主题/语言切换 ──
        top_row = QHBoxLayout()
        # 左上角 Logo
        self.logo_label = QLabel()
        logo_path = resource_path("assets/logo_os11_img_pad.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaledToHeight(36, Qt.SmoothTransformation)
                self.logo_label.setPixmap(logo_pixmap)
        else:
            self.logo_label.setText("Vivo OTA")
            self.logo_label.setStyleSheet("font-weight:bold; font-size:15px; color:#4a90d9;")
        self.logo_label.setFixedHeight(40)
        top_row.addWidget(self.logo_label)
        top_row.addStretch()
        self.lang_btn = QPushButton(t('lang_toggle', self.lang))
        self.lang_btn.setObjectName("iconBtn")
        self.lang_btn.setToolTip(t('lang_tip', self.lang))
        self.lang_btn.setFixedSize(48, 32)
        self.lang_btn.clicked.connect(self.toggle_language)
        top_row.addWidget(self.lang_btn)
        self.theme_btn = QPushButton(t('theme_toggle', self.lang))
        self.theme_btn.setObjectName("iconBtn")
        self.theme_btn.setFixedSize(120, 32)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_row.addWidget(self.theme_btn)
        main_layout.addLayout(top_row)
        
        # ── 设备型号选择器 ──
        self.device_model_group = QGroupBox(t('device_model_select', self.lang))
        device_model_layout = QVBoxLayout(self.device_model_group)
        
        row0 = QHBoxLayout()
        self.series_label = QLabel(t('series', self.lang))
        self.series_label.setFixedWidth(120)
        self.series_label.setAlignment(Qt.AlignCenter)
        row0.addWidget(self.series_label)
        self.series_combo = QComboBox()
        self.series_combo.addItems(list(DEVICE_DATABASE.keys()))
        self.series_combo.currentTextChanged.connect(self.on_series_changed)
        row0.addWidget(self.series_combo)
        device_model_layout.addLayout(row0)
        
        row0_2 = QHBoxLayout()
        self.model_label = QLabel(t('model', self.lang))
        self.model_label.setFixedWidth(120)
        self.model_label.setAlignment(Qt.AlignCenter)
        row0_2.addWidget(self.model_label)
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(400)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        row0_2.addWidget(self.model_combo)
        device_model_layout.addLayout(row0_2)
        
        main_layout.addWidget(self.device_model_group)
        
        # ── 配置参数输入 ──
        self.config_group = QGroupBox(t('config_params', self.lang))
        config_layout = QVBoxLayout(self.config_group)
        
        row1 = QHBoxLayout()
        self.model_sw_ver_label = QLabel(t('model_sw_ver_label', self.lang))
        self.model_sw_ver_label.setFixedWidth(120)
        self.model_sw_ver_label.setToolTip(t('model_sw_ver_tip', self.lang))
        self.model_sw_ver_label.setAlignment(Qt.AlignCenter)
        row1.addWidget(self.model_sw_ver_label)
        self.model_sw_ver_edit = QLineEdit()
        self.model_sw_ver_edit.setPlaceholderText(t('model_sw_ver_ph', self.lang))
        row1.addWidget(self.model_sw_ver_edit)
        config_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.device_model_label = QLabel(t('device_model_label', self.lang))
        self.device_model_label.setFixedWidth(120)
        self.device_model_label.setToolTip(t('device_model_tip', self.lang))
        self.device_model_label.setAlignment(Qt.AlignCenter)
        row2.addWidget(self.device_model_label)
        self.device_model_edit = QLineEdit()
        self.device_model_edit.setPlaceholderText(t('device_model_ph', self.lang))
        row2.addWidget(self.device_model_edit)
        config_layout.addLayout(row2)
        
        row3 = QHBoxLayout()
        self.sw_version_label = QLabel(t('sw_version_label', self.lang))
        self.sw_version_label.setFixedWidth(120)
        self.sw_version_label.setToolTip(t('sw_version_tip', self.lang))
        self.sw_version_label.setAlignment(Qt.AlignCenter)
        row3.addWidget(self.sw_version_label)
        self.sw_version_edit = QLineEdit()
        self.sw_version_edit.setPlaceholderText(t('sw_version_ph', self.lang))
        row3.addWidget(self.sw_version_edit)
        config_layout.addLayout(row3)
        
        row4 = QHBoxLayout()
        self.android_ver_label = QLabel(t('android_ver_label', self.lang))
        self.android_ver_label.setFixedWidth(120)
        self.android_ver_label.setToolTip(t('android_ver_tip', self.lang))
        self.android_ver_label.setAlignment(Qt.AlignCenter)
        row4.addWidget(self.android_ver_label)
        self.android_ver_edit = QLineEdit()
        self.android_ver_edit.setPlaceholderText(t('android_ver_ph', self.lang))
        self.android_ver_edit.setFixedWidth(80)
        row4.addWidget(self.android_ver_edit)
        row4.addStretch()
        config_layout.addLayout(row4)
        
        main_layout.addWidget(self.config_group)
        
        # ── 按钮区域 ──
        button_layout = QHBoxLayout()
        self.run_btn = QPushButton(t('start_get_link', self.lang))
        self.run_btn.setObjectName("runBtn")
        self.run_btn.clicked.connect(self.run_tracker)
        # 添加升级图标
        icon_path = resource_path("assets/ic_upgrade.png")
        if os.path.exists(icon_path):
            self.run_btn.setIcon(QIcon(icon_path))
            self.run_btn.setIconSize(QSize(20, 20))
        self.verbose_checkbox = QCheckBox(t('verbose_mode', self.lang))
        self.verbose_checkbox.setToolTip(t('verbose_tip', self.lang))
        self.verbose_checkbox.stateChanged.connect(self.on_verbose_changed)
        self.copy_btn = QPushButton(t('copy_clipboard', self.lang))
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setVisible(False)
        btn_icon_path = resource_path("assets/originui_vtoolbar_icon_save_rom13_5.png")
        if os.path.exists(btn_icon_path):
            self.copy_btn.setIcon(QIcon(btn_icon_path))
            self.copy_btn.setIconSize(QSize(18, 18))
        button_layout.addStretch()
        button_layout.addWidget(self.run_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.verbose_checkbox)
        button_layout.addWidget(self.copy_btn)
        main_layout.addLayout(button_layout)
        
        # ── 进度条 ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # ── 日志输出 ──
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)
        
        # ── 底部信息标签 ──
        self.credit_label = QLabel()
        self.credit_label.setOpenExternalLinks(True)
        self.credit_label.setTextFormat(1)  # Qt.RichText
        self._update_credit_label()
        main_layout.addWidget(self.credit_label)
        
        # ── 进程对象 ──
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_process_output)
        self.process.readyReadStandardError.connect(self.on_process_error)
        self.process.finished.connect(self.on_process_finished)
        
        # ── 应用初始主题 ──
        self._apply_theme()
        
        # 初始化型号列表
        self.on_series_changed(self.series_combo.currentText())
    
    # ── 主题/语言切换 ───────────────────────────────────
    def _apply_theme(self):
        """应用当前主题样式"""
        theme = THEMES[self.theme]
        self.setStyleSheet(make_stylesheet(theme))
        self.theme_btn.setText(t('theme_toggle', self.lang) if self.theme == 'light' else t('theme_toggle', self.lang))
        if self.theme == 'light':
            self.theme_btn.setText('🌙 暗色模式')
        else:
            self.theme_btn.setText('☀️ 亮色模式')
    
    def toggle_theme(self):
        """切换浅色/深色模式"""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self._apply_theme()
    
    def _update_credit_label(self):
        """刷新底部版权标签"""
        version_info = f"{APP_VERSION} | 2026-06-06" if self.lang == 'zh' else f"{APP_VERSION} | Built 2026-06-06"
        credit_html = (
            '<div style="text-align:center; padding:6px 0;">'
            '<span style="color:#888; font-size:11px;">'
            + t('credit_text', self.lang) +
            '</span>'
            '<a href="https://github.com/JerryTse-OSS/VIVO-OTA-Tracker" '
            'style="color:#4da6ff; font-size:11px; text-decoration:none;">'
            'JerryTse-OSS/VIVO-OTA-Tracker'
            '</a>'
            '<br><span style="color:#aaa; font-size:10px;">'
            + version_info +
            '</span>'
            '</div>'
        )
        self.credit_label.setText(credit_html)
    
    def _refresh_ui_texts(self):
        """刷新所有 UI 文本（语言切换时调用）"""
        self.setWindowTitle(t('window_title', self.lang))
        self.lang_btn.setText(t('lang_toggle', self.lang))
        self.lang_btn.setToolTip(t('lang_tip', self.lang))
        self.device_model_group.setTitle(t('device_model_select', self.lang))
        self.series_label.setText(t('series', self.lang))
        self.model_label.setText(t('model', self.lang))
        self.config_group.setTitle(t('config_params', self.lang))
        self.model_sw_ver_label.setText(t('model_sw_ver_label', self.lang))
        self.model_sw_ver_label.setToolTip(t('model_sw_ver_tip', self.lang))
        self.model_sw_ver_edit.setPlaceholderText(t('model_sw_ver_ph', self.lang))
        self.device_model_label.setText(t('device_model_label', self.lang))
        self.device_model_label.setToolTip(t('device_model_tip', self.lang))
        self.device_model_edit.setPlaceholderText(t('device_model_ph', self.lang))
        self.sw_version_label.setText(t('sw_version_label', self.lang))
        self.sw_version_label.setToolTip(t('sw_version_tip', self.lang))
        self.sw_version_edit.setPlaceholderText(t('sw_version_ph', self.lang))
        self.android_ver_label.setText(t('android_ver_label', self.lang))
        self.android_ver_label.setToolTip(t('android_ver_tip', self.lang))
        self.android_ver_edit.setPlaceholderText(t('android_ver_ph', self.lang))
        self.run_btn.setText(t('start_get_link', self.lang))
        self.verbose_checkbox.setText(t('verbose_mode', self.lang))
        self.verbose_checkbox.setToolTip(t('verbose_tip', self.lang))
        self.copy_btn.setText(t('copy_clipboard', self.lang))
        self._update_credit_label()
    
    def toggle_language(self):
        """切换中/英文"""
        new_lang = 'en' if self.lang == 'zh' else 'zh'
        self.lang = new_lang
        self._refresh_ui_texts()
        # 重新加载型号列表以更新下拉框显示文本
        current_series = self.series_combo.currentText()
        current_idx = self.model_combo.currentIndex()
        self.on_series_changed(current_series)
        self.model_combo.setCurrentIndex(current_idx)
    
    def on_series_changed(self, series):
        """系列变化时更新型号列表（格式：设备名 | PD2408 | V2408A）"""
        self.model_combo.clear()
        if series in DEVICE_DATABASE:
            devices = DEVICE_DATABASE[series]
            for device in devices:
                display = f"{device['model']}  |  {device['codename']}  |  {device['model_sw_ver']}"
                self.model_combo.addItem(display, device)
    
    def on_model_changed(self, index):
        """型号变化时自动填充参数并同步 current_config"""
        if index >= 0:
            device = self.model_combo.currentData()
            if device:
                # MODEL_SW_VER 填 codename（如 PD2408）
                self.model_sw_ver_edit.setText(device["codename"])
                # DEVICE_MODEL 填 model_sw_ver（如 V2408A）
                self.device_model_edit.setText(device["model_sw_ver"])
                # 同步到 current_config
                self.current_config['MODEL_SW_VER'] = device["codename"]
                self.current_config['DEVICE_MODEL'] = device["model_sw_ver"]
    
    def _style_messagebox(self, msg_box):
        """为 QMessageBox 应用当前主题样式，确保弹窗颜色与程序一致"""
        msg_box.setStyleSheet(make_stylesheet(THEMES[self.theme]))
    
    def _detect_device_type(self):
        """根据型号自动识别设备类型（DPD开头=平板，否则=手机）"""
        model_sw_ver = self.model_sw_ver_edit.text().strip()
        if model_sw_ver.startswith('DPD'):
            return 'tablet'
        return 'phone'
    
    def check_run_enabled(self):
        """检查输入完整性（仅用于日志提示，不再控制按钮状态）"""
        pass
    
    def run_tracker(self):
        """运行 OTA Tracker"""
        # 运行前先同步界面最新值到 current_config
        self.current_config['DEVICE_TYPE'] = self._detect_device_type()
        self.current_config['MODEL_SW_VER'] = self.model_sw_ver_edit.text().strip()
        self.current_config['DEVICE_MODEL'] = self.device_model_edit.text().strip()
        self.current_config['SW_VERSION'] = self.sw_version_edit.text().strip()
        self.current_config['ANDROID_VER'] = self.android_ver_edit.text().strip()
        
        # 验证输入：任一字段为空或安卓版本非数字则弹窗提示
        android_ver = self.current_config['ANDROID_VER']
        if not self.current_config['MODEL_SW_VER'] or \
           not self.current_config['DEVICE_MODEL'] or \
           not self.current_config['SW_VERSION'] or \
           not android_ver.isdigit():
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(t('warn_title', self.lang))
            msg_box.setText(t('warn_fill_all', self.lang))
            # 使用自定义图标替换默认警告图标
            warn_icon_path = resource_path("assets/originui_vtoolbar_icon_details_rom13_5.png")
            if os.path.exists(warn_icon_path):
                msg_box.setIconPixmap(QPixmap(warn_icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                msg_box.setWindowIcon(QIcon(warn_icon_path))
            else:
                msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            self._style_messagebox(msg_box)
            msg_box.exec_()
            return
        
        self.log_output.clear()
        self.raw_output = ""
        self.last_result_text = ""
        self.copy_btn.setVisible(False)
        
        # 简洁模式：显示等待提示
        if not self.verbose_checkbox.isChecked():
            self.log_output.append(t('please_wait', self.lang))
        else:
            self.log_output.append("==============================================")
            self.log_output.append("  Vivo OTA Tracker")
            self.log_output.append("==============================================")
            self.log_output.append("")
        
        # 禁用按钮
        self.run_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        # 设置工作目录（先清理旧目录）
        self._cleanup_work_dir()
        self.work_dir = tempfile.mkdtemp(prefix="vivo_ota_")
        
        # 复制 libs 目录到临时目录
        src_libs = resource_path("libs")
        dst_libs = os.path.join(self.work_dir, "libs")
        shutil.copytree(src_libs, dst_libs)
        
        # 复制 unicorn.dll
        src_dll = resource_path("natives/windows_64/unicorn.dll")
        dst_dll = os.path.join(self.work_dir, "unicorn.dll")
        if os.path.exists(src_dll):
            shutil.copy(src_dll, dst_dll)
        
        # 步骤1：运行 Java JAR
        if self.verbose_checkbox.isChecked():
            self.log_output.append(t('step_running', self.lang))
        self.current_stage = 'run'
        
        # 获取 JAR 和 Java 路径
        jar_path = resource_path("unidbg-android-0.9.10-SNAPSHOT.jar")
        
        # 查找 Java 运行时
        java_path = self.find_java()
        if not java_path:
            self.log_output.append(f"[{t('error_title', self.lang)}] {t('error_no_java', self.lang)}")
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)
            return
        
        # 运行命令（通过 -D 系统属性传入配置参数）
        java_cmd = [
            java_path,
            f"-DDEVICE_TYPE={self.current_config['DEVICE_TYPE']}",
            f"-DMODEL_SW_VER={self.current_config['MODEL_SW_VER']}",
            f"-DDEVICE_MODEL={self.current_config['DEVICE_MODEL']}",
            f"-DSW_VERSION={self.current_config['SW_VERSION']}",
            f"-DANDROID_VER={self.current_config['ANDROID_VER']}",
            "-Djava.library.path=" + self.work_dir,
            "-jar", jar_path,
        ]
        
        if self.verbose_checkbox.isChecked():
            self.log_output.append(f"{t('exec_cmd', self.lang)}: " + " ".join(java_cmd))
            self.log_output.append("")
        
        self.process.setWorkingDirectory(self.work_dir)
        self.process.start(java_cmd[0], java_cmd[1:])
    
    def find_java(self):
        """查找 Java 运行时"""
        # 1. 检查资源目录中的嵌入式 JRE
        embedded_jre = resource_path("jre/bin/java.exe")
        if os.path.exists(embedded_jre):
            return embedded_jre
        
        # 2. 检查系统 PATH
        for path in os.environ["PATH"].split(os.pathsep):
            java_exe = os.path.join(path, "java.exe")
            if os.path.exists(java_exe):
                return java_exe
        
        return None
    
    def on_verbose_changed(self):
        """切换日志模式时，如果当前有输出则刷新显示"""
        pass
    
    def on_process_output(self):
        """处理进程标准输出"""
        output = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        self.raw_output += output
        
        # 详细模式：实时输出日志
        if self.verbose_checkbox.isChecked():
            self.log_output.append(output)
            self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    
    def on_process_error(self):
        """处理进程错误输出"""
        error = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
        self.raw_output += error
        
        # 详细模式：实时输出错误日志
        if self.verbose_checkbox.isChecked():
            self.log_output.append(error)
            self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    
    def _cleanup_work_dir(self):
        """彻底清理临时目录"""
        if hasattr(self, 'work_dir') and self.work_dir is not None and os.path.exists(self.work_dir):
            try:
                shutil.rmtree(self.work_dir, ignore_errors=True)
            except Exception:
                pass
        self.work_dir = None
    
    def parse_results(self, raw_text):
        """解析 Java 输出，提取关键信息为简洁格式"""
        result = {}
        
        # 解析 Device 行: "Device: phone | V2506A / PD2506"
        device_match = re.search(r'Device:\s*(\w+)\s*\|\s*(\S+)\s*/\s*(\S+)', raw_text)
        if device_match:
            result['device_type'] = device_match.group(1)
            result['device_model'] = device_match.group(2)
            result['codename'] = device_match.group(3)
        
        # 解析 Base Version
        base_match = re.search(r'Base Version:\s*(\S+)', raw_text)
        if base_match:
            result['base_version'] = base_match.group(1)
        
        # 解析 Update Version
        ver_match = re.search(r'=== Update Information ===.*?Version:\s*(\S+)', raw_text, re.DOTALL)
        if not ver_match:
            ver_match = re.search(r'Version:\s*(\S+)', raw_text)
        if ver_match:
            result['update_version'] = ver_match.group(1)
        
        # 解析文件大小 "Size: X bytes (Y MB)"
        size_match = re.search(r'Size:\s*\d+\s*bytes\s*\(([\d.]+)\s*MB\)', raw_text)
        if size_match:
            result['file_size'] = size_match.group(1)
        
        # 解析下载链接
        url_match = re.search(r'Download URL:\s*(https?://\S+)', raw_text)
        if url_match:
            result['download_url'] = url_match.group(1).strip()
        
        return result
    
    def format_clean_result(self, parsed):
        """格式化解析结果为简洁中文输出"""
        lines = []
        lines.append("")
        lines.append("=" * 50)
        lines.append(f"            {t('ota_banner', self.lang)}")
        lines.append("=" * 50)
        
        # 设备类型
        dt = parsed.get('device_type', '')
        dt_map = {'phone': t('phone_cn', self.lang), 'tablet': t('tablet_cn', self.lang)}
        dt_cn = dt_map.get(dt, dt)
        lines.append(f"  {t('device_type_field', self.lang)}: {dt} ({dt_cn})")
        
        # 设备型号
        if 'device_model' in parsed and 'codename' in parsed:
            lines.append(f"  {t('device_model_field', self.lang)}: {parsed['device_model']} / {parsed['codename']}")
        elif 'device_model' in parsed:
            lines.append(f"  {t('device_model_field', self.lang)}: {parsed['device_model']}")
        
        # Android 版本
        android_ver = self.current_config.get('ANDROID_VER', '')
        if android_ver:
            lines.append(f"  {t('android_ver_field', self.lang)}: {android_ver}")
        
        # 软件版本（优先 update_version）
        if 'update_version' in parsed:
            lines.append(f"  {t('sw_ver_field', self.lang)}: {parsed['update_version']}")
        
        # 软件包大小
        if 'file_size' in parsed:
            lines.append(f"  {t('file_size_field', self.lang)}: {parsed['file_size']} MB")
        
        # 下载链接
        if 'download_url' in parsed:
            lines.append(f"  {t('download_url_field', self.lang)}: {parsed['download_url']}")
        
        lines.append("=" * 50)
        return '\n'.join(lines)
    
    def copy_to_clipboard(self):
        """一键复制简洁结果到剪贴板"""
        if not self.last_result_text:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(t('info_title', self.lang))
            msg_box.setText(t('no_result_to_copy', self.lang))
            msg_box.setIcon(QMessageBox.Information)
            info_icon_path = resource_path("assets/icon.png")
            if os.path.exists(info_icon_path):
                msg_box.setWindowIcon(QIcon(info_icon_path))
            self._style_messagebox(msg_box)
            msg_box.exec_()
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.last_result_text, QClipboard.Clipboard)
        clipboard.setText(self.last_result_text, QClipboard.Selection)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(t('success_title', self.lang))
        msg_box.setText(t('copied', self.lang))
        msg_box.setIcon(QMessageBox.Information)
        info_icon_path = resource_path("assets/icon.png")
        if os.path.exists(info_icon_path):
            msg_box.setWindowIcon(QIcon(info_icon_path))
        self._style_messagebox(msg_box)
        msg_box.exec_()
    
    def on_process_finished(self, exit_code):
        """进程结束处理"""
        # 先清理临时目录
        self._cleanup_work_dir()
        
        if exit_code != 0:
            self.log_output.append(f"\n[{t('error_title', self.lang)}] {t('error_exec_fail', self.lang)}: {exit_code}")
            self.progress_bar.setVisible(False)
            self.copy_btn.setVisible(False)
            self.run_btn.setEnabled(True)
            return
        
        if self.current_stage == 'run':
            # 简洁模式：解析并格式化结果
            if not self.verbose_checkbox.isChecked():
                parsed = self.parse_results(self.raw_output)
                clean_result = self.format_clean_result(parsed)
                self.log_output.clear()
                self.log_output.append(clean_result)
                self.last_result_text = clean_result.strip()
                self.copy_btn.setVisible(True)
            else:
                # 详细模式也缓存一份纯文本结果用于复制
                parsed = self.parse_results(self.raw_output)
                self.last_result_text = self.format_clean_result(parsed).strip()
                self.copy_btn.setVisible(True)
            
            self.log_output.append("")
            self.log_output.append(t('done', self.lang))
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)
            self.current_stage = None
            self.raw_output = ""
    
    def closeEvent(self, event):
        """关闭窗口时清理"""
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished(3000)
        # 清理临时目录
        self._cleanup_work_dir()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VivoOtaTrackerGUI()
    window.show()
    sys.exit(app.exec_())