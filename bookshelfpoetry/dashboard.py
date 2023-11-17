from bookshelfpoetry import get_random_poem, get_syllable_counts, Corpus
from bookshelfpoetry.bookshelf import get_bookshelf_html

import pandas as pd
import streamlit as st
from pathlib import Path
import re
import dhlab as dh  # type: ignore

@st.cache_resource()
def get_corpus_from_freetext(freetext: str | None = None, number: int = 2000) -> Corpus:
    """Get corpus based on freetext."""
    if freetext is not None:
        return tuple(dh.Corpus(freetext=freetext, limit=number).corpus.itertuples())
    return tuple(dh.Corpus(doctype="digibok", limit=number).corpus.itertuples())


@st.cache_resource()
def get_corpus_from_urnlist(urn_raw: str) -> Corpus | None:
    """Get corpus based on urn list."""
    urns = re.findall("URN:NBN[^\s.,]+", urn_raw)
    if not urns:
        return None
    return tuple(dh.Corpus.from_identifiers(urns).corpus.itertuples())

def corpus_selection_widget() -> Corpus | None:
    """Widget to select corpus to create poem from"""
    column1, column2 = st.columns([1, 3])
    with column1:
        method = st.selectbox(
            "Metode for å angi tekst",
            options=["Stikkord", "Urnliste", "Excelkorpus"],
            help="Lim inn en tekst med URNer, eller last opp et excelark med korpus"
            " lagd for eksempel med https://beta.nb.no/dhlab/korpus/, "
            "eller finn tekster ved hjelp av stikkord",
        )

    with column2:
        if method == "Urnliste":
            urn_raw = st.text_area(
                "Lim inn URNer:",
                "",
                help="Lim tekst med URNer. Teksten trenger ikke å være formatert, "
                "og kan inneholde mer enn URNer",
            )
            corpus = get_corpus_from_urnlist(urn_raw)
            if corpus is None:
                st.write("Fant ingen URNer i teksten")
            return corpus
        elif method == "Excelkorpus":
            uploaded_file = st.file_uploader(
                "Last opp et korpus",
                help=(
                    "Dra en fil over hit, fra et nedlastningsikon, "
                    + "eller velg fra en mappe"
                ),
            )
            if uploaded_file is None:
                return None
            return pd.read_excel(uploaded_file).itertuples()
        else:
            stikkord = st.text_input(
                "Angi noen stikkord for å forme et utvalg tekster",
                "",
                help="Skriv inn for eksempel forfatter og tittel for bøker, "
                "eller avisnavn for aviser."
                "For aviser kan dato skrives på formatet YYYYMMDD.",
            )
            if stikkord == "":
                return get_corpus_from_freetext(None)
            return get_corpus_from_freetext(freetext=stikkord)

st.set_page_config(page_title="Bokhylledikt")
# This is to get custom css for the books
with open(Path(__file__).parent.parent/'assets/bookstyle.css') as f:
   css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Bokhylledikt")
st.write(
    "Utforsk nasjonalbiblioteket gjennom dikt! "
    + "Velg et korpus med menyen under og trykk på den røde knappen for å finne nye bokhylledikt. "
    + "Hver strofe er tittelen til en bok du kan finne i nasjonalbiblioteket. "
    + "Trykk på en strofe for å få mer informasjon om teksten. "
)

corpus = corpus_selection_widget()
if corpus is not None:
    syllable_counts = get_syllable_counts(corpus)
    try:
        poem = get_random_poem(syllable_counts)
    except ValueError:
        st.write(
            "Jeg fant dessverre ingen dikt i dette korpuset :(  \n"
            "Kanskje du må prøve et større korpus."
        )
    else:
        st.markdown(get_bookshelf_html(poem), unsafe_allow_html=True)
        button = st.button(
            "Trykk her for å plukke et nytt tilfeldig dikt", type="primary"
        )

with st.expander("Hva er dette for noe?"):
    st.write(
        "Dette verktøyet lar deg utforske nasjonalbibliotekets samling ved å"
        + " sette sammen [haikuinspirerte](https://snl.no/haiku) dikt av tilfeldige "
        + " boktitler fra et korpus. Titlene er valgt slik at første strofe skal ha fem"
        + " stavelser, andre strofe skal ha syv stavelser, og tredje strofe skal ha fem"
        + " stavelser. \n\n"
        + " Merk at antall stavelser er kun estimert basert på antall vokaler"
        + " og vil ikke alltid være riktig."
        + " Estimatet vil for eksempel ikke ta hensyn til tall eller diftonger. \n\n"
        + " 'Titteldiktene' er også kun inspirert av strukturen til haiku og" 
        + " følger ikke reglene til tradisjonell haiku. "
    )
