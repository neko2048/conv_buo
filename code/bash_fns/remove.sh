#!/bin/bash

read rmfig
if $rmfig; then 
    find . -name '*.jpg' -delete && echo "---------- File Cleared ----------"
else
    echo "---------- Skip Deleting Files ----------"
fi