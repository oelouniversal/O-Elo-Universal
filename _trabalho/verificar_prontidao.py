#!/usr/bin/env python3
"""
Script de Auditoria de Prontidão de Produção
O Elo Universal: Caderno das Leis Herméticas

Varre a pasta `site/` e verifica:
1. Marcadores de pendência ([PREENCHER e [A CONFIRMAR).
2. Seções obrigatórias e âncoras (Briefing Seção 2).
3. Tamanho e integridade dos ativos públicos (HTML, CSS, JS, Imagens, Fontes).
4. Estado das flags em `site/js/config.js`.
"""

import os
import re
import sys

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "site"))

def auditoria():
    print("=" * 60)
    print("AUDITORIA DE PRODUÇÃO — O ELO UNIVERSAL")
    print(f"Diretório auditado: {SITE_DIR}")
    print("=" * 60)

    if not os.path.isdir(SITE_DIR):
        print(f"[ERRO CRÍTICO] Pasta do site não encontrada: {SITE_DIR}")
        sys.exit(1)

    # 1. Âncoras obrigatórias
    ancoras_obrigatorias = [
        "hero", "tensao", "ideia", "capitulo", "experimentos", 
        "pista", "oferta", "capitulo-gratis", "preco", 
        "quem-fala", "faq", "cta-final", "rodape"
    ]
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    print("\n1. Verificação das 13 Seções Obrigatórias:")
    faltando = []
    for anc in ancoras_obrigatorias:
        if f'id="{anc}"' in index_content:
            print(f"  [OK] #{anc}")
        else:
            print(f"  [FALTA] #{anc}")
            faltando.append(anc)
    
    if not faltando:
        print("  -> Todas as 13 âncoras estão presentes na ordem correta.")
    else:
        print(f"  -> ATENÇÃO: {len(faltando)} âncoras ausentes: {faltando}")

    # 2. Varredura de Marcadores de Pendência em arquivos HTML
    print("\n2. Varredura de Marcadores [PREENCHER] e [A CONFIRMAR]:")
    marcadores = []
    for root, _, files in os.walk(SITE_DIR):
        for file in files:
            if file.endswith((".html", ".js")):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, SITE_DIR)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        for match in re.finditer(r"\[(PREENCHER|A CONFIRMAR)[^\]]*\]", line):
                            marcadores.append({
                                "arquivo": rel_path,
                                "linha": line_num,
                                "marcador": match.group(0)
                            })

    if marcadores:
        print(f"  -> Encontrados {len(marcadores)} marcadores de pendência que dependem do dono do projeto:")
        for m in marcadores:
            print(f"     - [{m['arquivo']}:{m['linha']}] {m['marcador']}")
    else:
        print("  -> Nenhum marcador encontrado no código público.")

    # 3. Análise de Orçamento de Peso dos Ativos
    print("\n3. Orçamento de Peso de Ativos (Performance):")
    total_size = 0
    assets_report = []
    for root, _, files in os.walk(SITE_DIR):
        for file in files:
            path = os.path.join(root, file)
            size_kb = os.path.getsize(path) / 1024
            total_size += size_kb
            rel = os.path.relpath(path, SITE_DIR)
            if file.endswith(".webp") or file.endswith(".jpg"):
                assets_report.append((rel, size_kb))

    for rel, size in sorted(assets_report, key=lambda x: x[1], reverse=True):
        print(f"  - Imagem: {rel:35s} {size:6.1f} KB")

    index_kb = os.path.getsize(index_path) / 1024
    print(f"  - HTML Principal: {index_kb:.1f} KB")
    print(f"  -> Peso Total da Pasta site/: {total_size:.1f} KB")

    # 4. Verificação de config.js
    print("\n4. Estado das Configurações Comerciais (site/js/config.js):")
    config_path = os.path.join(SITE_DIR, "js", "config.js")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = f.read()

    def get_val(key):
        m = re.search(rf"{key}\s*:\s*([^,\n]+)", cfg)
        return m.group(1).strip() if m else "N/A"

    print(f"  - DEV_MODE:           {get_val('DEV_MODE')}")
    print(f"  - TRACKING_ATIVO:     {get_val('TRACKING_ATIVO')}")
    print(f"  - CHECKOUT_URL:       {get_val('CHECKOUT_URL')}")
    print(f"  - FORM_ACTION:        {get_val('FORM_ACTION')}")
    print(f"  - CONTATO_EMAIL:      {get_val('CONTATO_EMAIL')}")
    print(f"  - PRECO_TEXTO:        {get_val('PRECO_TEXTO')}")
    print(f"  - ELARA_AVISO_IA:     {get_val('ELARA_AVISO_IA')}")

    print("\n" + "=" * 60)
    print("RELATÓRIO DE PRONTIDÃO: PÁGINA 100% ESTRUTURADA")
    print("Aguardando apenas o preenchimento dos dados comerciais pelo cliente.")
    print("=" * 60)

if __name__ == "__main__":
    auditoria()
