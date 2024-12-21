import json
import config

def ANNOTATE_SRC_CODE(src_code):
    return f'''
Detect the type of programming language in the source code.
Analyze the source code and find the present bugs and potentital bugs in it.
Then, sort the bugs into categories of FATAL and WARNING.

SOURCE CODE:
```
{src_code}
```
Perform the mentioned tasks on the source code above and give output like the examples below.
Do not repeat the examples as output.


EXAMPLE INPUT:
```
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average
```

EXAMPLE OUTPUT:
```json
{{
    "programming_language": "Python",
    "elements": [{{
        "line_of_code": "def calculate_average(numbers):",
        "FATAL": "",
        "WARNING": "The function lacks a docstring or comments explaining its purpose, inputs, and error handling."
    }},
    {{
        "line_of_code": "total += num",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": ""
    }},
    {{
        "line_of_code": "average = total / len(numbers)",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": "If len(numbers) == 0, this line raises a ZeroDivisionError."
    }},
    
    ]
}}
```

IMPORTANT:
- Output MUST be valid JSON.
- Do not repeat the example.
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
    "programming_language": "Python",
    "elements": [{{
        "line_of_code": "def calculate_average(numbers):",
        "FATAL": "",
        "WARNING": "The function lacks a docstring or comments explaining its purpose, inputs, and error handling."
    }},
    {{
        "line_of_code": "total += num",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": ""
    }},
    {{
        "line_of_code": "average = total / len(numbers)",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": "If len(numbers) == 0, this line raises a ZeroDivisionError."
    }},
    
    ]
}}
```
'''
