import camera
import gc
import os

from upagekite.proto import asyncio, fuzzy_sleep_ms  # Compatibility hacks
from upagekite.httpd import url


@url('/cam.jpg')
def web_cam_jpg(request_env):
  cam_jpg = request_env['app']['cam.jpg']
  if not cam_jpg:
    yield {'code': 404, 'msg': 'Not found', 'ttl': 1}

  else:
    # We yield the image a little bit at a time, so as not to
    # block the main loop for too long.
    yield {
      'hdrs': {'Content-Length': len(cam_jpg)},
      'mimetype': 'image/jpeg',
      'ttl': 15}
    for c in range(0, len(cam_jpg), 1024):
      yield cam_jpg[c:c+1024]


async def camera_loop(global_app_env):
    uPK = global_app_env['uPK']

    try:
        # If we do not set the framebuffer location, then the camera will
        # compete with the TLS stack for DRAM and we cannot have both.
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        camera.framesize(camera.FRAME_VGA)
    except Exception as e:
        uPK.error('[demo_camera] Camera init failed: %s' % e)
        return

    while await fuzzy_sleep_ms(15000):
        try:
            global_app_env['cam.jpg'] = camera.capture()
            gc.collect()
            uPK.info('[demo_camera] Captured new image, see /cam.jpg')
        except Exception as e:
            uPK.error('[demo_camera] Camera capture failed: %s' % e)

    camera.deinit()


def setup_camera(global_app_env):
    global_app_env['httpd'].static_max_age = 60
    asyncio.get_event_loop().create_task(camera_loop(global_app_env))
