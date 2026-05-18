#!/usr/bin/env python3
"""
Home Assistant Documentation to PDF Converter
Converts Jekyll/Liquid markdown to clean markdown for PDF generation.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

REPO_URL = "https://github.com/home-assistant/home-assistant.io.git"
CLONE_DIR = "home-assistant.io"
OUTPUT_PDF = "Home-Assistant-Dokumentation.pdf"
COMBINED_MD = "combined_documentation.md"

DOC_DIRS = [
    "source/_docs",
    "source/_includes",
    "source/_actions",
    "source/_conditions",
    "source/_triggers",
    "source/_dashboards",
    "source/_template_functions",
    "source/installation",
    "source/getting-started",
    "source/common-tasks",
    "source/dashboards",
    "source/voice_control",
    "source/faq",
    "source/help",
    "source/cloud",
    "source/android",
    "source/ios",
    "source/apps",
    "source/actions",
    "source/conditions",
    "source/triggers",
    "source/template-functions",
    "source/more-info",
    "source/developers",
    "source/blueprints",
]

EXCLUDE_DIRS = [
    "source/_posts", "source/_integrations", "source/integrations",
    "source/blog", "source/images", "source/assets", "source/javascripts",
    "source/stylesheets", "source/static", "source/.well-known",
    "source/_data", "source/_layouts", "source/audio", "source/blue",
    "source/changelogs", "source/code_of_conduct", "source/community",
    "source/conference", "source/connect", "source/connectzbt1",
    "source/green", "source/home-energy-management", "source/privacy",
    "source/security", "source/socials", "source/state-of-the-open-home",
    "source/tag", "source/tos", "source/video", "source/voice-pe", "source/yellow",
]

def clone_or_update_repo():
    if os.path.exists(CLONE_DIR):
        print("Repository exists, updating...")
        subprocess.run(["git", "-C", CLONE_DIR, "pull", "--quiet"], check=True)
    else:
        print("Cloning repository...")
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, CLONE_DIR], check=True)

def find_doc_files():
    doc_files = []
    repo_path = Path(CLONE_DIR)
    for doc_dir in DOC_DIRS:
        dir_path = repo_path / doc_dir
        if dir_path.exists():
            for ext in ["*.md", "*.markdown"]:
                doc_files.extend(dir_path.rglob(ext))
    doc_files = sorted(set(doc_files))
    filtered = []
    for f in doc_files:
        if not any(str(f).startswith(str(repo_path / excl)) for excl in EXCLUDE_DIRS):
            filtered.append(f)
    print(f"Found {len(filtered)} documentation files")
    return filtered

def strip_front_matter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content

def get_display_title(md_file, repo_path):
    rel_path = md_file.relative_to(repo_path / "source")
    title = str(rel_path)
    title = re.sub(r'\.(md|markdown)$', '', title)
    title = title.replace('_', ' ').replace('-', ' ')
    title = title.title()
    return title

class LiquidProcessor:
    """Process Jekyll Liquid tags in Home Assistant documentation."""

    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)

    def process_file(self, content, source_file=None, code_blocks=None):
        """Process all Liquid tags in content."""
        if code_blocks is None:
            code_blocks = []

        # Convert example blocks to code blocks first
        content = self._convert_example_blocks(content, code_blocks)
        # Then protect all code blocks (including newly converted ones)
        content = self._protect_code_blocks(content, code_blocks)
        content = self._process_includes(content, source_file, code_blocks)
        content = self._process_configuration_blocks(content)
        content = self._process_configuration_basic_blocks(content)
        content = self._process_details_blocks(content)
        content = self._process_tip_blocks(content)
        content = self._process_note_blocks(content)
        content = self._process_important_blocks(content)
        content = self._process_caution_blocks(content)
        content = self._process_warning_blocks(content)
        content = self._process_labs_blocks(content)
        content = self._process_my_links(content)
        content = self._process_term_tags(content)
        content = self._process_icon_tags(content)
        content = self._process_conditionals(content)
        content = self._process_loops(content)
        content = self._process_assign(content)
        content = self._process_macros(content)
        content = self._process_remaining_liquid(content)
        # Restore all code blocks
        content = self._restore_code_blocks(content, code_blocks)
        return content

    def _protect_code_blocks(self, content, code_blocks):
        """Protect existing code blocks from Liquid processing."""
        def protect_code(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        content = re.sub(r'```[\s\S]*?```', protect_code, content)
        return content

    def _restore_code_blocks(self, content, code_blocks):
        """Restore protected code blocks."""
        def restore_code(match):
            idx = int(match.group(1))
            return code_blocks[idx]

        content = re.sub(r'__CODE_BLOCK_(\d+)__', restore_code, content)
        return content

    def _convert_example_blocks(self, content, code_blocks):
        """Convert {% example %}...{% endexample %} blocks directly to code blocks."""
        def convert_example(match):
            block_content = match.group(1).strip()
            lines = block_content.split('\n')

            keywords = ['automation:', 'action:', 'condition:', 'template:',
                       'trigger:', 'script:', 'output:']
            lang = 'yaml'
            header = ''

            for kw in keywords:
                if lines[0].strip().startswith(kw):
                    lang = 'yaml' if kw != 'output:' else 'text'
                    header = f"**{kw.rstrip(':')}**\n\n"
                    break

            code_block = f"{header}\n```{lang}\n{block_content}\n```"
            code_blocks.append(code_block)
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        content = re.sub(r'\{%\s*example\s*%\}(.*?)\{%\s*endexample\s*%\}',
                        convert_example, content, flags=re.DOTALL)
        return content

    def _process_includes(self, content, source_file=None, code_blocks=None):
        """Process {% include file.md %} tags by including the file content."""
        def replace_include(match):
            include_path = match.group(1).strip()
            full_path = self.repo_path / "source" / "_includes" / include_path

            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        included_content = f.read()
                    # Recursively process the included content, passing the same code_blocks list
                    return self.process_file(included_content, full_path, code_blocks)
                except Exception:
                    return f"[Include error: {include_path}]"
            else:
                return f"[Include not found: {include_path}]"

        content = re.sub(r'\{%\s*include\s+([^%]+)%\}', replace_include, content)
        return content

    def _process_details_blocks(self, content):
        """Process {% details "Title" %}...{% enddetails %} blocks."""
        def replace_details(match):
            title = match.group(1).strip().strip('"').strip("'")
            body = match.group(2).strip()
            return f"\n<details>\n<summary>{title}</summary>\n\n{body}\n\n</details>\n"

        content = re.sub(r'\{%\s*details\s+"([^"]+)"\s*%\}(.*?)\{%\s*enddetails\s*%\}',
                        replace_details, content, flags=re.DOTALL)
        return content

    def _process_tip_blocks(self, content):
        """Process {% tip %}...{% endtip %} blocks."""
        def replace_tip(match):
            body = match.group(1).strip()
            return f"\n> **💡 Tip:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*tip\s*%\}(.*?)\{%\s*endtip\s*%\}',
                        replace_tip, content, flags=re.DOTALL)
        return content

    def _process_note_blocks(self, content):
        """Process {% note %}...{% endnote %} blocks."""
        def replace_note(match):
            body = match.group(1).strip()
            return f"\n> **📝 Note:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*note\s*%\}(.*?)\{%\s*endnote\s*%\}',
                        replace_note, content, flags=re.DOTALL)
        return content

    def _process_important_blocks(self, content):
        """Process {% important %}...{% endimportant %} blocks."""
        def replace_important(match):
            body = match.group(1).strip()
            return f"\n> **⚠️ Important:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*important\s*%\}(.*?)\{%\s*endimportant\s*%\}',
                        replace_important, content, flags=re.DOTALL)
        return content

    def _process_caution_blocks(self, content):
        """Process {% caution %}...{% endcaution %} blocks."""
        def replace_caution(match):
            body = match.group(1).strip()
            return f"\n> **🔶 Caution:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*caution\s*%\}(.*?)\{%\s*endcaution\s*%\}',
                        replace_caution, content, flags=re.DOTALL)
        return content

    def _process_warning_blocks(self, content):
        """Process {% warning %}...{% endwarning %} blocks."""
        def replace_warning(match):
            body = match.group(1).strip()
            return f"\n> **🚨 Warning:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*warning\s*%\}(.*?)\{%\s*endwarning\s*%\}',
                        replace_warning, content, flags=re.DOTALL)
        return content

    def _process_labs_blocks(self, content):
        """Process {% labs %}...{% endlabs %} blocks."""
        def replace_labs(match):
            body = match.group(1).strip()
            return f"\n> **🧪 Labs:**\n> {body.replace(chr(10), chr(10) + '> ')}\n"

        content = re.sub(r'\{%\s*labs\s*%\}(.*?)\{%\s*endlabs\s*%\}',
                        replace_labs, content, flags=re.DOTALL)
        return content

    def _process_configuration_blocks(self, content):
        """Process {% configuration %}...{% endconfiguration %} blocks into tables."""
        def replace_config(match):
            body = match.group(1).strip()
            lines = body.split('\n')
            rows = []
            current_key = None
            current_data = {}

            for line in lines:
                if not line.strip():
                    continue

                if not line.startswith(' ') and not line.startswith('\t'):
                    if current_key:
                        rows.append(current_data)
                    current_key = line.rstrip(':').strip()
                    current_data = {'key': current_key, 'description': '', 'required': '', 'type': '', 'default': ''}
                else:
                    line = line.strip()
                    if line.startswith('description:'):
                        current_data['description'] = line.split(':', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('required:'):
                        current_data['required'] = line.split(':', 1)[1].strip()
                    elif line.startswith('type:'):
                        current_data['type'] = line.split(':', 1)[1].strip()
                    elif line.startswith('default:'):
                        current_data['default'] = line.split(':', 1)[1].strip()

            if current_key:
                rows.append(current_data)

            if not rows:
                return body

            table = "| Option | Type | Required | Default | Description |\n"
            table += "|--------|------|----------|---------|-------------|\n"

            for row in rows:
                required = "Yes" if row['required'] == 'true' else "No"
                table += f"| `{row['key']}` | {row['type']} | {required} | {row['default']} | {row['description']} |\n"

            return f"\n{table}\n"

        content = re.sub(r'\{%\s*configuration\s*%\}(.*?)\{%\s*endconfiguration\s*%\}',
                        replace_config, content, flags=re.DOTALL)
        return content

    def _process_configuration_basic_blocks(self, content):
        """Process {% configuration_basic %}...{% endconfiguration_basic %} blocks."""
        def replace_config_basic(match):
            body = match.group(1).strip()
            lines = body.split('\n')
            rows = []
            current_key = None
            current_desc = ''

            for line in lines:
                if not line.strip():
                    continue

                if not line.startswith(' ') and not line.startswith('\t'):
                    if current_key:
                        rows.append((current_key, current_desc))
                    current_key = line.rstrip(':').strip()
                    current_desc = ''
                else:
                    if line.strip().startswith('description:'):
                        current_desc = line.strip().split(':', 1)[1].strip().strip('"').strip("'")

            if current_key:
                rows.append((current_key, current_desc))

            if not rows:
                return body

            table = "| Option | Description |\n"
            table += "|--------|-------------|\n"

            for key, desc in rows:
                table += f"| `{key}` | {desc} |\n"

            return f"\n{table}\n"

        content = re.sub(r'\{%\s*configuration_basic\s*%\}(.*?)\{%\s*endconfiguration_basic\s*%\}',
                        replace_config_basic, content, flags=re.DOTALL)
        return content

    def _process_my_links(self, content):
        """Process {% my integrations title="..." %} tags."""
        def replace_my(match):
            args = match.group(1).strip()
            title_match = re.search(r'title="([^"]+)"', args)
            title = title_match.group(1) if title_match else args.split()[0]
            return title

        content = re.sub(r'\{%\s*my\s+([^%]+)%\}', replace_my, content)
        return content

    def _process_term_tags(self, content):
        """Process {% term xyz %} tags."""
        def replace_term(match):
            args = match.group(1).strip().strip('"').strip("'")
            return args

        content = re.sub(r'\{%\s*term\s+([^%]+)%\}', replace_term, content)
        return content

    def _process_icon_tags(self, content):
        """Process {% icon "mdi:xyz" %} tags."""
        def replace_icon(match):
            icon_name = match.group(1).strip().strip('"').strip("'")
            return f"`{icon_name}`"

        content = re.sub(r'\{%\s*icon\s+"([^"]+)"\s*%\}', replace_icon, content)
        return content

    def _process_conditionals(self, content):
        """Remove {% if %}...{% endif %} blocks (can't evaluate without context)."""
        content = re.sub(r'\{%\s*if\s+[^%]*%\}\s*(.*?)\{%\s*endif\s*%\}',
                        r'\1', content, flags=re.DOTALL)
        content = re.sub(r'\{%\s*else\s*%\}', '', content)
        content = re.sub(r'\{%\s*elsif\s+[^%]*%\}', '', content)
        return content

    def _process_loops(self, content):
        """Remove {% for %}...{% endfor %} blocks."""
        content = re.sub(r'\{%\s*for\s+[^%]*%\}.*?\{%\s*endfor\s*%\}',
                        '', content, flags=re.DOTALL)
        return content

    def _process_assign(self, content):
        """Remove {% assign %} tags."""
        content = re.sub(r'\{%\s*assign\s+[^%]*%\}', '', content)
        return content

    def _process_macros(self, content):
        """Remove {% macro %}...{% endmacro %} and {% from %}...{% do %} blocks."""
        content = re.sub(r'\{%\s*macro\s+[^%]*%\}.*?\{%\s*endmacro\s*%\}',
                        '', content, flags=re.DOTALL)
        content = re.sub(r'\{%\s*from\s+[^%]*%\}', '', content)
        content = re.sub(r'\{%\s*do\s+[^%]*%\}', '', content)
        content = re.sub(r'\{%\s*set\s+[^%]*%\}', '', content)
        return content

    def _process_remaining_liquid(self, content):
        """Remove any remaining Liquid tags."""
        # Remove known Liquid structural tags
        liquid_keywords = ['if', 'for', 'assign', 'capture', 'case', 'cycle', 'decrement',
                          'increment', 'tablerow', 'unless', 'comment', 'raw', 'include',
                          'extends', 'block', 'endblock', 'super', 'call', 'import', 'from',
                          'do', 'set', 'macro', 'filter', 'with', 'autoescape']
        for kw in liquid_keywords:
            content = re.sub(r'\{%\s*' + kw + r'[^%]*%\}', '', content)
        # Remove variable outputs that look like complete expressions
        content = re.sub(r'\{\{\s*\w+[^}]*\}\}', '', content)
        return content

def create_combined_markdown(doc_files):
    print("\nCombining documentation files...")
    repo_path = Path(CLONE_DIR)
    processor = LiquidProcessor(repo_path)

    with open(COMBINED_MD, 'w', encoding='utf-8') as out:
        out.write("""# Home Assistant Dokumentation

**Vollständige Dokumentation**

Quelle: https://www.home-assistant.io/docs/

Lizenz: CC BY-NC-SA 3.0

---

""")
        out.write("## Inhaltsverzeichnis\n\n")
        for i, md_file in enumerate(doc_files, 1):
            title = get_display_title(md_file, repo_path)
            out.write(f"{i}. {title}\n")
        out.write("\n---\n\n")

        for i, md_file in enumerate(doc_files):
            if (i + 1) % 100 == 0:
                print(f"  Processing file {i + 1}/{len(doc_files)}...")
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = strip_front_matter(content)
                if not content.strip():
                    continue
                content = processor.process_file(content, md_file)
                if not content.strip():
                    continue
                title = get_display_title(md_file, repo_path)
                out.write(f"\n\n---\n\n## {title}\n\n")
                out.write(content)
                out.write("\n\n")
            except Exception as e:
                print(f"  Warning: {md_file}: {e}")

    file_size = os.path.getsize(COMBINED_MD) / (1024 * 1024)
    print(f"Combined markdown file: {file_size:.1f} MB")

def convert_to_pdf():
    print("\nConverting to PDF...")
    print("This may take several minutes...")

    with open(COMBINED_MD, 'r', encoding='utf-8') as f:
        md_content = f.read()

    print("Converting markdown to HTML...")
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'md_in_html']
    )

    css = CSS(string="""
        @page {
            size: A4;
            margin: 2cm 2.5cm;
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #417690;
            }
        }
        @page :first {
            @bottom-center { content: ""; }
        }
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #333;
        }
        h1 {
            color: #417690;
            font-size: 24pt;
            border-bottom: 3px solid #417690;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h2 {
            color: #417690;
            font-size: 16pt;
            border-bottom: 1px solid #417690;
            padding-bottom: 5px;
            margin-top: 25px;
            page-break-before: always;
        }
        h3 {
            color: #417690;
            font-size: 13pt;
            margin-top: 20px;
            page-break-after: avoid;
        }
        h4, h5, h6 {
            color: #417690;
            margin-top: 15px;
            page-break-after: avoid;
        }
        p { margin: 8px 0; text-align: justify; }
        code {
            background: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #c7254e;
        }
        pre {
            background: #f5f5f5;
            padding: 12px;
            border-radius: 5px;
            overflow: auto;
            font-size: 8.5pt;
            line-height: 1.3;
            page-break-inside: avoid;
        }
        pre code { background: none; padding: 0; color: #333; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 12px 0;
            page-break-inside: avoid;
            font-size: 9pt;
        }
        th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
        th { background: #417690; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        blockquote {
            border-left: 4px solid #417690;
            margin: 12px 0;
            padding: 10px 16px;
            background: #f5f9fc;
            color: #555;
        }
        ul, ol { margin: 8px 0; padding-left: 25px; }
        li { margin: 4px 0; }
        a { color: #417690; text-decoration: none; }
        hr { border: none; border-top: 2px solid #417690; margin: 20px 0; }
        details {
            margin: 12px 0;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 5px;
        }
        summary {
            color: #417690;
            font-weight: bold;
            cursor: pointer;
        }
    """)

    html_doc = HTML(string=f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body>{html_body}</body></html>""")

    html_doc.write_pdf(OUTPUT_PDF, stylesheets=[css])
    print(f"PDF created: {OUTPUT_PDF}")

def main():
    print("=" * 60)
    print("Home Assistant Documentation to PDF Converter")
    print("=" * 60)

    print("\n[1/4] Getting repository...")
    clone_or_update_repo()

    print("\n[2/4] Finding documentation files...")
    doc_files = find_doc_files()
    if not doc_files:
        print("No documentation files found!")
        sys.exit(1)

    print("\n[3/4] Processing files...")
    create_combined_markdown(doc_files)

    print("\n[4/4] Generating PDF...")
    convert_to_pdf()

    if os.path.exists(OUTPUT_PDF):
        pdf_size = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"SUCCESS!")
        print(f"File: {os.path.abspath(OUTPUT_PDF)}")
        print(f"Size: {pdf_size:.1f} MB")
        print(f"Sections: {len(doc_files)}")
        print(f"{'=' * 60}")
    else:
        print("\nFailed to create PDF!")
        sys.exit(1)

if __name__ == "__main__":
    main()
