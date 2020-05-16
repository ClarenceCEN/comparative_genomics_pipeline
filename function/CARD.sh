#!/bin/bash

#cearte file (done once)
#for i in *.faa
#do
#mkdir ${i%%.faa}
#mv ./$i ./${i%%.faa}
#done

#analysis
for i in *
do
echo '======='$i'=========='

cd /plus/CCFM/stu01/cs/CARD/$i/

ls
python /plus/work/soft/CARD/rgi.py -t protein -i $i.faa -o sample
python /plus/work/soft/CARD/convertJsonToTSV.py -i sample.json -o sample.CARD
perl /plus/work/soft/CARD/convertCARDTxtToXls.pl sample.CARD.txt sample
cd ../
done
