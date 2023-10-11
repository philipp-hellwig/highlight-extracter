import fitz


def get_highlights(page):
    # list to store the co-ordinates of all highlights
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


def get_highlighted_text(page, page_no, highlights):
    highlighted_text = [f"Page {page_no}:\n"]
    prev_highlight = False
    all_words = page.get_text_words()
    for highlight in highlights:
        highlighted_segment = []
        for word in all_words:
            word_rect = fitz.Rect(word[0:4])
            word_rect.y1 -= 5  # make rectangles thin enough for intersects function to work
            if highlight.intersects(word_rect):
                highlighted_segment.append(word[4])

        # add a line break if highlights are far enough apart
        if prev_highlight and abs(highlight.y0 - prev_highlight.y1) > 10:
            highlighted_text.append("\n")
        highlighted_text.append(" ".join(highlighted_segment))
        prev_highlight = highlight
    return " ".join(highlighted_text)


def find_highlights(pdf, start=1, end=None):
    """
    :param pdf: path of a pdf file in string format
    :param start: first page (integer) the highlight parser should find_highlights in.
    :param end: last page (integer) the highlight parser should find_highlights in.
    :return: string of all highlighted text
    """

    all_highlighted_text = ""
    doc = fitz.open(stream=pdf, filetype="pdf")
    if not end:
        end = len(doc)
    else:
        end += 1
    for i in range(start-1, end):
        page = doc[i]
        highlights = get_highlights(page)
        page_text = get_highlighted_text(page, i+1, highlights)
        if str(page_text) != f"Page {i+1}:\n":
            all_highlighted_text += page_text + "\n\n"

    return all_highlighted_text


def save_highlights(path, text_highlights):
    """
    saves highlights of a pdf to a txt file.
    :param path: the path of the notes
    :param text_highlights: highlights of the given pdf in string format
    """
    with open(path, "w") as f:
        f.write(text_highlights)


if __name__ == "__main__":
    main()
