import os
import shutil
import sys
from datetime import datetime
from os.path import expanduser

home = expanduser("~")


def main(path):
    files = os.listdir(path)
    for access_log in files:
        if not os.path.isdir(access_log):
            file_name = path + "/" + access_log
            print "find %s" % file_name
            strftime = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime('%Y-%m-%d')
            print "time:%s" % strftime
            if strftime.find("2018-01-30") > -1:
                print "new file skip."
                continue
            dst_dir = os.path.join(home, os.path.basename(file_name))
            print "dst_dir:%s" % dst_dir
            print "copy %s  ---->   %s" % (file_name, dst_dir)
            shutil.copy(file_name, dst_dir)
            print "delete %s" % file_name
            os.remove(file_name)
            print "copy %s  ---->   %s" % (dst_dir, file_name)
            shutil.copy(dst_dir, file_name)
            print "delete %s" % dst_dir
            os.remove(dst_dir)


if __name__ == '__main__':
    main(sys.argv[1])
