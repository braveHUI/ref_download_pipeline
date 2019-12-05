rule seqid2ncbi:
    input :
        out_dir + "genomes.done",
        refseq = download_dir,
        txtfiles = txtfiles_path,

    output:
        directory(summary_dir),
        temp(touch(out_dir + "summary.done"))
    script:
        "scripts/seqid2ncbi_id.py"









