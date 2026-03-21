#!/usr/bin/env python3
"""
Script de conversion Markdown → LaTeX pour le mémoire
Convertit les chapitres .md en fichiers .tex compatibles avec le préambule
"""

import re
import sys
from pathlib import Path


def protect_code_blocks(md_content):
    """Protège les blocs de code en les remplaçant par des placeholders
    ET remplace les caractères Unicode problématiques dans les blocs"""
    code_blocks = []

    # Caractères Unicode à remplacer dans les blocs de code
    unicode_map_code = {
        '─': '-', '│': '|', '┌': '+', '┐': '+', '└': '+', '┘': '+',
        '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
        '═': '=', '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
        '╠': '+', '╣': '+', '╦': '+', '╩': '+', '╬': '+',
        '→': '->', '←': '<-', '↔': '<->', '⇒': '=>', '⇐': '<=', '⇔': '<=>',
    }

    def save_code_block(match):
        block = match.group(0)
        # Remplacer les caractères Unicode dans ce bloc
        for old, new in unicode_map_code.items():
            block = block.replace(old, new)
        code_blocks.append(block)
        return f"\n___CODE_BLOCK_{len(code_blocks)-1}___\n"

    md_content = re.sub(r'```.*?```', save_code_block, md_content, flags=re.DOTALL)
    return md_content, code_blocks


def restore_code_blocks(md_content, code_blocks):
    """Restaure les blocs de code depuis les placeholders"""
    for i, block in enumerate(code_blocks):
        md_content = md_content.replace(f"___CODE_BLOCK_{i}___", block)
    return md_content


def escape_latex_special_chars(text):
    """Échappe les caractères spéciaux LaTeX"""
    # Ordre important : backslash en premier
    replacements = [
        ('\\', '\\textbackslash{}'),
        ('%', '\\%'),
        ('$', '\\$'),
        ('&', '\\&'),
        ('#', '\\#'),
        ('_', '\\_'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('~', '\\textasciitilde{}'),
        ('^', '\\textasciicircum{}'),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text


def convert_table_to_latex(table_lines):
    """Convertit un tableau Markdown en tableau LaTeX"""
    if len(table_lines) < 3:
        return '\n'.join(table_lines)

    # Ligne 1: header
    header_cells = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
    num_cols = len(header_cells)

    # Ligne 2: séparateur (ignorer)
    # Lignes suivantes: données
    data_rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        if cells:
            data_rows.append(cells)

    # Générer LaTeX
    latex = '\\begin{table}[H]\n'
    latex += '\\centering\n'
    latex += '\\begin{tabular}{' + '|'.join(['l'] * num_cols) + '}\n'
    latex += '\\hline\n'

    # En-têtes
    latex += ' & '.join(header_cells) + ' \\\\\n'
    latex += '\\hline\n'

    # Données
    for row in data_rows:
        # Compléter si moins de colonnes
        while len(row) < num_cols:
            row.append('')
        latex += ' & '.join(row[:num_cols]) + ' \\\\\n'

    latex += '\\hline\n'
    latex += '\\end{tabular}\n'
    latex += '\\end{table}\n'

    return latex


def convert_markdown_to_latex(md_content):
    """Convertit le contenu Markdown en LaTeX"""

    # Supprimer la section références (déjà dans bibliography.bib)
    md_content = re.sub(
        r'## Références bibliographiques.*$',
        '',
        md_content,
        flags=re.DOTALL
    )

    # 1. Protéger les blocs de code (ne pas les transformer)
    md_content, code_blocks = protect_code_blocks(md_content)

    # 2. Protéger les tableaux Markdown (mettre en commentaire pour révision manuelle)
    lines = md_content.split('\n')
    result_lines = []
    in_table = False
    table_lines = []

    for i, line in enumerate(lines):
        # Détecter ligne de tableau (contient |)
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        elif in_table:
            # Fin du tableau - mettre en commentaire
            if len(table_lines) >= 2:
                result_lines.append('')
                result_lines.append('% TODO: Convertir ce tableau Markdown en LaTeX')
                for tline in table_lines:
                    result_lines.append('% ' + tline)
                result_lines.append('%')
            else:
                # Pas un vrai tableau
                result_lines.extend(table_lines)
            result_lines.append(line)
            in_table = False
            table_lines = []
        else:
            result_lines.append(line)

    # Si tableau en fin de fichier
    if in_table and len(table_lines) >= 2:
        result_lines.append('% TODO: Convertir ce tableau Markdown en LaTeX')
        for tline in table_lines:
            result_lines.append('% ' + tline)

    md_content = '\n'.join(result_lines)

    # 3. Remplacer les caractères Unicode spéciaux par des versions LaTeX-safe
    unicode_replacements = {
        '─': '-', '│': '|', '┌': '+', '┐': '+', '└': '+', '┘': '+',
        '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
        '═': '=', '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
        '╠': '+', '╣': '+', '╦': '+', '╩': '+', '╬': '+',
        '→': '->', '←': '<-', '↔': '<->', '⇒': '=>', '⇐': '<=', '⇔': '<=>',
        '•': '*', '◦': 'o', '▪': '-', '▫': 'o', '…': '...',
        '≥': '>=', '≤': '<=', '≠': '!=', '≈': '~=',
        '×': 'x', '÷': '/', '±': '+/-', '°': ' deg', 'µ': 'micro',
        '²': '^2', '³': '^3', '√': 'sqrt', '∞': 'inf',
        '✓': '[OK]', '✗': '[X]', '✔': '[OK]', '✘': '[X]',
        '✅': '[OK]', '❌': '[X]', '⚠': '[!]', '⚠️': '[!]',
        'ρ': 'rho', 'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
        'δ': 'delta', 'ε': 'epsilon', 'θ': 'theta', 'λ': 'lambda',
        'σ': 'sigma', 'τ': 'tau', 'φ': 'phi', 'ω': 'omega',
    }

    for unicode_char, replacement in unicode_replacements.items():
        md_content = md_content.replace(unicode_char, replacement)

    # Remove Unicode variation selectors (U+FE0F, U+FE0E, etc.) that cause LaTeX errors
    md_content = md_content.replace('\uFE0F', '').replace('\uFE0E', '')

    # 4. Convertir les titres (AVANT l'échappement LaTeX)
    md_content = re.sub(r'^# (.+)$', r'\\chapter{\1}', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (\d+\.\d+) (.+)$', r'\\section{\2}\n\\label{sec:\1}', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^### (\d+\.\d+\.\d+) (.+)$', r'\\subsection{\2}\n\\label{subsec:\1}', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^#### (.+)$', r'\\subsubsection{\1}', md_content, flags=re.MULTILINE)

    # 5. Convertir URLs (AVANT l'échappement LaTeX)
    md_content = re.sub(r'https?://[^\s\)]+', lambda m: f'___URL___{m.group(0)}___URL___', md_content)

    # 6. Gras et italique (AVANT l'échappement LaTeX)
    # Protéger le contenu entre ** et * (NE PAS matcher les retours à la ligne)
    def protect_bold(match):
        return f'___BOLD___{match.group(1)}___BOLD___'

    def protect_italic(match):
        return f'___ITALIC___{match.group(1)}___ITALIC___'

    # [^\n] pour ne pas matcher les retours à la ligne
    md_content = re.sub(r'\*\*([^\n*]+?)\*\*', protect_bold, md_content)
    md_content = re.sub(r'\*([^\n*]+?)\*', protect_italic, md_content)

    # 7. Code inline (AVANT l'échappement LaTeX)
    def protect_code_inline(match):
        return f'___CODEINLINE___{match.group(1)}___CODEINLINE___'

    md_content = re.sub(r'`([^`]+)`', protect_code_inline, md_content)

    # 8. Protéger les commandes LaTeX déjà présentes
    md_content = re.sub(r'(\\[a-zA-Z]+(?:\{[^}]*\})?)', r'___LATEXCMD___\1___LATEXCMD___', md_content)

    # 9. MAINTENANT échapper les caractères spéciaux LaTeX dans le texte normal
    lines = md_content.split('\n')
    escaped_lines = []

    for line in lines:
        # Ne pas échapper les lignes qui sont des commandes LaTeX
        if line.strip().startswith('\\chapter') or line.strip().startswith('\\section') or \
           line.strip().startswith('\\subsection') or line.strip().startswith('\\subsubsection') or \
           line.strip().startswith('\\label') or line.strip().startswith('\\begin') or \
           line.strip().startswith('\\end') or line.strip().startswith('\\item'):
            escaped_lines.append(line)
        else:
            # Échapper caractères spéciaux sauf dans les zones protégées
            parts = re.split(r'(___[A-Z]+___.*?___[A-Z]+___)', line)
            escaped_parts = []
            for part in parts:
                if part.startswith('___') and part.endswith('___'):
                    # Zone protégée, ne pas échapper
                    escaped_parts.append(part)
                else:
                    # Texte normal, échapper
                    escaped_parts.append(escape_latex_special_chars(part))
            escaped_lines.append(''.join(escaped_parts))

    md_content = '\n'.join(escaped_lines)

    # 10. Restaurer les commandes LaTeX protégées
    md_content = md_content.replace('___LATEXCMD___', '').replace('___LATEXCMD___', '')

    # 11. Restaurer et convertir le gras, italique, code
    def restore_bold(match):
        content = match.group(1)
        # Ensure % is escaped even in bold text
        content = content.replace('%', '\\%')
        return f'\\textbf{{{content}}}'

    def restore_italic(match):
        content = match.group(1)
        # Ensure % is escaped even in italic text
        content = content.replace('%', '\\%')
        return f'\\textit{{{content}}}'

    def restore_code_inline(match):
        content = match.group(1)
        return f'\\texttt{{{content}}}'

    md_content = re.sub(r'___BOLD___(.+?)___BOLD___', restore_bold, md_content)
    md_content = re.sub(r'___ITALIC___(.+?)___ITALIC___', restore_italic, md_content)
    md_content = re.sub(r'___CODEINLINE___(.+?)___CODEINLINE___', restore_code_inline, md_content)

    # 12. Restaurer les URLs
    def restore_url(match):
        url = match.group(1)
        return f'\\url{{{url}}}'

    md_content = re.sub(r'___URL___(.+?)___URL___', restore_url, md_content)

    # 13. Restaurer les blocs de code et les convertir
    def convert_code_block(match):
        lang = match.group(1) or 'text'
        code = match.group(2)
        if lang in ['python', 'json', 'bash']:
            return f'\\begin{{lstlisting}}[style={lang}]\n{code}\n\\end{{lstlisting}}'
        else:
            return f'\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}'

    md_content = restore_code_blocks(md_content, code_blocks)
    md_content = re.sub(r'```(\w+)?\n(.*?)```', convert_code_block, md_content, flags=re.DOTALL)

    # 14. Listes à puces (avec environnement itemize)
    lines = md_content.split('\n')
    result_lines = []
    in_list = False

    for i, line in enumerate(lines):
        if line.strip().startswith('- ') and not in_list:
            result_lines.append('\\begin{itemize}')
            result_lines.append('\\item ' + line.strip()[2:])
            in_list = True
        elif line.strip().startswith('- ') and in_list:
            result_lines.append('\\item ' + line.strip()[2:])
        elif not line.strip().startswith('- ') and in_list:
            result_lines.append('\\end{itemize}')
            result_lines.append(line)
            in_list = False
        else:
            result_lines.append(line)

    if in_list:
        result_lines.append('\\end{itemize}')

    md_content = '\n'.join(result_lines)

    # 15. Citations (références)
    md_content = re.sub(r'\(([A-Z][a-z]+ et al\., \d{4})\)', r'~\\cite{TODO}', md_content)

    # 16. Lignes horizontales
    md_content = re.sub(r'^---+$', r'\\medskip\\hrule\\medskip', md_content, flags=re.MULTILINE)

    return md_content


def convert_chapter(input_md, output_tex, chapter_num):
    """Convertit un chapitre Markdown en LaTeX"""

    print(f"Converting {input_md} → {output_tex}")

    # Lire Markdown
    with open(input_md, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convertir
    tex_content = convert_markdown_to_latex(md_content)

    # Ajouter en-tête
    header = f"% Chapitre {chapter_num} - Généré automatiquement depuis {input_md.name}\n"
    header += f"% Ne pas éditer directement - modifier le fichier Markdown source\n\n"

    tex_content = header + tex_content

    # Écrire LaTeX
    with open(output_tex, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    print(f"  ✓ Conversion réussie")


def main():
    """Point d'entrée principal"""

    latex_dir = Path(__file__).parent

    chapters = [
        ('chapitre1_introduction.md', 'chapters/01-introduction.tex', 1),
        ('chapitre2_etat_art.md', 'chapters/02-etat-art.tex', 2),
        ('chapitre3_methodologie.md', 'chapters/03-methodologie.tex', 3),
        ('chapitre4_resultats.md', 'chapters/04-resultats.tex', 4),
        ('chapitre5_conclusion.md', 'chapters/05-conclusion.tex', 5),
    ]

    print("=== Conversion Markdown → LaTeX ===\n")

    for md_file, tex_file, num in chapters:
        input_path = latex_dir / md_file
        output_path = latex_dir / tex_file

        if not input_path.exists():
            print(f"⚠ Fichier introuvable: {input_path}")
            continue

        convert_chapter(input_path, output_path, num)

    print("\n=== Conversion terminée ===")
    print("\nÉtapes suivantes:")
    print("1. Vérifier les fichiers .tex générés dans chapters/")
    print("2. Ajuster manuellement les tableaux complexes si nécessaire")
    print("3. Ajouter les citations BibTeX (remplacer TODO par clés)")
    print("4. Compiler avec: latexmk -pdf main.tex")


if __name__ == '__main__':
    main()
