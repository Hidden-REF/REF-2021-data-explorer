# pylint: disable=E0401
""" Codebook for REF 2021 data """


COL_INST_NAME = "Institution name"
COL_MAIN_PANEL_NAME = "Main panel name"
COL_UNIT_OF_ASSESSMENT = "Unit of assessment name"
COL_MULTIPLE_SUBMISSION_NAME = "Multiple submission name"
COL_MULIPLE_SUBMISSION_LETTER = "Multiple submission letter"
COL_JOINT_SUBMISSION = "Joint submission"
COL_TOTAL_FTE_JOINT = "Total FTE of submitted staff for joint submission"
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

FIELDS_TO_NOT_DISPLAY = [
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


COLUMNS_UNIT_ENVIRONMENT_STATEMENTS = [
    "Unit context and structure, research and impact strategy",
    "People",
    "Income, infrastructure and facilities",
    "Collaboration and contribution to the research base, economy and society",
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
