from upagekite import uPageKite, uPageKiteDefaults, LocalHTTPKite
from upagekite.httpd import HTTPD

# from demo_routes import setup_routes
# from demo_security import setup_security
# from demo_websocket import setup_websocket
# from demo_camera import setup_camera


# This is where upagekite.esp32_install puts things
ESP32_SETTINGS_PATH = '/bootstrap-config.json'
ESP32_WEBROOT_PATH  = '/bootstrap_live/www'


class UPageKiteSettings(uPageKiteDefaults):
    WATCHDOG_TIMEOUT = None
    WITH_SSL = True

    trace = lambda msg: None  # Silently discard trace messages
    debug = print
    error = print
    info = print


if __name__ == '__main__':
    print("=2= Launching webapp!")

    try:
        with open(ESP32_SETTINGS_PATH, 'rb') as fd:
            settings = json.loads(fd.read())
            local_port = 80
            web_root = ESP32_WEBROOT_PATH
        print('=2= Loaded setting from %s' % (ESP32_SETTINGS_PATH,))

    except:
        # If the above failed, perhaps we are running locally?
        # Let's try and grab settings from environment variables.
        #
        import os
        settings = {
            'kite_name': os.getenv('UPK_KITE_NAME', None),
            'kite_secret': os.getenv('UPK_KITE_SECRET', None)}
        web_root = os.path.join(os.getenv('HACKDIR', './'), 'webapp', 'www')
        local_port = 8080
        print('=2= Attempted to load settings from environment.')


    # This gets exposed to the URL handlers; these are effectively
    # the app's global variables.
    global_app_env = {
        'uPK': UPageKiteSettings,
        'kites': [],
        'socks': [],
        'web_root': web_root,
        'settings': settings}

    httpd = HTTPD(
        settings.get('kite_name', 'esp32.mch2022.example.org'),
        web_root,
        {'app': global_app_env},
        UPageKiteSettings)
    global_app_env['httpd'] = httpd

    kite = LocalHTTPKite(local_port,
        settings.get('kite_name'),
        settings.get('kite_secret'),
        httpd.handle_http_request)

    if settings.get('kite_name'):
        print('=2= Flying kite https://%s/' % (settings['kite_name'],))
        global_app_env['kites'].append(kite)

    if kite.fd and local_port:
        print('=2= Listening on http://localhost:%d/' % (local_port,))
        global_app_env['socks'].append(kite)

    upk_manager = uPageKite(global_app_env['kites'],
        socks=global_app_env['socks'],
        uPK=UPageKiteSettings)

    # setup_routes(global_app_env)
    # setup_security(global_app_env)
    # setup_websocket(global_app_env)
    # setup_camera(global_app_env)

    UPageKiteSettings.debug('global_app_env=%s' % global_app_env)
    print('=2= Starting PageKite event loop. Press CTRL+C to abort.')
    upk_manager.run()
