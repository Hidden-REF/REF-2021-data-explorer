""" Codebook for REF 2021 data """


COL_INST_NAME = "Institution name"
COL_OUTPUT_TITLE = "Title"
COL_OUTPUT_PLACE = "Place"
COL_OUTPUT_PUBLISHER = "Publisher"
COL_OUTPUT_VOL_TITLE = "Volume title"
COL_OUTPUT_VOL_NO = "Volume"
COL_OUTPUT_ISSUE = "Issue"
COL_OUTPUT_FIRST_PAGE = "First page"
COL_OUTPUT_ARTICLE_NO = "Article number"
COL_OUTPUT_ISBN = "ISBN"
COL_OUTPUT_ISSN = "ISSN"
COL_OUTPUT_DOI = "DOI"
COL_OUTPUT_PATENT_NO = "Patent number"
COL_OUTPUT_MONTH = "Month"
COL_OUTPUT_URL = "URL"
COL_OUTPUT_SUPP = "Supplementary information"
COL_IMPACT_SUMMARY = "1. Summary of the impact"
COL_IMPACT_DETAILS = "4. Details of the impact"

CATEGORY_FIELDS_EXCLUDE_CHARTS = []

FILEDS_TO_NOT_DISPLAY = [
    COL_OUTPUT_TITLE,
    COL_OUTPUT_PUBLISHER,
    COL_OUTPUT_ISBN,
    COL_OUTPUT_ISSN,
    COL_OUTPUT_DOI,
    COL_OUTPUT_PATENT_NO,
    COL_OUTPUT_URL,
    COL_OUTPUT_PLACE,
    COL_OUTPUT_VOL_NO,
    COL_OUTPUT_VOL_TITLE,
    COL_OUTPUT_ISSUE,
    COL_OUTPUT_FIRST_PAGE,
    COL_OUTPUT_ARTICLE_NO,
    COL_OUTPUT_MONTH,
    COL_OUTPUT_SUPP,
    COL_IMPACT_SUMMARY,
    COL_IMPACT_DETAILS,
]

ADDED_SUFFIXES = ["(added)", "(binned)"]

ADDED_DESCRIPTIONS = {
    "Total number of doctoral degrees awarded  (added)": "sum of doctoral degrees awarded from 2013 to 2019",
    "Environment evaluation - 1 star (binned)": (
        "binned percentages for the environment evaluation for 1*;"
        " applies respectivelly to all `Environment evaluation` fields below"
    ),
    "Impact evaluation - 1 star (binned)": (
        "binned percentages for the impact case studies evaluation for 1*;"
        " applies respectivelly to all `Impact evaluation` fields below"
    ),
    "Outputs evaluation - 1 star (binned)": (
        "binned percentages for the outputs evaluation for 1*;"
        " applies respectivelly to all `Outputs evaluation` fields below"
    ),
    "Overall evaluation - 1 star (binned)": (
        "binned percentages for the outputs evaluation for 1*;"
        " applies respectivelly to all `Overall evaluation` fields below"
    ),
    "Research group submissions (added)": "number of research group submissions",
    "Output submissions (added)": "number of output submissions",
    "Output submissions - Chapter in book (added)": (
        "number of output submissions for chapter in book;"
        " applies respectivelly to all `Output submissions` fields below"
    ),
    "Impact case study submissions (added)": "number of impact case study submissions",
}
