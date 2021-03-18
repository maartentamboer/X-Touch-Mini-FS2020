# Developing
To develop on the project, perform the following steps.

## Code
TBD

## Documentation
The documentation uses [mkdocs](https://www.mkdocs.org/) with the [material](https://squidfunk.github.io/mkdocs-material/) theme. The table of contents is managed in `mkdocs.yml`, all the pages are located in the `docs` subfolder. To preview the documentation on your own system you need to have Python installed and in the `PATH`. After that run the following commands once to install mkdocs.
```
pip install mkdocs
pip install mkdocs-material
```
After that the documentation can be generated with the command below. This will host a website on localhost that is automatically updated when you save a file.
```
mkdocs serve
```