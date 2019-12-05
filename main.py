import schedule
import os
import time
import argparse
import logging
import json
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)


def run(path, condapath, restart):
    if not path.endswith("/"):
        path =path + "/"
    last_outfile = path + "bwadb.txt"
    meta_file = path + "meta.tsv"
    if os.path.exists(last_outfile):
        os.remove(last_outfile)
    if os.path.exists(meta_file):
        os.remove(meta_file)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = base_dir + "/workflows/full_pipeline.smk"
    config_path = path + "config.yaml"
    json_path = path + "cluster_db.json"
    base_shell = "snakemake --snakefile {} --use-conda --conda-prefix {} --config  out_dir={} --configfile {}  --restart-times {}  --cluster-config {}".format(base_path,condapath, path, config_path, restart, json_path)
    shell = " --latency-wait 60 -j 81 --cluster 'qsub -cwd -l vf={cluster.vf},p={cluster.p} -e {cluster.err} -o {cluster.std} -V -S /bin/bash -q {cluster.q} -N {cluster.name}'"
    logger.info(base_shell + shell)
    os.system(base_shell + shell)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create main")
    parser.add_argument('-p', '--path', help='输出路径', default=os.getcwd())
    parser.add_argument('-c', '--condapath', help='conda环境目录', default='/share/data2/hegh/miniconda3/envs/')
    parser.add_argument('-r', '--restart', help='snakemake重试次数', default=3)
    parser.add_argument('-d', '--debug', help='是否打开调试模式', default=False)
    args = parser.parse_args()
    logging_level = logging.DEBUG if args.debug else logging.INFO
    path = args.path + "/root.log"
    handler = TimedRotatingFileHandler(path,
                                       when="midnight",
                                       interval=1,
                                       backupCount=5)
    logging.basicConfig(level=logging_level,
                        format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        handlers=[handler])
    if args.debug:
        schedule.every().monday.at("10:00").do(run, args.path, args.condapath, args.restart)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run(args.path, args.condapath, args.restart)