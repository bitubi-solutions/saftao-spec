#!/usr/bin/env python3
"""Validador de referência contra o XSD (requer lxml). Usado para gerar e verificar os casos de conformidade.

Uso: python3 tools/validate.py schema/SAFTAO1.01_01.xsd ficheiro.xml
Saída: JSON {"valid": bool, "errors": [{"line": n, "message": "..."}]}
"""
import json
import sys

from lxml import etree


def validate(xsd, xml):
    schema = etree.XMLSchema(etree.parse(xsd))
    try:
        doc = etree.parse(xml)
    except etree.XMLSyntaxError as e:
        return {"valid": False, "errors": [{"line": e.lineno, "message": str(e)}]}
    ok = schema.validate(doc)
    return {"valid": ok, "errors": [{"line": e.line, "message": e.message} for e in schema.error_log]}


if __name__ == "__main__":
    print(json.dumps(validate(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
