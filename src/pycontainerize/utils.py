import errno
import os
import shutil

from pycontainerize.errors import DircopyError


def dircopy(src, dest, force=True, print_file=True):
    try:
        if os.path.exists(dest) and force:
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        if print_file:
            print(dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            raise DircopyError('Directory %s not copied. Error: %s' % (src, e))
