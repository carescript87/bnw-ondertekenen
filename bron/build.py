import base64, io, json, re, sys
from html.parser import HTMLParser
from PIL import Image

S = __import__('os').path.dirname(__import__('os').path.abspath(__file__))


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.lists = []      # [type, counter]
        self.bq = 0
        self.b = self.i = self.mark = 0
        self.cur = None
        self.pending = None  # marker for the next paragraph in an li

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'ol':
            self.lists.append([a.get('type', '1'), int(a.get('start', 1)) - 1])
        elif tag == 'ul':
            self.lists.append(['•', 0])
        elif tag == 'li':
            l = self.lists[-1]
            l[1] += 1
            self.pending = '•' if l[0] == '•' else (chr(96 + l[1]) + '.' if l[0] == 'a' else str(l[1]) + '.')
        elif tag == 'blockquote':
            self.bq += 1
        elif tag == 'p':
            self.cur = {'runs': [], 'mark': False}
        elif tag == 'strong':
            self.b += 1
        elif tag == 'em':
            self.i += 1
        elif tag == 'mark':
            self.mark += 1
        elif tag == 'br' and self.cur is not None:
            self.cur['runs'].append([' ', ''])
        elif tag == 'img' and self.cur is not None:
            self.cur['img'] = True

    def handle_endtag(self, tag):
        if tag in ('ol', 'ul'):
            self.lists.pop()
        elif tag == 'blockquote':
            self.bq -= 1
        elif tag == 'strong':
            self.b -= 1
        elif tag == 'em':
            self.i -= 1
        elif tag == 'mark':
            self.mark -= 1
        elif tag == 'p':
            c, self.cur = self.cur, None
            runs = []
            for t, f in c['runs']:
                if runs and runs[-1][1] == f:
                    runs[-1][0] += t
                else:
                    runs.append([t, f])
            text = ''.join(r[0] for r in runs).strip()
            if not text and not c.get('img'):
                return
            blk = {'k': 'p', 'runs': runs, 'lvl': 1 if (self.bq or (self.lists and self.lists[-1][0] == '•')) else 0,
                   'mark': c['mark'], 'text': text}
            if self.pending:
                blk['k'] = 'li'
                blk['m'] = self.pending
                self.pending = None
            elif not self.lists:
                allb = all('b' in f for t, f in runs if t.strip())
                m = re.match(r'^(\d+)\.\s+', text)
                if allb and text.startswith('Artikel'):
                    blk['k'] = 'h'
                elif allb and text.upper() == text:
                    blk['k'] = 'cap'
                elif m:
                    blk['k'] = 'li'
                    blk['m'] = m.group(1) + '.'
                    n = len(m.group(0))
                    # strip the marker from the leading run(s)
                    while n and runs:
                        take = min(n, len(runs[0][0]))
                        runs[0][0] = runs[0][0][take:]
                        n -= take
                        if not runs[0][0]:
                            runs.pop(0)
            self.blocks.append(blk)

    def handle_data(self, d):
        if self.cur is None:
            return
        d = d.replace('\n', ' ')
        f = ('b' if self.b else '') + ('i' if self.i else '')
        if self.mark:
            self.cur['mark'] = True
        self.cur['runs'].append([d, f])


def parse(name):
    p = P()
    p.feed(open(f'{S}/{name}.html', encoding='utf-8').read())
    b = p.blocks
    title = b[0]['text']
    first_mark = next(i for i, x in enumerate(b) if x['mark'])
    after = next(i for i in range(first_mark, len(b)) if not b[i]['mark'])
    end = next(i for i, x in enumerate(b) if x['text'].startswith('Aldus overeengekomen'))
    noemen = next(x for x in b[first_mark:after] if x['text'].startswith('hierna te noemen'))
    tail = b[end:]
    coop = [x['text'] for x in tail[1:] if not x['mark']]
    clean = lambda L: [{k: v for k, v in x.items() if k in ('k', 'runs', 'lvl', 'm')} for x in L]
    return {'title': title, 'pre': clean(b[1:first_mark]), 'noemen': noemen['runs'],
            'post': clean(b[after:end]), 'tail': [x['text'] for x in tail]}


def img(path, w, fmt='PNG'):
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    im = bg.convert('RGB')
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    o = io.BytesIO()
    im.save(o, fmt, optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(o.getvalue()).decode(), im.size


logo, logo_sz = img(f'{S}/logo-bnw.png', 900)
sig, sig_sz = img(f'{S}/handtekening-cooperatie.png', 481)
tpl = open(f'{S}/template.html', encoding='utf-8').read()

DOCS = {
    'led': dict(file='ledenovereenkomst-bnw', short='Ledenovereenkomst', rol='Lid',
                coop='Coöperatieve Vereniging Beweegzorg Noord-West U.A.'),
    'ken': dict(file='kennismakersovereenkomst-bnw', short='Kennismakersovereenkomst', rol='Kennismaker',
                coop='Coöperatieve Vereniging Beweegzorg Noord-West U.A.'),
}
for key, meta in DOCS.items():
    d = parse(key)
    if '--dump' in sys.argv:
        print(key, d['title'], len(d['pre']), len(d['post']))
        print(json.dumps(d['tail'], ensure_ascii=False, indent=1))
        for x in d['pre'] + d['post']:
            print(x['k'], x.get('m', ''), x['lvl'], ''.join(r[0] for r in x['runs'])[:70])
    d.pop('tail')
    d.update(meta)
    d['logoRatio'] = logo_sz[1] / logo_sz[0]
    d['sigRatio'] = sig_sz[1] / sig_sz[0]
    out = (tpl.replace('__TITLE__', meta['short'] + ' BNW')
              .replace('__H1__', d['title'])
              .replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))
              .replace('__LOGO__', logo).replace('__SIG__', sig))
    open(f'{S}/{meta["file"]}.html', 'w', encoding='utf-8').write(out)
    print(meta['file'], len(out))

prep = open(f'{S}/prep-template.html', encoding='utf-8').read().replace('__LOGO__', logo)
open(f'{S}/bnw-ondertekenlinks.html', 'w', encoding='utf-8').write(prep)
print('prep', len(prep))
