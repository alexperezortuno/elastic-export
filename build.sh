#!/usr/bin/env bash
ver=$(grep '^VERSION_ID' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')
name=$(grep '^NAME' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')
name=${name//" "/"-"}
name=`echo "$name" | awk '{ print tolower($1) }'`

pyinstaller main.py -F  -n "pylastic-${name}-${ver}" \
--onefile --noconfirm \
--log-level=INFO \
--add-data="README.md:." \
--hidden-import=elasticsearch \
--hidden-import=elasticsearch_dsl \
--hidden-import=pandas \
--hidden-import=numpy \
--hidden-import=coloredlogs \
--clean