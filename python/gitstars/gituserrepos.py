import sys
from pygithub3 import Github

if len(sys.argv) < 2:
    print 'Usage: python {} userid'.format(sys.argv[0])
    print 'For example: python {} mattn'.format(sys.argv[0])
    print '****************************************************************'
    print ''
    print 'This script list out the public repositories created by an user'
    print ''
    print 'IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print 'We need to install pygithub3 package'
    print '  $ pip install pygithub3'
    print ''
    print '****************************************************************'
    sys.exit(1)

gh = Github()
repos = gh.repos.list(sys.argv[1], type='owner').all()
created_repos = [x for x in repos if not x.fork]
stared = sorted((i for i in created_repos ), key=lambda x : -x.stargazers_count)
for repo in stared:
    print '{}, star:{}, forks:{}'.format(repo.name, repo.stargazers_count, repo.forks)

