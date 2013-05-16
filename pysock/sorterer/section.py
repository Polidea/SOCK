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


class DeepRecord():
    def __init__(self, content):
        self.content = content

        start_index = content.find('/*')
        end_index = content.find('*/')
        self.name = content[start_index + 2:end_index]


class Record():
    def __init__(self, lines, start_line_index):
        self.start_line_index = start_line_index
        self.end_line_index = self.find_end_line_index(lines)
        self.property_lines = self.load_attribute_lines(lines)
        self.name = self.find_record_name()
        self.deep_record_start_line_index = None
        self.deep_record_end_line_index = None
        self.deep_records = self.load_deep_records(lines)

    def find_end_line_index(self, lines):
        end_record_key = '};'

        line_index = 0
        while True:
            line = lines[self.start_line_index + line_index]
            if end_record_key in line:
                return self.start_line_index + line_index
            line_index += 1

        AssertionError('No end line index in record %s', str(self))

    def load_attribute_lines(self, lines):
        attribute_lines = []
        for line_index in range(0, self.end_line_index - self.start_line_index + 1):
            attribute_lines.append(lines[self.start_line_index + line_index])
        return attribute_lines

    def find_record_name(self):
        start_line = self.property_lines[0]
        key_start_index = start_line.find('/*')
        key_end_index = start_line.find('*/')
        return start_line[key_start_index + 2:key_end_index]

    def load_deep_records(self, lines):
        start_key = ' = ('
        end_key = ');'

        line_index = self.start_line_index
        for line in self.property_lines:
            if start_key in line:
                self.deep_record_start_line_index = line_index
            elif end_key in line:
                self.deep_record_end_line_index = line_index
            line_index += 1

        if self.deep_record_start_line_index is None or self.deep_record_end_line_index is None:
            return None

        deep_records = []
        for line_index in range(self.deep_record_start_line_index + 1, self.deep_record_end_line_index):
            deep_records.append(DeepRecord(lines[line_index]))

        return deep_records


class Section(object):
    def __init__(self, key, lines):
        self.key = key
        self.start_line_index = None
        self.end_line_index = None
        self.records = []

        self.find_start_and_end_line_indexes(lines)
        self.feed_records(lines)

    def find_start_and_end_line_indexes(self, lines):
        starting_line = '/* Begin %s section */' % self.key
        ending_line = '/* End %s section */' % self.key
        line_index = 0

        for line in lines:
            if starting_line in line:
                self.start_line_index = line_index
            if ending_line in line:
                self.end_line_index = line_index
                break
            line_index += 1

    def feed_records(self, lines):
        line_index = self.start_line_index + 1

        while (line_index < self.end_line_index):
            record = Record(lines, line_index)
            self.records.append(record)
            line_index += len(record.property_lines)


