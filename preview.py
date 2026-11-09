"""Open the static CCL site through localhost so YouTube receives a Referer.

Python standard library only. Close the launch window or press Ctrl+C to stop.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import argparse
import threading
import webbrowser
import sys

DIST = Path(__file__).resolve().parent / 'dist'

class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', default='index.html')
    parser.add_argument('--port', type=int, default=4331)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if args.page not in {p.name for p in DIST.glob('*.html')}:
        parser.error('--page must be one of the website HTML filenames')
    handler = partial(PreviewHandler, directory=str(DIST))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError:
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    port = server.server_address[1]
    url = f'http://127.0.0.1:{port}/{args.page}'
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print('Local: ' + url, flush=True)
    print('Keep this window open while using the preview. Close it or press Ctrl+C to stop.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        thread.join()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
