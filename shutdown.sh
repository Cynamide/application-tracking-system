#! /bin/bash
kill $(ps | grep npm | awk '{print $1}')
kill $(ps | grep node | awk '{print $1}')
kill $(ps | grep flask | awk '{print $1}')
