import codecs
import json
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen, Request
from rhythmbox_netease.cipher import encrypt

def http_post(url, **kwargs):
    return urlopen(Request(url, data=urlencode(kwargs).encode(),
                           headers={'Cookie': 'os=linux'}))

def forward(**kwargs):
    return http_post('http://music.163.com/api/linux/forward',
                     eparams=encrypt(json.dumps(kwargs)))

def forward_json(method, url, **kwargs):
    response = forward(method=method, url=url, params=kwargs)
    reader = codecs.getreader(response.info().get_content_charset())
    return json.load(reader(response))

def user_playlist(uid, offset, limit):
    return forward_json('GET', 'http://music.163.com/api/user/playlist/',
                        uid=uid, offset=offset, limit=limit)

def playlist_detail(id, n):
    return forward_json('GET', 'http://music.163.com/api/v3/playlist/detail', id=id, n=n)

def song_enhance_player_url(br, ids):
    return forward_json('POST', 'http://music.163.com/api/song/enhance/player/url',
                        br=br, ids=ids)
