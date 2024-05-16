#!/bin/bash
#PBS -N antismash_ncbi_genomes
#PBS -j oe
#PBS -l ncpus=40
#PBS -l mem=50gb
#PBS -m abe
#PBS -l walltime=800:00:00
#PBS -M ballen3@go.olemiss.edu

#changes the current directory to the directory from which the job was submitted.
cd "${PBS_O_WORKDIR}" || exit

source activate antismash

#set input files
assemblies="/ddn/home12/r2620/chapter_3/ncbi-genomes-2024-05-15" 
annotations="/ddn/home12/r2620/chapter_3/ncbi-genomes-2024-05-15"
#set output dir
antismash_out="/ddn/home12/r2620/chapter_3/antismash_out"

#Run antismash for fungi
for i in "${assemblies}"/*.fna.gz
do
    # extract the basename of i, excluding the "_genomic.fna.gz" ending
    sample_name=$(basename ${i} "_genomic.fna.gz")
    
    # Create the output directory if it doesn't exist
    mkdir -p "$antismash_out"/"${sample_name}"
    
    # Run antismash
    echo "********** Antismash started for ${sample_name} **********"
    antismash "$i" \
    --taxon fungi \
    --output-dir "$antismash_out"/"${sample_name}" \
    --output-basename "${sample_name}" \
    --cb-general --cb-knownclusters --cb-subclusters \
    --asf --pfam2go --clusterhmmer --cassis --cc-mibig --tfbs \
    --genefinding-gff3 "$annotations"/"${sample_name}"_genomic.gff
    echo "********** Antismash done for ${sample_name} **********"
done
