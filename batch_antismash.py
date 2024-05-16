import os

#set input files
assemblies="/ddn/home12/r2620/chapter_3/ncbi-genomes-2024-05-15/fna" 
annotations="/ddn/home12/r2620/chapter_3/ncbi-genomes-2024-05-15/gff"
#set output dir
antismash_out="/ddn/home12/r2620/chapter_3/antismash_out"
PBS_O_WORKDIR = "{PBS_O_WORKDIR}"

# Read file names from the directory
file_names = os.listdir(assemblies)

# Generate bash scripts
for file_name in file_names:
    #Extract prefix from the file name
    prefix = file_name.split("_genomic.fna.gz")[0]

    # Generate script content
    script_content = f"""#!/bin/bash
#PBS -N {prefix}_ncbi_antismash
#PBS -j oe
#PBS -l ncpus=12
#PBS -l mem=35gb
#PBS -m abe
#PBS -l walltime=800:00:00
#PBS -M ballen3@go.olemiss.edu

source activate antismash7.1

# Changes the current directory to the directory from which the job was submitted.
cd "${PBS_O_WORKDIR}" || exit

# Create the output directory if it doesn't exist
mkdir -p {antismash_out}/{prefix}

# Run Antismash
echo "********** Antismash started for {prefix} at $(date) **********"
antismash {os.path.join(assemblies, file_name)} \
--taxon fungi \
--output-dir {antismash_out}/{prefix} \
--verbose \
--cb-general --cb-knownclusters --cb-subclusters \
--pfam2go --clusterhmmer \
--genefinding-gff3 {os.path.join(annotations, prefix + "_genomic.gff")}
"""
    # Generate script file name
    script_filename = f"as_{prefix}.sh"

    # Write script content to the file
    with open(script_filename, "w") as f:
        f.write(script_content)

    # Add execute permission to the script
    os.chmod(script_filename, 0o755)

    # Print confirmation
    print(f"Generated bash script: {script_filename}")

### to submit the resulting scripts all at once run this 3 line loop
#for script in as_*.sh; do
#    qsub "$script"
#done