# PyDFNotesExtractor

This project pretends to reimplement the pdfannots repo using just PyMuPDF2.
Information about config file, templates and more [here](https://github.com/pho-souza/PyDFannots/blob/main/doc/README.MD)

-----------

To install, use the command:
``python setup.py install``

# Usage

The basic usage is:

``pydfannots -i <input> -o <output>``


```

Flags

Required arguments to extraction:
* <input>  Path to input PDF
* <output>  Path to output in format selected by user.

Flags:
    -h, --help Show context-sensitive help.
    -v, --version   Display current version of pydfannots.
    -ac, --adjust-color Classify colors from annotations. 
    -at, --adjust-text  Adjust text to eliminate hyphens and linebreaks.
    -ad, --adjust-date Adjust date to the format YYYY-MM-DD HH:mm:SS
    -c, --columns   Number of columns of file. Default value: 1
    -tol, --tolerance   Tolerance interval for columns width in percentage of total width. Default is 0.1
    -rg, --reorder-group    Reorder annotations using some criteria.
    -img, --image   Extract rectangle annotation as image.
    -ink, --ink-annotation  Extract ink anotations as image.
    -temp, --template   Select a jinja2 template. Default set to PyDFannots/templates/template_html.html.
    -il, --intersection_level   Level of intersection between text and highlights. Value between 0 and 1. Default set to 0.1.
    -f, --format    Format to export file. Default set to "". Support to json and csv.
    -il, --intersection-level   Level of intersection between text and highlights. Value between 0 and 1. Default set to 0.1.
    -it, --import-template  Local templates to be imported into program folder.
    -dt, --delete-template Templates to be removed from templates folder.
    -cfg, --config  User defined default configs.

-ad, -at, -at, -ink and -img are set True by default. If you want to disable some o them, use the flags:

Negative flags:
    -nad, --no-adjust-date  Disable -ad flag.
    -nat, --no-adjust-text  Disable -at flag.
    -nac, --no-adjust-color  Disable -ac flag.
    -nink, --no-ink-annotation  Disable -ink flag.
    -nimg, --no-image  Disable -img flag.

```

---------------

# Sample output

Examples of usage:

## Json 

For export json file
``pydfannots -i tests/PDF_WIKI.pdf -o tests/output/PDF_WIKI.json -f json``

The file is stored [here](tests/PDF_WIKI.pdf)

The result of the first and last annotations is:

```json
[
    {
        "type": "Highlight",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.06354998069789362,
            0.10534321117787815,
            0.0844559146640051
        ],
        "start_xy": [
            0.012611183456309485,
            0.06354998069789362
        ],
        "text": "PDF",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "has_img": false,
        "img_path": "",
        "color": [
            0.00392200006172061,
            1.0,
            1.0
        ],
        "index": 1,
        "y": 0.06354998069789362,
        "column": 1,
        "color_name": "Cyan"
    },
    {
        "type": "Squiggly",
        "page": 3,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012227813480186606,
            0.7828160666393338,
            0.4113873094767294,
            0.7968488685351279
        ],
        "start_xy": [
            0.012227813480186606,
            0.7828160666393338
        ],
        "text": "At the end of a PDF file is a footer containing",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "has_img": false,
        "img_path": "",
        "color": [
            1.0,
            0.0,
            0.0
        ],
        "index": 19,
        "y": 0.7828160666393338,
        "column": 1,
        "color_name": "Red"
    }
]
```

