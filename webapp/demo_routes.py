from upagekite.httpd import url, _HANDLERS


# OK, lol, let's pretend the chip runs PHP
#
@url('/')
def web_root(request_env):
    return {
        'code': 301,
        'msg': 'Moved',
        'hdrs': {'Location': '/index.php'},
        'ttl': 1}


# We can set up multiple URL routes in one go...
#
@url('/index.php', '/wp-admin', '/wp-admin/')
def web_root_php(request_env):
    # Peek under the hood to figure out which URL paths exist
    urls = '\n'.join('<li><a href="%s">%s</a>' % (url, url)
        for url in _HANDLERS)
    return {
        'body': '<h1>PHP is great!</h1><ul>%s</ul>\n' % urls,
        'mimetype': 'text/html; charset=utf-8',
        'ttl': 60}


# A generator can be used to incrementally generate results
#
# Under the hood, this becomes an async request and the app can
# do other things while processing this one.
#
@url('/fibonacci.txt')
def web_fibonacci(request_env):
    yield {
        # We could add a body, but choose not to
        'mimetype': 'text/plain; charset=utf-8',
        'ttl': 600}

    yield '## Please enjoy the first 25 fibonacci numbers ##\n'

    i1 = i2 = 1
    for count in range(0, 25):
        yield '%d\n' % i1
        i1, i2 = i2, (i1 + i2)


def setup_routes(global_app_env):
    pass
