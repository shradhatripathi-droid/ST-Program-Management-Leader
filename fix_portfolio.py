#!/usr/bin/env python3
"""Fix 0x9d encoding corruption and restore missing asset references."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BAD = "\x9d"
MID = "\u00b7"
EM = "\u2014"
EN = "\u2013"
TIMES = "\u00d7"
ARR = "\u2192"
HARR = "\u2194"

FILES = [
    ROOT / "index.html",
    ROOT / "assets" / "diagrams.js",
    ROOT / "README.md",
]


def fix_text(text: str) -> str:
    text = text.replace("20 ? 1.9M", f"20 {ARR} 1.9M")
    text = text.replace("Bloomberg ? Traders", f"Bloomberg {HARR} Traders")
    text = text.replace(f"91{BAD}", f"91{TIMES}")
    text = text.replace(f"3{BAD}", f"3{TIMES}")
    text = text.replace(f"$8{BAD}10M", f"$8{EN}10M")

    text = re.sub(r"(\d{4}) " + re.escape(BAD) + r" Present", rf"\1 {EN} Present", text)
    text = re.sub(r"(\d{4}) " + re.escape(BAD) + r" (\d{4})", rf"\1 {EN} \2", text)

    em_dash_patterns = [
        r"(<title>Shradha Tripathi) " + re.escape(BAD) + r" (Product Management Leader)",
        r"(<h3>Intuit) " + re.escape(BAD) + r" (Staff Product Manager)",
        r"(<h3>Amazon) " + re.escape(BAD) + r" (Sr\. Technical Product Manager)",
        r"(<h3>Amazon) " + re.escape(BAD) + r" (Alexa Multimodal Devices)",
        r"(<h3>Flipkart) " + re.escape(BAD) + r" (Senior Manager)",
        r"(<h3>Deutsche Bank) " + re.escape(BAD) + r" (Manager, Business Engineering)",
        r"(<h3>The Hartford) " + re.escape(BAD) + r" (Financial Analyst)",
        r"(<h3>CSC) " + re.escape(BAD) + r" (Statistical and Financial Analyst)",
        r"(Trusted By) " + re.escape(BAD) + r" (Companies)",
        r"(Product Portfolio) " + re.escape(BAD) + r" (Revenue)",
        r"(Built for GitHub) " + re.escape(BAD) + r" (Product Management Leader Portfolio)",
        r"(Amazon) " + re.escape(BAD) + r" (AI/ML Product Operating Model)",
    ]
    for pattern in em_dash_patterns:
        text = re.sub(pattern, rf"\1 {EM} \2", text)

    text = text.replace(BAD, MID)
    return text


def fix_index_html(text: str) -> str:
    text = fix_text(text)

    text = text.replace(
        '<img class="logo-icon" src="https://cdn.simpleicons.org/amazon/FF9900" alt="Amazon" title="Amazon" />',
        '<img class="logo-icon" src="./assets/logo-amazon.png" alt="Amazon" title="Amazon" />',
    )
    text = text.replace(
        '<img class="company-logo" src="https://cdn.simpleicons.org/intuit/236CFF" alt="Intuit logo" />',
        '<img class="company-logo" src="./assets/logo-intuit.svg" alt="Intuit logo" />',
    )
    text = text.replace(
        '<img class="company-logo icon" src="https://cdn.simpleicons.org/amazon/FF9900" alt="Amazon logo" />',
        '<img class="company-logo icon" src="./assets/logo-amazon.png" alt="Amazon logo" />',
    )
    text = text.replace(
        '<img class="company-logo" src="https://cdn.simpleicons.org/deutschebank/0018A8" alt="Deutsche Bank logo" />',
        '<img class="company-logo" src="./assets/logo-deutsche-bank.svg" alt="Deutsche Bank logo" />',
    )
    text = text.replace(
        '<img class="company-logo" src="https://cdn.simpleicons.org/thehartford/003DA5" alt="The Hartford logo" />',
        '<img class="company-logo" src="./assets/logo-hartford.png" alt="The Hartford logo" />',
    )
    text = text.replace(
        '<img class="company-logo" src="https://cdn.simpleicons.org/csc/0033A0" alt="CSC logo" />',
        '<img class="company-logo" src="./assets/logo-csc.png" alt="CSC logo" />',
    )

    education = """      <table>
        <tr>
          <th><img class="edu-logo" src="./assets/logo-mit.png" alt="MIT" /> Designing and Building AI Products and Services</th>
          <td>MIT, Boston, MA</td>
        </tr>
        <tr>
          <th><img class="edu-logo" src="./assets/logo-suny-albany.png" alt="SUNY Albany" /> MS, Information Science</th>
          <td>State University of New York, Albany, NY</td>
        </tr>
        <tr><th><img class="edu-logo" src="./assets/logo-isi.png" alt="Indian Statistical Institute" /> Six Sigma Black Belt</th><td>Indian Statistical Institute, India</td></tr>
      </table>"""

    text = re.sub(
        r"<section>\s*<h2>Education &amp; Certifications</h2>\s*<table>.*?</table>\s*</section>",
        f"<section>\n      <h2>Education &amp; Certifications</h2>\n{education}\n    </section>",
        text,
        count=1,
        flags=re.DOTALL,
    )

    return text


def main() -> None:
    product_diagrams = ROOT.parent / "product-management-leader" / "assets" / "diagrams.js"
    if product_diagrams.exists():
        shutil.copy2(product_diagrams, ROOT / "assets" / "diagrams.js")

    for path in FILES:
        if not path.exists():
            continue
        original = path.read_text(encoding="latin-1")
        fixed = fix_text(original)
        if path.name == "index.html":
            fixed = fix_index_html(fixed)
        path.write_text(fixed, encoding="utf-8")
        remaining = fixed.count(BAD)
        print(f"Fixed {path.name}: remaining bad bytes={remaining}")


if __name__ == "__main__":
    main()
