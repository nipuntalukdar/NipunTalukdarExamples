import tarfile
import os

def extract_tar_archive(tarfl, outdir):
    try:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        elif not os.path.isdir(outdir):
            return False
        with tarfile.open(tarfl, 'r:*') as tarin:
            tarin.extractall(outdir)
    except Exception, e:
        print 'Some problem', e
        return False
    return True

if __name__ == '__main__':
    if tarfile.is_tarfile('a.tgz'):
        extract_tar_archive('a.tgz', 'tmp')
