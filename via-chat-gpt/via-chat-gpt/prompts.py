import json
import config

def ANNOTATE_SRC_CODE(src_code):
    return f'''
Detect the type of programming language in the source code.
Comment the element definitions (classes and functions) of this source code with documentation, using the appropriate format for that language.

SOURCE CODE:
```
{src_code}
```

If the element already has a comment then do NOT output for that element.


EXAMPLE PYTHON INPUT:
```
import json

def read_from_json_file(path_to_json, encoding='utf-8'):
    with open(path_to_json, encoding=encoding) as f:
        data = json.load(f)
        return data
```

EXAMPLE PYTHON OUTPUT:
```json
{{
    "programming_language": "Python",
    "overall_comment": "_QUOTE__QUOTE__QUOTE_Read and write JSON files._QUOTE__QUOTE__QUOTE_",
    "elements": [{{
        "definition": "def read_from_json_file(path_to_json, encoding='utf-8'):",
        "comment": "    _QUOTE__QUOTE__QUOTE_Read JSON data from a file.\\n    Args:\\n    path_to_json (str): The path to the JSON file.\\n    encoding (str): The encoding of the file. Default is 'utf-8'.\\n    Returns:\\n    dict: The JSON data read from the file.\\n_QUOTE__QUOTE__QUOTE_"
    }}
    ]
}}
```

# EXAMPLE R INPUT:
```
moving_average <- function(x, window_size = 3) {{

  if (!is.numeric(window_size) || window_size <= 0 || window_size != floor(window_size)) {{
    stop()
  }}

  n <- length(x)
  result <- numeric(n)
  
  for (i in 1:n) {{
    start <- max(1, i - window_size + 1)
    result[i] <- mean(x[start:i], na.rm = TRUE)
  }}
  
  return(result)
}}

```
EXAMPLE R OUTPUT:

```json
{{
    "programming_language": "R",
    "overall_comment": "# Calculate Averages.",
    "elements": [{{
        "definition": "moving_average <- function(x, window_size = 3)",
        "comment": " #_SQUOTE_ Calculate the Moving Average\n #_SQUOTE_\n #_SQUOTE_ This function calculates the moving average of a numeric vector. It takes a window size parameter to determine how many previous values to include in the average calculation.\n #_SQUOTE_\n #_SQUOTE_ @param x A numeric vector for which the moving average will be calculated.\n #_SQUOTE_ @param window_size A positive integer specifying the number of elements to include in the moving average window. Default is 3.\n #_SQUOTE_\n #_SQUOTE_ @return A numeric vector of the same length as `x`, containing the moving average values.\n #_SQUOTE_"
    }}
    ]
}}
```




IMPORTANT:
- Make sure that comments have correct indentation.
- Do NOT comment on elements that already have a comment.
- Output MUST be valid JSON. Escape \" with _QUOTE_, \"\"\" with _QUOTE__QUOTE__QUOTE_ and \' with _SQUOTE_.
- If the programming language is R, documentation should be in ROxygen style.
'''

def _pick_longest(parts):
    max_len = -1
    longest = None
    for part in parts:
        if len(part) > max_len:
            longest = part
            max_len = len(part)
    return longest

def _clean_text(text):
    BAD_TEXTS = ['```json', '```']
    for BAD in BAD_TEXTS:
        if BAD in text:
            parts = text.split(BAD)
            text = _pick_longest(parts)
    return text

def parse_response(response):
    response = _clean_text(response)

    return json.loads(response)

def dummy_response():
    if not config.is_dry_run:
        return None

    return '''
```json
{{
    "overall_comment": "_QUOTE__QUOTE__QUOTE_Read and write JSON files._QUOTE__QUOTE__QUOTE_",
    "elements": [{{
        "definition": "def read_from_json_file(path_to_json, encoding='utf-8'):",
        "comment": "    _QUOTE__QUOTE__QUOTE_Read JSON data from a file.\\nArgs:\\npath_to_json (str): The path to the JSON file.\\nencoding (str): The encoding of the file. Default is 'utf-8'.\\nReturns:\\ndict: The JSON data read from the file.\\n_QUOTE__QUOTE__QUOTE_"
    }}
    ]
}}
```
'''
