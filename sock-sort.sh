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


echo "pre-commit pysock script start"

temp_file_name="sock_temp_file_which_will_be_deleted_automatically"
script_name="pysock/sock.py"

######## Getting staged files paths and dumping to file
git diff --name-only --cached >> $temp_file_name

######## Looking for path of project.pbxproj file
file="$temp_file_name"
while read line 
do
	if [[ $line =~ .*project.pbxproj.* ]]; then
		pathToProjectPbxproj=$line
		break
	fi
done <"$file"

######## Running python script which sorts the project.pbxproj sections if path found (need to change the python script file here)
[ -n "$pathToProjectPbxproj" ] && python $script_name $pathToProjectPbxproj

##### Test changes
###chmod 777 $pathToProjectPbxproj
###echo someChangeInsertedInFile >> $pathToProjectPbxproj

######## Re-adding sorted project.pbxproj if path exists
[ -n "$pathToProjectPbxproj" ] && git add $pathToProjectPbxproj

######## Cleaning up the file
rm $temp_file_name

echo "pre-commit pysock script end"