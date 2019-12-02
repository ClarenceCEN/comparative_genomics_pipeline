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

	`bash file_name_join.sh`

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







