# 🎵 Spotify Dashboard - Top Tracks

Dashboard web temático que consome a API do Spotify e exibe análises visuais das suas 100 músicas mais tocadas usando Flask e ECharts.

## 📁 Estrutura do Projeto

```
DASH_SPOTIFY/
├── data/                    # (opcional) Para armazenar dados locais
├── static/                  # Arquivos estáticos
│   ├── style.css           # Estilos com tema Spotify
│   └── dashboard.js        # Lógica dos gráficos ECharts
├── templates/              # Templates HTML
│   └── dashboard.html      # Página principal
├── venv/                   # Ambiente virtual Python
├── app.py                  # Aplicação Flask principal
├── spotify_client.py       # Cliente para API do Spotify
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo

```

## 🚀 Como Configurar

### 1. Criar App no Spotify for Developers

1. Acesse https://developer.spotify.com/dashboard
2. Faça login com sua conta Spotify
3. Clique em "Create app"
4. Preencha:
   - **App name**: Spotify Dashboard
   - **App description**: Dashboard de análise de músicas
   - **Redirect URI**: `http://localhost:5000/callback`
   - **API/SDKs**: Web API
5. Aceite os termos e clique em "Save"
6. Na página do app, copie:
   - **Client ID**
   - **Client Secret** (clique em "Show client secret")

### 2. Configurar o Ambiente

```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Credenciais

Abra `app.py` e substitua as credenciais do Spotify:

```python
CLIENT_ID = 'seu_client_id_aqui'
CLIENT_SECRET = 'seu_client_secret_aqui'
REDIRECT_URI = 'http://localhost:5000/callback'
```

### 4. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 🎨 Funcionalidades

### Visualizações Disponíveis

1. **Top 10 Músicas por Popularidade** - Gráfico de barras horizontal mostrando as músicas mais populares
2. **Top 10 Artistas Mais Ouvidos** - Gráfico de pizza com os artistas que você mais escuta
3. **Músicas por Ano de Lançamento** - Gráfico de barras mostrando a distribuição temporal
4. **Popularidade Média por Ano** - Gráfico de linha mostrando tendências de popularidade

### Cards de Estatísticas

- Total de tracks analisadas
- Popularidade média das músicas
- Artista favorito (mais presente na lista)

## 🔧 Tecnologias Utilizadas

- **Backend**: Flask 3.0.0
- **API**: Spotify Web API (OAuth 2.0)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Gráficos**: Apache ECharts 5.4.3
- **HTTP Client**: Requests 2.31.0

## 📊 Como Funciona

1. **Autenticação**: O usuário faz login via OAuth 2.0 do Spotify
2. **Coleta de Dados**: A aplicação busca as top 50 tracks do usuário via `/v1/me/top/tracks`
3. **Processamento**: Os dados são agregados por artista, ano, popularidade, etc.
4. **Visualização**: O frontend consome a API `/api/top_tracks` e renderiza os gráficos com ECharts

## 🎯 Endpoints da Aplicação

- `GET /` - Página inicial (redireciona para login ou dashboard)
- `GET /login` - Inicia o fluxo de autenticação OAuth
- `GET /callback` - Recebe o código de autorização do Spotify
- `GET /dashboard` - Página principal com os gráficos (requer autenticação)
- `GET /api/top_tracks` - API JSON com dados processados das músicas
- `GET /logout` - Remove tokens e desloga o usuário

## 🔐 Segurança

- Tokens de acesso são armazenados em sessão Flask (criptografada)
- Use `app.secret_key` fixo e seguro em produção
- Nunca commite credenciais no Git (adicione ao `.gitignore`)

## 🚀 Melhorias Futuras

- [ ] Adicionar análise de audio features (danceability, energy, valence)
- [ ] Implementar cache de dados para reduzir chamadas à API
- [ ] Permitir escolher período de análise (short_term, medium_term, long_term)
- [ ] Adicionar comparação com playlists de charts globais
- [ ] Exportar dados para CSV/JSON
- [ ] Deploy em cloud (Heroku, Render, Railway)
- [ ] Adicionar mais gráficos (radar, scatter, heatmap)

## 📝 Notas

- A API do Spotify limita a 50 tracks por chamada
- Para obter 100 tracks, você pode implementar paginação no `spotify_client.py`
- Os dados refletem suas preferências com base no algoritmo do Spotify
- É necessário ter uma conta Spotify (free ou premium)

## 🐛 Troubleshooting

**Erro 401 Unauthorized**:
- Verifique se o CLIENT_ID e CLIENT_SECRET estão corretos
- Confirme que o REDIRECT_URI no código é exatamente o mesmo configurado no dashboard do Spotify

**Erro 403 Forbidden**:
- Verifique se o app tem os scopes corretos (`user-top-read`)
- Tente deslogar e fazer login novamente

**Gráficos não aparecem**:
- Abra o console do navegador (F12) e verifique erros JavaScript
- Confirme que o ECharts está carregando corretamente

## 📄 Licença

Este projeto é livre para uso educacional e pessoal.

## 👨‍💻 Autor

Desenvolvido com ❤️ para análise de dados musicais do Spotify.
