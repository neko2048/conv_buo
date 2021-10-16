#!/bin/bash

# ============ collect figures ============
echo "---------- collecting and sorting figures ----------"
while read dirname others; do
    PATTERN="./$dirname*.jpg"
    if ls $PATTERN 1> /dev/null 2>&1; then
        mv $dirname*.jpg $dirname
        echo "+ $dirname figures are sorted"
    else
        echo "- No $dirname figures generated"
    fi
done < subfolder_name.txt
