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
COL_RESULTS_DEGREES = "Total number of doctoral degrees awarded  (added)"
COL_RESULTS_EVALUATION_ENV_ONE_STAR_BINNED = "Environment evaluation - 1 star (binned)"
COL_RESULTS_EVALUATION_IMPACT_ONE_STAR_BINNED = "Impact evaluation - 1 star (binned)"
COL_RESULTS_EVALUATION_OUTPUTS_ONE_STAR_BINNED = "Outputs evaluation - 1 star (binned)"
COL_RESULTS_EVALUATION_OVERALL_ONE_STAR_BINNED = "Overall evaluation - 1 star (binned)"
COL_RESULTS_GROUPS_SUBMISSIONS = "Research group submissions (added)"
COL_RESULTS_OUTPUTS_SUBMISSIONS = "Output submissions (added)"
COL_RESULTS_OUTPUTS_SUBMISSIONS_CHAPTER_IN_BOOK = (
    "Output submissions - Chapter in book (added)"
)
COL_RESULTS_IMPACT_SUBMISSIONS = "Impact case study submissions (added)"
COL_RESULTS_UNIT_ENV_CONTEXT = (
    "Unit context and structure, research and impact strategy (added)"
)
COL_RESULTS_UNIT_ENV_PEOPLE = "People (added)"
COL_RESULTS_UNIT_ENV_INCOME_ETC = "Income, infrastructure and facilities (added)"
COL_RESULTS_UNIT_ENV_COLAB_CONTRIB = (
    "Collaboration and contribution to the research base, economy and society (added)"
)

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
    COL_RESULTS_UNIT_ENV_CONTEXT,
    COL_RESULTS_UNIT_ENV_PEOPLE,
    COL_RESULTS_UNIT_ENV_INCOME_ETC,
    COL_RESULTS_UNIT_ENV_COLAB_CONTRIB,
]

COLUMNS_REDUCED_RESULTS = [
    "Institution name",
    "Main panel name",
    "Unit of assessment name",
    "Multiple submission letter",
    "Multiple submission name",
    "Joint submission",
    "% of eligible staff submitted",
    "Total FTE of submitted staff for joint submission",
    "Environment evaluation - 1 star",
    "Environment evaluation - 1 star (binned)",
    "Environment evaluation - 2 stars",
    "Environment evaluation - 2 stars (binned)",
    "Environment evaluation - 3 stars",
    "Environment evaluation - 3 stars (binned)",
    "Environment evaluation - 4 stars",
    "Environment evaluation - 4 stars (binned)",
    "Environment evaluation - Unclassified",
    "Environment evaluation - Unclassified (binned)",
    "Impact evaluation - 1 star",
    "Impact evaluation - 1 star (binned)",
    "Impact evaluation - 2 stars",
    "Impact evaluation - 2 stars (binned)",
    "Impact evaluation - 3 stars",
    "Impact evaluation - 3 stars (binned)",
    "Impact evaluation - 4 stars",
    "Impact evaluation - 4 stars (binned)",
    "Impact evaluation - Unclassified",
    "Impact evaluation - Unclassified (binned)",
    "Outputs evaluation - 1 star",
    "Outputs evaluation - 1 star (binned)",
    "Outputs evaluation - 2 stars",
    "Outputs evaluation - 2 stars (binned)",
    "Outputs evaluation - 3 stars",
    "Outputs evaluation - 3 stars (binned)",
    "Outputs evaluation - 4 stars",
    "Outputs evaluation - 4 stars (binned)",
    "Outputs evaluation - Unclassified",
    "Outputs evaluation - Unclassified (binned)",
    "Overall evaluation - 1 star",
    "Overall evaluation - 1 star (binned)",
    "Overall evaluation - 2 stars",
    "Overall evaluation - 2 stars (binned)",
    "Overall evaluation - 3 stars",
    "Overall evaluation - 3 stars (binned)",
    "Overall evaluation - 4 stars",
    "Overall evaluation - 4 stars (binned)",
    "Overall evaluation - Unclassified",
    "Overall evaluation - Unclassified (binned)",
    "Research group submissions (added)",
    "Output submissions (added)",
    "Output submissions - Chapter in book (added)",
    "Output submissions - Journal article (added)",
    "Output submissions - Authored book (added)",
    "Output submissions - Edited book (added)",
    "Output submissions - Exhibition (added)",
    "Output submissions - Performance (added)",
    "Output submissions - Digital or visual media (added)",
    "Output submissions - Conference contribution (added)",
    "Output submissions - Scholarly edition (added)",
    "Output submissions - Other (added)",
    "Output submissions - Working paper (added)",
    "Output submissions - Patent/ published patent application (added)",
    "Output submissions - Composition (added)",
    "Output submissions - Website content (added)",
    "Output submissions - Design (added)",
    "Output submissions - Artefact (added)",
    "Output submissions - Research report for external body (added)",
    "Output submissions - Research data sets and databases (added)",
    "Output submissions - Translation (added)",
    "Output submissions - Software (added)",
    "Output submissions - Devices and products (added)",
    "Impact case study submissions (added)",
    "Total number of doctoral degrees awarded  (added)",
]

ADDED_SUFFIXES = ["(added)", "(binned)"]

ADDED_DESCRIPTIONS = {
    COL_RESULTS_DEGREES: "total doctoral degrees awarded from 2013 to 2019",
    COL_RESULTS_EVALUATION_ENV_ONE_STAR_BINNED: (
        "binned percentages for the environment evaluation for 1*;"
        " applies respectivelly to all `Environment evaluation` fields below"
    ),
    COL_RESULTS_EVALUATION_IMPACT_ONE_STAR_BINNED: (
        "binned percentages for the impact case studies evaluation for 1*;"
        " applies respectivelly to all `Impact evaluation` fields below"
    ),
    COL_RESULTS_EVALUATION_OUTPUTS_ONE_STAR_BINNED: (
        "binned percentages for the outputs evaluation for 1*;"
        " applies respectivelly to all `Outputs evaluation` fields below"
    ),
    COL_RESULTS_EVALUATION_OVERALL_ONE_STAR_BINNED: (
        "binned percentages for the outputs evaluation for 1*;"
        " applies respectivelly to all `Overall evaluation` fields below"
    ),
    COL_RESULTS_GROUPS_SUBMISSIONS: "number of research group submissions",
    COL_RESULTS_OUTPUTS_SUBMISSIONS: "number of output submissions",
    COL_RESULTS_OUTPUTS_SUBMISSIONS_CHAPTER_IN_BOOK: (
        "number of output submissions for chapter in book;"
        " applies respectivelly to all `Output submissions` fields below"
    ),
    COL_RESULTS_IMPACT_SUBMISSIONS: "number of impact case study submissions",
    COL_RESULTS_UNIT_ENV_CONTEXT: (
        "unit context and structure, research and impact strategy section"
        " from the unit environment statement; applies respectively to the next three fields"
    ),
}
