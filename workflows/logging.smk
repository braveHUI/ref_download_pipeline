from shutil import copyfile
import sys
import datetime
import os
import logging

logging.basicConfig(level=logging.DEBUG, filename='root.log',
                        format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

try:
    pipeline_path 
except NameError:
    pipeline_path = workflow.basedir + "/../"

today = datetime.datetime.now()

if "out_dir" not in config.keys():
    out_dir = "{}/".format(os.getcwd())
else:
    out_dir=config["out_dir"]
    if not out_dir.endswith("/"):
        out_dir = out_dir + "/"

if "logging_folder" not in config.keys():
    logging_folder = "logs/"
else:
    logging_folder=config["logging_folder"]
    if not logging_folder.endswith("/"):
        logging_folder = logging_folder + "/"

if "--dryrun" not in sys.argv and "-n" not in sys.argv:
    date = today.strftime("%Y/%m/%d")
    time = today.strftime('%H_%M_%S_%f')[:-4]
    logging_folder = str(logging_folder+"/"+date+"/"+time).replace("//", "/")
    if not logging_folder.endswith("/"):
        logging_folder = logging_folder + "/"
    os.makedirs(logging_folder, exist_ok=True)
    cmd_file = logging_folder + "/cmd.txt"
    with open(cmd_file, "w") as f:
        f.write(" ".join(sys.argv)+"\n")
    if workflow.overwrite_configfile is not None:
        copyfile(workflow.overwrite_configfile, logging_folder+"/config.yaml")

