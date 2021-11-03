import argparse
import os
import sys
import logging

def argument_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', '-i', type=str, metavar='INI',
                            required=True, dest='ini',
                            help='Required; Specify a sample ini file.')
    arg_parser.add_argument('--config', '-c', type=str, metavar='CONFIG',
                            required=True, dest='conf',
                            help='Required; Specify a config file.')
    arg_parser.add_argument('--outdir', '-o', type=str, metavar='OUTDIR',
                            required=True, dest='outdir',
                            help='Required; Specify an output directory.')
    args = arg_parser.parse_args()
    return args


def checkpath(path):
    if not os.path.exists(path):
        errmsg = f'Error: Cannot find "{path}"'
        sys.exit(errmsg)


def makedir(dirpath):
    if not os.path.exists(dirpath):
        try:
            os.mkdir(dirpath)
        except OSError:
            sys.exit(f'Error: Failed to make a directory "{dirpath}"')
    else:
        pass

def setup_logger(name, logfile):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # creates a file handler that logs messages above DEBUG level
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(filename)s %(funcName)s :\n%(message)s')
    fh.setFormatter(fh_formatter)
    # creates a file handler that logs messages above INFO level
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(filename)s : %(message)s', '%Y-%m-%d %H:%M:%S')
    sh.setFormatter(sh_formatter)
    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger

