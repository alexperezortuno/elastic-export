#!/usr/bin/env bash
ver=$(grep '^VERSION_ID' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')

pyinstaller main.py -F  -n "pylastic-ubuntu-${ver}-x86_x64" \
--onefile --noconfirm \
--log-level=INFO \
--add-data=README.md:. \
--hidden-import=elasticsearch \
--hidden-import=elasticsearch_dsl \
--hidden-import=pandas \
--hidden-import=numpy \
--hidden-import=coloredlogs \
--clean