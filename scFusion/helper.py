import os
import subprocess


def move_files(indir, outdir):
    start = 131761
    stop = 131887
    for i in range(start, stop+1):
        dirname = f'HRR{i}'
        f1 = f'HRR{i}_f1.fastq.gz'
        f1_new = f'{i}_1.fastq.gz'
        p1 = os.path.join(indir, dirname, f1)
        p1_new = os.path.join(outdir, f1_new)
        cmd1 = f'mv {p1} {p1_new}'
        print(cmd1)
        execute(cmd1)
        f2 = f'HRR{i}_r2.fastq.gz'
        f2_new = f'{i}_2.fastq.gz'
        p2 = os.path.join(indir, dirname, f2)
        p2_new = os.path.join(outdir, f2_new)
        cmd2 = f'mv {p2} {p2_new}'
        print(cmd2)
        execute(cmd2)


def execute(cmd):
    proc = subprocess.run(cmd, shell=True, cwd=None,
                          text=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    # print(proc.stdout)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)
    return proc.stdout
