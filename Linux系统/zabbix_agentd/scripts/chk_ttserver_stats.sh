#!/bin/bash
argv="$1"
port="$2"
/bin/echo stats | nc 127.0.0.1 $port | grep -w "$argv" | awk '{print $NF}'