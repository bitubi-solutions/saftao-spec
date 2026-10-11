#!/usr/bin/env python3
"""Gera spec/02-fields.md a partir do XSD, para que a referência de campos nunca divirja do esquema.

Uso: python3 -I tools/xsd_to_md.py schema/SAFTAO1.01_01.xsd > spec/02-fields.md
Apenas biblioteca padrão.
"""
import sys
import xml.etree.ElementTree as ET

XS = "{http://www.w3.org/2001/XMLSchema}"


def local(tag):
    return tag.split("}")[1]


class Schema:
    def __init__(self, path):
        self.root = ET.parse(path).getroot()
        self.elements, self.types, self.groups = {}, {}, {}
        for c in self.root:
            name = c.get("name")
            if c.tag == XS + "element":
                self.elements[name] = c
            elif c.tag in (XS + "simpleType", XS + "complexType"):
                self.types[name] = c
            elif c.tag == XS + "group":
                self.groups[name] = c

    @staticmethod
    def strip(q):
        return q.split(":")[-1] if q else q

    def simple_info(self, node):
        """Descrição curta das restrições de um simpleType."""
        r = node.find(XS + "restriction")
        if r is None:
            return ""
        base = self.strip(r.get("base"))
        parts = []
        enums = [e.get("value") for e in r.findall(XS + "enumeration")]
        if enums:
            parts.append("valores: " + ", ".join(f"`{e}`" for e in enums))
        for k in ("pattern", "minLength", "maxLength", "length", "minInclusive", "maxInclusive", "totalDigits", "fractionDigits"):
            for e in r.findall(XS + k):
                v = e.get("value")
                if k == "pattern" and len(v) > 60:
                    v = f"<expressão com {v.count('|') + 1} alternativas, ver o XSD>"
                parts.append(f"{k}={v}")
        ref = self.types.get(base)
        inherited = self.simple_info(ref) if ref is not None and local(ref.tag) == "simpleType" else ""
        shown = base if ref is None else base
        text = f"{shown}" + (f" ({'; '.join(parts)})" if parts else "")
        return text + (f" ⟵ {inherited}" if inherited and not parts else "")

    def type_desc(self, el):
        if el.get("fixed"):
            return f"valor fixo `{el.get('fixed')}`"
        t = el.get("type")
        if t:
            t = self.strip(t)
            n = self.types.get(t)
            if n is not None and local(n.tag) == "simpleType":
                return f"`{t}`: {self.simple_info(n)}"
            return f"`{t}`" if n is None else f"`{t}` (complexo)"
        inline = el.find(XS + "simpleType")
        if inline is not None:
            return self.simple_info(inline)
        return ""

    def children(self, node, seen):
        """Itera os elementos filhos (resolvendo refs, groups e extensões)."""
        out = []
        for c in node:
            tag = local(c.tag)
            if tag in ("sequence", "choice", "all"):
                for el, occ, ch in self.children(c, seen):
                    out.append((el, occ, ch or tag == "choice"))
                if tag == "choice":
                    pass
            elif tag == "element":
                out.append((c, (c.get("minOccurs", "1"), c.get("maxOccurs", "1")), False))
            elif tag == "group":
                g = self.groups.get(self.strip(c.get("ref")))
                if g is not None:
                    out.extend(self.children(g, seen))
            elif tag in ("complexContent", "extension"):
                if tag == "extension":
                    base = self.types.get(self.strip(c.get("base")))
                    if base is not None:
                        out.extend(self.children(base, seen))
                out.extend(self.children(c, seen))
        return out

    def occurs(self, occ):
        lo, hi = occ
        hi = "n" if hi == "unbounded" else hi
        return {"1": "obrigatório", "0": "opcional"}.get(lo, lo) + ("" if hi == "1" else f", até {hi}")

    def walk(self, el, depth, path, lines, occ, choice):
        ref = el.get("ref")
        target = self.elements.get(self.strip(ref)) if ref else el
        name = self.strip(ref) if ref else el.get("name")
        if name in path:
            lines.append(f"{'  ' * depth}- **{name}**: (recursivo)")
            return
        tdesc = self.type_desc(target)
        label = self.occurs(occ) + (", alternativa (choice)" if choice else "")
        lines.append(f"{'  ' * depth}- **{name}** ({label})" + (f": {tdesc}" if tdesc else ""))
        ct = target.find(XS + "complexType")
        if ct is None and target.get("type"):
            t = self.types.get(self.strip(target.get("type")))
            if t is not None and local(t.tag) == "complexType":
                ct = t
        if ct is not None:
            for ch, o, c in self.children(ct, path):
                self.walk(ch, depth + 1, path | {name}, lines, o, c)


def main(xsd):
    s = Schema(xsd)
    print("<!-- Gerado por tools/xsd_to_md.py a partir de schema/SAFTAO1.01_01.xsd. Não editar à mão. -->")
    print("# 02 — Referência de campos\n")
    print("Estrutura completa do ficheiro SAF-T (AO) versão 1.01_01, derivada do XSD. "
          "Cada linha indica o elemento, se é obrigatório ou opcional, quantas ocorrências admite e as restrições do tipo.\n")
    print("Para as notas técnicas de cada campo (regras de preenchimento), ver o Decreto Executivo 317/20 (ver `sources.md`).\n")
    lines = []
    root = s.elements["AuditFile"]
    s.walk(root, 0, frozenset(), lines, ("1", "1"), False)
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
