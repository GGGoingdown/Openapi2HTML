# Redoc or Swagger HTML Generator

This script generates an HTML representation for OpenAPI specifications using either Redoc or Swagger.

## Description

- The main purpose of this script is to convert OpenAPI JSON files into a user-friendly documentation format, either using Redoc or Swagger.

- This tool provides options to automatically generate the latest version of the documentation, specify the save location, and choose between Redoc and Swagger representations.

- Additionally, the script supports customization of the Swagger UI by allowing users to override default parameters.

## Features

- Support for Redoc and Swagger UI.
- Customizable Swagger UI parameters.
- Option to generate the latest version of the documentation automatically.
- Resilient file and directory handling using `pathlib`.

## How to Use

```bash
python src/main.py --source [path_to_openapi_file] --filename [output_html_filename] --save-to [directory_to_save_html] --save-type [redoc|swagger] --auto-latest
```

### Arguments

- `--source`: Path to the OpenAPI file (Required).
- `--filename`: Name of the output HTML file.
- `--save-to`: Directory where the generated HTML file will be saved. Default is "docs".
- `--save-type`: The type of HTML to be generated. It can either be "redoc" or "swagger". Default is "redoc".
- `--auto-latest`: If set, an additional file named "latest.html" will be generated.

## Notes

- Currently, Swagger UI is not fully implemented.
