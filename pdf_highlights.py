import fitz


def get_annotations(page):
    annot = page.first_annot
    highlights = []
    while annot:
        if annot.type[0] == 8:
            all_coordinates = annot.vertices
            if len(all_coordinates) == 4:
                coord = fitz.Quad(all_coordinates).rect
                coord.y1 -= 5
                highlights.append(coord)
            else:
                all_coordinates = [all_coordinates[x:x + 4] for x in range(0, len(all_coordinates), 4)]
                for i in range(len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    coord.y1 -= 5
                    highlights.append(coord)
        annot = annot.next
    return highlights


def get_annotation_text(page, highlights, markdown=False):
    prev_highlight = False
    all_words = page.get_text_words()
    highlighted_text = []
    for highlight in highlights:
        highlighted_segment = ["### "] if highlight.height > 10 and markdown else []
        for i, word in enumerate(all_words):
            word_rect = fitz.Rect(word[0:4])
            word_rect.y1 -= 5  # make rectangles thin enough for intersects function to work
            if highlight.intersects(word_rect):
                highlighted_segment.append(word[4])
                pos_highlight = i
        # add a line break if highlights are far enough apart
        if prev_highlight and abs(highlight.y0 - prev_highlight.y1) > 10:
            highlighted_text.append([highlighted_text[-1][0] + .5, "\n\n"])
        highlighted_text.append([pos_highlight, " ".join(highlighted_segment)])
        prev_highlight = highlight
    highlighted_text = sorted(highlighted_text)
    return " ".join([h[1] for h in highlighted_text])


def get_highlights(pdf, start=1, end=None, display_pages=False, markdown=False):
    """
    :param pdf: path of a pdf file in string format
    :param start: first page (integer) the highlight parser should find_highlights in.
    :param end: last page (integer) the highlight parser should find_highlights in.
    :param display_pages: whether to add page indicators into the highlights string
    :param markdown: whether to use heading ###
    :return: string of all highlighted text
    """
    all_highlighted_text = ""
    # doc = fitz.open(pdf) # for running with path string
    doc = fitz.open(stream=pdf, filetype="pdf")
    if end is None or end > doc.page_count:
        end = doc.page_count
    for i in range(start-1, end):
        page_text = f"*Page {i + 1}*\n\n" if display_pages else ""
        page = doc[i]
        highlights = get_annotations(page)
        page_text += get_annotation_text(page, highlights, markdown)
        all_highlighted_text += page_text + "\n\n"
    return all_highlighted_text


def save_highlights(path, text_highlights):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text_highlights)


if __name__ == "__main__":
    main()
