import re

def check_file(filename, regex_reference_filename):
    cpp_code = open(filename).read()
    regex_reference = open(regex_reference_filename).read()
    regex_reference = regex_reference.split("\n")
    ignore = re.compile(r'^\s*$|^\s*###.*$')
    anywhere = re.compile(r'^\s*\[anywhere\](.*)')
    cpp_code_lines = cpp_code.split("\n")
    cpp_line = 0
    info = "none"
    for ref_line, r in enumerate(regex_reference):
        if not ignore.match(r):
            m = anywhere.match(r)
            anywhere_flag = False
            if m:
                r = m.group(1)
                anywhere_flag = True
            rm = r'^\s*'+re.sub(r'\s+', r'\\s*', r)+r'\s*$'  # \\ --> see https://docs.python.org/3/library/re.html
            pat = re.compile(rm)
            if anywhere_flag:
                ok = False
                for l in cpp_code_lines:
                    if pat.search(l):
                        ok = True
                if not ok:
                    raise Exception("{} line {}: '{}', '{}' not found!".format(regex_reference_filename, ref_line + 1, r, rm))
            else:
                while cpp_line < len(cpp_code_lines) and not pat.search(
                        cpp_code_lines[cpp_line]):
                    cpp_line += 1
                if cpp_line == len(cpp_code_lines):
                    raise Exception("{} line {}: '{}', '{}' mismatch/not found!".format(regex_reference_filename, ref_line + 1, r, info))
                info = "last match of ref line {} in line {}".format(ref_line+1, cpp_line+1)
                #print(info)
                cpp_line += 1


def get_expected_error_regex(filename):
    error_line = None
    error_regex = None
    expected = re.compile(r'expected:\s*(.*)$')

    text = open(filename).read()
    text = text.split("\n")
    for lineno, line in enumerate(text):
        m = expected.search(line)
        if m:
            assert error_regex is None
            assert error_line is None
            error_line = lineno+1
            error_regex = m.group(1)

    assert error_line is not None
    assert error_regex is not None
    return f"{filename}.*:{error_line}.*:.*{error_regex}"