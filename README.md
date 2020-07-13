## Belgian Law Tools
This is a toolset allowing for extraction of belgian law, from official sources (though the only legal version remains the paper one).

For the moment, work is concentrated on the tool justel2md.py, which extracts
text resources from [justel](https://www.ejustice.just.fgov.be/cgi_loi/loi.pl) and converts them to markdown.

See **example.md** for an example. (Original is: [here](http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel) )

<center> 🚧This repo is still under construction, markdown conversion is still in an early stage 🚧</center>

### Why Markdown ?
It's a simple formatting language, able to achieve a nice result considering the rudimentary source.

It's also readily convertible to other formats, while being human readable in its original form, not needing
any specialized toolset other then a basic text editor.

### Installation
#### Locally
Once the repository cloned locally, and you have python3.8 and pipenv installed:
```bash
# Go to project directory
> cd [project_dir]

# Install python inventory
> pipenv install --dev
```
Present tool has only been used, and tested, on GNU/Linux (Debian).


#### With Docker

Compile it then run it:
```bash
# Go to project directory
> cd [project_dir]

# Compile it with
> docker build -t be_law_tools .
```

### Usage
This toolset needs python3.8 and pipenv.
```bash
Usage: justel2md.py scan [OPTIONS]

  Generate a url for each date within given interval, and scan for useable
  documents.

Options:
  -s, --start-date TEXT
  -e, --end-date TEXT
  -i, --interval [year|month|day]
  -t, --doc-type [constitution|loi|decret|ordonnance|arrete|grondwet|wet|decreet|ordonnantie|besluit]
  -o, --output-dir TEXT
  --help                          Show this message and exit.
```


#### Extraction
##### Without Docker
To extract, provide a start (optionally end date and an output dir):
```bash
# Quick extract last year to ./ouput directory
> pipenv run ./justel2md.py --debug scan -s 2020-01-01

# Specific extraction
> pipenv run ./justel2md.py --debug scan -s 1804-01-01 -e 1850-01-01 -o /some_output_dir
```

##### Using Docker
```bash
# Then run with
> docker run -it --rm -v /some_output_dir:/opt/be_law_tools/output be_law_tools --debug scan -s 2020-01-01
```

In a dev environnement for local tests before commiting, map your local repo like this:
```bash
# MY_WORKDIR being you local repo
> docker run -it --rm -v /MY_WORKDIR:/opt/be_law_tools/ be_law_tools --debug scan -s 2020-01-01
```

### Test
```bash
> cd [project_dir]
> pipenv install --dev
> pipenv run ./justel2md.py test -c > EXAMPLE.md
```

Toolset development is **behaviour driven**. As such, tests and scenarios can be found in `tests/behave`.
To execute the tests:
```bash
# Use makefile
> make behave

# Run behave directly
> pipenv run behave tests/behave
```
