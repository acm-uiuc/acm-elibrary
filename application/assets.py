from flask_assets import Bundle

common_css = Bundle(
    'vendor/reset.min.css',
    'vendor/foundation/foundation.min.css',
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css')

common_js = Bundle(
    'vendor/jquery/jquery-2.1.1.min.js',
    'vendor/foundation/foundation.min.js',
    'vendor/list.min.js',
    'js/main.js',
    output='public/js/common.js')

scribd_js = Bundle(
    'vendor/scribd_api.js',
    output='public/js/scribd.js')

login_css = Bundle(
    'css/login.css',
    filters='cssmin',
    output='public/css/login.css')
