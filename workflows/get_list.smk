include:
    "logging.smk"

import pandas
import getpass
username = getpass.getuser()
txtfiles_path = "/home/{}/.cache/ncbi-genome-download".format(username)
download_dir = out_dir + "library/"
refseq_dir = out_dir + "library/refseq/"
summary_dir = out_dir + "library/summary/"
if not os.path.isdir(refseq_dir):
    logging.debug("Not existed {} directory".format(refseq_dir))
    raise ValueError("Not existed {} directory".format(refseq_dir))


