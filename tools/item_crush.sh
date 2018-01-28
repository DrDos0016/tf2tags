#!/bin/sh
for png in `find ../assets/images -name "*.png"`;
do
    echo "crushing $png"    
    pngcrush -brute "$png" temp.png
    mv -f temp.png $png
done;
