"""Build an offline study guide from authored JSON (Python standard library)."""
import argparse
import base64
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

MIME={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg',
      '.svg':'image/svg+xml','.webp':'image/webp','.gif':'image/gif'}

class EmbedImages(HTMLParser):
    def __init__(self,base):
        super().__init__(convert_charrefs=False)
        self.base=base
        self.parts=[]
        self.images=0

    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='script' and values.get('src'):
            raise ValueError('Use inline JavaScript, not script src.')
        if tag=='link' and 'stylesheet' in (values.get('rel') or '').lower().split():
            raise ValueError('Use inline CSS, not linked stylesheets.')
        if tag in {'iframe','object','embed','source','video','audio'}:
            raise ValueError(f'<{tag}> is not supported by this offline builder.')
        if tag=='image' and any(k in values for k in ('href','xlink:href')):
            raise ValueError('Use an embedded <img> or native SVG shapes instead of SVG image href.')
        if tag!='img':
            self.parts.append(self.get_starttag_text())
            return
        if 'srcset' in values:
            raise ValueError('Use a single image src rather than srcset.')
        src=values.get('src')
        if not src:
            raise ValueError('Each image needs a src.')
        if not src.startswith('data:image/'):
            parsed=urlsplit(src)
            if parsed.scheme or parsed.netloc or src.startswith('//'):
                raise ValueError(f'Use an image path relative to the JSON file: {src}')
            if parsed.query or parsed.fragment:
                raise ValueError('Image paths cannot contain URL query/fragment suffixes.')
            target=(self.base/unquote(parsed.path)).resolve()
            mime=MIME.get(target.suffix.lower())
            if not mime:
                raise ValueError(f'Unsupported image format: {target.suffix}')
            raw=target.read_bytes()
            if mime=='image/svg+xml':
                svg=raw.decode('utf-8-sig')
                if re.search(r'<script\b|(?:href|xlink:href)\s*=\s*[\'\"](?!#)',svg,re.I):
                    raise ValueError('SVG image assets must contain self-contained shapes and no scripts.')
            src='data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii')
        attrs=[(k,src if k=='src' else v) for k,v in attrs]
        self.parts.append('<img'+''.join(' '+k if v is None else f' {k}="{escape(v,quote=True)}"' for k,v in attrs)+'>')
        self.images+=1

    def handle_startendtag(self,tag,attrs):
        if tag in {'img','link','image','source','embed','script','iframe','object','video','audio'}:
            self.handle_starttag(tag,attrs)
        else:
            self.parts.append(self.get_starttag_text())
    def handle_endtag(self,tag): self.parts.append(f'</{tag}>')
    def handle_data(self,data): self.parts.append(data)
    def handle_entityref(self,name): self.parts.append('&'+name+';')
    def handle_charref(self,name): self.parts.append('&#'+name+';')
    def handle_comment(self,data): self.parts.append('<!--'+data+'-->')
    def handle_decl(self,decl): self.parts.append('<!'+decl+'>')

def build(content_path,output_path):
    content_path=Path(content_path).resolve()
    output_path=Path(output_path).resolve()
    if content_path==output_path:
        raise ValueError('Output must not overwrite the input JSON.')
    if output_path.suffix.lower() not in {'.html','.htm'}:
        raise ValueError('Output must be an HTML file.')
    data=json.loads(content_path.read_text(encoding='utf-8-sig'))
    if not isinstance(data,dict):
        raise ValueError('Content must be a JSON object.')
    title=data.get('title');sections=data.get('sections')
    if not isinstance(title,str) or not title.strip():
        raise ValueError('Provide a nonempty title.')
    if not isinstance(sections,list) or not sections:
        raise ValueError('Provide a nonempty sections array.')
    seen=set();nav=[];bodies=[]
    for section in sections:
        if not isinstance(section,dict):
            raise ValueError('Each section must be an object.')
        key=section.get('id','')
        if not isinstance(key,str) or not re.fullmatch(r'[a-z][a-z0-9-]*',key):
            raise ValueError('Section IDs must begin with a lowercase letter and use letters, digits, or hyphens.')
        if key in seen or key in {'guide-sources','image-dialog','close-image','enlarged-image'}:
            raise ValueError(f'Duplicate or reserved section ID: {key}')
        seen.add(key)
        heading=section.get('title');body=section.get('body_html')
        if not isinstance(heading,str) or not heading.strip() or not isinstance(body,str) or not body.strip():
            raise ValueError('Each section needs title and body_html strings.')
        nav.append(f'<a href="#{key}">{escape(heading)}</a>')
        bodies.append(f'<section id="{key}"><h2>{escape(heading)}</h2>{body}</section>')
    opt={}
    for key in ['subtitle','intro_html','source_notes_html','extra_css','extra_js']:
        opt[key]=data.get(key,'')
        if not isinstance(opt[key],str):
            raise ValueError(f'{key} must be a string.')
    if re.search(r'</script\b',opt['extra_js'],re.I) or re.search(r'</style\b',opt['extra_css'],re.I):
        raise ValueError('Extra JS/CSS must not contain closing script/style tags.')
    template=(Path(__file__).resolve().parents[1]/'assets/guide_template.html').read_text(encoding='utf-8')
    values={'TITLE':escape(title),'SUBTITLE':escape(opt['subtitle']),
            'INTRO':opt['intro_html'],'NAVIGATION':''.join(nav),'SECTIONS':''.join(bodies),
            'SOURCES':('<section id="guide-sources"><h2>Sources and property notes</h2>'+opt['source_notes_html']+'</section>') if opt['source_notes_html'] else '',
            'EXTRA_CSS':opt['extra_css'],'EXTRA_JS':opt['extra_js']}
    authored=re.sub(r'@@([A-Z_]+)@@',lambda m:values[m.group(1)],template)
    if re.search(r'@@[A-Z_]+@@',authored):
        raise ValueError('Unresolved template token in authored content.')
    parser=EmbedImages(content_path.parent)
    parser.feed(authored);parser.close()
    result=''.join(parser.parts)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(result,encoding='utf-8')
    return {'output':str(output_path),'sections':len(sections),'embedded_images':parser.images,'bytes':output_path.stat().st_size}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('content',type=Path,help='Authored content JSON; image paths are relative to this file.')
    p.add_argument('output',type=Path,help='Destination self-contained .html file.')
    args=p.parse_args()
    try:
        print(json.dumps(build(args.content,args.output),indent=2))
    except (ValueError,OSError,KeyError) as exc:
        print(f'Build failed: {exc}',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
