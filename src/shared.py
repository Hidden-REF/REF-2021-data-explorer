""" Shared text for the app. """

REF2021_URL = "https://results2021.ref.ac.uk/"
PROC_URL = "https://github.com/softwaresaved/ref-2021-analysis"
DATA_INFO = f"The data used in this app is from the [REF 2021 website]({REF2021_URL})"\
            f" (accessed 2023/08/10) and has been processed with [{PROC_URL}]({PROC_URL})"
DATA_EXPORT_FORMATS = ["CSV"]
PROC_TEXT = "Processing request..."
# prompts
DISTRIBUTION_SELECT_PROMPT = "Select column to plot"
GROUPED_DISTRIBUTION_SELECT_PROMPT = "Select columns to plot"
BIN_NUMBER_PROMPT = "Select number of bins"
SELECT_STATS_PROMPT = "Select what to plot"
SELECT_DATA_RANGE_PROMPT = "Select data range"
EXCLUDE_NEGATIVE_PROMPT = "Exclude negative values"
# headers
header_style = "######"
VISUALISE_HEADER = f"{header_style} Visualise data"
EXPLORE_HEADER = f"{header_style} Select and explore data"
# tabs headers
DISTRIBUTIONS_TAB_HEADER = "Distributions"
GROUPED_DISTRIBUTIONS_TAB_HEADER = "Grouped distributions"
HISTOGRAMS_TAB_HEADER = "Histograms"
SHOW_SELECTED_TAB_HEADER = "Show selected data"
VISUALISE_SELECTED_TAB_HEADER = "Visualise selected data"
# buttons
DOWNLOAD_SELECTED_DATA_BUTTON = "Download selected data as csv"
# warnings
NO_SELECTED_RECORDS_WARNING = "No records match the selection"
NOT_SUITABLE_FOR_HISTOGRAM_WARNING = "The data is not suitable for a histogram"
