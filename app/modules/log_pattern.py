import re


def log_pattern():
    pattern = re.compile(
        r'(\S+) - - \[(.*?)\] "(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (.+?) HTTP/1\.[01]" (\d+) (\d+) "(.*?)" "(.*?)"(?: (\S+))?$'
    )
    return pattern
