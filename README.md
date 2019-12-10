# Comparative Genomics Pipeline
 
This is the Comparative Genomics analysis pipeline for Zhai/Chen Lab.

## Homologous gene analysis

1. Use `/web crawler/scratch_niche_information.py` to collect sequence information.
Download the protein sequences into one file.

	`mkdir -p othomcl; cd othomcl`
2. Use `/pan_genome/orth_adj.sh` to adjust the headers of the faa files and to generate fasta files.
	`bash orth_adj.sh`

3. Copy all the fasta files into working directory.

	`cp *.fasta /plus/work/soft/ORTHOMCLV1.4/sample_data`
4. Use `pan_genome/file_name_join.sh` to generate the string that joins the file names with comma. 
	
	e.g.

	`bash file_name_join_orth.sh`

	Then copy the string and run the following code, replace 'LP16.fasta,ST3.fasta' with the string you just copied.

	`nohup /plus/work/soft/ORTHOMCLV1.4/orthomcledit.pl --mode 1 --fa_files LP16.fasta,ST3.fasta &`
	
	This step costs a long time to run.

5. Step 4 will generate `nohup.out` file. Just run `tail nohup.out` to check the results.

	
	> Final ORTHOMCL Result: /plus/work/soft/ORTHOMCLV1.4/Nov_2/all_orthomcl.out generated!!!

	And we can copy that output file to current path.

	`cp /plus/work/soft/ORTHOMCLV1.4/Nov_2/all_orthomcl.out ./`

6. Generate species information table

	`ls *.fasta |awk -F'.fasta' '{print $1"\t"$0}' > faa.list`

	`/plus/work/soft/ORTHOMCLV1.4/orthomcl2speciesedit.pl all_orthomcl.out faa.list`

7. Step 6 will generate a 'choose_coregene' file, which contains all the core-genes.

	`cd choose_coregene`

	Then we should concatenate all the sequences in order to do the alignment.

	`cat *.faa > all.faa`

	Re-orgnize the file, extract the core-genes for each strain. Use the 'cat_core.sh` file

	`bash cat_core_genes.sh`

## Pan-genome Analysis

1. `mkdir PGAP; cd PGAP` to create working directory

2. move all the faa files as well as cog anotation and nr anotation files into one data file

	`mkdir pan_genome_data; cd pan_genome_data`

	`cp /$PATH/*.faa ./`

	`cp /$PATH/*_cog.xls ./`

	`cp /$PATH/*nr.xls ./`

3. run `bash pan_genome.sh` under `~/PGAP/pan_genome_data/` to generate other needed file into `~/PGAP/input`

4. Go back to working directory `cd ~/PGAP/`,run `bash file_name_join_pan.sh` to get the string, which are files names joined with "+". Copy that string and run

	`perl /plus/work/soft/PGAP-1.2.1/PGAPedit.pl -strains WCF+ST3+ZJ3+LPP8+LP16 -input input/ -output output --cluster -pangenome --variation --evolution --function -method MP --thread 1 --bootstrap 500`
	
	(replace "WCF+ST3+ZJ3+LPP8+LP16" with the string you just copied)

5. It will raise error. Run `python check_err.py` and `python delete.py` to delete redandunt genes in files under `./input/`
	
6. Run this again:

	`perl /plus/work/soft/PGAP-1.2.1/PGAPedit.pl -strains WCF+ST3+ZJ3+LPP8+LP16 -input input/ -output output --cluster -pangenome --variation --evolution --function -method MP --thread 1 --bootstrap 500`

	This step will cost a very very very very long time and very very very very big space. Not recommended.

7. Analysis the results.






