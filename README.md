SOCK
====

**Simple Omitter of Conflicts Kit** - tool that prevents some of merge conflicts in .pbxproj file in **Xcode** projects

How does it work?
----
Right now we have only one way to deal with this problem: **sock-sort** script. It sorts critical sections in .pbxproj file such as:
- PBXBuildFile
- PBXFileReference
- PBXGroup
- PBXResourcesBuildPhase
- PBXSourcesBuildPhase

Sorted pbxproj file is less vulnerable to merge conflicts because in unsorted file all new resources, files and so on are added at the end of the section. In our approach new files are added in alphabetically sorted list so there is significant chance (which gets bigger with every file added to the project) to insert this file in different line - which is handled better by git merge tools.

Sorting script is ran every time you commit changes of .pbxproj file.

How to use it?
---
1. First off you need to clone **pysock** directory and **sock-sort.sh** script into root of your project.
2. Next you need to create git hook: `ln -s ../../sock-sort.sh .git/hooks/pre-commit`
3. Add permissions `chmod 555 .git/hooks/pre-commit` 
4. In your master branch sort .pbxproj file for the first time by changing something in .pbxproj and commiting **or** manually running sorting script: `python pysock/sock.py AwesomeProject.xcodeproj/project.pbxproj` and then commiting changes.
5. And your done! Every next branch will have sorted .pbxproj file and every time you merge you'll see less conflicts.

**Warning** it is required that every person in team uses this script otherwise it will generate more conflicts.

License
---
    Tomasz Netczuk (netczuk.tomasz at gmail.com)
    Dariusz Seweryn (dariusz.seweryn at gmail.com) 

    Copyright (c) 2009-2013 Polidea Sp. z o.o. (http://www.polidea.pl)
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met: 
    
    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer. 
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution. 
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
    The views and conclusions contained in the software and documentation are those
    of the authors and should not be interpreted as representing official policies, 
    either expressed or implied, of the FreeBSD Project.

Team
---
Tomasz Netczuk [@neciu](https://github.com/neciu)  

Dariusz Seweryn [@dariuszseweryn](https://github.com/dariuszseweryn)  

---

Thanks [@wojtekerbetowski](https://github.com/wojtekerbetowski) for marking this problem and organizing [Name Collision](https://www.hackerleague.org/hackathons/name-collision) on which we have started work on this script. 
