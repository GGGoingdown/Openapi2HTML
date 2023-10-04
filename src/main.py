from typing import Optional, Any, Dict

import json
import argparse
from pathlib import Path

swagger_ui_default_parameters = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}


def get_swagger_ui_html(
    *,
    openapi_schema: Dict,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Optional[str] = None,
    init_oauth: Optional[Dict[str, Any]] = None,
    swagger_ui_parameters: Optional[Dict[str, Any]] = None,
) -> str:
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        spec: "{openapi_schema}",
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(value)},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(init_oauth)})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return html


def get_redoc_html(
    *,
    openapi_schema: Dict,
    title: str,
    redoc_js_url: str = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
        <div id="redoc-container"></div>
        <script src="{redoc_js_url}"> </script>
        <script>
            var spec = {openapi_schema};
            Redoc.init(spec, '{{}}', document.getElementById("redoc-container"));
        </script>
    </body>
    </html>
    """
    return html


def main(source: str, save_to: str, save_type: str, auto_latest: bool):
    with open(source, "r") as f:
        openapi_schema = json.load(f)

    # Get title from openapi schema
    title = openapi_schema["info"]["title"]
    version = openapi_schema["info"]["version"]

    if save_type == "redoc":
        html = get_redoc_html(openapi_schema=openapi_schema, title=title)
    elif save_type == "swagger":
        html = get_swagger_ui_html(openapi_schema=openapi_schema, title=title)
    else:
        raise NotImplementedError(f"Unknown save type: {save_type}")

    version = version.replace(".", "")
    title = title.lower().replace(" ", "_")

    save_file_paths = []
    if auto_latest:
        save_file_paths.append(Path(save_to) / f"{title}_latest.html")

    save_file_paths.append(Path(save_to) / f"{title}_{version}.html")

    for save_file_path in save_file_paths:
        # Save html file
        with open(str(save_file_path), "w") as f:
            f.write(html)

        print("Save {} to {}".format(save_type, save_file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redoc or Swagger HTML Generator")
    parser.add_argument("--source", type=str, required=True, help="OpenAPI file path")
    parser.add_argument("--filename", type=str, default="", help="HTML file name")
    parser.add_argument(
        "--save-to", type=str, default="docs", help="Save html file to where"
    )
    parser.add_argument(
        "--save-type",
        type=str,
        default="redoc",
        choices=["redoc", "swagger"],
        help="HTML type, redoc or swagger",
    )
    parser.add_argument(
        "--auto-latest",
        action="store_true",
        help="Generate latest.html",
    )
    args = parser.parse_args()

    # Make sure the path is absolute
    openapi_file = Path(args.source).resolve()
    if not openapi_file.is_file():
        raise FileNotFoundError(f"File {openapi_file} not found")

    # Get html filename, if not specified, use the openapi filename
    html_filename = args.filename
    if html_filename == "":
        html_filename = openapi_file.stem + ".html"

    # TODO: Swagger is not implemented yet
    if args.save_type == "swagger":
        raise NotImplementedError("Swagger is not implemented yet")

    # Make sure the path is absolute
    save_to = Path(args.save_to).resolve()
    if not save_to.is_dir():
        save_to.mkdir(parents=True, exist_ok=False)

    main(
        source=str(openapi_file),
        save_to=str(save_to),
        save_type=args.save_type,
        auto_latest=args.auto_latest,
    )
