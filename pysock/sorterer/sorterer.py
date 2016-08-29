# Tomasz Netczuk (netczuk.tomasz at gmail.com)
# Dariusz Seweryn (dariusz.seweryn at gmail.com)
#
# Copyright (c) 2009-2013 Polidea Sp. z o.o. (http://www.polidea.pl)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.


import os
from section import Section


def sort_critical_sections_in_pbx_file(pbx_file_path):
    raw_lines = read_raw_lines(pbx_file_path)

    sort_lines_in_section(section_key='PBXBuildFile', lines=raw_lines)
    sort_lines_in_section(section_key='PBXFrameworksBuildPhase', lines=raw_lines)
    sort_lines_in_section(section_key='PBXFileReference', lines=raw_lines)
    sort_lines_in_section(section_key='PBXGroup', lines=raw_lines)
    sort_lines_in_section(section_key='PBXResourcesBuildPhase', lines=raw_lines)
    sort_lines_in_section(section_key='PBXSourcesBuildPhase', lines=raw_lines)
    sort_lines_in_section(section_key='PBXHeadersBuildPhase', lines=raw_lines)

    write_sorted_raw_lines(raw_lines, pbx_file_path)


def sort_lines_in_section(section_key, lines):
    section = Section(key=section_key, lines=lines)

    if section.start_line_index is None or section.end_line_index is None:
        AssertionError('Section %s does not contain starting or ending line index.' % section_key)

    section.records.sort(key=lambda x: x.name, reverse=False)

    for record in section.records:
        for line in record.property_lines:
            del lines[section.start_line_index + 1]

    line_index = section.start_line_index + 1
    for record in section.records:
        sort_deep_records_in_record(record)
        for line in record.property_lines:
            lines.insert(line_index, line)
            line_index += 1


def sort_deep_records_in_record(record):
    if record.deep_records is None:
        return
    record.deep_records.sort(key=lambda x: x.name, reverse=False)

    line_index = record.deep_record_start_line_index + 1
    for deep_record in record.deep_records:
        record.property_lines[line_index - record.start_line_index] = deep_record.content
        line_index += 1


def read_raw_lines(pbx_file_path):
    pbx_file = open(pbx_file_path, 'r')
    raw_lines = []
    for raw_line in pbx_file.read().splitlines():
        raw_lines.append(raw_line)
    pbx_file.close()
    return raw_lines


def write_sorted_raw_lines(raw_lines, pbx_file_path):
    os.remove(pbx_file_path)
    pbx_file = open(pbx_file_path, 'w')
    for line in raw_lines:
        pbx_file.write('%s\n' % line)
    pbx_file.close()
