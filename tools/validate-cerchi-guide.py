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
    return f" {value} " if node.tag in {"br", "p", "li", "h1", "h2", "h3", "h4", "blockquote"} else value


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
        clean = [re.sub(r"^\s*(?:#{3,6}\s+|>\s*|[-*+]\s+|\d+[.)]\s+)", "", line.strip())
                 for line in block.splitlines() if line.strip() != "---"]
        value = markdown_plain(" ".join(clean))
        if value:
            blocks.append(value)
    return blocks


def manuscript_structure(source):
    """Parse the supported H1, opening, numbered index and H2/H3 guide layout."""
    lines = source.read_text(encoding="utf-8").splitlines()
    if any(re.match(r"^\s*(?:```|~~~|\||<(?!!--)|#{4,6}\s)", line) for line in lines):
        raise ValueError("unsupported Markdown structure; human review is required")
    nonblank = [index for index, line in enumerate(lines) if line.strip()]
    if not nonblank or not re.fullmatch(r"# (?!#).+", lines[nonblank[0]]):
        return None
    first = nonblank[0]
    title = markdown_plain(lines[first][2:])
    subtitle_at = next((i for i in range(first + 1, len(lines)) if lines[i].strip()), None)
    if subtitle_at is None or not re.fullmatch(r"## (?!#).+", lines[subtitle_at]):
        raise ValueError("full manuscript needs an H2 subtitle after its H1")
    subtitle = markdown_plain(lines[subtitle_at][3:])
    index_at = next((i for i in range(subtitle_at + 1, len(lines)) if lines[i].strip() == "## Indice"), None)
    if index_at is None:
        raise ValueError("full manuscript needs a ## Indice after the introduction")
    intro = manuscript_blocks(lines[subtitle_at + 1:index_at])
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
        body_lines = lines[start + 1:end]
        subheadings = [markdown_plain(line[4:]) for line in body_lines if re.match(r"^### (?!#)", line)]
        sections.append((heading, subheadings, manuscript_blocks(body_lines)))
    return title, subtitle, intro, index, sections


def toc_label_matches(label, heading):
    return label == heading or (heading.startswith(label + " — ") and bool(heading[len(label) + 3:].strip()))


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


def validate(page, cover, source, root):
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    slug = page.parent.name
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
    require(canonical not in sitemap_text, "candidate canonical already appears in the public sitemap")

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
    require(not any(node.tag == "meta" and node.attrs.get("name") == "robots" and "noindex" in node.attrs.get("content", "").lower() for node in nodes), "public guide must not have noindex")
    require(any(node.tag == "header" and "site-header" in node.attrs.get("class", "").split() for node in nodes), "shared site header missing")
    require(any(node.tag == "footer" for node in nodes), "shared site footer missing")
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
    heroes = list(main.find(css_class="hero"))
    require(len(heroes) == 1, "expected one compact hero")
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
        hero_links = list(heroes[0].find("a"))
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
    require(bool(article.get("@context") == "https://schema.org" and normalized(article.get("description", "")) and article.get("inLanguage") in {"it", "it-IT"}), "Article JSON-LD needs context, description and Italian language")
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

    sections = [node for node in main_nodes if node.tag == "article" and "guide-section" in node.attrs.get("class", "").split()]
    require(len(sections) >= 5, "guide needs opening, body and three final sections")
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
        if heroes and images and sections:
            require(main_nodes.index(heroes[0]) < main_nodes.index(images[0]) < main_nodes.index(toc) < main_nodes.index(sections[0]), "required order: hero → cover → TOC → editorial opening")

    faq_visible = "FAQ" in headings
    require(faq_visible == ("FAQPage" in schemas), "FAQPage JSON-LD is required exactly when visible FAQ exists")
    if faq_visible and "FAQPage" in schemas:
        faq_section = sections[headings.index("FAQ")]
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
        if path.startswith("/cerchi/guide/") and path not in {f"/cerchi/guide/{slug}/", f"/cerchi/guide/{slug}/index.html"}:
            guide_url = BASE + path.lstrip("/").removesuffix("index.html")
            require(guide_url in sitemap_text, f"guide link is not published in sitemap: {value}")
        if path in {f"/cerchi/guide/{slug}/", f"/cerchi/guide/{slug}/index.html"}:
            target = page
        elif path == f"/assets/img/cerchi/{cover.name}":
            target = cover
        else:
            target = root / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
        require(target.is_file(), f"missing local target: {value}")
        if url.fragment and target.is_file():
            target_ids = ids if target == page else [item.attrs["id"] for item in walk(Tree(target.read_text(encoding="utf-8")).root) if "id" in item.attrs]
            require(unquote(url.fragment) in target_ids, f"missing local fragment: {value}")

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
                require(labels == index, "TOC labels differ from the manuscript index or are out of order")
            require(len(index) == len(source_sections), "manuscript index does not cover every source section")
            for position, (expected, subheadings, blocks) in enumerate(source_sections, 1):
                if position >= len(sections):
                    break
                section = sections[position]
                actual = headings[position]
                require(actual == expected, f"manuscript H2 {position} missing, altered or out of order: {expected}")
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
    args = parser.parse_args()
    errors = validate(args.page.resolve(), args.cover.resolve(), args.source.resolve(), args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Technical checks passed: {args.page} (source blocks, cover, metadata, structure and links checked)")
    print("REVIEW REQUIRED: normalized text checks cannot prove identical Markdown emphasis, markup semantics or editorial equivalence; compare the rendered page with the definitive manuscript.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
