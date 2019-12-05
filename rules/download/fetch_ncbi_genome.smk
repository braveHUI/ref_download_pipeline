import os

rule get_ncbi_genomes:
    conda:
        pipeline_path + "envs/ncbi_genome_download.yml"
    params:
        group = config["params"]["ncbi_genome_download"]["group"]
    threads:
        config["params"]["ncbi_genome_download"]["thread"]
    output:
       temp(touch(out_dir + "genomes.done")),
    benchmark:
        out_dir + "benchmarks/download/get_ncbi_genomes.txt"
    log:
        logging_folder + "get_ncbi_genomes.err"
    message:
        "ncbi-genome-download -p {threads} -r 10 -o {download_dir}  -H -l complete,chromosome -F all {params[group]} 2>{log}"
    shell:
        """
        ncbi-genome-download -p {threads} -r 10 -o {download_dir}  -H -l complete,chromosome -F all {params[group]} 2>{log}
        """


