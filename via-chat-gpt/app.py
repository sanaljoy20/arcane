import os
import base64
import subprocess
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import flask
from difflib import ndiff


from dotenv import load_dotenv

load_dotenv()


# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ARCANE"
server = app.server

# Layout
app.layout = dbc.Container([
    html.H1("ARCANE", className="text-center my-4"),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id="upload-file",
                children=html.Div([
                    "Drag and Drop or ",
                    html.A("Select a File")
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id="file-info", className="mt-3"),
            dbc.Button("Process File", id="process-btn", color="primary", className="mt-3", disabled=True),
            html.A("Download Generated File", id="download-link", href="", target="_blank", className="btn btn-secondary mt-3", style={"display": "none"})
        ], width=2, className="bg-light text-body"),
        dbc.Col([
            html.H5("Input File Content:", className="mt-3"),
            dcc.Markdown(id="input-content", style={"whiteSpace": "pre-wrap", "backgroundColor": "#f8f9fa", "padding": "10px", "border": "1px solid #ddd", "height": "100vh"}),
        ], width=5),
        dbc.Col([
            html.H5("Generated:", className="mt-3"),
            html.Div(id="comparison-content", style={"whiteSpace": "pre-wrap", "backgroundColor": "#f8f9fa", "padding": "10px", "border": "1px solid #ddd", "overflowX": "auto", "height": "100vh"})
        ], width=5)
    ])
], fluid=True)

# Callbacks
@app.callback(
    [Output("file-info", "children"), Output("input-content", "children"), Output("process-btn", "disabled")],
    [Input("upload-file", "contents")],
    [State("upload-file", "filename")]
)
def upload_file(contents, filename):
    if contents is None:
        return "No file uploaded yet.", "", True

    content_type, content_string = contents.split(",")
    decoded_content = base64.b64decode(content_string).decode("utf-8")
    
    file_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "w", newline="") as f:
        f.write(decoded_content)

    return f"Uploaded File: {filename}", f"```{filename.split('.')[-1]}\n{decoded_content}\n```", False

@app.callback(
    [Output("comparison-content", "children"),
     Output("download-link", "href"),
     Output("download-link", "style")],
    [Input("process-btn", "n_clicks")],
    [State("upload-file", "filename")]
)
def process_file(n_clicks, filename):
    if not n_clicks or not filename:
        return "", "", {"display": "none"}

    input_file_path = os.path.join("temp", filename)
    output_dir = os.path.join("temp", "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run([
            "python", "doc_ai", input_file_path, "--out-dir", output_dir
        ], check=True)

        output_file_path = os.path.join(output_dir, filename)
        if os.path.exists(output_file_path):
            with open(input_file_path, "rb") as f:
                input_content = f.read().decode("utf-8").splitlines()
            with open(output_file_path, "rb") as f:
                output_content = f.read().decode("utf-8").splitlines()

            # Find Differences
            diff = ndiff(input_content, output_content)

            # Create a visual representation of differences
            diff_table = []
            for line in diff:
                if line.startswith("- "):
                    diff_table.append(html.Div(line[2:], style={"backgroundColor": "#ffcccc", "whiteSpace": "pre-wrap"}))
                elif line.startswith("+ "):
                    diff_table.append(html.Div(line[2:], style={"backgroundColor": "#ccffcc", "whiteSpace": "pre-wrap"}))
                else:
                    diff_table.append(html.Div(line[2:], style={"whiteSpace": "pre-wrap"}))

            
            comparison_component = html.Div(diff_table, style={"fontFamily": "monospace", "border": "1px solid #ccc", "padding": "10px"})


            # Prepare download link
            download_link = f"/download/{filename}"

            return comparison_component, download_link, {"display": "inline-block"}
        else:
            return "Output file not generated. Check your package.", "", {"display": "none"}
    except subprocess.CalledProcessError as e:
        return f"Error processing file: {str(e)}", "", {"display": "none"}

@app.server.route("/download/<filename>")
def download_file(filename):
    output_dir = os.path.join("temp", "output")
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return flask.send_file(file_path, as_attachment=True)
    return "File not found.", 404

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
