import json

def transform(src, dst, var_name):
    with open(src, 'r', encoding='utf-8') as f:
        data = json.load(f)
    out = []
    for e in data:
        trans = e.get('translations', [])
        zh = '；'.join(
            ((t.get('type', '') + '. ') if t.get('type') else '') + t.get('translation', '')
            for t in trans
        )
        phrases = e.get('phrases', [])
        ex = phrases[0]['phrase'] if phrases else ''
        out.append({'en': e.get('word', ''), 'ph': '', 'zh': zh, 'ex': ex})
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('const ' + var_name + ' = ')
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';')
    print(dst, 'entries:', len(out))

transform('cet4_raw.json', 'cet4.js', 'CET4_DATA')
transform('cet6_raw.json', 'cet6.js', 'CET6_DATA')
