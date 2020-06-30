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
title = 'Vikipedi:Sayfa taşıma talepleri'
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
        currentMonth = monthList[datetime.now().month-1]
        currentYear = datetime.now().year
        archivePage = "Vikipedi:Sayfa_taşıma_talepleri/Arşiv/" + str(currentYear) + "/" + currentMonth
        now = datetime.now()
        content = mavri.content_of_section(wiki, title, section, xx)

        if content != '':
            timestamp = re.findall('\{\{\s*User:Evrifaessa\/STT\s*\|\s*([^\|\}]*)\s*\|\s*[^\|\}]*\s*\}\}', content)
            informer = re.findall('\{\{\s*User:Evrifaessa\/STT\s*\|\s*[^\|\}]*\s*\|\s*([^\|\}]*)\s*\}\}', content)
            if timestamp and informer:
                timestamp = timestamp[0]
                informer = informer[0]
                contentLow = content.lower()
                resolved = "{{yapıldı}}" in contentLow or "{{done}}" in contentLow or "{{yapılmadı}}" in contentLow or "{{yapılmadı2}}" in contentLow or "{{yapılmadı ve yapılmayacak}}" in contentLow 
                not_time = datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]))
                diff = now - not_time

                if resolved:
                    if diff.total_seconds() > 60 * 60 * 12:
                        summary = 'Sayfa taşıma talebi sonuçlandırılmış - ' + summary_ek
                        archiveSummary = 'Sonuçlandırılan sayfa taşıma talebi arşivleniyor - ' + summary_ek
                        mavri.appendtext_on_page(wiki, archivePage, "\n" + content, archiveSummary, xx)
                        mavri.section_clear(wiki, title, section, summary, xx)
                    else:
                        print('Talep sonuçlandırılmış ama gereken süre geçmemiş, arşivlenmiyor.')
                else:
                    print('Talep henüz sonuçlandırılmamış, arşivlenmiyor.')
            section += 1
        else:
            section = 1
            time.sleep(60)