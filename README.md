## Belgian Law Tools
This repository is under construction, tests are going on.

For the moment, work is concentrated on the tool justel2md.py, converting
text resources from [justel](https://www.ejustice.just.fgov.be/cgi_loi/loi.pl) to markdown.

See **example.md** for an example. (Original is: [here](http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel) )

### Usage
This toolset needs python3.8 and pipenv
After cloning, do:

```bash
> cd [project_dir]
> pipenv install --dev
> pipenv run ./justel2md.py -c > EXAMPLE.md

```
