import numpy as np


class OneHotEncoder:
    """
    One-Hot Encoder/Decoder for DNA sequences.


    Parameters
    ----------
    alphabet : str
        Alphabet of the sequences. Default is "ACGT".
    unknown : str
        Character to use for unknown bases. Default is "N".
    channel_axis : int
        Axis for the channel dimension in one-hot encoding.
        Can be 1 (N, 4, L), -1 (N, L, 4), or 2 (N, L, 4). Default is -1.
    """
    def __init__(self, alphabet: str = "ACGT", unknown: str = "N", channel_axis: int = -1):
        if channel_axis not in (1, -1, 2):
            raise ValueError("channel_axis must be 1, -1, or 2")

        self.alphabet = alphabet.upper()
        self.vocab_size = len(alphabet)
        self.unknown = unknown.upper()
        self.channel_axis = channel_axis

        # --- Pre-compute Lookups ---
        # ASCII to Index Lookup; 255 means unknown
        self._lookup = np.full(128, 255, dtype=np.uint8)
        for i, char in enumerate(self.alphabet):
            self._lookup[ord(char)] = i

        # Index to Byte Lookup (S1)
        self._rev_lookup = np.frombuffer(self.alphabet.encode("ascii"), dtype="S1")

    def to_onehot(self, seqs: str | list[str]) -> np.ndarray:
        """
        Converts list of sequences to one-hot encoded array.

        Parameters
        ----------
        seqs : str | list[str]
            Input sequence or list of sequences.
            If sequence lengths differ, they will be padded with unknown character at the end.

        Returns
        -------
        np.ndarray
            One-hot encoded array.
            Shape is (N, 4, L) if channel_axis=1, else (N, L, 4).
            If input is a single sequence, returns array of shape (4, L) or (L, 4).
        """
        is_single = isinstance(seqs, str)
        if is_single:
            seqs = [seqs]

        # Fixed width strings (pad with null bytes)
        L = max(len(s) for s in seqs) if seqs else 0
        arr = np.array([s.upper() for s in seqs], dtype=f"S{L}")  # (N,)
        N = arr.shape[0]

        # View raw bytes as integers (uint8)
        arr_bytes = arr.view(np.uint8).reshape(N, L)

        # Map to indices
        idx = self._lookup[arr_bytes]
        invalid = (idx == 255)
        idx_safe = idx.copy()
        idx_safe[invalid] = 0

        # Build One-Hot: (N, L) -> (N, L, 4)
        onehot = np.eye(self.vocab_size, dtype=np.float32)[idx_safe]  # (N, L, 4)
        if np.any(invalid):
            onehot[invalid] = 0

        # Transpose to (N, 4, L)
        if self.channel_axis == 1:
            onehot = onehot.transpose(0, 2, 1)

        return onehot if not is_single else onehot[0]

    def from_onehot(self, onehot: np.ndarray) -> list[str] | str:
        """
        Converts one-hot encoded array back to sequences.

        Parameters
        ----------
        onehot : np.ndarray
            One-hot encoded array.
            Shape can be (N, 4, L), (N, L, 4), (4, L), or (L, 4).

        Returns
        -------
        list[str] | str
            Decoded sequences. If input is a single sequence, returns a single string.
        """
        is_single = (onehot.ndim == 2)
        if is_single:
            onehot = onehot[np.newaxis, :, :]

        # Accept (N, 4, L) or (N, L, 4)
        if onehot.shape[1] == self.vocab_size:
            oh = onehot.transpose(0, 2, 1)   # (N, L, 4)
        else:
            oh = onehot                      # (N, L, 4)

        # Argmax gives candidate base
        idx = np.argmax(oh, axis=-1)          # (N, L)

        # Index -> base
        chars = self._rev_lookup[idx]         # (N, L) S1

        # Anything not exactly 1 becomes 'N'
        maxv = oh.max(axis=-1)                # (N, L)
        mask = (maxv != 1.0)
        if np.any(mask):
            chars = chars.copy()
            chars[mask] = b"N"

        # Join bytes into strings
        strings = chars.view(f"S{chars.shape[1]}").ravel()
        seqs = [s.decode("utf-8") for s in strings]

        return seqs[0] if is_single else seqs


def reverse_complement(array: np.ndarray) -> np.ndarray:
    """
    Get reverse complement of one-hot DNA encoding.
    The channel order is assumed to be A, C, G, T.

    Parameters
    ----------
    array : np.ndarray
        Input array of shape (4, L) for single sequence or (N, 4, L) for batch of sequences.

    Returns
    -------
    np.ndarray
        Reverse complement of the input array with the same shape.
    """
    rc = np.array([3, 2, 1, 0])  # A<->T, C<->G

    if array.ndim == 2:
        # single sequence
        if array.shape[0] != 4:
            raise ValueError(f"Expected shape (4, L) for single sequence, got {array.shape}")
        return array[:, ::-1][rc, :]

    if array.ndim == 3:
        # batch of sequences
        if array.shape[1] != 4:
            raise ValueError(f"Expected shape (N, 4, L) for batch of sequences, got {array.shape}")
        return array[:, :, ::-1][:, rc, :]

    raise ValueError(f"Expected 2D or 3D array, got shape {array.shape}")


def reverse_complement_string(
    seq: str, mapping={"A": "T", "G": "C", "T": "A", "C": "G", "N": "N"}
) -> str:
    """Get reverse complement of DNA sequence."""
    return "".join(mapping[s] for s in reversed(seq))
