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