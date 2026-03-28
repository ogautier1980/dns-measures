#!/usr/bin/env python3
"""
Markdown → LaTeX conversion for the DNS thesis chapters.
Reads chapter*.md files and writes chapters/*.tex.
"""

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Citation map: (exact-string-to-replace, replacement)
# Processed in order so longest/most-specific patterns come first.
# ---------------------------------------------------------------------------
CITATION_REPLACEMENTS = [
    # Multi-citation parentheticals
    ('(van Rijswijk-Deij et al., 2016; van Rijswijk-Deij, 2018)',
     r'\cite{vanRijswijk2016,vanRijswijk2018blog}'),
    ('(Bajpai et al., 2017; Nosyk et al., 2024)',
     r'\cite{Bajpai2017,Nosyk2024}'),
    ('(Bortzmeyer, 2013; Finnegan, 2018)',
     r'\cite{Bortzmeyer2013,Finnegan2018}'),
    # RFC 1034 and RFC 1035
    ('RFC 1034 and RFC 1035 (Mockapetris, 1987)',
     r'\cite{RFC1034,RFC1035}'),
    ('(RFC 1034 and RFC 1035, Mockapetris, 1987)',
     r'\cite{RFC1034,RFC1035}'),
    ('RFC 1034 (Mockapetris, 1987)',
     r'RFC~1034~\cite{RFC1034}'),
    ('(RFC 1034, Mockapetris, 1987)',
     r'\cite{RFC1034}'),
    ('RFC 1035 (Mockapetris, 1987)',
     r'RFC~1035~\cite{RFC1035}'),
    ('(RFC 1035, Mockapetris, 1987)',
     r'\cite{RFC1035}'),
    # RFC 7871 compound forms (specific → general)
    ('RFC 7871 (Contavalli et al., 2016)',
     r'RFC~7871~\cite{RFC7871}'),
    # Narrative forms: Author (year) → Author~\cite{key}
    ('van Rijswijk-Deij et al. (2016)',
     r'van Rijswijk-Deij et al.~\cite{vanRijswijk2016}'),
    ('van Rijswijk-Deij (2018)',
     r'van Rijswijk-Deij~\cite{vanRijswijk2018blog}'),
    ('Le Pochat et al. (2019)',
     r'Le Pochat et al.~\cite{LePochat2019}'),
    ('Nosyk et al. (2024)',
     r'Nosyk et al.~\cite{Nosyk2024}'),
    ('Bortzmeyer (n.d., tutorial)',
     r'Bortzmeyer~\cite{Bortzmeyer_tutorial}'),
    ("Bortzmeyer's tutorial (n.d.)",
     r"Bortzmeyer's tutorial~\cite{Bortzmeyer_tutorial}"),
    ('Bortzmeyer (n.d.)',
     r'Bortzmeyer~\cite{Bortzmeyer_tutorial}'),
    ('Bortzmeyer (2013)',
     r'Bortzmeyer~\cite{Bortzmeyer2013}'),
    ('Holterbach et al. (2015)',
     r'Holterbach et al.~\cite{Holterbach2015}'),
    ('Bajpai et al. (2017)',
     r'Bajpai et al.~\cite{Bajpai2017}'),
    ('Boswell and Perkins (2024)',
     r'Boswell and Perkins~\cite{Boswell2024}'),
    ('Jones et al. (2016)',
     r'Jones et al.~\cite{Jones2016}'),
    ('Calder et al. (2015)',
     r'Calder et al.~\cite{Calder2015}'),
    ('Koch et al. (2021)',
     r'Koch et al.~\cite{Koch2021}'),
    ('Hours et al. (2016)',
     r'Hours et al.~\cite{Hours2016}'),
    ('Wang et al. (2018)',
     r'Wang et al.~\cite{Wang2018}'),
    ('Contavalli et al. (2016)',
     r'Contavalli et al.~\cite{RFC7871}'),
    ('Finnegan (2018)',
     r'Finnegan~\cite{Finnegan2018}'),
    ('Kisteleki et al. (2016)',
     r'Kisteleki et al.~\cite{Kisteleki2016}'),
    ('van der Toorn et al. (2018)',
     r'van der Toorn et al.~\cite{vanderToorn2018}'),
    ('Xu et al. (2023)',
     r'Xu et al.~\cite{Xu2023}'),
    ('Cicalese et al. (2015)',
     r'Cicalese et al.~\cite{Cicalese2015}'),
    ('Li and Huang (2025)',
     r'Li and Huang~\cite{Li2025}'),
    ('Li & Huang (2025)',
     r'Li and Huang~\cite{Li2025}'),
    ('Edgio (2017)',
     r'Edgio~\cite{Edgio2017}'),
    # Parenthetical forms: (Author, year) → \cite{key}
    ('(van Rijswijk-Deij et al., 2016)',  r'\cite{vanRijswijk2016}'),
    ('(van Rijswijk-Deij, 2018)',         r'\cite{vanRijswijk2018blog}'),
    ('(Le Pochat et al., 2019)',          r'\cite{LePochat2019}'),
    ('(Nosyk et al., 2024)',              r'\cite{Nosyk2024}'),
    ('(Holterbach et al., 2015)',         r'\cite{Holterbach2015}'),
    ('(Bajpai et al., 2017)',             r'\cite{Bajpai2017}'),
    ('(Boswell and Perkins, 2024)',       r'\cite{Boswell2024}'),
    ('(Jones et al., 2016)',              r'\cite{Jones2016}'),
    ('(Calder et al., 2015)',             r'\cite{Calder2015}'),
    ('(Koch et al., 2021)',               r'\cite{Koch2021}'),
    ('(Hours et al., 2016)',              r'\cite{Hours2016}'),
    ('(Wang et al., 2018)',               r'\cite{Wang2018}'),
    ('(RFC 7871, 2016)',                  r'\cite{RFC7871}'),
    ('(Contavalli et al., 2016)',         r'\cite{RFC7871}'),
    ('(Finnegan, 2018)',                  r'\cite{Finnegan2018}'),
    ('(Bortzmeyer, 2013)',                r'\cite{Bortzmeyer2013}'),
    ('(Kisteleki et al., 2016)',          r'\cite{Kisteleki2016}'),
    ('(van der Toorn et al., 2018)',      r'\cite{vanderToorn2018}'),
    ('(Xu et al., 2023)',                 r'\cite{Xu2023}'),
    ('(Cicalese et al., 2015)',           r'\cite{Cicalese2015}'),
    ('(Li and Huang, 2025)',              r'\cite{Li2025}'),
    ('(Edgio, 2017)',                     r'\cite{Edgio2017}'),
    # Standalone RFC 7871 (fallback after compound forms handled above)
    ('RFC 7871',                          r'RFC~7871~\cite{RFC7871}'),
]


# ---------------------------------------------------------------------------
# Unicode substitution table
# ---------------------------------------------------------------------------
UNICODE_MAP = {
    '\u2014': '---',              # em-dash
    '\u2013': '--',               # en-dash
    '\u2212': '-',                # minus sign (U+2212)
    '\u2018': '`',                # left single quotation
    '\u2019': "'",                # right single quotation
    '\u201c': "``",               # left double quotation
    '\u201d': "''",               # right double quotation
    '\u2026': r'\ldots{}',        # ellipsis
    '\u00a0': '~',                # non-breaking space
    '\u2248': r'$\approx$',       # ≈ approximately equal
    '\u2260': r'$\neq$',          # ≠ not equal
    '\u2265': r'$\geq$',          # ≥
    '\u2264': r'$\leq$',          # ≤
    '\u00d7': r'$\times$',        # × multiplication sign
    '\u00b1': r'$\pm$',           # ±
    '\u221e': r'$\infty$',        # ∞
    '\u221a': r'$\sqrt{}$',       # √
    '\u00b2': r'$^{2}$',          # ²
    '\u00b3': r'$^{3}$',          # ³
    # Bullets / checkmarks
    '\u2022': r'\textbullet{}',   # •
    '\u25e6': 'o',                # ◦
    '\u25aa': '-',                # ▪
    '\u2713': '[OK]', '\u2717': '[X]',
    '\u2714': '[OK]', '\u2718': '[X]',
    '\u2705': '[OK]', '\u274c': '[X]',
    '\u26a0': '[!]',              # ⚠
    # Box-drawing characters
    '\u2500': '-', '\u2502': '|', '\u250c': '+', '\u2510': '+',
    '\u2514': '+', '\u2518': '+', '\u251c': '+', '\u2524': '+',
    '\u252c': '+', '\u2534': '+', '\u253c': '+',
    '\u2550': '=', '\u2551': '|', '\u2554': '+', '\u2557': '+',
    '\u255a': '+', '\u255d': '+', '\u2560': '+', '\u2563': '+',
    '\u2566': '+', '\u2569': '+', '\u256c': '+',
    # Arrows
    '\u2192': r'$\rightarrow$',
    '\u2190': r'$\leftarrow$',
    '\u2194': r'$\leftrightarrow$',
    '\u21d2': r'$\Rightarrow$',
    '\u21d0': r'$\Leftarrow$',
    '\u21d4': r'$\Leftrightarrow$',
    # Greek letters used in statistics (in math mode)
    '\u03c1': r'$\rho$',
    '\u03b1': r'$\alpha$', '\u03b2': r'$\beta$',
    '\u03b3': r'$\gamma$', '\u03b4': r'$\delta$',
    '\u03b5': r'$\epsilon$', '\u03bb': r'$\lambda$',
    '\u03c3': r'$\sigma$', '\u03c4': r'$\tau$',
    # Greek capitals
    '\u0394': r'$\Delta$', '\u03a3': r'$\Sigma$',
    '\u03a0': r'$\Pi$',    '\u0393': r'$\Gamma$',
    '\u0398': r'$\Theta$', '\u03a9': r'$\Omega$',
    # Unicode variation selectors (remove silently)
    '\ufe0f': '', '\ufe0e': '',
}


# ---------------------------------------------------------------------------
# Regex for protected-zone placeholders (used in escape loop)
# ---------------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(
    r'(___(?:P\d+_[A-Z]+|TABLEBLOCK_\d+|CODEBLOCK_\d+)___)'
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def escape_text(text: str) -> str:
    """Escape LaTeX special characters in plain text."""
    text = text.replace('\\', r'\textbackslash{}')
    text = text.replace('%',  r'\%')
    text = text.replace('$',  r'\$')
    text = text.replace('&',  r'\&')
    text = text.replace('#',  r'\#')
    text = text.replace('_',  r'\_')
    text = text.replace('{',  r'\{')
    text = text.replace('}',  r'\}')
    text = text.replace('~',  r'\textasciitilde{}')
    text = text.replace('^',  r'\textasciicircum{}')
    return text


def escape_inner(text: str) -> str:
    """Escape special chars inside bold/italic content.
    Like escape_text but skips placeholders."""
    parts = PLACEHOLDER_RE.split(text)
    result = []
    for p in parts:
        if PLACEHOLDER_RE.match(p):
            result.append(p)
        else:
            result.append(escape_text(p))
    return ''.join(result)


def escape_cell(text: str) -> str:
    """Escape a table cell.

    Order of operations ensures no content is escaped twice:
    1. Protect inline code, math, bold, italic (each escaped/preserved once).
    2. Escape remaining plain-text characters.
    3. Restore protected content.
    """
    protected: dict[str, str] = {}
    pid = [0]

    # Use null-byte prefix+suffix as placeholder delimiters (safe in LaTeX strings)
    def protect(content: str) -> str:
        key = f'\x00C{pid[0]}\x00'
        protected[key] = content
        pid[0] += 1
        return key

    # Inline code: escape the code content properly NOW
    text = re.sub(r'`([^`\n]+)`',
                  lambda m: protect(r'\texttt{' + escape_text(m.group(1)) + '}'),
                  text)
    # Math $...$
    text = re.sub(r'\$[^$\n]+\$', lambda m: protect(m.group(0)), text)
    # Bold — escape inner content before protecting
    text = re.sub(r'\*\*([^\n*]+?)\*\*',
                  lambda m: protect(r'\textbf{' + escape_text(m.group(1)) + '}'), text)
    # Italic — escape inner content before protecting
    text = re.sub(r'\*([^\n*]+?)\*',
                  lambda m: protect(r'\textit{' + escape_text(m.group(1)) + '}'), text)

    # Escape plain-text special characters
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    text = text.replace('&', r'\&')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('^', r'\textasciicircum{}')
    text = text.replace('~', r'\textasciitilde{}')

    # Restore all protected content
    for key, val in protected.items():
        text = text.replace(key, val)

    return text.strip()


# ---------------------------------------------------------------------------
# Phase 1 – Protect code blocks
# ---------------------------------------------------------------------------

def protect_code_blocks(text: str):
    blocks = []

    def replace_block(m):
        lang = (m.group(1) or '').strip()
        code = m.group(2)
        # Basic unicode cleanup inside code blocks
        for char, repl in {'\u2192': '->', '\u2190': '<-',
                           '\u2500': '-', '\u2502': '|'}.items():
            code = code.replace(char, repl)
        idx = len(blocks)
        blocks.append((lang, code))
        return f'\n___CODEBLOCK_{idx}___\n'

    text = re.sub(r'```(\w*)\n(.*?)```', replace_block, text, flags=re.DOTALL)
    return text, blocks


def restore_code_blocks(text: str, blocks) -> str:
    for i, (lang, code) in enumerate(blocks):
        if lang in ('python', 'json', 'bash'):
            latex = f'\\begin{{lstlisting}}[style={lang}]\n{code}\n\\end{{lstlisting}}'
        elif lang == '':
            latex = f'\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}'
        else:
            latex = f'\\begin{{lstlisting}}[language={lang}]\n{code}\n\\end{{lstlisting}}'
        text = text.replace(f'___CODEBLOCK_{i}___', latex)
    return text


# ---------------------------------------------------------------------------
# Phase 2 – Extract and convert Markdown tables
# ---------------------------------------------------------------------------

def extract_tables(text: str):
    tables = []
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*\|', line):
            table_lines = [line]
            i += 1
            while i < len(lines) and re.match(r'^\s*\|', lines[i]):
                table_lines.append(lines[i])
                i += 1
            if len(table_lines) >= 3:
                idx = len(tables)
                tables.append(convert_table(table_lines))
                result.append(f'___TABLEBLOCK_{idx}___')
            else:
                result.extend(table_lines)
        else:
            result.append(line)
            i += 1
    return '\n'.join(result), tables


def convert_table(lines) -> str:
    header_raw = [c.strip() for c in lines[0].split('|')]
    header_raw = [c for c in header_raw if c]   # drop empty from borders
    n = len(header_raw)
    if n == 0:
        return '\n'.join(lines)

    data_rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|')]
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        if cells:
            while len(cells) < n:
                cells.append('')
            data_rows.append(cells[:n])

    col_spec = ' '.join(['l'] * n)
    tex = [
        '\\begin{table}[H]',
        '\\centering',
        '\\small',
        f'\\begin{{tabular}}{{{col_spec}}}',
        '\\toprule',
        ' & '.join(f'\\textbf{{{escape_cell(h)}}}' for h in header_raw) + ' \\\\',
        '\\midrule',
    ]
    for row in data_rows:
        tex.append(' & '.join(escape_cell(c) for c in row) + ' \\\\')
    tex += ['\\bottomrule', '\\end{tabular}', '\\end{table}']
    return '\n'.join(tex)


def restore_tables(text: str, tables) -> str:
    for i, tbl in enumerate(tables):
        text = text.replace(f'___TABLEBLOCK_{i}___', tbl)
    return text


# ---------------------------------------------------------------------------
# Phase 3 – Citation replacement
# ---------------------------------------------------------------------------

def replace_citations(text: str) -> str:
    for old, new in CITATION_REPLACEMENTS:
        text = text.replace(old, new)
    return text


# ---------------------------------------------------------------------------
# Phase 4 – Unicode normalisation
# ---------------------------------------------------------------------------

def normalise_unicode(text: str) -> str:
    for char, repl in UNICODE_MAP.items():
        text = text.replace(char, repl)
    return text


# ---------------------------------------------------------------------------
# Phase 5 – Heading conversion
# ---------------------------------------------------------------------------

def convert_headings(text: str) -> str:
    # H1: "# Chapter N - Title" or "# Chapter N — Title"
    text = re.sub(
        r'^#\s+Chapter\s+\d+\s+[-\u2014]\s+(.+)$',
        r'\\chapter{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+(.+)$', r'\\chapter{\1}', text, flags=re.MULTILINE)

    # H2 with section number
    def h2_label(m):
        return f'\\section{{{m.group(2)}}}\n\\label{{sec:{m.group(1)}}}'
    text = re.sub(r'^##\s+(\d+\.\d+)\s+(.+)$', h2_label, text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', r'\\section{\1}', text, flags=re.MULTILINE)

    # H3 with subsection number
    def h3_label(m):
        return f'\\subsection{{{m.group(2)}}}\n\\label{{subsec:{m.group(1)}}}'
    text = re.sub(r'^###\s+(\d+\.\d+\.\d+)\s+(.+)$', h3_label, text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+(.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)

    # H4
    text = re.sub(r'^####\s+(.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    return text


# ---------------------------------------------------------------------------
# Phases 6-9 – Protect inline markup, escape plain text, restore
# ---------------------------------------------------------------------------

def protect_and_escape(text: str) -> str:
    store = {}
    counter = [0]

    def save(tag, content):
        key = f'___P{counter[0]}_{tag}___'
        store[key] = content
        counter[0] += 1
        return key

    # -- 0. Protect display math $$...$$ FIRST (before $...$) --
    def protect_display_math(m):
        inner = m.group(1).strip()
        return save('DMATH', f'\\[\n{inner}\n\\]')
    text = re.sub(r'\$\$(.+?)\$\$', protect_display_math, text, flags=re.DOTALL)

    # -- 1. Protect ~\cite{...} as a unit (non-breaking space before citation) --
    def protect_tilde_cite(m):
        return save('CMD', f'~\\cite{{{m.group(1)}}}')
    text = re.sub(r'~\\cite\{([^}]*)\}', protect_tilde_cite, text)

    # -- 2. Protect existing LaTeX commands with braces: \cmd{...} --
    def protect_cmd(m):
        return save('CMD', m.group(0))
    text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', protect_cmd, text)
    # Also protect bare \cite{} patterns from citations step
    text = re.sub(r'\\cite\{[^}]+\}', protect_cmd, text)
    # Protect ~\ref and similar that might remain
    text = re.sub(r'~\\[a-zA-Z]+\{[^}]*\}', protect_cmd, text)

    # -- 3. Protect URLs --
    def protect_url(m):
        url = m.group(0)
        return save('URL', f'\\url{{{url}}}')
    text = re.sub(r'https?://[^\s\)\]]+', protect_url, text)

    # -- 4. Protect inline math $...$ (single dollar) --
    def protect_math(m):
        return save('MATH', m.group(0))
    text = re.sub(r'\$[^$\n]+\$', protect_math, text)

    # -- 5. Protect bold **...** (escape inner content) --
    def protect_bold(m):
        inner = escape_inner(m.group(1))
        return save('B', f'\\textbf{{{inner}}}')
    text = re.sub(r'\*\*([^\n*]+?)\*\*', protect_bold, text)

    # -- 6. Protect italic *...* (escape inner content) --
    def protect_italic(m):
        inner = escape_inner(m.group(1))
        return save('I', f'\\textit{{{inner}}}')
    text = re.sub(r'\*([^\n*]+?)\*', protect_italic, text)

    # -- 7. Protect inline code `...` --
    def protect_code(m):
        # Fully escape all LaTeX special chars inside \texttt{...}
        content = escape_text(m.group(1))
        return save('TT', f'\\texttt{{{content}}}')
    text = re.sub(r'`([^`\n]+)`', protect_code, text)

    # -- 8. Escape plain text (line by line, respecting protected zones) --
    LATEX_CMD_STARTS = (
        '\\chapter', '\\section', '\\subsection', '\\subsubsection',
        '\\label', '\\begin', '\\end', '\\item',
        '\\toprule', '\\midrule', '\\bottomrule',
        '\\medskip', '\\bigskip', '\\hrule', '\\noindent',
        '\\[', '\\]',
    )
    lines = text.split('\n')
    escaped = []
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(cmd) for cmd in LATEX_CMD_STARTS):
            escaped.append(line)
            continue
        # Split on protected zones (including TABLEBLOCK, CODEBLOCK placeholders)
        parts = PLACEHOLDER_RE.split(line)
        out = []
        for part in parts:
            if PLACEHOLDER_RE.match(part):
                out.append(part)
            else:
                out.append(escape_text(part))
        escaped.append(''.join(out))
    text = '\n'.join(escaped)

    # -- 9. Restore all protected content --
    for key in sorted(store, key=len, reverse=True):
        text = text.replace(key, store[key])

    return text


# ---------------------------------------------------------------------------
# Phase 10 – Block structures: blockquotes, lists, horizontal rules
# ---------------------------------------------------------------------------

def convert_block_structures(text: str) -> str:
    # -- Blockquotes --
    lines = text.split('\n')
    result, in_quote = [], False
    for line in lines:
        if line.startswith('> '):
            if not in_quote:
                result.append('\\begin{quote}')
                in_quote = True
            result.append(line[2:])
        else:
            if in_quote:
                result.append('\\end{quote}')
                in_quote = False
            result.append(line)
    if in_quote:
        result.append('\\end{quote}')
    text = '\n'.join(result)

    # -- Bullet lists (- item) --
    lines = text.split('\n')
    result, in_blist = [], False
    for line in lines:
        stripped = line.strip()
        if re.match(r'^-\s+\S', stripped):
            if not in_blist:
                result.append('\\begin{itemize}')
                in_blist = True
            result.append('  \\item ' + re.sub(r'^-\s+', '', stripped))
        else:
            if in_blist:
                result.append('\\end{itemize}')
                in_blist = False
            result.append(line)
    if in_blist:
        result.append('\\end{itemize}')
    text = '\n'.join(result)

    # -- Numbered lists (1. item) --
    lines = text.split('\n')
    result, in_nlist = [], False
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+\.\s+\S', stripped):
            if not in_nlist:
                result.append('\\begin{enumerate}')
                in_nlist = True
            result.append('  \\item ' + re.sub(r'^\d+\.\s+', '', stripped))
        else:
            if in_nlist:
                result.append('\\end{enumerate}')
                in_nlist = False
            result.append(line)
    if in_nlist:
        result.append('\\end{enumerate}')
    text = '\n'.join(result)

    # -- Horizontal rules → vertical space --
    text = re.sub(r'^\s*---+\s*$', r'\\bigskip', text, flags=re.MULTILINE)

    return text


# ---------------------------------------------------------------------------
# Master conversion
# ---------------------------------------------------------------------------

def convert_markdown_to_latex(md: str) -> str:
    # Drop reference/bibliography section (handled by .bib)
    md = re.sub(
        r'^## (Bibliography|References|Références bibliographiques).*$', '',
        md, flags=re.DOTALL | re.MULTILINE)

    md, code_blocks  = protect_code_blocks(md)
    # Unescape Markdown backslash-escapes (\_ \* etc.) so they don't get double-escaped
    md = re.sub(r'\\([_*\[\]()#`!{}])', r'\1', md)
    md               = replace_citations(md)
    md               = normalise_unicode(md)   # before table extraction so cells are clean
    md, tables       = extract_tables(md)
    md               = convert_headings(md)
    md               = protect_and_escape(md)
    md               = convert_block_structures(md)

    # Restore tables and code blocks AFTER block-structure processing
    md = restore_tables(md, tables)
    md = restore_code_blocks(md, code_blocks)

    return md


# ---------------------------------------------------------------------------
# Per-chapter driver
# ---------------------------------------------------------------------------

def convert_chapter(src: Path, dst: Path, num: int):
    print(f'  Chapter {num}: {src.name} → {dst.name}')
    md  = src.read_text(encoding='utf-8')
    tex = convert_markdown_to_latex(md)
    header = (
        f'% Chapter {num} — auto-generated from {src.name}\n'
        f'% Edit the Markdown source, not this file.\n\n'
    )
    dst.write_text(header + tex, encoding='utf-8')
    print(f'    OK')


CHAPTERS = [
    ('md/en/chapter1_introduction.md',     'chapters/01-introduction.tex',  1),
    ('md/en/chapter2_state_of_the_art.md', 'chapters/02-etat-art.tex',      2),
    ('md/en/chapter3_methodology.md',      'chapters/03-methodologie.tex',   3),
    ('md/en/chapter4_results.md',          'chapters/04-resultats.tex',      4),
    ('md/en/chapter5_conclusion.md',       'chapters/05-conclusion.tex',     5),
]


def main():
    latex_dir = Path(__file__).parent
    print('=== Markdown → LaTeX ===\n')
    for md_name, tex_name, num in CHAPTERS:
        src = latex_dir / md_name
        dst = latex_dir / tex_name
        if not src.exists():
            print(f'  [SKIP] {src} not found')
            continue
        convert_chapter(src, dst, num)
    print('\n=== Done ===')


if __name__ == '__main__':
    main()
