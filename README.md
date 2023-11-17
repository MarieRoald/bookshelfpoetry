# Bookshelf poetry

Create haiku-inspired poems using book titles from the Norwegian National Library's collection.

## See it live
Try it out yourself on https://bookshelfpoetry.azurewebsites.net/ (you may need to be patient and refresh the site, it's hosted for free on Azure)

## How It Works

1. Select a corpus of texts using the provided widgets. You can choose texts based on keywords, type in a list of URNs, or upload an [Excel sheet with a pre-prepared corpus](https://dh.nb.no/run/korpus/).
2. Each verse of the poem is the title of a book from the National Library. Click on a verse to get more information about the text.
3. If you want to generate another poem, simply press the "Trykk her for å plukke et nytt tilfeldig dikt" button.

## What is a Bookshelf Poem?

This tool allows you to explore the collection of the National Library by assembling haiku-inspired poems from random book titles. The titles are selected such that the first verse will have five syllables, the second verse seven, and the third verse five.

Please note that syllable counts are estimated based on the number of vowels and may not always be accurate. For example, the estimate does not account for numbers or diphthongs.

The 'title poems' are also merely inspired by haiku structure and do not adhere to the rules of traditional haiku.

## Installation

To install and run this dashboard, you need to have [Poetry](https://python-poetry.org) installed. Then clone the repository and run the Streamlit application:

```bash
git clone [REPOSITORY_URL]
cd [REPOSITORY_DIRECTORY]
poetry install
poetry run streamlit src/book_haiku/dashboard.py
```
