"""Frozen replayable card sampling protocol; not a security guarantee or ritual."""
import hashlib

PROTOCOL='future-cards-sha256-fy-v1'
SIZE=1<<32


def seed_bytes(seed):
    if not isinstance(seed,str):raise ValueError('Seed must be explicit Unicode text')
    try:encoded=seed.encode('utf-8',errors='strict')
    except UnicodeError as exc:raise ValueError('Seed must be valid UTF-8 text') from exc
    if not 1<=len(encoded)<=256:raise ValueError('Seed must contain1-256 UTF-8 bytes;no normalization')
    return encoded


class Stream:
    def __init__(self,seed,domain):
        encoded=seed_bytes(seed)
        if domain not in ('deck','orientation'):raise ValueError('Unknown protocol domain')
        self.prefix=b'FutureCards\0v1\0'+domain.encode('ascii')+b'\0'+len(encoded).to_bytes(4,'big')+encoded
        self.counter=0;self.pending=[];self.words_used=0;self.rejections=0

    def word(self):
        if not self.pending:
            if self.counter>=1<<64:raise ValueError('Stream counter exhausted')
            block=hashlib.sha256(self.prefix+self.counter.to_bytes(8,'big')).digest()
            self.counter+=1
            self.pending=[int.from_bytes(block[i:i+4],'big') for i in range(0,32,4)]
        self.words_used+=1
        return self.pending.pop(0)

    def below(self,n):
        if type(n) is not int or not 1<=n<=SIZE:raise ValueError('Bound must be integer in1..2^32')
        limit=SIZE-SIZE%n
        while True:
            word=self.word()
            if word<limit:return word%n
            self.rejections+=1


def shuffle_pack(identifiers,seed,*,rounds=1,cut=False):
    if type(rounds) is not int or rounds not in (1,3) or type(cut) is not bool:raise ValueError('Unsupported shuffle protocol settings')
    if not isinstance(identifiers,(list,tuple)) or not identifiers or any(not isinstance(k,str) or not k for k in identifiers) or len(set(identifiers))!=len(identifiers):
        raise ValueError('Pack requires distinct nonempty identifiers')
    if cut and len(identifiers)<2:raise ValueError('Nonempty cut requires at least two cards')
    stream=Stream(seed,'deck');pack=list(identifiers);cuts=[]
    for _ in range(rounds):
        for i in range(len(pack)-1,0,-1):
            j=stream.below(i+1);pack[i],pack[j]=pack[j],pack[i]
        if cut:
            k=1+stream.below(len(pack)-1);cuts.append(k);pack=pack[k:]+pack[:k]
    return pack,dict(rounds=rounds,cuts=cuts,words_used=stream.words_used,rejected_words=stream.rejections)


def orientations(seed,count,policy):
    if type(count) is not int or not 0<=count<=78:raise ValueError('Invalid orientation count')
    if policy not in ('upright_only','seeded_reversals'):raise ValueError('Unknown seeded orientation policy')
    seed_bytes(seed)
    if policy=='upright_only':return ['upright']*count
    stream=Stream(seed,'orientation')
    return ['reversed' if stream.below(2) else 'upright' for _ in range(count)]
