#!/bin/bash
find /usr/local/bin -type f -perm -111 -size -50k \
  -exec file {} \; \
  | grep -i text \
  | cut -d: -f1 \
  | sort \
  > my_scripts.txt
