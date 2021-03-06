"""

Copyright (c) 2013, Los Alamos National Security, LLC
All rights reserved.

Copyright 2013. Los Alamos National Security, LLC. This software
was produced under U.S. Government contract DE-AC52-06NA25396 for Los Alamos 
National Laboratory (LANL), which is operated by Los Alamos National Security, 
LLC for the U.S. Department of Energy. The U.S. Government has rights to use, 
reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR LOS ALAMOS 
NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY 
LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is modified to produce 
derivative works, such modified software should be clearly marked, so as not 
to confuse it with the version available from LANL.
 
Additionally, permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including without 
limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom 
the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

----------------------------------------------------------

Collect and process command line options for the script.

@author: Roy Nielsen
@additional contributors:
"""
import os
import re
import sys
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser, SUPPRESS_HELP

from funcs import log_message

class ProgramOptions(object) :
    """
    Class for holding the command line options
    
    @author: Roy Nielsen
    """
    def __init__(self) :
        """
        Initialization routine for our program options
        
        Acquiring command line arguments with OptionParser
        """
        parser = OptionParser(usage="  %prog [options]\n\n" + \
         "Message levels are mutually exclusive.  The messages print to " + \
         "both the screen and to syslog.  \n\nDefault is to print \"" + \
         "Normal\" messages to the screen.", version="%prog 1.0")

        parser.add_option("-m", "--message-level", type='choice', \
                          action='store', dest="message_level", \
                          choices=['normal', 'quiet', 'verbose', 'debug'], \
                          default="normal", help="How verbose to be.  Default" + \
                          " is \"normal\"", metavar="LEVEL")

        parser.add_option("-q", "--quiet", action="store_true", dest="quiet", \
                          default=0, help="Don't print status messages")

        parser.add_option("-v", "--verbose", action="store_true", \
                          dest="verbose", default=0, \
                          help="Print status messages")

        parser.add_option("-d", "--debug", action="store_true", dest="debug", \
                          default=0, help="Print debug messages")

        parser.add_option("--fls", action="store", dest="fls", \
                          default="", help="Location of the fls executable, " + \
                          " if not in the user's path.  OPTIONAL parameter.")
                  
        parser.add_option("--icat", action="store", dest="icat", \
                          default="", help="Location of the icat executable, " + \
                          " if not in the user's path.  OPTIONAL parameter.")
                  
        parser.add_option("-r", "--root-dir", action="store", dest="root", \
                          default="", help="Directory you want to recover." + \
                          "  REQUIRED parameter.")
                  
        parser.add_option("-s", "--source-dir", action="store", dest="source", \
                          default="", help="Source - location of the bitstream" + \
                          " image.  REQUIRED parameter.")
                  
        parser.add_option("-t", "--target-dir", action="store", dest="target", \
                          default="", help="Target or destination directory " + \
                          "to copy data to.  REQUIRED parameter.")
                  
        parser.add_option("-f", "--filesystem-type", action="store", dest="filesystem", \
                          default="", help="Filesystem type to analyze.  Valid " + \
                          "filesystems can come from \"The Sleuth Kit\"'s " + \
                          "\"fls -f list\" command.  REQUIRED parameter.")
                  
        (self.opts, self.args) = parser.parse_args()
        
        self.validate_options()


    def get_message_level(self) :
        """
        Return the message level passed in, or the default value
        
        @author: Roy Nielsen
        """
        if self.opts.message_level and \
           not re.match("^normal$", self.opts.message_level) :
            msg_lvl = self.opts.message_level

        if self.opts.quiet != 0 :
            msg_lvl = "quiet"
    
        elif self.opts.verbose != 0 :
            msg_lvl = "verbose"

        elif self.opts.debug != 0 :
            msg_lvl = "debug"
        else :
            msg_lvl = "normal"

        return msg_lvl


    def get_source(self) :
        """
        Return the path of the bitstream image
        
        @author: Roy Nielsen
        """
        return self.opts.source


    def get_target(self) :
        """
        Return the target directory to copy deleted information to

        @author: Roy Nielsen
        """
        return self.opts.target
       

    def get_fls(self) :
        """
        Get the location of the fls command, if not in the default location.
        
        FUTURE MODIFICAITON - better input validation
        
        @author: Roy Nielsen
        """
        if re.match("^\s*$", self.opts.fls) :
            flss = ["/usr/local/bin/fls"]
            for fls_path in flss :
                if os.path.exists(fls_path):
                    fls = fls_path
                    break;

            if re.match("^\s$", self.opts.fls):
                log_message("No valid path for fls...", "normal", self.message_level)
                log_message("Exiting...", "normal", self.message_level)
                sys.exit(100)
            
        else :
            if os.path.exists(self.opts.fls) :
                #####
                # Make sure the last item in the path is "fls"
                fls_path = self.opts.fls.split("/")[-1]
                if re.match("^fls$", self.opts.fls) :
                    fls = self.opts.fls
                else :
                    log_message("Looking for fls, not: \"" + str(fls_path) + \
                                "\"", "normal", self.message_level)
                    log_message("Exiting...", "normal", self.message_level)
                    sys.exit(95)
            else :
                log_message("No valid path for fls...", "normal", self.message_level)
                log_message("Exiting...", "normal", self.message_level)
                sys.exit(99)

        return fls
    

    def get_icat(self) :
        """
        Get the location of the icat command, if not in the default location.
        
        FUTURE MODIFICAITON - better input validation
        
        @author: Roy Nielsen
        """
        if re.match("^\s*$", self.opts.icat) :
            icats = ["/usr/local/bin/icat"]
            for icat_path in icats :
                if os.path.exists(icat_path):
                    icat = icat_path
                    break;

            if re.match("^\s$", self.opts.icat):
                log_message("No valid path for icat...", "normal", self.message_level)
                log_message("Exiting...", "normal", self.message_level)
                sys.exit(98)
            
        else :
            if os.path.exists(self.opts.icat) :
                #####
                # Make sure the last item in the path is "icat"
                icat_path = self.opts.icat.split("/")[-1]
                if re.match("^icat$", self.opts.icat) :
                    icat = self.opts.icat
                else :
                    log_message("Looking for icat, not: \"" + str(icat_path) + \
                                "\"", "normal", self.message_level)
                    log_message("Exiting...", "normal", self.message_level)
                    sys.exit(97)
            else :
                log_message("No valid path for icat...", "normal", self.message_level)
                log_message("Exiting...", "normal", self.message_level)
                sys.exit(96)

        return icat


    def get_fs_type(self) :
        """
        Return the filesystem type, checking the fls command for fs types first.
        
        @author: Roy Nielsen
        """
        return self.opts.filesystem
       
       
    def get_fls_fs_types(self) :
        """
        Collect file system types from the fls command for get_fs_type to
        validate "legal" filesystem types.
        
        FUTURE FUNCTIONALITY
        
        @author:
        """
        pass
    
    def get_root_dir(self) :
        """
        Return the root directory that you want to search for -- for instance
        If a user's home directory was deleted, you would want to search for:
        /home/<username>  (Linux)
        /Users/<user shortname>  (Mac)
    
        @author: Roy Nielsen
        """
        return self.opts.root


    def log_options(self) :
        """
        Log what options were passed in to the program.
        
        FUTURE FUNCTIONALITY
        
        @author:
        """
        pass

    
    def validate_options(self) :
        """
        Validate that source, target and filesystem are provided, otherwise
        exit.

        @author: Roy Nielsen
        """
        if re.match("^\s*$", self.opts.source) or \
           re.match("^\s*$", self.opts.target) or \
           re.match("^\s*$", self.opts.filesystem) or \
           re.match("^\s*$", self.opts.root) :
            help = Popen([sys.argv[0], "-h"], stdout=PIPE, stderr=STDOUT).communicate()[0]
            print help
            sys.exit(255)

