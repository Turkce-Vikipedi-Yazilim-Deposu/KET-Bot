# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import socket
import time
from datetime import datetime
import platform

import mavri

wiki = 'tr.wikipedia'
username = 'Arşivleyici'
xx = mavri.login(wiki, username)
title = 'Vikipedi:Hizmetli duyuru panosu'
version = 'V3.0g'
summary_ek = " (" + username + ", " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
section = 1
ignore_list=[]
mpa = dict.fromkeys(range(32))

monthList = [
    'Ocak', 
    'Şubat', 
    'Mart', 
    'Nisan', 
    'Mayıs', 
    'Haziran', 
    'Temmuz', 
    'Ağustos', 
    'Eylül', 
    'Ekim', 
    'Kasım', 
    'Aralık'
]

while 1:
    now = datetime.now()
    content = mavri.content_of_section(wiki, title, section, xx)

    if content != '':
        timestamp = re.findall('\{\{\s*User:Evrifaessa\/HDP\s*\|\s*([^\|\}]*)\s*\|\s*[^\|\}]*\s*\}\}', content)
        informer = re.findall('\{\{\s*User:Evrifaessa\/HDP\s*\|\s*[^\|\}]*\s*\|\s*([^\|\}]*)\s*\}\}', content)
        if timestamp and informer:
            timestamp = timestamp[0]
            informer = informer[0]
            contentLow = content.lower()
            not_time = datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]))
            diff = now - not_time
            currentMonth = monthList[not_time.month-1]
            currentYear = not_time.year
            archivePage = "Vikipedi:Hizmetli duyuru panosu/Kayıt/" + str(currentYear) + "/" + currentMonth

            if diff.total_seconds() > 60 * 60 * 24 * 3:
                summary = 'Üzerinden 3 gün geçen talep arşivleniyor - ' + summary_ek
                archiveSummary = 'Sonuçlandırılan talep arşivleniyor - ' + summary_ek
                mavri.appendtext_on_page(wiki, archivePage, "\n" + content, archiveSummary, xx)
                mavri.section_clear(wiki, title, section, summary, xx)
            else:
                print('Gerekli süre geçmemiş, arşivlenmiyor.')
            section += 1
        else:
            section = 1
            time.sleep(120)