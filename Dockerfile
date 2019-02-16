# Copyright (c) Mike Harmon.
# Distributed under the terms of the Modified BSD License.

FROM jupyter/base-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    git \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-xetex \
    unzip \
    vim \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER $NB_UID

RUN mkdir /home/$NB_USER/greenbuildings \
          /home/$NB_USER/greenbuildings/data \
          /home/$NB_USER/greenbuildings/images && \
    fix-permissions /home/$NB_USER


COPY data/nyc-zip-code-tabulation-areas-polygons.geojson          /home/$NB_USER/greenbuildings/data/
COPY data/nyc_benchmarking_disclosure_data_reported_in_2016.xlsx  /home/$NB_USER/greenbuildings/data/
COPY data/neighborhoods.pkl                                       /home/$NB_USER/greenbuildings/data/
COPY requirements.txt                                             /home/$NB_USER/greenbuildings/
COPY Local_Law_84_Analysis.ipynb                                  /home/$NB_USER/greenbuildings/
COPY *.py                                                         /home/$NB_USER/greenbuildings/
COPY images/*.png                                                 /home/$NB_USER/greenbuildings/images/

RUN conda install python==3.6.6 geopandas==0.3.0 && \
    pip install -r /home/$NB_USER/greenbuildings/requirements.txt


# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions /home/$NB_USER

USER $NB_UID

