""" Shared text for the app. """
import streamlit as st
import read_write as rw

# settings
LAYOUT = "wide"
REPO_URL = "https://github.com/Hidden-REF/REF-2021-data-explorer"

# titles
PAGE_TITLES = {
    "home": "REF 2021 Data Explorer",
    "groups": "Research Groups",
    "outputs": "Outputs",
    "impacts": "Impact Case Studies",
    "degrees": "Doctoral Degrees Awarded",
    "income": "Research Income",
    "income_in_kind": "Research Income in Kind",
    "results": "Results",
    "results_chat": "Results Chat",
}


# home page
REF2021_URL = "https://results2021.ref.ac.uk/"
PROC_URL = "https://github.com/softwaresaved/ref-2021-analysis"
DATA_SOURCE_HEADER = "Data"
DATA_SOURCE_TEXT = f"""
The raw data on this website has been sourced from the [REF 2021 website]({REF2021_URL})
(accessed 2023/08/10). The raw data was processed to convert from raw
data formats (excel and pdf files) to parquet files, interpret codes,
fix alignment issues, add aggregate variables, change data structure to make
it more suitable for analyses and visualisations, and remove some columns
that were not useful for analyses and visualisations.

The python code used to process the raw data is available from [{PROC_URL}]({PROC_URL}).
Processing logs are also available to browse on each page and
give details of the processing steps taken. When fields were added
or the structure of the raw data was changed these steps
are described in summary at the top of the page as well as in the logs.
The fields added in the processing have the suffixes ` (added)` or ` (binned)`
in the field names.
"""

WARNING_TEXT = """
    This site is currently under construction.

    Changes will be made on a frequent basis.

    Until we announce that the website is complete, please do not use any of the results from
    analysis you conduct on this site unless you have independently verified the results.

    """
ABOUT_TEXT = """
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

INITIAL_SIDEBAR_STATE = "expanded"
MENU_ITEMS = {
    "Get Help": REPO_URL,
    "Report a bug": REPO_URL,
    "About": DATA_SOURCE_TEXT,
}

# feedback
PROC_TEXT = "Processing request..."

# labels
RECORDS_LABEL = "Records"
INSTITUTIONS_LABEL = "Institutions"
CATEGORY_LABEL_SINGULAR = "level"
CATEGORY_LABEL_PLURAL = "levels"
OBJECT_LABEL = "string"

# prompts
DISTRIBUTION_SELECT_PROMPT = "Select the categorical field of interest"
GROUPED_DISTRIBUTION_SELECT_PROMPT = "Select columns to plot"
BIN_NUMBER_PROMPT = "Select number of bins"
SELECT_STATS_PROMPT = "Select what to plot"
SELECT_DATA_RANGE_PROMPT = "Select data range"
EXCLUDE_NEGATIVE_PROMPT = "Exclude negative values"
SIDEBAR_HOME_PROMPT = """
Select a data set from the side bar, then use the main section of the website
to choose elements of the data set to visualise for the entire data set or a subset.
"""

# headers
HEADER_STYLE = "######"

DESCRIBE_HEADER = f"{HEADER_STYLE} :book: Browse the data fields and processing logs"
VISUALISE_HEADER = f"{HEADER_STYLE} :bar_chart: Visualise data "
EXPLORE_HEADER = f"{HEADER_STYLE} :mag: :bar_chart: Select and explore data"

# titles
TITLE_STYLE = "#####"
ADDED_TITLE = f"{TITLE_STYLE} Fields added in processing"
FIELDS_TITLE = f"{TITLE_STYLE} Fields"
LOGS_TITLE = f"{TITLE_STYLE} Processing logs"

# tabs headers
DISTRIBUTIONS_TAB_HEADER = "Distributions"
GROUPED_DISTRIBUTIONS_TAB_HEADER = "Grouped distributions (categorical)"
HISTOGRAMS_TAB_HEADER = "Histograms"
SHOW_SELECTED_TAB_HEADER = "Show selected data"
VISUALISE_SELECTED_TAB_HEADER = "Visualise selected data"

# tabs descriptions
DISTRIBUTIONS_TAB_DESCRIPTION = """
Explore the distribution of record numbers across different levels of the categorical fields in this dataset. 
"""

# buttons
DOWNLOAD_SELECTED_DATA_BUTTON = "Download selected data as csv"
CLEAR_CHAT_BUTTON = "Clear chat history"

# warnings
NO_SELECTED_RECORDS_WARNING = "No records match the selection"
NOT_SUITABLE_FOR_HISTOGRAM_WARNING = "The data is not suitable for a histogram"
PREFIX_WARNING = "Warning: "

# descriptions
RESULTS_DESCRIPTION = """\
The Results data was pivoted by the values of the `Profile` field
to convert the data to a wide format with one (institution, unit of assessment)
pair per row to enable more flexible analyses and visualisations.
"""

GROUPS_DESCRIPTION = f"""\
{PREFIX_WARNING}Information was not available to decode the **Research group code** field.
"""

# chat
CHAT_TITLE = "Results Chat"
NO_ANSWER = "Sorry, I do not know the answer to that question."
TOKEN_NOTAVAILABLE = ":warning: Open AI token not available for the chat"
OPENAI_KEY_PROMPT = "Enter your OpenAI API Key to use the chat"
OPENAI_KEY_PLACEHOLDER = "Paste your OpenAI API key here (sk-...)"
OPENAI_KEY_HELP = (
    "You can get your API key from https://platform.openai.com/account/api-keys"
)
OPENAI_KEY_ERROR = "OpenAI authentication failed, try setting another key"

CHAT_PROMPT = f"""

You are a research assistant for the Research Excellence Framework 2021. Data
is stored in parquet format within the '{rw.CHAT_DB}' table. You must respond to questions
with a valid SQL query. Do not return any natural language explanation, only
the SQL query. Ensure that columns with spaces are quoted in the query.

If you are filtering using a WHERE clause, you must SELECT the columns being
filtered.
"""
CHAT_PROMPT = (
    CHAT_PROMPT
    + """

The dataset has the following schema:

{schema}
"""
)

CHAT_WARNING_TEXT = """
This is an **experimental** interface utilising GPT models to provide a
natural language query to the the REF 2021 dataset.

This chat may give **incorrect or misleading** answers. Check the
generated query before using in reports!
"""

CHAT_SIDEBAR_TEXT = """

You can ask questions such as:

> Show me universities with units that achieved more than 75% of outputs in
> their overall evaluation 4 stars

"""


def page_config(page):
    """Set the page configuration.
    
    Args:
        page (str): The page name.
    """

    st.set_page_config(
        page_title=PAGE_TITLES[page],
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
        menu_items=MENU_ITEMS,
    )


def sidebar_content(path):
    """Add logos to the sidebar."""
    with st.sidebar:
        cols = st.columns([0.35, 0.65])
        with cols[0]:
            st.image("assets/rse_skyline_reverse.png")
        with cols[1]:
            st.image("assets/SSI_PRIMARY-LOGO.svg")

        if path != "results_chat":
            st.warning(WARNING_TEXT, icon="⚠️")
            if path == "home":
                st.markdown(SIDEBAR_HOME_PROMPT)


def prepare_page(page):
    """Prepare the page.

    Args:
        page (str): The page name.

    Returns:
        tuple: The data set and logs.
    """

    page_config(page)
    sidebar_content(page)
    st.title(PAGE_TITLES[page])
    (dset, logs) = rw.get_dataframes(page)

    return (dset, logs)


def sidebar_settings():
    """Set the sidebar settings."""

    # css = """
    # [data-testid="stSidebar"] {
    # min-height: 50vh
    # }
    # """
    # st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    css = """
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """
    st.markdown(css, unsafe_allow_html=True)
