""" Shared text for the app. """

# settings
LAYOUT = "wide"
REPO_URL = "https://github.com/Hidden-REF/REF-2021-data-explorer"

# titles
HOME_TITLE = "REF 2021 Data Explorer"
RESEARCH_GROUPS_TITLE = "Research Groups"
OUTPUTS_TITLE = "Outputs"
IMPACT_CASE_STUDIES_TITLE = "Impact Case Studies"
DOCTORAL_DEGREES_TITLE = "Doctoral Degrees Awarded"
RESEARCH_INCOME_TITLE = "Research Income"
RESEARCH_INCOME_IN_KIND_TITLE = "Research Income in Kind"
RESULTS_TITLE = "Results"

# home page
REF2021_URL = "https://results2021.ref.ac.uk/"
PROC_URL = "https://github.com/softwaresaved/ref-2021-analysis"
DATA_SOURCE_HEADER = "Data source"
DATA_SOURCE_TEXT = f"The data used in this app is from the [REF 2021 website]({REF2021_URL})"\
                   f" (accessed 2023/08/10) and has been processed with [{PROC_URL}]({PROC_URL})"
ABOUT_HEADER = "About the REF 2021 Explorer"
WARNING_TEXT = \
    """
    This site is currently under construction.

    Changes will be made on a frequent basis.

    Until we announce that the website is complete, please do not use any of the results from
    analysis you conduct on this site unless you have independently verified the results.

    """
ABOUT_TEXT = \
    """
    The Research Excellent Framework (REF) is the UK's approach to assessing
    the excellence of UK research. It employs a process of
    expert review across all UK universities for 34 subject-based units of assessment. The
    REF is conducted around every seven years, with the most recent taking place in 2021.

    All of the data on this website is published openly on the REF 2021 website.
    This site is dedicated to understanding the results of the REF 2021 by
    providing users with the ability to analyse and search the REF data.

    Submissions for REF 2021 consisted of data sets on
    - Research Groups
    - Outputs (e.g. journal articles, books, datasets, etc.)
    - Impact Case Studies
    - Doctoral Degrees Awarded
    - Research Income
    - Research Income in Kind
    - Research Environment

    The website currently allows for any of the above information to be analysed and visualised.
    Select a data set from the side bar, then use the main section of the website
    to choose elements of the data set to visualise.
    You can also compare elements of the data set and visualise the results.
    """

# formats
DATA_EXPORT_FORMATS = ["CSV"]

# feedback
PROC_TEXT = "Processing request..."

# labels
RECORDS_LABEL = "Records"
INSTITUTIONS_LABEL = "Institutions"

# prompts
DISTRIBUTION_SELECT_PROMPT = "Select column to plot"
GROUPED_DISTRIBUTION_SELECT_PROMPT = "Select columns to plot"
BIN_NUMBER_PROMPT = "Select number of bins"
SELECT_STATS_PROMPT = "Select what to plot"
SELECT_DATA_RANGE_PROMPT = "Select data range"
EXCLUDE_NEGATIVE_PROMPT = "Exclude negative values"

# headers
header_style = "######"
DESCRIBE_HEADER = f"{header_style} Data description"
VISUALISE_HEADER = f"{header_style} Visualise data"
EXPLORE_HEADER = f"{header_style} Select and explore data"

# titles
title_style = "#####"
COLUMNS_TITLE = f"{header_style} Data columns"

# tabs headers
DISTRIBUTIONS_TAB_HEADER = "Distributions (categorical)"
GROUPED_DISTRIBUTIONS_TAB_HEADER = "Grouped distributions (categorical)"
HISTOGRAMS_TAB_HEADER = "Histograms"
SHOW_SELECTED_TAB_HEADER = "Show selected data"
VISUALISE_SELECTED_TAB_HEADER = "Visualise selected data"

# buttons
DOWNLOAD_SELECTED_DATA_BUTTON = "Download selected data as csv"

# warnings
NO_SELECTED_RECORDS_WARNING = "No records match the selection"
NOT_SUITABLE_FOR_HISTOGRAM_WARNING = "The data is not suitable for a histogram"

# chat
CHAT_TITLE = "Chat"
CHAT_SIDEBAR_TEXT = """
## REFChat

REFChat is an **experimental** interface utilising GPT models to provide a
natural language query to the the REF 2021 dataset. You can ask it questions
such as:

> Show me universities with units that achieved more than 75% of outputs in
> their overall evaluation 4 stars

:warning: REFChat may give **incorrect or misleading** answers. Check the
generated query before using in reports!

"""
