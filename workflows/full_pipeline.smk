include:
    "get_list.smk"

include:
    pipeline_path +  "rules/download/fetch_ncbi_genome.smk"

include:
    pipeline_path +  "rules/seqid2ncbi/seqidparse.smk"

include:
    pipeline_path + "rules/index/bwa.smk"






rule all:
    input:
        out_dir + "bwadb.txt"




