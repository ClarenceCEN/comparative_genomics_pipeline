# Comparative Genomics Pipeline
 
This is the Comparative Genomics analysis pipeline for Zhai/Chen Lab.

## Homologous gene analysis

1. Use `/web crawler/scratch_niche_information.py` to collect sequence information.
Download the protein sequences into one file.

	`mkdir -p othomcl; cd othomcl`
2. Use `/pan_genome/oth_adj.sh` to adjust the headers of the faa files and to generate fasta files.

3. Copy all the fasta files into working directory.

	`cp *.fasta /plus/work/soft/ORTHOMCLV1.4/sample_data`
4. Use `pan_genome/file_name_join.sh` to generate the string that joins the file names with comma. 
	`nohup /plus/work/soft/ORTHOMCLV1.4/orthomcledit.pl --mode 1 --fa_files LP16.fasta,LPP8.fasta,ST3.fasta,WCF.fasta,ZJ3.fasta &`
	This step costs a long time to run.

5. 






