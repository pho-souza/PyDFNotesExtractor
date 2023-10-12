# PyDFNotesExtractor


This project pretends to reimplement the pdfannots repo using just PyMuPDF2.

-----------

To install, use the command:
``python setup.py install``

## Usage

The basic usage is:

``pydfannots -i <input> -o <output>``


```

Flags

Arguments:
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

-ad, -at, -at, -ink and -img are set True by default. If you want to disable some o them, use the flags:

Negative flags:
    -nad, --no-adjust-date  Disable -ad flag.
    -nat, --no-adjust-text  Disable -at flag.
    -nac, --no-adjust-color  Disable -ac flag.
    -nink, --no-ink-annotation  Disable -ink flag.
    -nimg, --no-image  Disable -img flag.

```

---------------git ad

## Sample output

Examples of usage:

### Json 

For export json file
``pydfannots -i tests/PDF_WIKI.pdf -o tests/output/PDF_WIKI.json -f json``

The file is stored [here](tests/PDF_WIKI.pdf)

The result are:

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
        "color_name": "Cyan",
        "index": 1,
        "y": 0.06354998069789362,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.12793119668196828,
            0.650557996270963,
            0.19460500501912828
        ],
        "start_xy": [
            0.012611183456309485,
            0.12793119668196828
        ],
        "text": "Portable Document Format (PDF), standardized as ISO 32000, is a file format developed by Adobe in 1992 to present documents, including text formatting and images, in a manner independent of application software, hardware, and operating systems.[2][3]",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 2,
        "y": 0.12793119668196828,
        "column": 1
    },
    {
        "type": "Square",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.6652648667779736,
            0.1314687912265449,
            0.9882260914614286,
            0.3117187482422527
        ],
        "start_xy": [
            0.6652648667779736,
            0.1314687912265449
        ],
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Orange",
        "index": 3,
        "y": 0.1314687912265449,
        "column": 1,
        "has_img": true,
        "img_path": "img/PDF_WIKI_p1_1.png"
    },
    {
        "type": "Highlight",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.2971247010423428,
            0.4419473574874395,
            0.31389724805452984
        ],
        "start_xy": [
            0.012611183456309485,
            0.2971247010423428
        ],
        "text": "PDF was standardized as ISO 32000 in 2008.[5]",
        "content": "Remember the year",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 4,
        "y": 0.2971247010423428,
        "column": 1
    },
    {
        "type": "FreeText",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.22390915409334902,
            0.4678581643918196,
            0.47306204204527674,
            0.5035697465773871
        ],
        "start_xy": [
            0.22390915409334902,
            0.4678581643918196
        ],
        "content": "Test",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 5,
        "y": 0.4678581643918196,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.48915645476735176,
            0.1309550207353948,
            0.5102050044094735
        ],
        "start_xy": [
            0.012611183456309485,
            0.48915645476735176
        ],
        "text": "History",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Cyan",
        "index": 6,
        "y": 0.48915645476735176,
        "column": 1
    },
    {
        "type": "Text",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.3282825655979667,
            0.605952742027693,
            0.3618982696139908,
            0.6297350853941298
        ],
        "start_xy": [
            0.3282825655979667,
            0.605952742027693
        ],
        "content": "Necess\u00e1rio avaliar",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 7,
        "y": 0.605952742027693,
        "column": 1
    },
    {
        "type": "FreeText",
        "page": 1,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.1262622687625188,
            0.9321430258865959,
            0.2286893230028237,
            0.9440472616012047
        ],
        "start_xy": [
            0.1262622687625188,
            0.9321430258865959
        ],
        "content": "Avalia\u00e7\u00e3o escrita",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Black",
        "index": 8,
        "y": 0.9321430258865959,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.044888731588841616,
            0.18543332920364786,
            0.6729763306173429,
            0.1989654883853866
        ],
        "start_xy": [
            0.044888731588841616,
            0.18543332920364786
        ],
        "text": "Typeset text stored as content streams (i.e., not encoded in plain text);",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 9,
        "y": 0.18543332920364786,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.044888731588841616,
            0.2050621089454576,
            0.7263731652958481,
            0.21859426812719635
        ],
        "start_xy": [
            0.044888731588841616,
            0.2050621089454576
        ],
        "text": "Vector graphics for illustrations and designs that consist of shapes and lines;",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 10,
        "y": 0.2050621089454576,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.044888731588841616,
            0.22469081610931518,
            0.5706030319584112,
            0.2382229752910539
        ],
        "start_xy": [
            0.044888731588841616,
            0.22469081610931518
        ],
        "text": "Raster graphics for photographs and other types of images",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 11,
        "y": 0.22469081610931518,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.044888731588841616,
            0.2444908072402894,
            0.36656413097280677,
            0.25785175503286367
        ],
        "start_xy": [
            0.044888731588841616,
            0.2444908072402894
        ],
        "text": "Multimedia objects in the document.",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Yellow",
        "index": 12,
        "y": 0.2444908072402894,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.27693111967676104,
            0.9874058059105493,
            0.30791595386045395
        ],
        "start_xy": [
            0.012611183456309485,
            0.27693111967676104
        ],
        "text": "a PDF document can also support links (inside document or web page), forms, JavaScript",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Red",
        "index": 13,
        "y": 0.27693111967676104,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.044888731588841616,
            0.37458264955830145,
            0.9620629217286933,
            0.4041750031516976
        ],
        "start_xy": [
            0.044888731588841616,
            0.37458264955830145
        ],
        "text": "An equivalent subset of the PostScript page description programming language but in declarative form, for generating the layout and graphics.",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Orange",
        "index": 14,
        "y": 0.37458264955830145,
        "column": 1
    },
    {
        "type": "Highlight",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.49327674140090977,
            0.24013041370767324,
            0.5090599057691416
        ],
        "start_xy": [
            0.012611183456309485,
            0.49327674140090977
        ],
        "text": "PostScript language",
        "content": "H2",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Cyan",
        "index": 15,
        "y": 0.49327674140090977,
        "column": 1
    },
    {
        "type": "Square",
        "page": 2,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.017154094310782148,
            0.7194860697144616,
            0.9959644330914845,
            0.9157748106459372
        ],
        "start_xy": [
            0.017154094310782148,
            0.7194860697144616
        ],
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Red",
        "index": 16,
        "y": 0.7194860697144616,
        "column": 1,
        "has_img": true,
        "img_path": "img/PDF_WIKI_p2_2.png"
    },
    {
        "type": "Highlight",
        "page": 3,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012611183456309485,
            0.478570924154661,
            0.9874697176036705,
            0.5274008260387048
        ],
        "start_xy": [
            0.012611183456309485,
            0.478570924154661
        ],
        "text": "Objects may be either direct (embedded in another object) or indirect. Indirect objects are numbered with an object number and a generation number and defined between the obj and endobj keywords if residing in the document root. Beginning with PDF version 1.5,",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Green",
        "index": 17,
        "y": 0.478570924154661,
        "column": 1
    },
    {
        "type": "Underline",
        "page": 3,
        "author": "PHO-SOUZA",
        "rect_coord": [
            0.012227813480186606,
            0.61329552602649,
            0.9874326837012359,
            0.6472198398509423
        ],
        "start_xy": [
            0.012227813480186606,
            0.61329552602649
        ],
        "text": "An index table, also called the cross-reference table, is located near the end of the file and gives the byte offset file.[19] of each indirect object from the start of the file.[19]",
        "content": "",
        "created": "2023-04-08 11:16:57",
        "modified": "20230408111657-03'00'",
        "color_name": "Green",
        "index": 18,
        "y": 0.61329552602649,
        "column": 1
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
        "color_name": "Red",
        "index": 19,
        "y": 0.7828160666393338,
        "column": 1
    }
]
```

