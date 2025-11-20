from flask import Flask, render_template, redirect, request, session, jsonify, url_for
from spotify_client import SpotifyClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega .env
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Em produção, use uma chave fixa e segura

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

spotify = SpotifyClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)


@app.route('/')
def index():
    """Página inicial - redireciona para o dashboard se autenticado"""
    if 'access_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', authenticated=False)


@app.route('/login')
def login():
    """Redireciona para o Spotify para autenticação"""
    auth_url = spotify.get_auth_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Callback do Spotify após autenticação"""
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return f"Erro na autenticação: {error}", 400

    if code:
        token_info = spotify.get_access_token(code)
        session['access_token'] = token_info['access_token']
        if 'refresh_token' in token_info:
            session['refresh_token'] = token_info['refresh_token']
        return redirect(url_for('dashboard'))

    return "Código de autorização não recebido", 400


@app.route('/dashboard')
def dashboard():
    """Página do dashboard com os gráficos"""
    if 'access_token' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', authenticated=True)


@app.route('/api/top_tracks')
def api_top_tracks():
    """Endpoint JSON que retorna as tracks da playlist processadas"""
    if 'access_token' not in session:
        print("ERRO: Usuário não autenticado")
        return jsonify({'error': 'Não autenticado'}), 401

    access_token = session['access_token']

    # Buscar tracks da playlist
    print(f"Buscando tracks da playlist: {PLAYLIST_ID}")
    playlist_data = spotify.get_playlist_tracks(access_token, PLAYLIST_ID, limit=100)

    # Debug
    print("=" * 60)
    print("DEBUG: Response da API Spotify:")
    print(f"Keys na resposta: {playlist_data.keys() if isinstance(playlist_data, dict) else 'Não é dict'}")
    if 'items' in playlist_data:
        print(f"Número de items: {len(playlist_data['items'])}")
    print("=" * 60)

    if 'error' in playlist_data:
        print(f"ERRO na API: {playlist_data['error']}")
        return jsonify(playlist_data), 400

    # Processar dados para os gráficos
    tracks_data = []
    artists_count = {}
    years_count = {}
    popularity_by_year = {}

    items = playlist_data.get('items', [])
    print(f"Processando {len(items)} tracks...")

    if len(items) == 0:
        print("AVISO: Playlist retornou 0 items")
        return jsonify({
            'error': 'Playlist vazia',
            'message': 'A playlist não contém músicas ou você não tem permissão para acessá-la.',
            'tracks': [],
            'artists_count': {},
            'years_count': {},
            'avg_popularity_by_year': {},
            'total_tracks': 0,
            'most_popular_track': None
        })

    for item in items:
        # Em playlists, o item tem uma estrutura item.track
        track = item.get('track')
        if not track:
            continue

        track_name = track.get('name', 'Unknown')

        # Verificar se tem artistas
        if not track.get('artists') or len(track['artists']) == 0:
            continue

        artist_name = track['artists'][0]['name']
        popularity = track.get('popularity', 0)
        album = track.get('album', {})
        release_date = album.get('release_date', '')
        year = release_date[:4] if release_date else 'Unknown'
        duration_ms = track.get('duration_ms', 0)
        duration_min = round(duration_ms / 60000, 2) if duration_ms else 0

        tracks_data.append({
            'name': track_name,
            'artist': artist_name,
            'popularity': popularity,
            'year': year,
            'duration': duration_min,
            'album': album.get('name', 'Unknown'),
            'image': album['images'][0]['url'] if album.get('images') else None
        })

        # Contagem por artista
        if artist_name not in artists_count:
            artists_count[artist_name] = 0
        artists_count[artist_name] += 1

        # Contagem por ano
        if year not in years_count:
            years_count[year] = 0
            popularity_by_year[year] = []
        years_count[year] += 1
        popularity_by_year[year].append(popularity)

    # Calcular popularidade média por ano
    avg_popularity_by_year = {}
    for year, pops in popularity_by_year.items():
        if len(pops) > 0:
            avg_popularity_by_year[year] = round(sum(pops) / len(pops), 1)

    # Top 10 artistas mais presentes
    top_artists = sorted(artists_count.items(), key=lambda x: x[1], reverse=True)[:10]

    # Encontrar música mais popular
    most_popular_track = None
    if tracks_data:
        most_popular = max(tracks_data, key=lambda x: x['popularity'])
        most_popular_track = {
            'name': most_popular['name'],
            'artist': most_popular['artist'],
            'popularity': most_popular['popularity']
        }

    print(f"Processamento concluído: {len(tracks_data)} tracks válidas")
    if most_popular_track:
        print(f"Música mais popular: {most_popular_track['name']} - {most_popular_track['artist']} (Pop: {most_popular_track['popularity']})")

    return jsonify({
        'tracks': tracks_data,
        'artists_count': dict(top_artists),
        'years_count': years_count,
        'avg_popularity_by_year': avg_popularity_by_year,
        'total_tracks': len(tracks_data),
        'most_popular_track': most_popular_track
    })


@app.route('/logout')
def logout():
    """Remove tokens da sessão"""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("=" * 60)
    print("🎵 SPOTIFY DASHBOARD")
    print("=" * 60)
    print(f"Playlist ID configurada: {PLAYLIST_ID}")
    print("Servidor rodando em: http://127.0.0.1:9001")
    print("Pressione CTRL+C para parar")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=9001)
