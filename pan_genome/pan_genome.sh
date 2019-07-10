#!/bin/bash


for file in ./pan_genome_data/*.faa
do
name=`basename $file`
output_name="${name%.*}nr.xls"
output_name2="${name%.*}.function"
echo 'check '$output_name
if [ ! -f "$output_name" ]; then
	#echo $output_name
	echo '----'${name%.*}'-----'
	/plus/work/soft/bin/blast/blastp -query ${name%.*}.faa -db /plus/CCFM/stu02/cs/L._plantarum/lab/pan/data/nr_1590 -evalue 1e-10 -outfmt 5 -out ${name%.*}.out -num_threads 40
	/plus/work/soft/bin/blast/Blast2table -format 10 -xml ${name%.*}.out > ${name%.*}nr.xls -numhsps 1
	rm ${name%.*}.out
fi
if [ ! -f "$output_name2" ]; then
	cat ${name%.*}.faa |sed  /^$/d  > ${name%.*}.fan
	/plus/work/soft/bin/mergeAnnotation.pl -fa ${name%.*}.fan -nr ${name%.*}nr.xls --swissport ${name%.*}_cog.xls > ${name%.*}merge.xls
	cat ${name%.*}merge.xls |sed '1d'|awk  -F '\t'  '{print  "'"${name%.*}|"'"$1"\t"$7"\t"$4}'| sort -k 1 -n -t$'\t' > ${name%.*}.function
	cat ${name%.*}.fnn |sed  /^$/d  > ${name%.*}.fnnn
	/plus/work/soft/orthomclSoftware-v2.0.9/bin/orthomclAdjustFasta ${name%.*} ${name%.*}.fnnn 1
	mv ${name%.*}.fasta ${name%.*}.nuc
	/plus/work/soft/orthomclSoftware-v2.0.9/bin/orthomclAdjustFasta ${name%.*} ${name%.*}.fan 1
	mv ${name%.*}.fasta ${name%.*}.pep
	#cat ${name%.*}.pep |head -10
	#cat ${name%.*}.nuc |head -10
	#cat ${name%.*}.function |head -10
fi
echo 'done!'
done

rm *.fnnn
rm *.fan
rm *merge.xls

mv *.function ../input/
mv *.pep ../input/
mv *.nuc ../input/
