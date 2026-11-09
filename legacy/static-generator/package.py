"""Package only the standalone website output for static hosting."""
from pathlib import Path
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
RELEASES = ROOT / 'releases'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if not (DIST / 'index.html').is_file():
        raise FileNotFoundError('Run python src/build.py first.')
    files = sorted(p for p in DIST.rglob('*') if p.is_file())
    RELEASES.mkdir(exist_ok=True)
    target = RELEASES / 'ccl-website.zip'
    temporary = RELEASES / 'ccl-website.zip.tmp'
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            archive.write(path, path.relative_to(DIST).as_posix())
    with zipfile.ZipFile(temporary) as archive:
        damaged = archive.testzip()
        if damaged:
            raise ValueError('Archive checksum failed: ' + damaged)
    temporary.replace(target)
    print(json.dumps({'archive': str(target), 'files': len(files),
                      'bytes': target.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    main()
