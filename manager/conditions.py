import os

indir = '../conditions/'
int_cates = ['size']
bool_cates = ['is_new']

def conditions2dict(conds):
    ret = dict()
    for cond in conds:
        cond = cond.strip()
        k = cond.split(':')[0]
        vs_str = cond.split(':')[1]
        vs = vs_str.split(',')
        if len(vs_str) > 0 and len(vs) > 0:
            if k not in ret:
                ret[k] = []
            if k in int_cates:
                vs = [int(v) for v in vs]
            if k in bool_cates:
                vs = [bool(v) for v in vs]
            for v in vs:
                ret[k].append(v)
    return ret

def get_conds():
    ret = dict()
    for fname in os.listdir(indir):
        conds = conditions2dict(open(indir + fname, 'r').readlines())
        ret[fname] = conds
    return ret

if __name__ == '__main__':
    get_conds()
