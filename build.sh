#!/bin/bash
ver=$(grep '^VERSION_ID' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')

source bin/activate
pyinstaller main.py -F  -n "pylastic-ubuntu-${ver}-x86_x64" \
--onefile \
--noconfirm \
--hidden-import elasticsearch \
--hidden-import elasticsearch_dsl \
--hidden-import pandas \
--clean