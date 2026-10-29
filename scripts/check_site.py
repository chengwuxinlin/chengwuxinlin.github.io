#!/usr/bin/env python3
"""Dependency-free structural checks for the static site; not a browser/HTML validator."""

from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".local", "__pycache__"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


@dataclass
class Element:
    tag: str
    attrs: dict
    parent: object = None
    children: list = field(default_factory=list)
    text: str = ""

    def descendants(self, tag=None):
        return [item for child in self.children for item in [child, *child.descendants()]
                if tag is None or item.tag == tag]

    def content(self):
        return (self.text + " ".join(child.content() for child in self.children)).strip()


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.root = Element("document", {})
        self.stack = [self.root]
        self.feed(path.read_text(encoding="utf-8-sig"))
        self.close()
        self.elements = self.root.descendants()
        self.ids = [element.attrs["id"] for element in self.elements if "id" in element.attrs]

    def handle_starttag(self, tag, attrs):
        element = Element(tag, dict(attrs), parent=self.stack[-1])
        self.stack[-1].children.append(element)
        if tag not in VOID:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].text += data

    def find(self, tag):
        return [element for element in self.elements if element.tag == tag]


def public_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not EXCLUDED.intersection(path.relative_to(ROOT).parts):
            yield path


def local_target(reference, origin):
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None, ""
    value = unquote(parsed.path)
    target = (ROOT / value.lstrip("/")) if value.startswith("/") else origin.parent / value
    if not value:
        target = origin
    target = target.resolve()
    require(target.is_relative_to(ROOT), f"{origin.name}: reference escapes site root: {reference}")
    if target.is_dir():
        target /= "index.html"
    return target, unquote(parsed.fragment)


def check_reference(reference, origin, documents):
    if not reference or reference.startswith("data:"):
        return
    require(not reference.lower().startswith("javascript:"), f"{origin.name}: javascript URL is not allowed")
    target, fragment = local_target(reference, origin)
    if target is None:
        return
    require(target.is_file(), f"{origin.name}: missing local resource: {reference}")
    if fragment and target in documents:
        require(fragment in documents[target].ids, f"{origin.name}: missing anchor: {reference}")


def check_document(document, documents):
    label = document.path.relative_to(ROOT).as_posix()
    for value, count in Counter(document.ids).items():
        require(count == 1, f"{label}: duplicate ID: {value}")
    html = document.find("html")
    require(len(html) == 1 and bool(html[0].attrs.get("lang")), f"{label}: needs one html element with lang")
    require(len(document.find("main")) == 1, f"{label}: needs one main landmark")
    require(len(document.find("h1")) == 1, f"{label}: needs one h1")
    title = document.find("title")
    require(len(title) == 1 and bool(title[0].content()), f"{label}: missing title")
    require(any(e.attrs.get("name") == "description" and e.attrs.get("content") for e in document.find("meta")), f"{label}: missing description")
    for element in document.elements:
        for attribute in ("href", "src", "poster"):
            if attribute in element.attrs:
                check_reference(element.attrs[attribute], document.path, documents)
        if element.tag == "a" and element.attrs.get("target") == "_blank":
            require("noopener" in element.attrs.get("rel", "").split(), f"{label}: new-tab link lacks noopener: {element.attrs.get('href')}")
        if element.tag == "img":
            require("alt" in element.attrs, f"{label}: image lacks alt: {element.attrs.get('src')}")
            for dimension in ("width", "height"):
                value = element.attrs.get(dimension, "")
                require(value.isdigit() and int(value) > 0, f"{label}: image lacks positive {dimension}: {element.attrs.get('src')}")
        for attribute in ("aria-labelledby", "aria-describedby", "aria-controls"):
            for target in element.attrs.get(attribute, "").split():
                require(target in document.ids, f"{label}: {attribute} points to absent ID {target}")


def check_static_content(index):
    projects = [e for e in index.find("article") if "data-category" in e.attrs]
    require(len(projects) >= 12, "index.html: selected work must contain the twelve reviewed project articles")
    categories = set()
    for project in projects:
        categories.update(project.attrs["data-category"].split())
        require("hidden" not in project.attrs, f"{project.attrs.get('id')}: project is hidden without JavaScript")
        require(any(e.content() for e in project.descendants("h3")), f"{project.attrs.get('id')}: missing static project title")
        require(any(e.content() for e in project.descendants("p")), f"{project.attrs.get('id')}: missing static project description")
        covers = [e for e in project.descendants("figure") if "project-cover" in e.attrs.get("class", "").split()]
        require(len(covers) == 1, f"{project.attrs.get('id')}: needs one project cover")
        if covers:
            images = covers[0].descendants("img")
            require(len(images) == 1 and bool(images[0].attrs.get("alt", "").strip()), f"{project.attrs.get('id')}: cover needs descriptive alt text")
            require(any(e.content() for e in covers[0].descendants("figcaption")), f"{project.attrs.get('id')}: cover needs a visible source/type caption")
    filters = [e for e in index.find("button") if "data-filter" in e.attrs]
    values = [e.attrs["data-filter"] for e in filters]
    require("all" in values, "index.html: filters need an all-work option")
    require(len(values) == len(set(values)), "index.html: duplicate filter values")
    require(categories == set(values) - {"all"}, "index.html: project categories and filter values differ")
    require(sum(e.attrs.get("aria-pressed") == "true" for e in filters) == 1, "index.html: exactly one filter should initially be pressed")
    require(all(e.attrs.get("aria-pressed") in {"true", "false"} for e in filters), "index.html: filters need aria-pressed")
    publication_lists = [e for e in index.find("ol") if "publication-list" in e.attrs.get("class", "").split()]
    publications = [item for listing in publication_lists for item in listing.children if item.tag == "li"]
    require(len(publications) >= 5, "index.html: selected publications must contain at least five static entries")
    for publication in publications:
        require(any(e.content() for e in publication.descendants("h3")), "index.html: publication is missing a static title")
    return len(projects), len(publications)


def check_css(path, documents):
    """Check delimiter integrity and resource URLs, not full CSS grammar."""
    text = path.read_text(encoding="utf-8-sig")
    token = re.compile(r"/\*.*?\*/|'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", re.S)
    stripped = token.sub("", text)
    stack = []
    pairs = {"}": "{", ")": "(", "]": "["}
    for character in stripped:
        if character in "{([":
            stack.append(character)
        elif character in "})]":
            if not stack or stack.pop() != pairs[character]:
                require(False, f"{path.name}: unbalanced CSS delimiters")
                break
    require(not stack, f"{path.name}: unclosed CSS delimiters")
    for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", text, re.S):
        reference = match.group(2).strip()
        if not reference.startswith("#"):
            check_reference(reference, path, documents)


def main():
    files = list(public_files())
    html_files = [path for path in files if path.suffix.lower() == ".html"]
    documents = {}
    for path in html_files:
        try:
            documents[path.resolve()] = Document(path)
        except (UnicodeError, OSError) as error:
            require(False, f"{path.name}: {error}")
    for document in documents.values():
        check_document(document, documents)
    index = documents.get(ROOT / "index.html")
    require(index is not None, "Missing index.html")
    counts = check_static_content(index) if index else (0, 0)
    for path in files:
        suffix = path.suffix.lower()
        require(suffix not in {".pdf", ".tex", ".doc", ".docx", ".odt", ".rtf"}, f"Do not publish CV/document files: {path.relative_to(ROOT)}")
        if suffix == ".css":
            check_css(path, documents)
        if suffix == ".svg":
            try:
                ET.parse(path)
            except ET.ParseError as error:
                require(False, f"{path.name}: malformed SVG: {error}")
    if errors:
        print("Site checks FAILED:")
        print("\n".join(f"- {message}" for message in errors))
        return 1
    print(f"Site checks passed: {len(documents)} HTML pages, {counts[0]} static projects, {counts[1]} publication entries.")
    print("Local resources, anchors, IDs, metadata, image attributes, filter categories, CSS delimiters, SVG XML, and document exclusion verified.")
    print("Browser layout, interactions, contrast, and external link availability require separate review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
