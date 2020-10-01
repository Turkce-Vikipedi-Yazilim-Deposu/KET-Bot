# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import socket
import time
from datetime import datetime
import platform

import mavri

wiki = 'tr.wikipedia'
xx = mavri.login(wiki, 'Evrifaessa Bot')
title = 'Vikipedi:Kullanıcı engelleme talepleri'
version = 'V3.0g'
summary_ek = " (Evrifaessa Bot, " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
section = 1
mpa = dict.fromkeys(range(32))

while 1:
    try:
        datetime_now = datetime.now()
        now = datetime.now()
        content = mavri.content_of_section(wiki, title, section, xx)

        if content != '':
            vandal = re.findall('\{\{\s*[Vv]andal\s*\|\s*([^\}]*)\s*\}\}', content)

            if vandal:
                timestamp = re.findall('\{\{\s*User:Evrifaessa\/KET\s*\|\s*([^\|\}]*)\s*\|\s*[^\|\}]*\s*\}\}', content)
                informer = re.findall('\{\{\s*User:Evrifaessa\/KET\s*\|\s*[^\|\}]*\s*\|\s*([^\|\}]*)\s*\}\}', content)
                if timestamp and informer:
                    timestamp = timestamp[0]
                    informer = informer[0]
                    contentLow = content.lower()
                    vandal = vandal[0]
                    resolved = "{{yapıldı}}" in contentLow or "{{done}}" in contentLow or "{{yapılmadı}}" in contentLow or "{{yapılmadı2}}" in contentLow or "{{yapılmadı ve yapılmayacak}}" in contentLow 
                    blocked = mavri.blocked(wiki, vandal)
                    not_time = datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[8:10]),
                                        int(timestamp[10:12]), int(timestamp[12:14]))
                    vandal = vandal.translate(mpa)

                    try:
                        socket.inet_aton(vandal)
                        IP = 1
                    except socket.error:
                        IP = 0

                    if blocked.json()['query']['blocks'] and resolved == False:
                        timestamp = blocked.json()['query']['blocks'][0]['timestamp']
                        by = blocked.json()['query']['blocks'][0]['by']
                        reason = blocked.json()['query']['blocks'][0]['reason']

                        summary = '[[Özel:Katkılar/' + vandal + '|' + vandal + ']] engellenmiş, not bırakılıyor. [[Kullanıcı:' + by + '|' + by + ']] - ' + reason + summary_ek
                        newContent = content + "\n* '''Robot yardımcı notu:''' &ndash; {{yapıldı}} " + '[[Kullanıcı:' + by + '|' + by + ']] tarafından yapıldı.--~~~~'
                        mavri.change_section(wiki, title, section, newContent, summary, xx)
        else:
            section = 1
            time.sleep(60)
    except IndexError:
        pass