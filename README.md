# REF-2021-data-explorer

Data explorer app written with Streamlit

The app hosted on Azure is pubicly available at [https://ref2021explorer.azurewebsites.net].

## Setup

Create a virtual environment and install requirements

```shell
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run src/Home.py
```


## Running using Docker

Building the image: `docker build -t ref2021explorer .`

Running the image: `docker run -p 8501:8501 ref2021explorer`. This binds the
exposed port 8501 of the Docker container to port 8501 of the host; the
Streamlit application is then visible at http://localhost:8501

## Updating data

The app is set with the default `None` value for the `ttl` (see [st.cache_data](https://docs.streamlit.io/library/api-reference/performance/st.cache_data)). This means that the app has to be restarted every time the data files in [ref-2021-analysis repository](https://github.com/softwaresaved/ref-2021-analysis) are updated.

## Chat interface

To run the experimental REFChat interface, you will need an OpenAI key.

* Set up billing: https://platform.openai.com/account/billing/overview
* Set usage limits! https://platform.openai.com/account/limits
* Get your API key: https://platform.openai.com/api-keys

Once you have the API key, before running Streamlit as in the
above snippet, export the key to your environment:
```shell
export OPENAI_API_KEY=<your key here>
```

Currently REFChat is **experimental**. Always check the results before
using it in a report. REFChat displays the SQL query used to perform the
data analysis; if the query is correct, the resulting data will be as
well.
