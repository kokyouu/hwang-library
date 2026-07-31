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
OUTPUT_PDF = OUTPUT_DIR / "FIT5032_Assessed_Lab_10_Report_Han_Wang.pdf"
LOGO = REPORT_DIR / "monash-university-vector-logo.png"
MONOCHROME_DIR = ROOT / "tmp" / "pdfs" / "lab10_monochrome"

STUDENT_NAME = "Han Wang"
STUDENT_ID = "36668664"
TUTORIAL = "Tuesday 2:00 pm"
REPORT_DATE = "30 July 2026"
REPOSITORY = "https://github.com/kokyouu/hwang-library"

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
            index for index, line in enumerate(lines[start_index + 1 :], start_index + 1) if end in line
        )
    return start_index + 1, lines[start_index:end_index]


def render_code_panel(
    output_name: str,
    title: str,
    source_path: str,
    start_marker: str,
    end_marker: str | None = None,
    max_lines: int = 46,
) -> Path:
    source = ROOT / source_path
    start_line, lines = extract_between(source, start_marker, end_marker)
    lines = lines[:max_lines]
    return render_text_panel(
        output_name,
        title,
        source_path,
        [(start_line + index, line) for index, line in enumerate(lines)],
    )


def render_text_panel(
    output_name: str,
    title: str,
    subtitle: str,
    numbered_lines: list[tuple[int | None, str]],
) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    output = FIGURES / output_name
    width = 1800
    margin = 54
    header_height = 112
    line_height = 31
    code_font = ImageFont.truetype(str(FONT_MONO), 21)
    code_bold = ImageFont.truetype(str(FONT_MONO_BOLD), 21)
    title_font = ImageFont.truetype(str(FONT_BOLD), 28)
    subtitle_font = ImageFont.truetype(str(FONT_REGULAR), 18)

    visual_lines: list[tuple[int | None, str]] = []
    for line_number, text in numbered_lines:
        wrapped = wrap(text.expandtabs(2), width=116, replace_whitespace=False, drop_whitespace=False) or [""]
        visual_lines.append((line_number, wrapped[0]))
        visual_lines.extend((None, segment) for segment in wrapped[1:])

    height = header_height + margin + max(1, len(visual_lines)) * line_height + margin
    image = PILImage.new("RGB", (width, height), "#202124")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, header_height), fill="#2c2e31")
    draw.rectangle((0, 0, 12, header_height), fill="#000000")
    draw.text((margin, 23), title, font=title_font, fill="#ffffff")
    draw.text((margin, 63), subtitle, font=subtitle_font, fill="#b9bdc2")

    y = header_height + 30
    for line_number, text in visual_lines:
        number = "" if line_number is None else str(line_number)
        draw.text((margin, y), number.rjust(4), font=code_font, fill="#7f858b")
        draw.text((145, y), text, font=code_font, fill="#edf0f2")
        y += line_height

    image.save(output, quality=95)
    return output


def generate_code_figures() -> None:
    render_code_panel(
        "fig05_router_code.png",
        "Lab 10 routes",
        "src/router/index.ts",
        "import { createRouter",
    )
    render_code_panel(
        "fig06_weather_view_code.png",
        "City search and browser geolocation",
        "src/views/WeatherView.vue",
        "async function searchByCity()",
        "</script>",
    )
    render_code_panel(
        "fig07_weather_service_code.png",
        "Weather API request and country matching",
        "src/services/weather.ts",
        "export async function searchWeatherByCity",
        "export async function getWeatherByCoordinates",
    )
    render_code_panel(
        "fig08_count_api_code.png",
        "Author and book statistics response",
        "src/views/CountBookAPI.vue",
        "<script setup",
        "</script>",
    )
    render_code_panel(
        "fig09_all_books_code.png",
        "GetAllBookAPI response",
        "src/views/GetAllBookAPI.vue",
        "<script setup",
        "</script>",
    )
    render_code_panel(
        "fig10_weather_test_code.png",
        "Weather-code unit test",
        "src/__tests__/weather.spec.ts",
        "import { describe",
    )

    history = subprocess.run(
        ["git", "log", "--graph", "--decorate", "--oneline", "-12"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    render_text_panel(
        "fig11_git_history.png",
        "Git commit history",
        "branch: lab10-api",
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


def scaled_image(path: Path, max_width: float = 16.6 * cm, max_height: float = 12.4 * cm) -> Image:
    grayscale_path = monochrome_image(path)
    with PILImage.open(grayscale_path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    return Image(str(grayscale_path), width=width * scale, height=height * scale)


def evidence(path: str, caption: str, styles: dict[str, ParagraphStyle], max_height: float = 12.4 * cm):
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
            "FIT5032 Internet Applications Development - Assessed Lab 10",
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
        title="FIT5032 Assessed Lab 10 Report",
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
    story.append(Paragraph("Assessed Lab 10", styles["CoverSub"]))
    story.append(Spacer(1, 0.75 * cm))
    story.append(Paragraph("API Service Integration", styles["CoverTitle"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Weather and Library JSON APIs", styles["CoverSub"]))
    story.append(Spacer(1, 1.15 * cm))

    details = [
        ["Student Name", STUDENT_NAME],
        ["Student ID", STUDENT_ID],
        ["Tutorial/Lab", TUTORIAL],
        ["Project Name", "hwang-library"],
        ["GitHub Repository", REPOSITORY],
    ]
    table = Table(details, colWidths=[4.5 * cm, 11.0 * cm], rowHeights=0.78 * cm)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Arial-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Arial"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.2),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.75 * cm))
    story.append(Paragraph(REPORT_DATE, styles["CoverSub"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Overview", styles["H1"]))
    story.append(
        Paragraph(
            "This report documents the completed FIT5032 Assessed Lab 10 implementation in the existing "
            "<font name='Consolas'>hwang-library</font> Vue 3 project. The application integrates an external "
            "weather service, supports browser-location and city-based weather requests, calculates author and "
            "book statistics from the Lab 2 dataset, and exposes all books as a JSON-formatted API page.",
            styles["Body"],
        )
    )
    criteria = [
        ["Assessment item", "Implemented evidence"],
        ["Task 10.1 - weather", "Current-location method and weather result UI"],
        ["Task 10.1 - statistics", "3 authors and 6 books in CountBookAPI"],
        ["Task 10.2 - city search", "Clayton, AU result in Celsius with a weather icon"],
        ["Task 10.2 - all books", "6 books shown as JSON on GetAllBookAPI"],
        ["Version control", "Dedicated lab10-api branch and focused commits"],
    ]
    criteria_table = Table(criteria, colWidths=[5.3 * cm, 10.2 * cm], repeatRows=1)
    criteria_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Arial"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(criteria_table)

    story.append(Paragraph("2. Page Setup and Routing", styles["H1"]))
    story.append(
        Paragraph(
            "The application uses Vue Router and a shared BHeader navigation component. The route name "
            "<font name='Consolas'>GetWeather</font> maps to <font name='Consolas'>/WeatherCheck</font>, while "
            "the two library response pages are available at <font name='Consolas'>/CountBookAPI</font> and "
            "<font name='Consolas'>/GetAllBookAPI</font>.",
            styles["Body"],
        )
    )
    story.append(evidence("fig05_router_code.png", "Figure 1. Vue Router configuration for all Lab 10 pages.", styles))

    story.append(PageBreak())
    story.append(Paragraph("3. Task 10.1 - Weather API", styles["H1"]))
    story.append(Paragraph("3.1 Current location and city controls", styles["H2"]))
    story.append(
        Paragraph(
            "The WeatherView component validates a city search, handles loading and error states, and uses the "
            "browser Geolocation API for the current-location workflow. Coordinates are sent only after the user "
            "selects the Use current location control.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig06_weather_view_code.png",
            "Figure 2. City-search and browser-geolocation methods in WeatherView.vue.",
            styles,
            max_height=15.0 * cm,
        )
    )
    story.append(
        evidence(
            "fig13_current_location.png",
            "Figure 3. Browser result for the authorised current location in Celsius using Open-Meteo.",
            styles,
            max_height=9.2 * cm,
        )
    )
    story.append(Paragraph("3.2 Search weather by city", styles["H2"]))
    story.append(
        Paragraph(
            "The external service accepts the assessed-lab example Clayton, AU. Country-code matching prevents "
            "the request from selecting a same-named city in another country. The returned Celsius temperature "
            "and weather code drive the corresponding weather icon.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig07_weather_service_code.png",
            "Figure 4. Weather API request, country matching and result mapping.",
            styles,
            max_height=14.0 * cm,
        )
    )
    story.append(
        evidence(
            "fig01_weather_clayton.png",
            "Figure 5. Browser result for Clayton, AU in Celsius with a clear-sky icon.",
            styles,
            max_height=10.2 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("4. Task 10.1 - Author and Book Statistics", styles["H1"]))
    story.append(
        Paragraph(
            "CountBookAPI imports the Lab 2 authors.json file, calculates the number of authors, reduces the "
            "nested famousWorks arrays into a total book count, and returns per-author counts. The response "
            "correctly reports 3 authors and 6 books.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig08_count_api_code.png",
            "Figure 6. CountBookAPI response calculation from authors.json.",
            styles,
            max_height=11.3 * cm,
        )
    )
    story.append(
        evidence(
            "fig02_count_book_api.png",
            "Figure 7. Browser response showing authorsCount 3 and totalBooks 6.",
            styles,
            max_height=10.2 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("5. Task 10.2 - GetAllBookAPI", styles["H1"]))
    story.append(
        Paragraph(
            "GetAllBookAPI flattens every author's famousWorks array and preserves the title, publication year, "
            "author name and author ID. The page presents the complete six-book collection as a JSON response at "
            "the required GetAllBookAPI route.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig09_all_books_code.png",
            "Figure 8. GetAllBookAPI transformation and JSON response structure.",
            styles,
            max_height=11.6 * cm,
        )
    )
    story.append(
        evidence(
            "fig03_all_books_api.png",
            "Figure 9. GetAllBookAPI browser response showing count 6 and the first response records.",
            styles,
            max_height=10.0 * cm,
        )
    )
    story.append(
        evidence(
            "fig04_all_books_api_continued.png",
            "Figure 10. Continued browser response showing all remaining books and the closing JSON structure.",
            styles,
            max_height=10.0 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("6. Verification and Responsive Layout", styles["H1"]))
    story.append(
        Paragraph(
            "The project passes Vue TypeScript checking, the production Vite build, and the Vitest suite. The "
            "weather-code unit test verifies clear, rain, snow and thunderstorm mappings. Browser checks also "
            "confirmed that all navigation labels, controls and results remain readable at a 390-pixel mobile "
            "viewport.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig10_weather_test_code.png",
            "Figure 11. Unit coverage for external weather-code mapping.",
            styles,
            max_height=7.0 * cm,
        )
    )
    story.append(
        evidence(
            "mobile_weather_check.png",
            "Figure 12. Responsive Weather Check page at a 390-pixel mobile viewport.",
            styles,
            max_height=13.2 * cm,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("7. Git Version Control", styles["H1"]))
    story.append(
        Paragraph(
            "Lab 10 was developed on the dedicated <font name='Consolas'>lab10-api</font> branch so the existing "
            "Lab 2 and Lab 3 history remained intact. The implementation and automated verification were recorded "
            "in separate focused commits before the report was added.",
            styles["Body"],
        )
    )
    story.append(
        evidence(
            "fig11_git_history.png",
            "Figure 13. Git history showing the focused Lab 10 implementation and test commits.",
            styles,
            max_height=9.0 * cm,
        )
    )
    story.append(
        evidence(
            "fig12_github_history.png",
            "Figure 14. GitHub commit history for the pushed lab10-api branch.",
            styles,
            max_height=10.0 * cm,
        )
    )

    story.append(Paragraph("8. Conclusion", styles["H1"]))
    story.append(
        Paragraph(
            "The completed Lab 10 application satisfies the Pass/Credit and Distinction/High Distinction functional "
            "criteria. It can retrieve weather using browser coordinates or a city query, displays temperatures in "
            "Celsius with a matching icon, calculates the author and book totals from the existing dataset, and "
            "shows all books as valid JSON. The implementation is tested, responsive, documented and maintained "
            "through a clear Git commit history.",
            styles["Body"],
        )
    )

    document.build(story, onFirstPage=page_decorator, onLaterPages=page_decorator)


if __name__ == "__main__":
    build_report()
    print(OUTPUT_PDF)
