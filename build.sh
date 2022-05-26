#!/usr/bin/env bash
ver=$(grep '^VERSION_ID' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')
name=$(grep '^NAME' /etc/os-release | awk -F'=' ' gsub(/"/,"") { print $2}')
name=${name//" "/"-"}
name=`echo "$name" | awk '{ print tolower($1) }'`

filename="pylastic-${name}-${ver}"

if [ ! -f "${filename}.spec" ]
then
  pyi-makespec --onefile main.py -n $filename
fi


pyinstaller "${filename}.spec" \
--onefile --noconfirm \
--log-level=INFO \
--add-data="README.md:." \
--hidden-import=elasticsearch \
--hidden-import=elasticsearch_dsl \
--hidden-import=pandas \
--hidden-import=numpy \
--hidden-import=coloredlogs \
--clean