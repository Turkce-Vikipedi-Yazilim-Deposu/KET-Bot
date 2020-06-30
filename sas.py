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
title = 'Vikipedi:Silinmeye aday sayfalar'
version = 'V3.0g'
summary_ek = " (" + username + ", " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
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
    content = mavri.content_of_page(wiki, title)

    regex = r"(?<=Silinmeye aday sayfalar/)[^}]*"

    if content != '{{/Başlık}}' and content != '{{/Başlık}}\n== Tartışmalar ==':
        pages = re.findall(regex.decode('UTF-8'), content)
        for page in pages:
            pageContent = mavri.content_of_page(wiki, "Vikipedi:Silinmeye aday sayfalar/" + page)
            timestampMonth = monthList[now.month-1]
            timestampYear = now.year
            archivePage = "Vikipedi:Silinmeye_aday_sayfalar/Kayıt/" + str(timestampYear) + "_" + str(timestampMonth)
            contentLow = pageContent.lower()
            resolved = '{{sas son}}' in contentLow

            archiveContent = mavri.content_of_page(wiki, archivePage.decode('UTF-8'))
            hasBeenArchived = '{{Vikipedi:Silinmeye aday sayfalar/' + page + '}}' in archiveContent

            if hasBeenArchived == False:
                append = '\n' + '{{Vikipedi:Silinmeye aday sayfalar/' + page + '}}'
                archiveSummary = 'Arşiv sayfalarında bulunmayan SAS alt sayfası arşivlere ekleniyor - ' + summary_ek
                mavri.appendtext_on_page(wiki, archivePage.decode('UTF-8'), append, archiveSummary, xx)
                print(page + ' arşiv sayfasına eklendi.')

            if resolved:
                summary = 'Sonuçlandırılan SAS arşivleniyor - ' + summary_ek
                print(page + " SAS sayfasından kaldırılıyor.")
                newContent = content.replace("{{Vikipedi:Silinmeye aday sayfalar/" + page + "}}", "")
                mavri.change_page(wiki, title, newContent, summary, xx)
    else:
        time.sleep(60)