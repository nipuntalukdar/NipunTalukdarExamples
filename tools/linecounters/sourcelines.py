#!/usr/bin/python
__author__ = "geet"

import json
import re
import sys
from optparse import OptionParser
from os import listdir, path

import chardet

cstyle_comments = {"whole_line": ["//"], "start": "/*", "end": "*/"}
python_comments = {
    "whole_line": ["#"],
    "start": "'''",
    "end": "'''",
    "start_alias": '"""',
    "end_alias": '"""',
}
perl_comments = {"whole_line": ["#"]}
php_comments = {"whole_line": ["//", "#"], "start": "/*", "end": "*/"}
ruby_comments = {"whole_line": ["#"], "start": "=begin", "end": "=end"}
lua_comments = {"whole_line": ["--"], "start": "--[[", "end": "]]"}
comment_syntax = {
    "C": cstyle_comments,
    "Java": cstyle_comments,
    "C++": cstyle_comments,
    "Scala": cstyle_comments,
    "Go": cstyle_comments,
    "Perl": perl_comments,
    "Python": python_comments,
    "PHP": php_comments,
    "Ruby": ruby_comments,
    "C#": cstyle_comments,
    "JavaScript": cstyle_comments,
    "Rust": cstyle_comments,
    "Lua": lua_comments,
}

extns_norm_map = {
    "c": "C",
    "h": "C",
    "c++": "C++",
    "cxx": "C++",
    "hpp": "C++",
    "hxx": "C++",
    "g++": "C++",
    "cc": "C++",
    "cpp": "C++",
    "pl": "Perl",
    "pm": "Perl",
    "scala": "Scala",
    "java": "Java",
    "go": "Go",
    "py": "Python",
    "php": "PHP",
    "rb": "Ruby",
    "cs": "C#",
    "js": "JavaScript",
    "rs": "Rust",
    "lua": "Lua",
    "wlua": "Lua",
}
skipdir_re = None
skiffile_re = None


def get_file_type(filepath):
    try:
        if skiffile_re:
            base = path.basename(filepath)
        extn_index = filepath.rfind(".")
        extn = filepath[extn_index + 1 :]
        if extn == "":
            return None
        extn = extn.lower()
        if extn not in comment_syntax.keys():
            if extn in extns_norm_map:
                extn = extns_norm_map[extn]
            else:
                return None
        return extn
    except ValueError:
        return None


def check_line(line, file_type, is_comm_started):
    if is_comm_started:
        # Look for end of multi-line-comments. If it is not there
        # simply ignore that line
        commennt_end_pos = line.find(comment_syntax[file_type]["end"])
        if commennt_end_pos == -1:
            return "", is_comm_started
        is_comm_started = False
        line = line[commennt_end_pos + len(comment_syntax[file_type]["end"]) :]
        if not line:
            return "", is_comm_started
        return check_line(line, file_type, is_comm_started)

    whole_comm_pos = -1
    is_comm_started = False
    if "whole_line" in comment_syntax[file_type]:
        comm_strs = comment_syntax[file_type]["whole_line"]
        whole_comm_pos = min([line.find(a) for a in comm_strs])
    multi_l_pos = line.find(comment_syntax[file_type]["start"])
    if multi_l_pos == whole_comm_pos == -1:
        return line, is_comm_started
    whole_line_comment = False
    if multi_l_pos == -1:
        whole_line_comment = True
    elif whole_comm_pos == -1:
        whole_line_comment = False
    elif whole_comm_pos <= multi_l_pos:
        whole_line_comment = True
    if whole_line_comment:
        return line[:whole_comm_pos], is_comm_started
    else:
        is_comm_started = True
        non_comm_part = line[:multi_l_pos]
        line, is_comm_started = check_line(
            line[multi_l_pos + len(comment_syntax[file_type]["start"]) :],
            file_type,
            is_comm_started,
        )
        if not line:
            line = non_comm_part
        return line, is_comm_started


def remove_whitespaces(line, file_type):
    if not line:
        return line
    line = line.strip()
    if not line:
        return line
    comment_keys = []
    if "whole_line" in comment_syntax[file_type]:
        comment_keys += comment_syntax[file_type]["whole_line"]
    if "start" in comment_syntax[file_type]:
        comment_keys.append(comment_syntax[file_type]["start"])
    if "end" in comment_syntax[file_type]:
        comment_keys.append(comment_syntax[file_type]["end"])
    for c_key in comment_keys:
        c_key_escaped = re.escape(c_key)
        line = re.sub(f"\s*{c_key_escaped}\s*", c_key, line)
    return line


def normalize_alias(line, file_type):
    if not line:
        return line
    if "start_alias" in comment_syntax[file_type]:
        line = line.replace(
            comment_syntax[file_type]["start_alias"], comment_syntax[file_type]["start"]
        )
    if "end_alias" in comment_syntax[file_type]:
        line = line.replace(
            comment_syntax[file_type]["end_alias"], comment_syntax[file_type]["end"]
        )
    return line


def count_real_lines(lines, file_type):
    reallines = 0
    is_comm_started = False
    for line in lines:
        line = remove_whitespaces(line, file_type)
        line = normalize_alias(line, file_type)
        if not line:
            continue
        line, is_comm_started = check_line(line, file_type, is_comm_started)
        if line == "":
            continue
        reallines += 1
    return reallines


def try_get_file_lines(filepath):
    try:
        encoding = None
        with open(filepath, "rb") as fp:
            data = fp.read()
            result = chardet.detect(data)
            encoding = result["encoding"]
        with open(filepath, "r", encoding=encoding) as fp:
            lines = fp.readlines()
            return True, lines
    except UnicodeDecodeError as e:
        print(f"Decode error for {filepath}: {e}")
        return False, []
    except Exception as e:
        print(filepath, e)
        return False, []


def get_file_lines(filepath):
    try:
        with open(filepath, "r") as fp:
            return True, fp.readlines()
    except UnicodeDecodeError:
        return try_get_file_lines(filepath)
    except Exception as e:
        print(filepath, e)
        return False, []


def countlines_in(dirstart, real_lines):
    if skipdir_re is not None:
        if skipdir_re.match(dirstart):
            return
    try:
        direntries = listdir(dirstart)
    except OSError:
        return
    next_level_dirs = []
    for fpath in direntries:
        filepath = dirstart + "/" + fpath
        if path.isdir(filepath):
            next_level_dirs.append(filepath)
            continue
        file_type = get_file_type(fpath)
        if file_type is None:
            continue
        if skiffile_re:
            base = path.basename(fpath)
            if skiffile_re.match(base):
                continue
        try:
            success, lines = get_file_lines(filepath)
            if not success:
                continue
            c_lines = count_real_lines(lines, file_type)
            if file_type not in real_lines:
                real_lines[file_type] = c_lines
            else:
                real_lines[file_type] += c_lines
        except Exception as e:
            print(filepath, e)

    for next_level_dir in next_level_dirs:
        if skipdir_re is not None:
            if skipdir_re.match(next_level_dir):
                continue
        countlines_in(next_level_dir, real_lines)


def update_comment_syntax(comment_syntax_file):
    try:
        fp = open(comment_syntax_file, "r")
        if fp is None:
            return False
        jsondata = json.load(fp)
        fp.close()
        for langkey in jsondata.keys():
            output_as = langkey.lower().strip()
            if len(output_as) == 0:
                continue
            if (
                "output_as" in jsondata[langkey]
                and len(jsondata[langkey]["output_as"]) > 0
            ):
                output_as = jsondata[langkey]["output_as"]
            extns_norm_map[langkey.lower().strip()] = output_as
            tmp = jsondata[langkey]
            if "other_extns" in tmp:
                for other_extn in tmp["other_extns"]:
                    extn = other_extn.strip().lower()
                    if extn == "":
                        continue
                    extns_norm_map[extn] = output_as
            comment_syntax[output_as] = {}
            if "start" in tmp:
                start = tmp["start"].strip()
                if len(start) == 0:
                    print("comment start cannot be empty")
                    return False
                if "end" not in tmp:
                    print("end for comment is not specified")
                    return False
                end = tmp["end"].strip()
                if len(end) == 0:
                    print("end for comment cannot be empty")
                    return False
                comment_syntax[output_as].update({"start": start, "end": end})

            if "whole_line" in tmp:
                whole_line_comments = tmp["whole_line"]
                whole_lines = []
                for wh_line in whole_line_comments:
                    wh = wh_line.strip()
                    if len(wh) == 0:
                        continue
                    whole_lines.append(wh)
                if len(whole_lines) > 0:
                    comment_syntax[output_as].update({"whole_line": whole_lines})
    except Exception as e:
        print(e)
        return False

    return True


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-c",
        "--comment-file",
        dest="comment_file",
        metavar="COMMENT_FILE",
        help="comment syntrax description file",
    )
    parser.add_option(
        "-d",
        "--root-source-dir",
        dest="start_dir",
        metavar="SOURCE_ROOT_DIR",
        help="root directory for source code",
    )
    parser.add_option(
        "-s",
        "--skip_dirs",
        dest="skip_dir_pattern",
        metavar="SKIP_DIR_REGEX",
        help="regular expression for directory name to be skipped",
    )
    parser.add_option(
        "-f",
        "--skip_files",
        dest="skip_regular_file",
        metavar="SKIP_FILE_REGEX",
        help="regular expression for file names to be skipped",
    )

    (options, args) = parser.parse_args()
    if options.start_dir is None:
        print("Please supply value for root_source_dir")
        sys.exit(1)

    if not path.isdir(options.start_dir):
        print(options.start_dir, " is not a directory")
        sys.exit(1)

    if options.comment_file is not None:
        if not update_comment_syntax(options.comment_file):
            print("Some problem in updating comment syntax")
            sys.exit(1)

    if options.skip_dir_pattern is not None:
        skipdir_re = re.compile(options.skip_dir_pattern)
    if options.skip_regular_file is not None:
        skiffile_re = re.compile(options.skip_regular_file)

    real_lines = {}
    countlines_in(options.start_dir, real_lines)
    for file_type, lines in real_lines.items():
        print(
            "File-type:%10s  Line-count:%8d"
            % (
                file_type,
                lines,
            )
        )
