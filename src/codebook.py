""" Codebook for REF 2021 data """
import pandas as pd


# about the ref process
COL_PANEL_CODE = 'Main panel code'
COL_PANEL_NAME = 'Main panel'
COL_UOA_NUMBER = 'Unit of assessment number'
COL_UOA_NAME = 'Unit of assessment'
# about the institution etc
COL_INST_CODE = 'Institution UKPRN code'
COL_INST_NAME = 'Institution'
COL_RG_CODE = 'Research group code'
COL_RG_NAME = 'Research group'
# about the submissions
COL_MULT_SUB_LETTER = 'Multiple submission letter'
COL_MULT_SUB_NAME = 'Multiple submission name'
COL_JOINT_SUB = 'Joint submission'
# about the submissions
COL_MULT_SUB_LETTER = 'Multiple submission letter'
COL_MULT_SUB_NAME = 'Multiple submission name'
COL_JOINT_SUB = 'Joint submission'
# about the degrees awarded
COL_DEGREES_2013 = 'Number of doctoral degrees awarded in academic year 2013'
COL_DEGREES_2014 = 'Number of doctoral degrees awarded in academic year 2014'
COL_DEGREES_2015 = 'Number of doctoral degrees awarded in academic year 2015'
COL_DEGREES_2016 = 'Number of doctoral degrees awarded in academic year 2016'
COL_DEGREES_2017 = 'Number of doctoral degrees awarded in academic year 2017'
COL_DEGREES_2018 = 'Number of doctoral degrees awarded in academic year 2018'
COL_DEGREES_2019 = 'Number of doctoral degrees awarded in academic year 2019'
COL_DEGREES_TOTAL = 'Total number of doctoral degrees awarded'
# about the outputs
COL_OUTPUT_TYPE_CODE = 'Output type code'
COL_OUTPUT_TYPE_NAME = 'Output type'
COL_OUTPUT_RG_NAME = 'Research group'
COL_OPEN_ACCESS = 'Open access status'
COL_OUTPUT_TITLE = 'Title'
COL_OUTPUT_PLACE = 'Place'
COL_OUTPUT_PUBLISHER = 'Publisher'
COL_OUTPUT_VOL_TITLE = 'Volume title'
COL_OUTPUT_VOL_NO = 'Volume'
COL_OUTPUT_ISSUE = 'Issue'
COL_OUTPUT_FIRST_PAGE = 'First page'
COL_OUTPUT_ARTICLE_NO = 'Article number'
COL_OUTPUT_ISBN = 'ISBN'
COL_OUTPUT_ISSN = 'ISSN'
COL_OUTPUT_DOI = 'DOI'
COL_OUTPUT_PATENT_NO = 'Patent number'
COL_OUTPUT_MONTH = 'Month'
COL_OUTPUT_URL = 'URL'
COL_OUTPUT_NON_ENGLISH = 'Non-English'
COL_OUTPUT_SUPP = 'Supplementary information'
COL_OUTPUT_CITATIONS = 'Citations applicable'
COL_OUTPUT_CROSS_REFERRAL = 'Cross-referral requested'
COL_OUTPUT_INTERDISCIPLINARY = 'Interdisciplinary'
COL_OUTPUT_FORENSIC_SCIENCE = 'Forensic science'
COL_OUTPUT_CRIMINOLOGY = 'Criminology'
COL_OUTPUT_DOUBLE_WEIGHTING = 'Propose double weighting'
COL_OUTPUT_RESERVE_OUTPUT = 'Is reserve output'
COL_OUTPUT_DELAYED = 'Delayed by COVID19'
# about the impact case studies
COL_IMPACT_TITLE = 'Title'
COL_IMPACT_FUNDING_PROGS = 'Funding programmes'
COL_IMPACT_FUNDERS = 'Name of funders'
COL_IMPACT_SUMMARY = '1. Summary of the impact'
COL_IMPACT_UNDERPIN_RESEARCH = '2. Underpinning research'
COL_IMPACT_REFERENCES_RESEARCH = '3. References to the research'
COL_IMPACT_DETAILS = '4. Details of the impact'
COL_IMPACT_CORROBORATE = '5. Sources to corroborate the impact'
# about results
COL_RESULTS_FTE_STAFF = 'FTE of submitted staff'
COL_RESULTS_PERC_STAFF_SUBMITTED = '% of eligible staff submitted'
COL_RESULTS_PERC_STAFF_SUBMITTED_BINNED = f"{COL_RESULTS_PERC_STAFF_SUBMITTED} (binned)"
COL_RESULTS_4star = '4 stars'
COL_RESULTS_3star = '3 stars'
COL_RESULTS_2star = '2 stars'
COL_RESULTS_1star = '1 star'
COL_RESULTS_UNCLASSIFIED = 'Unclassified'
COL_RESULTS_4star_BINNED = f"{COL_RESULTS_4star} (binned)"
COL_RESULTS_3star_BINNED = f"{COL_RESULTS_3star} (binned)"
COL_RESULTS_2star_BINNED = f"{COL_RESULTS_2star} (binned)"
COL_RESULTS_1star_BINNED = f"{COL_RESULTS_1star} (binned)"
COL_RESULTS_UNCLASSIFIED_BINNED = f"{COL_RESULTS_UNCLASSIFIED} (binned)"

# value to add if no entry in the data
VALUE_ADDED_NOT_SPECIFIED = 'Not specified'

enum_values = {
    # source: website
    COL_PANEL_NAME: {
        "A": "Medicine, health and life sciences",
        "B": "Physical sciences, engineering and mathematics",
        "C": "Social sciences",
        "D": "Arts and humanities"
        },
    # source: https://results2021.ref.ac.uk/filters/unit-of-assessment
    COL_UOA_NAME: {
        1: 'Clinical Medicine',
        2: 'Public Health, Health Services and Primary Care',
        3: 'Allied Health Professions, Dentistry, Nursing and Pharmacy',
        4: 'Psychology, Psychiatry and Neuroscience',
        5: 'Biological Sciences',
        6: 'Agriculture, Food and Veterinary Sciences',
        7: 'Earth Systems and Environmental Sciences',
        8: 'Chemistry',
        9: 'Physics',
        10: 'Mathematical Sciences',
        11: 'Computer Science and Informatics',
        12: 'Engineering',
        13: 'Architecture, Built Environment and Planning',
        14: 'Geography and Environmental Studies',
        15: 'Archaeology',
        16: 'Economics and Econometrics',
        17: 'Business and Management Studies',
        18: 'Law',
        19: 'Politics and International Studies',
        20: 'Social Work and Social Policy',
        21: 'Sociology',
        22: 'Anthropology and Development Studies',
        23: 'Education',
        24: 'Sport and Exercise Sciences, Leisure and Tourism',
        25: 'Area Studies',
        26: 'Modern Languages and Linguistics',
        27: 'English Language and Literature',
        28: 'History',
        29: 'Classics',
        30: 'Philosophy',
        31: 'Theology and Religious Studies',
        32: 'Art and Design: History, Practice and Theory',
        33: 'Music, Drama, Dance, Performing Arts, Film and Screen Studies',
        34: 'Communication, Cultural and Media Studies, Library and Information Management'
    },
    # source: https://results2021.ref.ac.uk/outputs
    COL_OUTPUT_TYPE_NAME: {
        'A': 'Authored book',
        'B': 'Edited book',
        'C': 'Chapter in book',
        'D': 'Journal article',
        'E': 'Conference contribution',
        'F': 'Patent/ published patent application',
        'G': 'Software',
        'H': 'Website content',
        'I': 'Performance',
        'J': 'Composition',
        'K': 'Design',
        'L': 'Artefact',
        'M': 'Exhibition',
        'N': 'Research report for external body',
        'P': 'Devices and products',
        'Q': 'Digital or visual media',
        'R': 'Scholarly edition',
        'S': 'Research data sets and databases',
        'T': 'Other',
        'U': 'Working paper',
        'V': 'Translation'
    },
    # source: info/submission_system_data_requirements/import_templates/ref2021schema-0920.json
    COL_OPEN_ACCESS: {
        1: "Compliant",
        2: "Not Compliant",
        3: "Disposit Exception",
        4: "Access Exception",
        5: "Technical Exception",
        6: "Other Exception",
        7: "Out Of Scope",
        8: "Exception Within 3 Months Of Publication"
    }
}

PERCENTAGE_BINS = range(0, 101, 10)


def bin_percentages_labels():
    """ Create bin percentage labels.

        Returns:
            labels (list): list of labels
    """

    bins = PERCENTAGE_BINS
    labels = [f"{bins[i]} to {bins[i+1]} %" for i in range(len(bins)-1)]
    # labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins)-1)]
    # labels[0] = f"[{bins[0]}, {bins[1]}]"

    return labels


def bin_percentages(dset, column, column_binned):
    """ Bin percentages in a column of a dataset.

        Args:
            dset (pandas.DataFrame): dataset
            column (str): column name
            column_binned (str): new column name for the binned column

        Returns:
            dset (pandas.DataFrame): dataset with new column
    """

    labels = bin_percentages_labels()
    dset[column_binned] = pd.cut(dset[column],
                                 bins=PERCENTAGE_BINS,
                                 right=True,
                                 include_lowest=True,
                                 labels=labels
                                 )
    return dset
