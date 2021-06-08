"""Functions for cleaning up Toloka results"""

import language_tool_python


def check_grammer(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    matches = [rule for rule in matches]
    print("matches found:")
    print(matches)
    corrected = language_tool_python.utils.correct(text, matches)
    print(corrected)
    return corrected

if __name__ == "__main__":
    check_grammer("drwing")