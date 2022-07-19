from upagekite.httpd import url


@url('/')
def web_root(request_env):
    return {
        'body': '<h1>Hello world!</h1>',
        'mimetype': 'text.html; charset=utf-8',
        'ttl': 60}


def setup_routes(global_app_env):
    pass 
