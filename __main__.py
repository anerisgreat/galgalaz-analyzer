import sys
import json
import spotify
import os

async def async_main(client, user_id, out_dir):
    user = await client.get_user(user_id)
    playlists = await user.get_playlists()
    for playlist in playlists:
        out_map = {}
        out_map['playlist-name'] = playlist.name
        out_map['tracks'] = []
        print('Playlist: ' + playlist.name)
        tracks = await playlist.get_all_tracks()
        out_map['tracks'] = [{
                'artist' : track.artist.name,
                'album-release-date' : track.album.release_date,
                'name' : track.name,
            } for track in tracks]
        for i in range(len(out_map['tracks'])):
            out_map['tracks'][i]['track-number'] = i + 1

        filename = os.path.join(out_dir, out_map['playlist-name'] + '.json' )
        with open(filename, 'w') as outfile:
            json.dump(out_map, outfile)
        print('Done with playlist.')
    await client.close()

def main(args):
    auth_json = {}
    with open(args[0]) as f:
        auth_json = json.load(f)

    client = spotify.Client(
            auth_json['client-id'],
            auth_json['client-secret'])
    user_id = args[1]
    out_dir = args[2]
    client.loop.run_until_complete(async_main(client, user_id, out_dir))

if __name__ == '__main__':
    main(sys.argv[1:])
