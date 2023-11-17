from bookshelfpoetry import TitlePoem
import random

STYLES = [f"style{i}" for i in range(1, 6)]
COLORS = [f"color{i}" for i in range(1, 6)]
FONTS = [f"font{i}" for i in range(1, 7)]
SIZES = [f"size{i}" for i in range(1, 4)]


def get_book_html(
    booktitle: str, url: str, style: str, font: str, color: str, size: str
) -> str:
    html = f"""
<a class="book {style} {font} {color} {size}" href="{url}">
        <div class="spine">
            <span class="decoration"></span>
            <span class="title">{booktitle}</span>
            <span class="decoration"></span>
        </div>
</a>
"""
    return html


def get_random_styling(
    styles: list[str] | None = None,
    fonts: list[str] | None = None,
    colors: list[str] | None = None,
    sizes: list[str] | None = None
) -> tuple[str, str, str, str]:
    """Get a random style, font, color or size for the books.
    """
    return (
        random.choice(styles or STYLES),
        random.choice(fonts or FONTS),
        random.choice(colors or COLORS),
        random.choice(sizes or SIZES),
    )


def get_bookshelf_html(titlepoem: TitlePoem) -> str:
    html = '<div class="books">\n'
    html += get_book_html(titlepoem[0].title, titlepoem[0].url, *get_random_styling())
    html += get_book_html(titlepoem[1].title, titlepoem[1].url, *get_random_styling(sizes=SIZES[:-1]))
    html += get_book_html(titlepoem[2].title, titlepoem[2].url, *get_random_styling())

    html += "</div>"
    return html
