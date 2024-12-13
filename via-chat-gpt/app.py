import os
import base64
import subprocess
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "MyPackage Dash App"

# Layout
app.layout = dbc.Container([
    html.H1("MyPackage Dash App", className="text-center my-4"),
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
        ], width=6),
        dbc.Col([
            html.H5("Input File Content:"),
            dcc.Markdown(id="input-content", style={"whiteSpace": "pre-wrap", "backgroundColor": "#f8f9fa", "padding": "10px", "border": "1px solid #ddd"}),
            html.H5("Generated File Content:", className="mt-3"),
            dcc.Markdown(id="output-content", style={"whiteSpace": "pre-wrap", "backgroundColor": "#f8f9fa", "padding": "10px", "border": "1px solid #ddd"})
        ], width=6)
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
    Output("output-content", "children"),
    [Input("process-btn", "n_clicks")],
    [State("upload-file", "filename")]
)
def process_file(n_clicks, filename):
    if not n_clicks or not filename:
        return ""

    input_file_path = os.path.join("temp", filename)
    output_dir = os.path.join("temp", "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run([
            "python", "via-chat-gpt", input_file_path, "--out-dir", output_dir
        ], check=True)

        output_file_path = os.path.join(output_dir, filename)
        if os.path.exists(output_file_path):
            with open(output_file_path, "r") as f:
                output_content = f.read()
            return f"```{filename.split('.')[-1]}\n{output_content}\n```"
        else:
            return "Output file not generated. Check your package."
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
