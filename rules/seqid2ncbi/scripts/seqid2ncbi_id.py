import argparse
import os


class Seqid2Taxid(object):
    def __init__(self, path, txtpath, outpath):
        self.path = os.path.join(path, "refseq")
        self.txtpath = path
        self.txtfile = txtpath
        self.outpath = outpath
        print (outpath)
        if not os.path.exists(self.outpath):
            os.system("mkdir {}".format(self.outpath))

    def use_logging(self, func):
        def wrapper():
            print("%s正在运行" % self.func.__name__)
            return self.func()
        return wrapper()

    def get_gene_dir(self, path):
        dirss = os.listdir(path)
        dirss = [os.path.join(path, diw) for diw in dirss if os.path.isdir(os.path.join(path, diw))]
        return dirss

    def get_report_file(self, gcf):
        seqitems = ""
        repos = os.listdir(gcf)
        repos = [rptxt for rptxt in repos if rptxt.endswith("report.txt")][0]
        report_path = os.path.join(gcf, repos)
        if os.path.exists(report_path):
            seqitems = self.read_report(report_path)
        return seqitems

    def read_report(self, report_path):
        items = []
        files = open(report_path, 'r')
        taxid = ""
        seqid = []
        for line in files:

            if "Taxid" in line:
                taxid = line.split(":")[1].strip()
            if "RefSeq assembly accession" in line:
                ref_accession = line.split(":")[1].strip()
            if not line.startswith("#"):
                # print(report_path)
                # print(line.split("  ")[0].split("\t"))
                seqid.append(line.split("   ")[0].split("\t")[6])
        files.close()
        for sei in seqid:
            item = {}
            item["taxid"] = taxid
            item["RefSeq-Accn"] = sei
            item["RefSeq_assembly_accession"] = ref_accession
            items.append(item)
        return items

    def write_seqid(self, seqpath, seqid_items):
        seqname = "refseq_" + seqpath.split("/")[-1] + "_seqid2taxid.tsv"
        seqname = os.path.join(self.outpath, seqname)
        refname = "refseq_" + seqpath.split("/")[-1] + "_seqid2refseq_acc.tsv"
        refname = os.path.join(self.outpath, refname)
        f = open(seqname, 'w')
        q = open(refname, 'w')
        for seqi in seqid_items:
            f.write(seqi["RefSeq-Accn"] + "\t" + seqi["taxid"] + "\n")
            q.write(seqi["RefSeq-Accn"] + "\t" + seqi["RefSeq_assembly_accession"] + "\n")
        f.close()
        q.close()
        print("%s 和 %s文件写入成功" % (seqname, refname))

    def write_refseq(self, seqpath, refseq_items):
        name = "seqid2refseq_acc_" + seqpath.split("/")[-1] + "_.tsv"
        f = open(name, 'w')
        top = {}
        top["taxid"] = "taxid"
        top["assembly_accession"] = "assembly_accession"
        refseq_items.insert(0, top)
        for ref_acc in refseq_items:
            f.write(ref_acc["assembly_accession"] + "\t" + ref_acc["taxid"] + "\n")
        f.close()
        print("%s写入成功 " % name)

    # @use_logging
    def get_txt(self):
        txtfiles = os.listdir(self.txtfile)
        txtfiles = [os.path.join(self.txtfile, tet) for tet in txtfiles if tet.endswith("summary.txt")]
        for tpa in txtfiles:
            list_items = self.read_taxid_txt(tpa)
            self.write_fan_path(tpa, list_items)

    # @use_logging
    def write_fan_path(self, txtfile, list_items):
        name = txtfile.split("/")[-1].split("_")[1]
        sem_name = "refseq_" + name + "_assembly_summary.txt.tsv"
        sem_name = os.path.join(self.outpath, sem_name)
        item = ["assembly_accession", "bioproject", "biosample", "wgs_master", "refseq_category", "taxid", "species_taxid", "organism_name", "infraspecific_name", "isolate", "version_status", "assembly_level", "release_type", "genome_rep", "seq_rel_date", "asm_name", "submitter", "gbrs_paired_asm", "paired_asm_comp", "ftp_path", "excluded_from_refseq", "relation_to_type_material", "local_path", "human_path\n"]
        list_items.insert(0, item)
        f = open(sem_name, 'w')
        for items in list_items:
            strname = "\t".join(items)
            f.write(strname)
        f.close()
        print("%s写入成功 " % sem_name)

    # @use_logging
    def read_taxid_txt(self, txtfiles):
        items = []
        fna_items = []
        fna_cunzzai_items = []
        name = txtfiles.split("/")[-1].split("_")[1]
        files = open(txtfiles, 'r')
        for line in files:
            if not line.startswith("#"):
                line_list = line.split("     ")[0].split("\t")
                fna_path = self.find_fna_path(name, line_list[0])
                if fna_path:
                    line_list[-1] = line_list[-1].strip("\n")
                    line_list.append(fna_path)
                    # items.append(line_list)
                    fna_cunzzai_items.append(fna_path)
                    hum_real_path = self.find_human_readable(name, line_list)
                    if hum_real_path:
                        line_list.append(hum_real_path + "\n")
                        items.append(line_list)
                    else:
                        print(hum_real_path)
                else:
                    fna_items.append(fna_path)
        files.close()
        return items

    # @use_logging
    def find_fna_path(self, name, gftname):
        fna_path = os.path.join(self.txtpath, "refseq", name, gftname)
        if os.path.exists(fna_path):
            fna_files = os.listdir(fna_path)
            fna_files = [fpa for fpa in fna_files if fpa.endswith("genomic.fna.gz") and "from" not in fpa.split("_")]
            fna_fasta = os.path.join(fna_path, fna_files[0])
            return fna_fasta
        else:
            return 0

    # @use_logging
    def find_human_readable(self, name, line_list):
        if name != 'viral':
            full_output_dir = os.path.join(self.txtpath, 'human_readable', 'refseq', name,
                                           line_list[7].split(' ')[0],
                                           line_list[7].split(' ')[1],
                                           self.get_strain_label(line_list))
        else:
            full_output_dir = os.path.join(self.txtpath, 'human_readable', 'refseq', name,
                                           line_list[7].replace(' ', '_'),
                                           self.get_strain_label(line_list, viral=True))
        if os.path.exists(full_output_dir):
            fna_files = os.listdir(full_output_dir)
            fna_files = [fpa for fpa in fna_files if fpa.endswith("genomic.fna.gz") and "from" not in fpa.split("_")]
            if len(fna_files) == 1:
                fna_fasta = os.path.join(full_output_dir, fna_files[0])
            elif len(fna_files) > 1:
                fanq_fasta = [fasw for fasw in fna_files if fasw.startswith(line_list[0])]
                fna_fasta = os.path.join(full_output_dir, fanq_fasta[0])
            # print("存在该%s 文件" % full_output_dir)
            else:
                fna_fasta = 0
        else:
            # print("不存在该%s 文件" % full_output_dir)
            fna_fasta = 0
        return fna_fasta

    # @use_logging
    def get_strain_label(self, line_list, viral=False):
        def get_strain(line_list):
            strain = line_list[8]
            if strain != '':
                return strain.split('=')[-1]
            strain = line_list[9]
            if strain != '':
                return strain
            if len(line_list[7].split(' ')) > 2 and not viral:
                return ' '.join(line_list[7].split(' ')[2:])
            return line_list[0]

        def cleanup(strain):
            strain = strain.strip()
            strain = strain.replace(' ', '_')
            strain = strain.replace(';', '_')
            strain = strain.replace('/', '_')
            strain = strain.replace('\\', '_')
            return strain
        return cleanup(get_strain(line_list))

    def run(self):
        # 1获取种类文件夹
        gene_dirs = self.get_gene_dir(self.path)
        print(gene_dirs)
        # 2获取每个种类下面的gcf文件夹
        for gene in gene_dirs:
            gcf_dirs = self.get_gene_dir(gene)
            seqid_item = []
            refseq_items = []
            top = {}
            top["RefSeq-Accn"] = "RefSeq-Accn"
            top["taxid"] = "taxid"
            top["species_taxid"] = "species_taxid"
            top["RefSeq_assembly_accession"] = "RefSeq_assembly_accession"
            seqid_item.append(top)
            # 3获取gcf文件夹下的report文件里面的信息
            for gcf in gcf_dirs:
                seqitem = self.get_report_file(gcf)
                for sei in seqitem:
                    seqid_item.append(sei)
            self.write_seqid(gene, seqid_item)
        # 添加2个路径
        self.get_txt()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="create seqid2taxid")
    # parser.add_argument('-p', '--path', help='参考库存放文件夹的路径', default='/share/data6/PMiD/library')
    # parser.add_argument('-f', '--txtpath', help='缓存文件存放的路径', default='/home/xujm/.cache/ncbi-genome-download')
    # parser.add_argument('-o', '--outpath', help='存放输出文件的路径', default='/share/data5/hegh/project1/5.17/toolkit')
    # args = parser.parse_args()
    # print(args.path, args.txtpath)
    path = snakemake.input["refseq"]
    txtpath = snakemake.input["txtfiles"]
    outpath = snakemake.output[0]
    print(path, txtpath, outpath)
    seqt = Seqid2Taxid(path, txtpath, outpath)
    seqt.run()