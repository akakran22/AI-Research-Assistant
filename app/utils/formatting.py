import re

def process_markdown_to_html(content: str) -> str:
    if not content:
        return ""
    lines = content.split("\n")
    processed_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("### "):
            processed_lines.append(
                f'<h3 style="color: #374151; margin-top: 1.5rem; margin-bottom: 0.8rem;">{line[4:]}</h3>'
            )
        elif line.startswith("## "):
            processed_lines.append(
                f'<h2 style="color: #1e40af; margin-top: 2rem; margin-bottom: 1rem; padding-bottom: 0.3rem; border-bottom: 2px solid #e2e8f0;">{line[3:]}</h2>'
            )
        elif line.startswith("# "):
            processed_lines.append(
                f'<h1 style="color: #1e40af; margin-top: 2.5rem; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 3px solid #3b82f6;">{line[2:]}</h1>'
            )
        elif line.startswith("- ") or line.startswith("* "):
            bullet_text = line[2:].strip()
            bullet_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", bullet_text)
            bullet_text = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", r"<em>\1</em>", bullet_text)
            processed_lines.append(f'<li style="margin-bottom: 0.5rem;">{bullet_text}</li>')
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", r"<em>\1</em>", line)
            line = re.sub(
                r"(https?://[^\s<>" + r"{}" + r"|\^\[\]]+)",
                r'<a href="\1" target="_blank" style="color: #3b82f6; text-decoration: underline;">\1</a>',
                line,
            )
            processed_lines.append(
                f'<p style="margin-bottom: 1rem; line-height: 1.6;">{line}</p>'
            )
    html = "\n".join(processed_lines)
    html = re.sub(
        r"(<li[^>]*>.*?</li>(?:\s*<li[^>]*>.*?</li>)*)",
        r'<ul style="margin-bottom: 1.5rem; padding-left: 1.5rem;">\1</ul>',
        html,
        flags=re.DOTALL,
    )
    return html
