##License

Los Alamos National Security, LLC owns the copyright to "tsk_get_files". The license for the software is BSD with standard clauses regarding modifications and redistribution.

tsk_get_files has been assigned the Los Alamos Computer Code Number LA-CC-13-102.

Copyright (c) 2013, Los Alamos National Security, LLC All rights reserved.

This software was produced under U.S. Government contract DE-AC52-06NA25396 for Los Alamos National Laboratory (LANL), which is operated by Los Alamos National Security, LLC for the U.S. Department of Energy. The U.S. Government has rights to use, reproduce, and distribute this software. NEITHER THE GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE. If software is modified to produce derivative works, such modified software should be clearly marked, so as not to confuse it with the version available from LANL.
Additionally, redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

- Neither the name of Los Alamos National Security, LLC, Los Alamos National Laboratory, LANL, the U.S. Government, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY LOS ALAMOS NATIONAL SECURITY, LLC AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL LOS ALAMOS NATIONAL SECURITY, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


=============

Recover deleted files based on a search string.  Wraps "fls" and "icat" from The Sleuth Kit: http://www.sleuthkit.org/sleuthkit/
 
tsk_get_files is a script that uses "The Sleuth Kit" commands "fls" and "icat" 
to rebuild a file structure from a disk image.  Although TSK is intended for 
use forensics purposes, this script can be used when a user's home directory is 
accidentally removed, either by an admin or a user.

The main purpose of this script is to wrap the "fls" and "icat" TSK utilities
to recover files based on a search string.

For instance if a user - "amrset" - lost his home directory - one could run:

   tsk_get_files.py -r amrset -s imageToRecoverFrom.img -t /tmp

and it will recover files from the image that have "amrset" in the path, found 
by "fls"

TSK is required to be available to tsk_get_files.py to function.  Specifically
the "fls" and "icat" commands.

WARNING: TSK and this script could be used on an attached disk, such as giving 
the source path as /dev/sdb, however that can be dangerous.  It's faster than 
creating a binary image first, but if not careful, the deleted data can be 
damaged.

The Sleuth Kit(TSK) can be found at: http://www.sleuthkit.org/sleuthkit/

