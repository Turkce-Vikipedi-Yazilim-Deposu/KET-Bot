# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import socket
import time
from datetime import datetime
import platform

import mavri

wiki = 'tr.wikipedia'
xx = mavri.login(wiki, 'KET Bot')
title = 'Vikipedi:Sürüm gizleme talepleri'
version = 'V3.0d'
summary_ek = " (KET Bot, " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
section = 1
ignore_list=[]
mpa = dict.fromkeys(range(32))

while 1:
        now = datetime.now()
        content = mavri.content_of_section(wiki, title, section, xx)

        if content != '':
            timestamp = re.findall('\{\{\s*User:Evrifaessa\/SGT\s*\|\s*([^\|\}]*)\s*\|\s*[^\|\}]*\s*\}\}', content)
            informer = re.findall('\{\{\s*User:Evrifaessa\/SGT\s*\|\s*[^\|\}]*\s*\|\s*([^\|\}]*)\s*\}\}', content)
            if timestamp and informer:
                timestamp = timestamp[0]
                informer = informer[0]
                contentLow = content.lower()
                resolved = "{{yapıldı}}" in contentLow or "{{done}}" in contentLow or "{{yapılmadı}}" in contentLow or "{{yapılmadı2}}" in contentLow or "{{yapılmadı ve yapılmayacak}}" in contentLow 
                not_time = datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]))
                diff = now - not_time

                if resolved:
                    if diff.total_seconds() > 60 * 60 * 24:
                        summary = 'Sürüm gizleme talebi sonuçlandırılmış - ' + summary_ek
                        mavri.section_clear(wiki, title, section, summary, xx)
                    else:
                        print('Talep sonuçlandırılmış ama gereken süre geçmemiş, arşivlenmiyor.')
                else:
                    print('Talep henüz sonuçlandırılmamış, arşivlenmiyor.')
            section += 1
        else:
            section = 1
            time.sleep(60)