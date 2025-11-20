import requests
import base64
from urllib.parse import urlencode


class SpotifyClient:
    """Cliente para interagir com a API do Spotify"""

    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    API_BASE_URL = 'https://api.spotify.com/v1'

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """Gera URL de autenticação do Spotify"""
        # Para playlists públicas, só precisamos de escopo básico
        scope = 'playlist-read-private playlist-read-collaborative'
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'show_dialog': True
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def get_access_token(self, code):
        """Troca o código de autorização por access token"""
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        return response.json()

    def get_user_top_tracks(self, access_token, limit=50, time_range='medium_term', offset=0):
        """
        Busca top tracks do usuário
        time_range: short_term (~4 semanas), medium_term (~6 meses), long_term (anos)
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {
            'limit': limit,
            'offset': offset,
            'time_range': time_range
        }

        url = f"{self.API_BASE_URL}/me/top/tracks"
        response = requests.get(url, headers=headers, params=params)

        print(f"GET {url} - Status: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"ERRO: {response.text}")
            return {'error': response.json()}

    def get_playlist_tracks(self, access_token, playlist_id, limit=100):
        """Busca tracks de uma playlist"""
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {
            'limit': limit,
            'fields': 'items(track(name,artists,popularity,album(name,release_date,images),duration_ms))'
        }

        url = f"{self.API_BASE_URL}/playlists/{playlist_id}/tracks"
        print(f"GET {url}")

        response = requests.get(url, headers=headers, params=params)

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"ERRO: {response.text}")
            return {'error': response.json()}

    def get_audio_features(self, access_token, track_ids):
        """Busca características de áudio das tracks (danceability, energy, etc)"""
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'ids': ','.join(track_ids)}

        url = f"{self.API_BASE_URL}/audio-features"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.json()}