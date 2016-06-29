import re

def remove_comments(det):
    return re.sub("\*.*\n", "\n", det)

def remove_empty_lines(det):
    return "\n".join([x for x in det.split("\n") if x])

def tokenize_line(line):
    tokens = []
    while line:
        tokens.append(line[:10])
        line = line[10:]
    return tokens

def split_into_tokens(det):
    lines = det.split("\n")
    tokens = [tokenize_line(x) for x in lines]
    return [[x.strip() for x in token_line] for token_line in tokens]

def convert_detect(det):
    det = remove_empty_lines(remove_comments(det))
    tokens = split_into_tokens(det)
    tokens = [' '.join(line) for line in tokens]
    return "\n".join(tokens)
