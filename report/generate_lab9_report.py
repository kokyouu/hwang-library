from __future__ import annotations

import subprocess
from pathlib import Path
from textwrap import wrap

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"
FIGURES = REPORT_DIR / "figures"
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PDF = OUTPUT_DIR / "FIT5032_Assessed_Lab_9_Report_Han_Wang.pdf"
LOGO = REPORT_DIR / "monash-university-vector-logo.png"
MONOCHROME_DIR = ROOT / "tmp" / "pdfs" / "lab9_monochrome"

STUDENT_NAME = "Han Wang"
STUDENT_ID = "36668664"
TUTORIAL = "Tuesday 2:00 pm"
REPORT_DATE = "31 July 2026"
REPOSITORY = "https://github.com/kokyouu/hwang-library"
BRANCH = "assessed-lab-9"
FUNCTION_URL = "https://fit-lab-library-zpfjrylreg.cn-hongkong.fcapp.run"
PREVIEW_URL = "https://b8fb1089.hwang-library.pages.dev"

FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
FONT_MONO = Path("C:/Windows/Fonts/consola.ttf")
FONT_MONO_BOLD = Path("C:/Windows/Fonts/consolab.ttf")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_BOLD)))
    pdfmetrics.registerFont(TTFont("Consolas", str(FONT_MONO)))


def extract_between(path: Path, start: str, end: str | None = None) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start_index = next(index for index, line in enumerate(lines) if start in line)
    if end is None:
        end_index = len(lines)
    else:
        end_index = next(
            index
            for index, line in enumerate(lines[start_index + 1 :], start_index + 1)
            if end in line
        )
    return start_index + 1, lines[start_index:end_index]


def render_text_panel(
    output_name: str,
    title: str,
    subtitle: str,
    numbered_lines: list[tuple[int | None, str]],
) -> Path:
    output = FIGURES / output_name
    width = 1800
    margin = 54
    header_height = 112
    line_height = 31
    code_font = ImageFont.truetype(str(FONT_MONO), 21)
    title_font = ImageFont.truetype(str(FONT_BOLD), 28)
    subtitle_font = ImageFont.truetype(str(FONT_REGULAR), 18)

    visual_lines: list[tuple[int | None, str]] = []
    for line_number, text in numbered_lines:
        wrapped = wrap(
            text.expandtabs(2), width=116, replace_whitespace=False, drop_whitespace=False
        ) or [""]
        visual_lines.append((line_number, wrapped[0]))
        visual_lines.extend((None, segment) for segment in wrapped[1:])

    height = header_height + margin + max(1, len(visual_lines)) * line_height + margin
    image = PILImage.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, header_height), fill="black")
    draw.text((margin, 23), title, font=title_font, fill="white")
    draw.text((margin, 63), subtitle, font=subtitle_font, fill="white")

    y = header_height + 30
    for line_number, text in visual_lines:
        number = "" if line_number is None else str(line_number)
        draw.text((margin, y), number.rjust(4), font=code_font, fill="black")
        draw.text((145, y), text, font=code_font, fill="black")
        y += line_height

    image.save(output, quality=95)
    return output


def render_code_panel(
    output_name: str,
    title: str,
    source_path: str,
    start_marker: str,
    end_marker: str | None = None,
    max_lines: int = 48,
) -> Path:
    start_line, lines = extract_between(ROOT / source_path, start_marker, end_marker)
    return render_text_panel(
        output_name,
        title,
        source_path,
        [(start_line + index, line) for index, line in enumerate(lines[:max_lines])],
    )


def generate_code_figures() -> None:
    render_code_panel(
        "lab9_code_count_route.png",
        "Firestore count cloud function",
        "aliyun-function/server.mjs",
        "async function countBooks",
        "async function buildMarketplace",
    )
    render_code_panel(
        "lab9_code_marketplace_route.png",
        "Marketplace response generated from live records",
        "aliyun-function/server.mjs",
        "async function buildMarketplace",
        "export async function handleRequest",
    )
    render_code_panel(
        "lab9_code_http_router.png",
        "HTTP routing, health check and error handling",
        "aliyun-function/server.mjs",
        "export async function handleRequest",
        "export function createServer",
    )

    history = subprocess.run(
        ["git", "log", "--graph", "--decorate", "--oneline", "-8"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    render_text_panel(
        "lab9_git_history_panel.png",
        "Git commit history",
        f"branch: {BRANCH}",
        [(None, line) for line in history],
    )


def monochrome_image(path: Path) -> Path:
    MONOCHROME_DIR.mkdir(parents=True, exist_ok=True)
    output = MONOCHROME_DIR / f"{path.stem}_grayscale.png"
    with PILImage.open(path) as source:
        rgba_source = source.convert("RGBA")
        white_background = PILImage.new("RGBA", rgba_source.size, "white")
        white_background.alpha_composite(rgba_source)
        ImageOps.grayscale(white_background.convert("RGB")).save(output)
    return output


def scaled_image(path: Path, max_width: float = 16.6 * cm, max_height: float = 12.5 * cm) -> Image:
    with PILImage.open(path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def evidence(
    path: str,
    caption: str,
    styles: dict[str, ParagraphStyle],
    max_height: float = 12.5 * cm,
) -> KeepTogether:
    return KeepTogether(
        [
            scaled_image(FIGURES / path, max_height=max_height),
            Spacer(1, 0.12 * cm),
            Paragraph(caption, styles["Caption"]),
            Spacer(1, 0.28 * cm),
        ]
    )


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=10.2,
            leading=14.4,
            textColor=colors.black,
            spaceAfter=7,
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Arial-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=8,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Arial-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "Caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.4,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.black,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Arial-Bold",
            fontSize=25,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.black,
        ),
        "CoverSub": ParagraphStyle(
            "CoverSub",
            parent=base["Heading2"],
            fontName="Arial",
            fontSize=15,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.black,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.8,
            leading=12,
            textColor=colors.black,
        ),
    }


def monochrome_table(data: list[list[str]], widths: list[float], header: bool = True) -> Table:
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Arial"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.8),
        ("GRID", (0, 0), (-1, -1), 0.55, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table


def page_decorator(canvas, doc) -> None:
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.5)
        canvas.line(2.15 * cm, A4[1] - 1.45 * cm, A4[0] - 2.15 * cm, A4[1] - 1.45 * cm)
        canvas.setFont("Arial", 8.2)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString(
            A4[0] / 2,
            A4[1] - 1.15 * cm,
            "FIT5032 Internet Applications Development - Assessed Lab 9",
        )
        canvas.drawCentredString(A4[0] / 2, 1.15 * cm, str(doc.page - 1))
    canvas.restoreState()


def build_report() -> None:
    register_fonts()
    generate_code_figures()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    styles = build_styles()

    document = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=2.15 * cm,
        leftMargin=2.15 * cm,
        topMargin=1.85 * cm,
        bottomMargin=1.7 * cm,
        title="FIT5032 Assessed Lab 9 Report",
        author=STUDENT_NAME,
    )
    story = []

    story.append(Image(str(monochrome_image(LOGO)), width=16.3 * cm, height=3.62 * cm))
    story.append(Spacer(1, 1.35 * cm))
    story.append(Paragraph("MONASH UNIVERSITY", styles["CoverSub"]))
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("Faculty of Information Technology", styles["CoverSub"]))
    story.append(Spacer(1, 1.0 * cm))
    story.append(Paragraph("FIT5032 Internet Applications Development", styles["CoverSub"]))
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph("Assessed Lab 9", styles["CoverSub"]))
    story.append(Spacer(1, 0.75 * cm))
    story.append(Paragraph("Cloud Functions", styles["CoverTitle"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Alibaba Cloud Function Compute and Firestore", styles["CoverSub"]))
    story.append(Spacer(1, 1.15 * cm))

    details = [
        ["Student Name", STUDENT_NAME],
        ["Student ID", STUDENT_ID],
        ["Tutorial/Lab", TUTORIAL],
        ["Project Name", "hwang-library"],
        ["Git Branch", BRANCH],
        ["GitHub Repository", REPOSITORY],
    ]
    detail_table = Table(details, colWidths=[4.5 * cm, 11.0 * cm], rowHeights=0.72 * cm)
    detail_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Arial-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Arial"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.2),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(detail_table)
    story.append(Spacer(1, 0.65 * cm))
    story.append(Paragraph(REPORT_DATE, styles["CoverSub"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Overview", styles["H1"]))
    story.append(
        Paragraph(
            "This report documents the completed FIT5032 Assessed Lab 9 implementation in the existing "
            "<font name='Consolas'>hwang-library</font> Vue 3 project. The solution uses one isolated Alibaba "
            "Cloud Function Compute web function to read the existing Cloud Firestore books collection. The "
            "same function exposes a count endpoint and the Distinction/High Distinction marketplace endpoint, "
            "while Cloudflare Pages hosts only the static Vue client.",
            styles["Body"],
        )
    )
    criteria = [
        ["Assessment item", "Completed result"],
        ["Cloud function", "Node.js 20 custom-runtime web function deployed in China (Hong Kong)"],
        ["Book count", "Live Firestore count returned through /api/books/count"],
        ["Vue integration", "Book Counter displays 3 records and the Alibaba Cloud source"],
        ["Extension task", "Marketplace prices and displays the live Firestore catalogue"],
        ["Deployment", "Static preview deployed from GitHub commit eeb790c"],
        ["Version control", "Dedicated assessed-lab-9 branch with focused commits"],
    ]
    story.append(monochrome_table(criteria, [5.1 * cm, 10.4 * cm]))

    story.append(Paragraph("2. Architecture and Resource Isolation", styles["H1"]))
    story.append(
        Paragraph(
            "The browser loads the Vue production build from Cloudflare Pages. Vue sends GET requests to the "
            "Function Compute public HTTPS trigger. The function reads the Firestore REST API and returns JSON "
            "with CORS headers. No existing Alibaba Cloud ECS, VPC, security group, load balancer, domain, NAS "
            "or OSS resource is attached to this Lab 9 function.",
            styles["Body"],
        )
    )
    architecture = [
        ["Component", "Configuration"],
        ["Vue client", PREVIEW_URL],
        ["Cloud API", FUNCTION_URL],
        ["Function", "fit5032-lab9-hwang-library"],
        ["Region/runtime", "cn-hongkong; Node.js 20 custom runtime on Debian 11"],
        ["Elasticity", "0 minimum instances; scales to zero when idle"],
        ["Network", "Default public egress only; VPC access disabled"],
        ["Data source", "Cloud Firestore project hwang-library-lab7, collection books"],
    ]
    story.append(monochrome_table(architecture, [4.0 * cm, 11.5 * cm]))
    story.append(PageBreak())
    story.append(Paragraph("2.1 Deployed function evidence", styles["H2"]))
    story.append(
        Paragraph(
            "The Function Compute detail page identifies the account, region, function, HTTP trigger, editable "
            "LATEST version and Debian 11 custom runtime in one deployment view.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_aliyun_function_detail.png",
            "Figure 1. Alibaba Cloud account, Hong Kong region, isolated function name, HTTP trigger and Node.js custom runtime.",
            styles,
            max_height=9.8 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("3. Alibaba Cloud Function Configuration", styles["H1"]))
    story.append(Paragraph("3.1 Public HTTP trigger", styles["H2"]))
    story.append(
        Paragraph(
            "The default HTTP trigger supports GET, HEAD and OPTIONS requests and exposes the function through "
            "HTTPS. Authentication is set to No Authentication because the assessed Vue application is a public "
            "client and cannot sign requests with an Alibaba Cloud access key. The function itself accepts only "
            "GET and OPTIONS and returns 405 for other methods.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_aliyun_http_trigger.png",
            "Figure 2. Public Function Compute URL and the selected No Authentication HTTP-trigger setting.",
            styles,
            max_height=12.4 * cm,
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("3.2 Scale-to-zero cost control", styles["H2"]))
    story.append(
        Paragraph(
            "No elastic policy or reserved instance is configured. Alibaba Cloud therefore uses elastic "
            "instances with a minimum instance count of 0. This avoids an always-on server and keeps the short "
            "lab verification within the approved low-cost limit.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_aliyun_elastic_config.png",
            "Figure 3. Elastic configuration confirming the default minimum instance count is 0.",
            styles,
            max_height=8.8 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("4. Cloud Function Implementation", styles["H1"]))
    story.append(Paragraph("4.1 Firestore book count", styles["H2"]))
    story.append(
        Paragraph(
            "The count handler retrieves the live books collection, calculates the document count and returns "
            "the collection, project and source metadata. The response identifies Alibaba Cloud Function Compute "
            "so the browser result can prove which cloud platform executed the request.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_code_count_route.png",
            "Figure 4. Count route returning the live Firestore document count and cloud-source metadata.",
            styles,
            max_height=8.2 * cm,
        )
    )
    story.append(Paragraph("4.2 Marketplace extension", styles["H2"]))
    story.append(
        Paragraph(
            "The marketplace handler calculates a catalogue value from the current number of records, generates "
            "Snapshot and Semester Feed offers, and attaches a per-record educational licence price. Values are "
            "derived at request time, so additions to Firestore automatically change the catalogue and offers.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_code_marketplace_route.png",
            "Figure 5. Marketplace product, licence offers and priced live records.",
            styles,
            max_height=12.0 * cm,
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("4.3 HTTP routing and error handling", styles["H2"]))
    story.append(
        Paragraph(
            "A small request router handles CORS preflight, rejects unsupported methods, provides a health "
            "endpoint and dispatches the two assessed API paths. Unexpected failures are returned as JSON with "
            "HTTP status 500.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_code_http_router.png",
            "Figure 6. Health, count and marketplace routes with method and error handling.",
            styles,
            max_height=9.8 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("5. Vue Results", styles["H1"]))
    story.append(Paragraph("5.1 Book Counter", styles["H2"]))
    story.append(
        Paragraph(
            "The production Vue build reads the Function Compute base URL from "
            "<font name='Consolas'>.env.production</font>. Selecting Get Book Count calls the Alibaba endpoint and "
            "displays the live count, collection, Firebase project and cloud source. The verified result is 3.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_book_counter_aliyun.png",
            "Figure 7. Online Book Counter showing 3 live Firestore records from Alibaba Cloud Function Compute.",
            styles,
            max_height=10.0 * cm,
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("5.2 Book Data Marketplace", styles["H2"]))
    story.append(
        Paragraph(
            "The marketplace page loads the second function route and presents the data as a commercial teaching "
            "dataset. The verified response contains three books, a catalogue value of AUD 13.50, Snapshot and "
            "Semester Feed offers, and the Alibaba Cloud source label.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_data_marketplace_aliyun.png",
            "Figure 8. Online marketplace with live offers and all three Firestore records.",
            styles,
            max_height=10.4 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("6. Deployment and Verification", styles["H1"]))
    story.append(
        Paragraph(
            "GitHub commit <font name='Consolas'>eeb790c</font> triggered a successful Cloudflare Pages preview "
            "deployment. Cloudflare serves only the static application; all Lab 9 API requests are sent to the "
            "Alibaba Cloud Function Compute public URL.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_cloudflare_deployment_aliyun.png",
            "Figure 9. Successful preview deployment for commit eeb790c on assessed-lab-9.",
            styles,
            max_height=9.4 * cm,
        )
    )
    verification = [
        ["Verification", "Result"],
        ["GET /health", "HTTP 200; Alibaba Cloud platform identified"],
        ["GET /api/books/count", "HTTP 200; count 3; Firestore project and collection confirmed"],
        ["GET /api/books/marketplace", "HTTP 200; 3 records and two offers"],
        ["Function tests", "3 passed"],
        ["Vue unit tests", "6 passed across 4 test files"],
        ["TypeScript", "vue-tsc completed without errors"],
        ["Production build", "Vite build completed successfully"],
        ["Online browser", "Book Counter and Marketplace loaded Alibaba data successfully"],
    ]
    story.append(Paragraph("6.1 Test results", styles["H2"]))
    story.append(monochrome_table(verification, [5.0 * cm, 10.5 * cm]))

    story.append(PageBreak())
    story.append(Paragraph("7. Git Version Control", styles["H1"]))
    story.append(
        Paragraph(
            "All work was completed on the dedicated <font name='Consolas'>assessed-lab-9</font> branch. The "
            "existing main branch and unrelated lab branches were not modified. The implementation commit was "
            "pushed to the requested GitHub repository before this report was generated.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "lab9_git_history_panel.png",
            "Figure 10. Local Git history for the assessed-lab-9 branch.",
            styles,
            max_height=7.2 * cm,
        )
    )
    story.append(
        evidence(
            "lab9_github_history_aliyun.png",
            "Figure 11. GitHub commit history showing the pushed Alibaba Cloud implementation commit.",
            styles,
            max_height=10.2 * cm,
        )
    )

    story.append(Paragraph("8. Conclusion", styles["H1"]))
    story.append(
        Paragraph(
            "The Assessed Lab 9 requirements are complete. The application counts live Firestore documents "
            "through an Alibaba Cloud web function, displays the result in Vue, provides the marketplace extension, "
            "passes automated and browser verification, and is deployed from a dedicated Git branch. The Alibaba "
            "resource is isolated, uses no existing server or VPC, and scales to zero when idle.",
            styles["Body"],
        )
    )

    document.build(story, onFirstPage=page_decorator, onLaterPages=page_decorator)


if __name__ == "__main__":
    build_report()
    print(OUTPUT_PDF)
