FROM python:3.8

RUN apt update -y && apt install -y nano pipenv
RUN cd /opt && git clone https://github.com/openjusticebe/be_law_tools
WORKDIR /opt/be_law_tools/
RUN pipenv install --dev --system --deploy

ENTRYPOINT ["python", "/opt/be_law_tools/justel2md.py"]
