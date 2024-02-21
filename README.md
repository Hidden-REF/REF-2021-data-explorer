[![Pylint](https://github.com/Hidden-REF/REF-2021-data-explorer/actions/workflows/pylint.yml/badge.svg)](https://github.com/Hidden-REF/REF-2021-data-explorer/actions/workflows/pylint.yml)

# Streamlit app to visualise and explore the REF2021 data

The app is hosted on Azure and is publicly available at [https://ref2021explorer.azurewebsites.net](https://ref2021explorer.azurewebsites.net).

## Data files

The data used by this app has been sourced from the [https://results2021.ref.ac.uk/e]({REF2021_URL})(accessed 2023/08/10) and processed in python using [ref-2021-analysis repository]({https://github.com/softwaresaved/ref-2021-analysis}). More details about the processing are also available on the home page of the app.

Processed data and processing logs are stored in the processing repository and retrieved by the app at runtime. The app is set with the default `None` value for the `ttl` (see [st.cache_data](https://docs.streamlit.io/library/api-reference/performance/st.cache_data)). This means that the app has to be restarted every time the data files in [ref-2021-analysis repository](https://github.com/softwaresaved/ref-2021-analysis) are updated.

## Chat interface

The REFChat is **experimental**. Always check the results before
using it in a report. REFChat displays the SQL query used to perform the
data analysis; if the query is correct, the resulting data will be as
well.

To run the experimental REFChat interface, you will need an OpenAI key.

* Set up billing: https://platform.openai.com/account/billing/overview
* Set usage limits! https://platform.openai.com/account/limits
* Get your API key: https://platform.openai.com/api-keys

Once you have the API key, if you want to run the app locally (see below), first export the key to your environment before running the app:
```shell
export OPENAI_API_KEY=<your key here>
```

Alternatively, you can enter the OpenAI key in the sidebar of the running app, either locally or on Azure.

## Setup to run locally

Create a virtual environment, install requirements:

```shell
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run src/Home.py
```

Alternatively, to run the docker image:

```shell
docker build -t ref2021explorer .`
`docker run -p 8501:8501 ref2021explorer`
```

This binds the exposed port 8501 of the Docker container to port 8501 of the host; the Streamlit application is then visible at http://localhost:8501
