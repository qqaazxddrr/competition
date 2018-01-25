#!/bin/sh

#  modelExtract.sh
#  
#
#  Created by 高旷 on 2017/12/5.
#
for loop in 1 2 3 4 5 6 7 8 9 10
do
    python getModel.py -m $loop
    echo "Model$loop is done!"
done
