__author__ = 'geet'

from os import listdir, path
import sys
import json
from optparse import OptionParser

cstyle_comments = {'whole_line': ['//'], 'start': '/*', 'end': '*/'}
python_comments = {'whole_line': ['#'], 'start': "'''", 'end': "'''"}
perl_comments = {'whole_line': ['#']}
php_comments = {'whole_line': ['//', '#'], 'start': '/*', 'end': '*/'}
comment_syntax = {'C': cstyle_comments, 'Java': cstyle_comments, 'C++': cstyle_comments, 'Scala': cstyle_comments,
                  'Go': cstyle_comments, 'Perl': perl_comments, 'Python': python_comments, 'PHP': php_comments}

extns_norm_map = {'c': 'C', 'h': 'C', 'c++': 'C++', 'cxx': 'C++', 'hpp': 'C++', 'hxx': 'C++', 'g++': 'C++', 'cc': 'C++',
                  'cpp': 'C++', 'pl': 'Perl', 'pm': 'Perl', 'scala': 'Scala', 'java': 'Java', 'go': 'Go',
                  'py': 'Python', 'php': 'PHP'}


def get_file_type(filepath):
    try:
        extn_index = filepath.rfind('.')
        extn = filepath[extn_index + 1:]
        if extn == '':
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


def check_whole_line(line, file_type):
    if 'whole_line' not in comment_syntax[file_type]: return line
    whole_comm_pos = -1
    comm_strs = comment_syntax[file_type]['whole_line']
    start_pos = 0
    end_pos = len(line)
    for comm_str in comm_strs:
        start_pos = line.encode(encoding='UTF-8', errors='strict').find(comm_str, start_pos, end_pos)
        if start_pos != -1:
            whole_comm_pos = start_pos
            if start_pos == 0: break
            end_pos = start_pos

    if whole_comm_pos != -1:
        line = line[:whole_comm_pos]
    return line


def check_for_countable_line(comment_started, line, file_type):
    increment = False
    start_pos = 0
    while True:
        if comment_started:
            start_pos = line.find(comment_syntax[file_type]['end'], start_pos)
            if start_pos == -1: break
            start_pos += len(comment_syntax[file_type]['end'])
            comment_started = False
            if start_pos == len(line):
                break
            continue
        new_pos = line.find(comment_syntax[file_type]['start'], start_pos)
        if new_pos == -1:
            increment = True
            break
        if new_pos != start_pos: increment = True
        comment_started = True
        start_pos = new_pos + len(comment_syntax[file_type]['start'])

    return comment_started, increment


def count_real_lines(lines, file_type):
    reallines = 0
    comment_started = False
    increment = False

    for line in lines:
        line = line.strip()
        if line == '': continue
        line = check_whole_line(line, file_type)
        if line == '': continue
        increment = True
        if 'start' in comment_syntax[file_type]:
            comment_started, increment = check_for_countable_line(comment_started, line, file_type)
        if increment: reallines += 1
    return reallines


def countlines_in(dirstart, real_lines):
    try:
        direntries = listdir(dirstart)
    except OSError as e:
        return
    next_level_dirs = []
    for fpath in direntries:
        filepath = dirstart + '/' + fpath
        if path.isdir(filepath):
            next_level_dirs.append(filepath)
            continue
        file_type = get_file_type(fpath)
        if file_type is None:
            continue

        try:
            fp = open(filepath, 'r')
            lines = fp.readlines()
            fp.close()
            c_lines = count_real_lines(lines, file_type)
            if file_type not in real_lines:
                real_lines[file_type] = c_lines
            else:
                real_lines[file_type] += c_lines
        except IOError as e:
            pass

    for next_level_dir in next_level_dirs:
        countlines_in(next_level_dir, real_lines)


def update_comment_syntax(comment_syntax_file):
    try:
        fp = open(comment_syntax_file, 'r')
        if fp is None:
            return False
        jsondata = json.load(fp)
        fp.close()
        for langkey in jsondata.keys():
            output_as = langkey.lower().strip()
            if len(output_as) == 0:
                continue
            if 'output_as' in jsondata[langkey] and len(jsondata[langkey]['output_as']) > 0:
                output_as = jsondata[langkey]['output_as']
            extns_norm_map[langkey.lower().strip()] = output_as
            tmp = jsondata[langkey]
            if 'other_extns' in tmp:
                for other_extn in tmp['other_extns']:
                    extn = other_extn.strip().lower()
                    if extn == '': continue
                    extns_norm_map[extn] = output_as
            comment_syntax[output_as] = {}
            if 'start' in tmp:
                start = tmp['start'].strip()
                if len(start) == 0:
                    print 'comment start cannot be empty'
                    return False
                if 'end' not in tmp:
                    print 'end for comment is not specified'
                    return False
                end = tmp['end'].strip()
                if len(end) == 0:
                    print 'end for comment cannot be empty'
                    return False
                comment_syntax[output_as].update({'start': start, 'end': end})

            if 'whole_line' in tmp:
                whole_line_comments = tmp['whole_line']
                whole_lines = []
                for wh_line in whole_line_comments:
                    wh = wh_line.strip()
                    if len(wh) == 0 : continue
                    whole_lines.append(wh)
                if len(whole_lines) > 0 :
                    comment_syntax[output_as].update({'whole_line' : whole_lines})
    except Exception as e:
        print e
        return False

    return True


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--comment-file', dest='comment_file', metavar='COMMENT_FILE',
                      help='comment syntrax description file')
    parser.add_option('-d', '--root-source-dir', dest='start_dir', metavar='SOURCE_ROOT_DIR',
                      help='root directory for source code')

    (options, args) = parser.parse_args()
    if options.start_dir is None:
        print 'Please supply value for root_source_dir'
        sys.exit(1)

    if not path.isdir(options.start_dir):
        print options.start_dir, ' is not a directory'
        sys.exit(1)

    if options.comment_file is not None:
        if not update_comment_syntax(options.comment_file):
            print 'Some problem in updating comment syntax'
            sys.exit(1)

    real_lines = {}
    countlines_in(options.start_dir, real_lines)
    for file_type, lines in real_lines.iteritems():
        print "File-type:%10s  Line-count:%8d" % (file_type, lines,)
