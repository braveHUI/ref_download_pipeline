import pandas
import os 
import queue
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
logger = logging.getLogger(__name__)

maxThreads = snakemake.params["threads"]
input_path = snakemake.input[1]
output_path = snakemake.output[0]
# print(input_path, output_path, maxThreads)


def run(input_path, output_path):
    summary_files = [f for f in os.listdir(input_path) if f.endswith("assembly_summary.txt.tsv")]
    acc_to_relepath = {}
    accs = []
    out_put_list = []
    out_dir_list = output_path.split("/")
    del out_dir_list[-1]
    out_dir = "/".join(out_dir_list) + "/"
    try:
        for file in summary_files:
            file = input_path + file
            summary_data = pandas.read_csv(file, sep="\t", index_col=0)
            domain = file.split("_")[1]
            for acc in summary_data.index:
                accs.append(acc)
                acc_to_relepath[acc] = "/".join(summary_data['local_path'][acc].split("/")[-3:])
                out_put = out_dir + "references/bwa_db/{}/all.fna".format(acc)
                output_dir = out_dir + "references/bwa_db/{}".format(acc)
                acc_to_relepath[acc] = out_dir + "library/refseq/" + acc_to_relepath[acc]
                if not os.path.exists(out_put):
                    os.makedirs(output_dir)
                    # print("创建%s文件成功" % output_dir)
                    logger.debug("")
                    os.system("gzip -t {}".format(acc_to_relepath[acc]))
                    os.system("gunzip -c {} > {}".format(acc_to_relepath[acc], out_put))
                    out_put_list.append(out_put)
    except Exception as e:
        logger.warning(e)

    write_data(output_path, accs)
    return out_put_list
    # accs_uniq = set(accs)
    # if len(accs_uniq) != len(accs):
    #     logging.debug("Has duplicate acc")
    #     raise ValueError("Has duplicate acc")


def write_data(output_path, accs):
    f = open(output_path, 'w')
    for acc in accs:
        f.write(acc + "\n")
    f.close()


class store(threading.Thread):
    def __init__(self, store, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.store = store

    def run(self):
        try:
            os.system(" samtools faidx {} > /dev/null".format(self.store))
            os.system(" bwa index {} >> /dev/null".format(self.store))
        except Exception as e:
            logger.error("{} : {}".format(self.store, e))
        finally:
            self.queue.get()
            self.queue.task_done()


def main(input_path, output_path):
    try:
        out_put_list = run(input_path, output_path)
        q = queue.Queue(maxThreads)
        if len(out_put_list):
            for s in out_put_list:
                q.put(s)
                t = store(s, q)
                t.start()
            q.join()
    except Exception as e:
        logger.warning(e)


if __name__ == "__main__":
    out_dir_list = output_path.split("/")
    del out_dir_list[-1]
    args_path = "/".join(out_dir_list) + "/"
    path = args_path + "/root.log"
    handler = TimedRotatingFileHandler(path,
                                       when="midnight",
                                       interval=1,
                                       backupCount=5)
    logging.basicConfig(level="INFO",
                        format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        handlers=[handler])
    main(input_path, output_path)