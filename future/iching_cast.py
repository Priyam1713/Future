"""I Ching casting protocol;independent domains,shared verified integer primitives."""
from .card_random import Stream, seed_bytes

PROTOCOL = 'future-iching-sha256-v1'
METHODS = ('three-coin', 'yarrow-marginal')
WEIGHTS = {'three-coin': (1, 3, 3, 1), 'yarrow-marginal': (1, 5, 7, 3)}


class CastingStream(Stream):
    def __init__(self, seed, method):
        if not isinstance(method, str) or method not in METHODS:
            raise ValueError('Unknown casting method/domain')
        encoded = seed_bytes(seed)
        self.prefix = (b'FutureIChing\0v1\0' + method.encode('ascii') + b'\0' +
                       len(encoded).to_bytes(4, 'big') + encoded)
        self.counter = 0
        self.pending = []
        self.words_used = 0
        self.rejections = 0


def coin_line(bits):
    if not isinstance(bits, (list, tuple)) or len(bits) != 3 or any(type(b) is not int or b not in (0, 1) for b in bits):
        raise ValueError('Exactly three integer coin bits required;0 tail2,1 head3')
    return 6 + sum(bits)


def yarrow_value(index):
    if type(index) is not int or not 0 <= index < 16:
        raise ValueError('Marginal draw index must be integer0..15')
    return 6 if index == 0 else 7 if index <= 5 else 8 if index <= 12 else 9


def cast(seed, method):
    stream = CastingStream(seed, method)
    lines, raw = [], []
    for _ in range(6):
        if method == 'three-coin':
            draw = [stream.below(2) for _ in range(3)]
            lines.append(coin_line(draw))
        else:
            draw = stream.below(16)
            lines.append(yarrow_value(draw))
        raw.append(draw)
    return lines, dict(protocol=PROTOCOL, method=method, seed=seed,
        raw=raw, raw_convention='coin bits0=tail2,1=head3' if method == 'three-coin' else 'indices0..15:0→6,1..5→7,6..12→8,13..15→9',
        line_order='bottom_to_top', words_used=stream.words_used, rejected_words=stream.rejections,
        blocks_generated=stream.counter, seed_encoding='strict UTF-8', normalization='none')
