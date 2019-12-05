rule  get_file_name:
    conda:
        pipeline_path + "envs/bwa-samtools.yml"
    input:
        out_dir + "summary.done",
        out_dir + "library/summary/"
    output:
        out_dir + "bwadb.txt",
    params:
        threads = config["params"]["build_database"]["thread"]
    benchmark:
        out_dir + "benchmarks/index/get_file_name.txt"
    script:
        "scripts/build_database.py"


