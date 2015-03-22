# -*- coding: utf-8 -*-

import mimetypes
import urllib
import urllib.request
import random
import string

_BOUNDARY_CHARS = string.digits + string.ascii_letters


# based on http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/
def encode_multipart(fields: dict, files: dict, boundary: str=None) -> tuple:
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = '--------------------' + ''.join(random.choice(_BOUNDARY_CHARS) for _ in range(30))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{}'.format(boundary),
            'Content-Disposition: form-data; name="{}"'.format(escape_quote(name)),
            '',
            str(value),
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{}'.format(boundary),
            'Content-Disposition: form-data; name="{}"; filename="{}"'.format(
                escape_quote(name), escape_quote(filename)),
            'Content-Type: {}'.format(mimetype),
            '',
            value['content'],
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = b'\r\n'.join(map(lambda line: line if isinstance(line, bytes) else line.encode(), lines))

    headers = {
        'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return body, headers


def post_multipart(url: str, fields: dict, files: dict) -> bytes:
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a dict of (name, value) elements for regular form fields.
    files is a dict of (name :  {'filename': filename, 'content': content) elements for data to be uploaded as files
    Return the server's response page.
    """
    body, headers = encode_multipart(fields, files)
    opener = urllib.request.build_opener()
    request = urllib.request.Request(url, body, headers)

    with opener.open(request) as f:
        return f.read()