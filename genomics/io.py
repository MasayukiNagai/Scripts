
def prepare_fasta(sequences, outpath):
    """Write list of sequence strings to FASTA format with max 80 chars per line"""
    max_width = 80

    with open(outpath, 'w') as f:
        for idx, seq in enumerate(sequences):
            seq_str = str(seq).strip().upper()
            f.write(f'>seq_{idx}\n')
            for i in range(0, len(seq_str), max_width):
                f.write(seq_str[i:i + max_width] + '\n')

