"""Validate one proposed Cerchi guide without changing published pages."""

import argparse
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urljoin, urlsplit


BASE = "https://alessandro-gentili.it/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
COVER_NAME = re.compile(r"cerchi-guida-(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*-1600x900\.webp\Z")
MODES = {"DRAFT", "PUBLICATION"}

# These editorial abbreviations have one specific, reviewed destination. All
# other labels still need to match their heading or be an unambiguous heading
# prefix; a valid href alone never makes a TOC label acceptable.
EDITORIAL_TOC_ALIASES = {
    "il problema umano: ordine, paura e autorità": "il problema umano — Ordine, paura e autorità",
    "weimar e la crisi dell'ordine": "Weimar — La crisi dell'ordine costituzionale",
    "faq": "Domande frequenti",
    "domande frequenti": "FAQ",
}


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def find(self, tag=None, css_class=None):
        for node in walk(self):
            if (tag is None or node.tag == tag) and (css_class is None or css_class in node.attrs.get("class", "").split()):
                yield node


def walk(node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def content(node):
    return "".join(content(child) if isinstance(child, Node) else child for child in node.children)


def visible_text(node):
    """Extract readable text with boundaries between HTML blocks and list items."""
    if not isinstance(node, Node):
        return node
    value = "".join(visible_text(child) for child in node.children)
    return f" {value} " if node.tag in {"br", "p", "li", "h1", "h2", "h3", "h4", "blockquote", "td", "th", "tr"} else value


def normalized(value):
    return " ".join(unicodedata.normalize("NFC", unescape(value)).split())


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.comments = []
        self.malformed = []
        self.feed(html)
        if len(self.stack) > 1:
            self.malformed.append("unclosed HTML elements")

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                if index != len(self.stack) - 1:
                    self.malformed.append(f"misnested </{tag}>")
                del self.stack[index:]
                return
        self.malformed.append(f"unmatched </{tag}>")

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_comment(self, data):
        self.comments.append(data)


def webp_size(path):
    raw = path.read_bytes()
    if len(raw) < 20 or raw[:4] != b"RIFF" or raw[8:12] != b"WEBP" or int.from_bytes(raw[4:8], "little") + 8 != len(raw):
        raise ValueError("cover must be a complete WebP file")
    offset = 12
    while offset + 8 <= len(raw):
        kind = raw[offset:offset + 4]
        length = int.from_bytes(raw[offset + 4:offset + 8], "little")
        data = raw[offset + 8:offset + 8 + length]
        if len(data) != length:
            raise ValueError("truncated WebP chunk")
        if kind == b"VP8X" and len(data) >= 10:
            return int.from_bytes(data[4:7], "little") + 1, int.from_bytes(data[7:10], "little") + 1
        if kind == b"VP8L" and len(data) >= 5 and data[0] == 0x2F:
            bits = int.from_bytes(data[1:5], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if kind == b"VP8 " and len(data) >= 10 and data[3:6] == b"\x9d\x01\x2a":
            return int.from_bytes(data[6:8], "little") & 0x3FFF, int.from_bytes(data[8:10], "little") & 0x3FFF
        offset += 8 + length + (length % 2)
    raise ValueError("unsupported WebP image data")


def markdown_plain(value):
    value = re.sub(r"!?\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"(?<!\w)[*_`~]+|[*_`~]+(?!\w)", "", value)
    return normalized(value)


def manuscript_blocks(lines):
    blocks = []
    for block in re.split(r"\n\s*\n", "\n".join(lines)):
        if block.strip() == "---":
            continue
        clean = []
        for line in block.splitlines():
            line = line.strip()
            if not line or line == "---":
                continue
            if "|" in line:
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                line = " ".join(cells)
            line = re.sub(r"^\s*(?:#{3,6}\s+|>\s*|[-*+]\s+|\d+[.)]\s+)", "", line)
            clean.append(line)
        value = markdown_plain(" ".join(clean))
        if value:
            blocks.append(value)
    return blocks


def manuscript_structure(source):
    """Parse the supported H1, opening, numbered index and H2/H3 guide layout."""
    lines = source.read_text(encoding="utf-8").splitlines()
    if any(re.match(r"^\s*(?:```|~~~|<(?!!--)|#{4,6}\s)", line) for line in lines):
        raise ValueError("unsupported Markdown structure; human review is required")
    nonblank = [index for index, line in enumerate(lines) if line.strip()]
    if not nonblank or not re.fullmatch(r"# (?!#).+", lines[nonblank[0]]):
        return None
    first = nonblank[0]
    title = markdown_plain(lines[first][2:])
    subtitle_at = next((i for i in range(first + 1, len(lines)) if lines[i].strip()), None)
    if subtitle_at is None:
        raise ValueError("full manuscript needs a subtitle after its H1")
    subtitle_line = lines[subtitle_at].strip()
    if re.fullmatch(r"## (?!#).+", subtitle_line):
        subtitle = markdown_plain(subtitle_line[3:])
        intro_start = subtitle_at + 1
    elif re.fullmatch(r"(?:\*\*.+\*\*|\*.+\*|__.+__|_.+_)", subtitle_line):
        subtitle = markdown_plain(subtitle_line)
        intro_heading_at = next((i for i in range(subtitle_at + 1, len(lines))
                                 if re.fullmatch(r"##\s+Introduzione(?:\s*[—:–-].*)?", lines[i].strip(), re.I)), None)
        if intro_heading_at is None:
            raise ValueError("emphasized subtitle needs an explicit Introduzione heading")
        intro_start = intro_heading_at + 1
    else:
        raise ValueError("full manuscript needs an H2 or emphasized subtitle after its H1")
    index_at = next((i for i in range(intro_start, len(lines)) if lines[i].strip() == "## Indice"), None)
    if index_at is None:
        raise ValueError("full manuscript needs a ## Indice after the introduction")
    intro = manuscript_blocks(lines[intro_start:index_at])
    first_section = next((i for i in range(index_at + 1, len(lines)) if re.match(r"^## (?!#)", lines[i])), None)
    if first_section is None:
        raise ValueError("full manuscript has no guide sections after the index")
    index = []
    for line in lines[index_at + 1:first_section]:
        if not line.strip() or line.strip() == "---":
            continue
        match = re.fullmatch(r"\s*(\d+)\.\s+(.+?)\s*", line)
        if not match or int(match.group(1)) != len(index) + 1:
            raise ValueError("manuscript index must be a consecutive numbered list")
        index.append(markdown_plain(match.group(2)))
    if not index:
        raise ValueError("manuscript index is empty")
    sections = []
    starts = [i for i in range(first_section, len(lines)) if re.match(r"^## (?!#)", lines[i])]
    for start, end in zip(starts, starts[1:] + [len(lines)]):
        heading = markdown_plain(lines[start][3:])
        heading = re.sub(r"^\d+[.)]\s*", "", heading)
        body_lines = lines[start + 1:end]
        subheadings = [markdown_plain(line[4:]) for line in body_lines if re.match(r"^### (?!#)", line)]
        sections.append((heading, subheadings, manuscript_blocks(body_lines)))
    return title, subtitle, intro, index, sections


def toc_key(value):
    value = unicodedata.normalize("NFC", unescape(value)).casefold()
    value = value.replace("’", "'").replace("‘", "'").replace("ʼ", "'")
    value = re.sub(r"\s*[:—–-]\s*", " — ", value)
    return " ".join(value.split())


def editorial_text_key(value):
    return normalized(value).replace("’", "'").replace("‘", "'").replace("ʼ", "'")


def toc_label_matches(label, heading):
    label_key, heading_key = toc_key(label), toc_key(heading)
    if label_key == heading_key:
        return True
    if {label_key, heading_key} == {toc_key("FAQ"), toc_key("Domande frequenti")}:
        return True
    alias_heading = next((expected for alias, expected in EDITORIAL_TOC_ALIASES.items()
                          if toc_key(alias) == label_key), None)
    if alias_heading is not None:
        return heading_key == toc_key(alias_heading)
    return heading_key.startswith(label_key + " — ") and bool(heading_key[len(label_key) + 3:].strip())


def final_headings_valid(headings):
    if len(headings) < 3:
        return False
    fonts, progress, closing = headings[-3:]
    return (not any(heading in {"Fonti", "Fonti e copyright", "Prosegui la lettura"}
                    or heading == "Chiusura editoriale"
                    or heading.startswith("Chiusura editoriale — ") for heading in headings[:-3])
            and fonts in {"Fonti", "Fonti e copyright"}
            and progress == "Prosegui la lettura"
            and (closing == "Chiusura editoriale"
                 or bool(re.fullmatch(r"Chiusura editoriale — [^—]+", closing))))


def validate(page, cover, source, root, mode="DRAFT", release_guides=(), report=None):
    errors = []
    report = report if report is not None else []

    def require(ok, message):
        if not ok:
            errors.append(message)

    slug = page.parent.name
    require(mode in MODES, f"mode must be one of {', '.join(sorted(MODES))}")
    require(page.name == "index.html" and page.parent.parent.name == "guide" and bool(SLUG.fullmatch(slug)), "page must be cerchi/guide/<unique-slug>/index.html")
    existing = root / "cerchi/guide" / slug / "index.html"
    require(not existing.exists() or existing.resolve() == page.resolve(), f"slug already published: {slug}")
    for label, path in (("page", page), ("cover", cover), ("source", source)):
        require(path.is_file(), f"{label} not found: {path}")
    if not all(path.is_file() for path in (page, cover, source)):
        return errors

    html = page.read_text(encoding="utf-8")
    tree = Tree(html)
    nodes = list(walk(tree.root))
    require(not tree.malformed, "malformed HTML: " + ", ".join(tree.malformed))
    ids = [node.attrs["id"] for node in nodes if "id" in node.attrs]
    require(len(ids) == len(set(ids)), "duplicate HTML IDs")
    require(not tree.comments and not re.search(r"\b(?:TODO|PLACEHOLDER|NOME AUTORE|Guida NN|Lorem ipsum|sezione-uno)\b", html, re.I), "template placeholder or HTML comment remains")
    canonical = BASE + f"cerchi/guide/{slug}/"
    sitemap = root / "sitemap.xml"
    sitemap_text = sitemap.read_text(encoding="utf-8") if sitemap.is_file() else ""
    sitemap_urls = {normalized(unescape(item)) for item in re.findall(r"<loc>\s*(.*?)\s*</loc>", sitemap_text, re.I | re.S)}
    if mode == "DRAFT":
        require(canonical not in sitemap_urls, "DRAFT candidate must remain absent from the public sitemap")
        report.append(f"PUBLICATION STATUS: NON PUBBLICATA (DRAFT; {canonical} absent from sitemap)")
    elif mode == "PUBLICATION":
        require(canonical in sitemap_urls, "PUBLICATION candidate canonical must be included in sitemap")

    release_urls = set()
    for value in release_guides:
        url = urljoin(BASE, value)
        parsed = urlsplit(url)
        local = root / unquote(parsed.path).lstrip("/")
        if parsed.path.endswith("/"):
            local = local / "index.html"
        require(parsed.netloc == "alessandro-gentili.it" and parsed.path.startswith("/cerchi/guide/") and local.is_file(), f"release guide must be an existing local guide URL: {value}")
        release_urls.add(url if url.endswith("/") else url + "/")

    def one(tag, attr, value):
        found = [node for node in nodes if node.tag == tag and node.attrs.get(attr) == value]
        require(len(found) == 1, f"expected one {tag}[{attr}={value}]")
        return found[0] if len(found) == 1 else None

    titles = [node for node in nodes if node.tag == "title"]
    require(len(titles) == 1 and bool(normalized(content(titles[0])) if titles else ""), "missing or duplicate meta title")
    description = one("meta", "name", "description")
    canonical_node = one("link", "rel", "canonical")
    require(bool(description and normalized(description.attrs.get("content", ""))), "missing meta description")
    require(bool(canonical_node and canonical_node.attrs.get("href") == canonical), "canonical must self-reference the candidate URL")
    for prop, expected in (("og:url", canonical), ("twitter:url", canonical)):
        node = one("meta", "property" if prop.startswith("og:") else "name", prop)
        require(bool(node and node.attrs.get("content") == expected), f"{prop} must match the self-canonical URL")
    require(not any(node.tag == "meta" and node.attrs.get("name") == "robots" and "noindex" in node.attrs.get("content", "").lower() for node in nodes), "public guide must not have noindex")
    require(any(node.tag == "header" and "site-header" in node.attrs.get("class", "").split() for node in nodes), "shared site header missing")
    require(any(node.tag == "footer" and "footer" in node.attrs.get("class", "").split() for node in nodes), "shared site footer missing")
    header = next((node for node in nodes if node.tag == "header" and "site-header" in node.attrs.get("class", "").split()), None)
    require(bool(header and any(n.tag == "nav" and "primary-nav" in n.attrs.get("class", "").split() for n in walk(header))
            and any(n.tag == "ul" and "primary-nav-list" in n.attrs.get("class", "").split() for n in walk(header))), "shared primary navigation structure missing")
    if header:
        require(any(n.tag == "a" and "brand" in n.attrs.get("class", "").split() for n in walk(header)), "shared brand link missing from primary navigation")
        nav_lists = [n for n in walk(header) if n.tag == "ul" and "primary-nav-list" in n.attrs.get("class", "").split()]
        if nav_lists:
            nav_items = [n for n in nav_lists[0].children if isinstance(n, Node) and n.tag == "li"]
            require(bool(nav_items) and all("primary-nav-item" in n.attrs.get("class", "").split() for n in nav_items), "primary navigation items need .primary-nav-item")
            nav_links = [n for n in walk(nav_lists[0]) if n.tag == "a"]
            require(bool(nav_links) and all({"primary-nav-link", "primary-nav-dropdown-link"}.intersection(n.attrs.get("class", "").split()) for n in nav_links), "primary navigation links need the established primary-nav link classes")
    footer = next((node for node in nodes if node.tag == "footer" and "footer" in node.attrs.get("class", "").split()), None)
    require(bool(footer and any(n.tag == "nav" and "footer-nav" in n.attrs.get("class", "").split() for n in walk(footer))), "shared footer navigation structure missing")
    stylesheet_path = root / "assets/style.css"
    stylesheet_text = stylesheet_path.read_text(encoding="utf-8") if stylesheet_path.is_file() else ""
    for selector in (".guide-page-main .guide-index", ".guide-page-main .guide-body",
                     ".guide-page-main .guide-section", ".guide-page-main .guide-section h2",
                     ".guide-page-main .guide-section h3", ".guide-page-main .guide-toc",
                     ".guide-page-main .guide-toc a", ".actions", ".btn,.btn-secondary"):
        require(selector in stylesheet_text, f"shared stylesheet is missing required guide selector: {selector}")
    require(any(node.tag == "link" and node.attrs.get("rel") == "stylesheet" and urljoin(canonical, node.attrs.get("href", "")) == BASE + "assets/style.css" for node in nodes), "shared stylesheet missing")
    require(any(node.tag == "script" and urljoin(canonical, node.attrs.get("src", "")) == BASE + "assets/script.js" for node in nodes), "shared script missing")

    cover_url = BASE + f"assets/img/cerchi/{cover.name}"
    for key, expected in {"og:type": "article", "og:title": None, "og:description": None, "og:image": cover_url}.items():
        node = one("meta", "property", key)
        require(bool(node and (node.attrs.get("content") == expected if expected else normalized(node.attrs.get("content", "")))), f"invalid {key}")
        if key == "og:title" and node and titles:
            require(node.attrs.get("content") == normalized(content(titles[0])), "og:title must match meta title")
        if key == "og:description" and node and description:
            require(node.attrs.get("content") == description.attrs.get("content"), "og:description must match meta description")
    for key, expected in {"twitter:card": "summary_large_image", "twitter:title": None, "twitter:description": None, "twitter:image": cover_url}.items():
        node = one("meta", "name", key)
        require(bool(node and (node.attrs.get("content") == expected if expected else normalized(node.attrs.get("content", "")))), f"invalid {key}")
        if key == "twitter:title" and node and titles:
            require(node.attrs.get("content") == normalized(content(titles[0])), "twitter:title must match meta title")
        if key == "twitter:description" and node and description:
            require(node.attrs.get("content") == description.attrs.get("content"), "twitter:description must match meta description")

    mains = [node for node in nodes if node.tag == "main"]
    require(len(mains) == 1, "expected one main element")
    if len(mains) != 1:
        return errors
    main = mains[0]
    main_nodes = list(walk(main))
    require({"page", "guide-page-main"}.issubset(set(main.attrs.get("class", "").split())), "main needs .page and .guide-page-main")
    heroes = list(main.find(css_class="hero"))
    require(len(heroes) == 1, "expected one compact hero")
    require(len(list(main.find(css_class="guide-hero"))) == 1, "hero needs .guide-hero")
    h1s = [node for node in main_nodes if node.tag == "h1"]
    require(len(h1s) == 1 and bool(normalized(content(h1s[0])) if h1s else ""), "expected one nonempty H1")
    number = None
    if len(heroes) == 1:
        eyebrow = list(heroes[0].find(css_class="eyebrow"))
        match = re.fullmatch(r"Guida (\d+) · Cerchi d’inchiostro", normalized(content(eyebrow[0]))) if len(eyebrow) == 1 else None
        require(bool(match), "hero eyebrow must be 'Guida NN · Cerchi d’inchiostro'")
        number = int(match.group(1)) if match else None
        if number is not None:
            for published in (root / "cerchi/guide").glob("*/index.html"):
                if published.resolve() == page:
                    continue
                published_number = re.search(r"Guida\s+(\d+)\s*·\s*Cerchi d.inchiostro", published.read_text(encoding="utf-8"))
                if published_number and int(published_number.group(1)) == number:
                    errors.append(f"guide number already published: {number}")
                    break
        leads = [node for node in heroes[0].find("p") if node not in eyebrow and not list(node.find("a"))]
        require(len(leads) == 1 and 1 <= len(normalized(content(leads[0]))) <= 100, "hero needs one short lead (about 90 characters)")
        require(bool(leads and "lead" in leads[0].attrs.get("class", "").split()), "hero lead needs .lead")
        actions = [node for node in heroes[0].find(css_class="actions")]
        require(len(actions) == 1, "hero CTA wrapper needs .actions")
        hero_links = list(heroes[0].find("a"))
        require(len([link for link in hero_links if "btn" in link.attrs.get("class", "").split()]) == 1
                and len([link for link in hero_links if "btn-secondary" in link.attrs.get("class", "").split()]) == 1,
                "hero CTAs need .btn and .btn-secondary")
        require(len(hero_links) == 2 and normalized(content(hero_links[0])) == "Hub Cerchi d’inchiostro" and urljoin(canonical, hero_links[0].attrs.get("href", "")) == BASE + "cerchi/", "hero needs the Hub CTA and one secondary CTA")
        if len(hero_links) == 2:
            second_url = urljoin(canonical, hero_links[1].attrs.get("href", ""))
            require(second_url == BASE + "cerchi/triadi/" or second_url.startswith(BASE + "cerchi/guide/"), "secondary hero CTA must point to Triadi or an existing guide")

    name_match = COVER_NAME.fullmatch(cover.name)
    require(bool(name_match and number is not None and int(name_match.group(1)) == number), "cover filename must use the standard guide number and 1600x900 WebP naming")
    try:
        require(webp_size(cover) == (1600, 900), "cover must be a genuine 1600x900 WebP")
    except ValueError as error:
        errors.append(str(error))
    images = [node for node in main_nodes if node.tag == "img"]
    require(bool(images), "visible cover image missing")
    if images:
        image = images[0]
        require(urljoin(canonical, image.attrs.get("src", "")) == cover_url, "visible cover does not match supplied WebP")
        require(len(normalized(image.attrs.get("alt", ""))) >= 20, "cover needs descriptive alt text")
        require(image.attrs.get("width") == "1600" and image.attrs.get("height") == "900", "cover HTML dimensions must be 1600x900")

    schemas = {}
    for script in [node for node in nodes if node.tag == "script" and node.attrs.get("type") == "application/ld+json"]:
        try:
            value = json.loads(content(script))
            schema_type = value.get("@type")
            require(isinstance(schema_type, str) and schema_type not in schemas, "duplicate or missing JSON-LD @type")
            if isinstance(schema_type, str):
                schemas[schema_type] = value
        except (json.JSONDecodeError, AttributeError) as error:
            errors.append(f"invalid JSON-LD: {error}")
    article = schemas.get("Article", {})
    breadcrumb = schemas.get("BreadcrumbList", {})
    require(bool(article and article.get("url") == canonical and article.get("mainEntityOfPage") == canonical and normalized(article.get("headline", ""))), "Article JSON-LD missing or inconsistent")
    html_languages = [node.attrs.get("lang", "") for node in nodes if node.tag == "html"]
    html_language = html_languages[0] if len(html_languages) == 1 else ""
    schema_language = article.get("inLanguage", "") if isinstance(article, dict) else ""
    require(bool(re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?", html_language)), "html element needs a valid lang attribute")
    require(bool(article.get("@context") == "https://schema.org" and normalized(article.get("description", ""))
                 and schema_language.split("-")[0].lower() == html_language.split("-")[0].lower()),
            "Article JSON-LD needs context, description and an inLanguage matching the document language")
    alternates = [node for node in nodes if node.tag == "link" and node.attrs.get("rel") == "alternate" and node.attrs.get("hreflang")]
    alternate_by_lang = {node.attrs.get("hreflang"): node.attrs.get("href") for node in alternates}
    document_language = html_language.split("-")[0].lower()
    if document_language in {"it", "en"}:
        require(alternate_by_lang.get(document_language) == canonical,
                f"{document_language} hreflang must self-reference the guide canonical")
    for alternate in alternates:
        hreflang = alternate.attrs.get("hreflang", "").lower()
        alternate_url = alternate.attrs.get("href", "")
        if hreflang == "x-default":
            require(alternate_url == canonical, "x-default must point to the approved self-canonical guide")
            continue
        parsed_alternate = urlsplit(alternate_url)
        require(parsed_alternate.netloc == "alessandro-gentili.it", f"hreflang target must use the canonical site: {alternate_url}")
        if parsed_alternate.netloc == "alessandro-gentili.it":
            alternate_path = unquote(parsed_alternate.path)
            alternate_file = page if alternate_url.rstrip("/") == canonical.rstrip("/") else root / alternate_path.lstrip("/")
            if alternate_path.endswith("/"):
                alternate_file = alternate_file / "index.html" if alternate_file != page else page
            require(alternate_file.is_file(), f"hreflang target does not exist locally: {alternate_url}")
            if alternate_file.is_file() and alternate_file != page:
                alternate_tree = Tree(alternate_file.read_text(encoding="utf-8"))
                alternate_nodes = list(walk(alternate_tree.root))
                canonical_values = [n.attrs.get("href") for n in alternate_nodes if n.tag == "link" and n.attrs.get("rel") == "canonical"]
                target_langs = [n.attrs.get("lang", "").split("-")[0].lower() for n in alternate_nodes if n.tag == "html"]
                require(len(canonical_values) == 1 and canonical_values[0] == alternate_url,
                        f"hreflang target must self-canonicalize: {alternate_url}")
                require(len(target_langs) == 1 and target_langs[0] == hreflang.split("-")[0],
                        f"hreflang target language does not match {hreflang}: {alternate_url}")
                returned_alternates = {n.attrs.get("hreflang"): n.attrs.get("href") for n in alternate_nodes
                                       if n.tag == "link" and n.attrs.get("rel") == "alternate" and n.attrs.get("hreflang")}
                require(returned_alternates.get(document_language) == canonical,
                        f"hreflang relation is not reciprocal: {alternate_url}")
    require(bool(isinstance(article.get("author"), dict) and article["author"].get("name") == "Alessandro Gentili"), "Article JSON-LD author must be Alessandro Gentili")
    require(bool(isinstance(article.get("publisher"), dict) and normalized(article["publisher"].get("name", ""))), "Article JSON-LD publisher missing")
    article_image = article.get("image") if isinstance(article, dict) else None
    image_url = article_image.get("url") if isinstance(article_image, dict) else article_image
    require(image_url == cover_url, "Article JSON-LD image must match the cover")
    if isinstance(article_image, dict):
        require(article_image.get("width") == 1600 and article_image.get("height") == 900, "Article JSON-LD image dimensions must be 1600x900")
    crumbs = breadcrumb.get("itemListElement", []) if isinstance(breadcrumb, dict) else []
    require(isinstance(crumbs, list) and len(crumbs) >= 3 and isinstance(crumbs[-1], dict) and crumbs[-1].get("item") == canonical, "BreadcrumbList JSON-LD missing or inconsistent")
    if isinstance(crumbs, list) and len(crumbs) >= 3 and all(isinstance(item, dict) for item in crumbs):
        require([item.get("position") for item in crumbs] == list(range(1, len(crumbs) + 1)) and crumbs[0].get("item") == BASE and crumbs[1].get("item") == BASE + "cerchi/", "BreadcrumbList positions and parent URLs are inconsistent")

    bodies = [node for node in main_nodes if "guide-body" in node.attrs.get("class", "").split()]
    indexes = [node for node in main_nodes if "guide-index" in node.attrs.get("class", "").split()]
    require(bool(bodies), "guide body needs .guide-body")
    require(len(indexes) == 1, "guide needs exactly one .guide-index")
    require(len(indexes) == 1 and indexes[0].tag == "article", ".guide-index must use the established article card wrapper")
    sections = [node for node in main_nodes if node.tag == "article" and "guide-section" in node.attrs.get("class", "").split()]
    require(len(sections) >= 5, "guide needs opening, body and three final sections")
    require(bool(sections) and all(any(section in list(walk(body)) for body in bodies) for section in sections), "all .guide-section blocks must be inside .guide-body")
    headings = []
    for section in sections:
        h2 = list(section.find("h2"))
        require(bool(section.attrs.get("id") and len(h2) == 1), "each guide section needs an ID and one H2")
        heading = normalized(content(h2[0])) if h2 else ""
        require(not re.match(r"\d+[.)]\s", heading), f"numbered body H2: {heading}")
        headings.append(heading)
    require(final_headings_valid(headings), "final sections must be Fonti → Prosegui la lettura → Chiusura editoriale")
    if len(sections) >= 3:
        progress_links = list(sections[-2].find("a"))
        require(any(urljoin(canonical, link.attrs.get("href", "")) == BASE + "cerchi/" for link in progress_links), "Prosegui la lettura needs the Cerchi hub link")
        require(not any("lettera-periodica" in link.attrs.get("href", "") for link in progress_links), "newsletter link belongs outside Prosegui la lettura")

    tocs = list(main.find("nav", "guide-toc"))
    require(len(tocs) == 1, "expected one .guide-toc")
    if len(tocs) == 1:
        toc = tocs[0]
        require(toc.attrs.get("aria-label", "").startswith("Indice della guida "), "TOC needs author-specific aria-label")
        require(any(normalized(content(h)) == "Indice della guida" for h in toc.find("h2")), "TOC needs visible title 'Indice della guida'")
        require(not any(normalized(content(h)) == "Indice" for h in main.find("h2")), "remove separate 'Indice' heading")
        toc_links = list(toc.find("a"))
        targets = [link.attrs.get("href", "")[1:] for link in toc_links if link.attrs.get("href", "").startswith("#")]
        require(len(targets) == len(toc_links) and len(targets) == len(set(targets)), "TOC links must be unique local anchors")
        section_by_id = {section.attrs.get("id"): heading for section, heading in zip(sections, headings)}
        for link in toc_links:
            target = link.attrs.get("href", "").removeprefix("#")
            label = re.sub(r"^\d+[.)]\s*", "", normalized(content(link)))
            require(target in section_by_id and toc_label_matches(label, section_by_id.get(target, "")), f"TOC label/section mismatch: #{target}")
        require(targets == [section.attrs.get("id") for section in sections[1:]], "TOC targets must follow every body section in order after the editorial opening")
        require(len(indexes) == 1 and toc in list(walk(indexes[0])), ".guide-toc must be inside .guide-index")
        if heroes and images and sections:
            require(main_nodes.index(heroes[0]) < main_nodes.index(images[0]) < main_nodes.index(toc) < main_nodes.index(sections[0]), "required order: hero → cover → TOC → editorial opening")

    faq_headings = {heading for heading in headings if toc_key(heading) in {toc_key("FAQ"), toc_key("Domande frequenti")}}
    faq_visible = bool(faq_headings)
    require(faq_visible == ("FAQPage" in schemas), "FAQPage JSON-LD is required exactly when visible FAQ exists")
    if faq_visible and "FAQPage" in schemas:
        faq_section = sections[next(index for index, heading in enumerate(headings) if heading in faq_headings)]
        questions = {normalized(content(h)) for h in faq_section.find("h3")}
        entries = schemas["FAQPage"].get("mainEntity", [])
        schema_questions = {normalized(item.get("name", "")) for item in entries if isinstance(item, dict)} if isinstance(entries, list) else set()
        require(bool(questions) and questions == schema_questions, "FAQPage questions must match visible FAQ H3")
        if isinstance(entries, list):
            visible_faq = normalized(content(faq_section))
            require(all(isinstance(item, dict) and item.get("@type") == "Question" and isinstance(item.get("acceptedAnswer"), dict)
                and item["acceptedAnswer"].get("@type") == "Answer"
                and bool(normalized(item["acceptedAnswer"].get("text", "")))
                and normalized(item["acceptedAnswer"].get("text", "")) in visible_faq for item in entries), "FAQPage needs a visible answer for each question")

    for node in nodes:
        attribute = "href" if node.tag == "a" or (node.tag == "link" and node.attrs.get("rel") == "stylesheet") else "src" if node.tag in {"img", "script", "source"} else None
        if not attribute or not node.attrs.get(attribute):
            continue
        value = node.attrs[attribute]
        if value.lower().split("#", 1)[0].split("?", 1)[0].endswith(".pdf"):
            errors.append(f"unrequested PDF link: {value}")
        if value.startswith(("mailto:", "tel:")):
            continue
        if value.startswith(("javascript:", "data:")):
            errors.append(f"unsupported local reference: {value}")
            continue
        url = urlsplit(urljoin(canonical, value))
        if url.netloc != "alessandro-gentili.it":
            continue
        path = unquote(url.path)
        require(not any(part in {"prototipi", "private", "test", "tests"} for part in Path(path).parts) and not path.endswith("delos-reference.html"), f"nonpublic target is forbidden: {value}")
        if path.startswith("/cerchi/guide/"):
            guide_url = BASE + path.lstrip("/").removesuffix("index.html")
            if not guide_url.endswith("/"):
                guide_url += "/"
        if path in {f"/cerchi/guide/{slug}/", f"/cerchi/guide/{slug}/index.html"}:
            target = page
        elif path == f"/assets/img/cerchi/{cover.name}":
            target = cover
        else:
            target = root / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
        require(target.is_file(), f"missing local target: {value}")
        if path.startswith("/cerchi/guide/") and target.is_file() and guide_url != canonical:
            if mode == "DRAFT" and guide_url not in sitemap_urls:
                report.append(f"LOCAL CANDIDATE LINK: {guide_url} exists locally but is not published")
            elif mode == "PUBLICATION":
                require(guide_url in sitemap_urls or guide_url in release_urls, f"PUBLICATION guide link must be published or included in --release-guide: {value}")
        if url.fragment and target.is_file():
            target_ids = ids if target == page else [item.attrs["id"] for item in walk(Tree(target.read_text(encoding="utf-8")).root) if "id" in item.attrs]
            require(unquote(url.fragment) in target_ids, f"missing local fragment: {value}")

    if mode == "PUBLICATION":
        index_paths = [root / "cerchi/index.html"]
        triads_referenced = any(urljoin(canonical, node.attrs.get("href", "")) == BASE + "cerchi/triadi/"
                                for node in main_nodes if node.tag == "a")
        if triads_referenced:
            index_paths.append(root / "cerchi/triadi/index.html")
        for index_path in index_paths:
            if not index_path.is_file():
                errors.append(f"PUBLICATION index page missing: {index_path.relative_to(root)}")
                continue
            index_tree = Tree(index_path.read_text(encoding="utf-8"))
            index_links = [node.attrs.get("href", "") for node in walk(index_tree.root) if node.tag == "a"]
            index_urls = {urljoin(BASE + str(index_path.relative_to(root)), link) for link in index_links}
            require(canonical in index_urls, f"PUBLICATION candidate must be linked from {index_path.relative_to(root)}")
        for italian, english, it_url, en_url in (
            (root / "cerchi/index.html", root / "en/cerchi/index.html", BASE + "cerchi/", BASE + "en/cerchi/"),
            (root / "cerchi/triadi/index.html", root / "en/cerchi/triads/index.html", BASE + "cerchi/triadi/", BASE + "en/cerchi/triads/"),
        ):
            for path in (italian, english):
                require(path.is_file(), f"PUBLICATION language overview missing: {path.relative_to(root)}")
            if not italian.is_file() or not english.is_file():
                continue
            pages = [(italian, it_url, "it"), (english, en_url, "en")]
            for path, expected_url, lang in pages:
                page_tree = Tree(path.read_text(encoding="utf-8"))
                page_nodes = list(walk(page_tree.root))
                canonical_values = [n.attrs.get("href") for n in page_nodes if n.tag == "link" and n.attrs.get("rel") == "canonical"]
                require(canonical_values == [expected_url], f"{path.relative_to(root)} canonical must be {expected_url}")
                language = next((n.attrs.get("lang", "").split("-")[0].lower() for n in page_nodes if n.tag == "html"), "")
                require(language == lang, f"{path.relative_to(root)} html lang must be {lang}")
                alternates = {n.attrs.get("hreflang"): n.attrs.get("href") for n in page_nodes if n.tag == "link" and n.attrs.get("rel") == "alternate" and n.attrs.get("hreflang")}
                require(alternates.get("it") == it_url and alternates.get("en") == en_url, f"{path.relative_to(root)} IT/EN hreflang pair is inconsistent")

    try:
        structure = manuscript_structure(source)
        if structure is None:
            legacy_lines = [re.sub(r"^\s*#{1,6}\s+", "", line) for line in source.read_text(encoding="utf-8").splitlines()]
            source_blocks = manuscript_blocks(legacy_lines)
            require(bool(source_blocks), "definitive source is empty")
            body_text = normalized(" ".join(visible_text(section) for section in sections))
            cursor = 0
            for index, block in enumerate(source_blocks, 1):
                found = body_text.find(block, cursor)
                if found < 0:
                    errors.append(f"source block {index} missing or altered in guide body: {block[:72]}")
                else:
                    cursor = found + len(block)
        else:
            title, subtitle, intro, index, source_sections = structure
            require(len(h1s) == 1 and normalized(content(h1s[0])) == title, "manuscript H1 differs from guide H1")
            require(len(sections) == len(source_sections) + 1, "manuscript section count differs from guide body")
            if sections:
                opening = normalized(visible_text(sections[0]))
                cursor = opening.find(subtitle)
                require(cursor >= 0, "original manuscript subtitle missing from editorial opening")
                cursor = max(0, cursor + len(subtitle))
                for block_number, block in enumerate(intro, 1):
                    found = opening.find(block, cursor)
                    if found < 0:
                        errors.append(f"introduction block {block_number} missing, altered or out of order: {block[:72]}")
                    else:
                        cursor = found + len(block)
            if len(tocs) == 1:
                labels = [re.sub(r"^\d+[.)]\s*", "", normalized(content(link))) for link in tocs[0].find("a")]
                require(len(labels) == len(index) and all(toc_key(actual) == toc_key(expected) for actual, expected in zip(labels, index)),
                        "TOC labels differ from the manuscript index or are out of order")
            require(len(index) == len(source_sections), "manuscript index does not cover every source section")
            for position, (expected, subheadings, blocks) in enumerate(source_sections, 1):
                if position >= len(sections):
                    break
                section = sections[position]
                actual = headings[position]
                require(editorial_text_key(actual) == editorial_text_key(expected), f"manuscript H2 {position} missing, altered or out of order: {expected}")
                actual_subheadings = [normalized(content(h)) for h in section.find("h3")]
                require(actual_subheadings == subheadings, f"manuscript H3/FAQ list differs in section {position}: {expected}")
                section_text = normalized(visible_text(section))
                cursor = 0
                for block_number, block in enumerate(blocks, 1):
                    found = section_text.find(block, cursor)
                    if found < 0:
                        errors.append(f"source block {position}.{block_number} missing, altered or out of order: {block[:72]}")
                    else:
                        cursor = found + len(block)
            for position, (label, (heading, _, _)) in enumerate(zip(index, source_sections), 1):
                require(toc_label_matches(label, heading), f"manuscript index item {position} does not match its source H2: {label}")
    except (UnicodeError, ValueError) as error:
        errors.append(f"source cannot be fully checked: {error}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path, help="new cerchi/guide/<slug>/index.html, including temporary candidates")
    parser.add_argument("--cover", type=Path, required=True, help="supplied WebP cover; may be in a temporary directory")
    parser.add_argument("--source", type=Path, required=True, help="definitive UTF-8 manuscript; full H1/subtitle/index structure is checked when present")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="repository root for existing local links")
    parser.add_argument("--mode", choices=sorted(MODES), default="DRAFT", help="DRAFT validates a local unpublished candidate; PUBLICATION applies sitemap and index release gates")
    parser.add_argument("--release-guide", action="append", default=[], help="additional existing guide URL included in the same authorized publication release; repeat as needed")
    args = parser.parse_args()
    report = []
    errors = validate(args.page.resolve(), args.cover.resolve(), args.source.resolve(), args.root.resolve(), args.mode, args.release_guide, report)
    for line in dict.fromkeys(report):
        print(line)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed: {args.page} (source blocks, cover, metadata, visual structure and links checked)")
    print("REVIEW REQUIRED: normalized source checks cannot prove identical emphasis, semantic markup or editorial equivalence; compare the rendered guide with the definitive manuscript.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
