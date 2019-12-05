include:
    "get_list.smk"

include:
    pipeline_path + "rules/index/bwa.smk"


rule all:
    input:
        expand(out_dir + "references/bwa_db/{asm_acc}/all.fna.fai", asm_acc=accs),
        expand(out_dir + "references/bwa_db/{asm_acc}/all.fna.bwt", asm_acc=accs)

