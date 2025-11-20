// Cores do tema Spotify
const SPOTIFY_COLORS = {
    green: '#1DB954',
    black: '#191414',
    darkGray: '#282828',
    gray: '#535353',
    lightGray: '#b3b3b3',
    white: '#FFFFFF'
};

// Paleta de cores para gráficos
const CHART_COLORS = [
    '#1DB954', '#1ed760', '#1fdf64', '#169c46', '#117a37',
    '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7'
];

// Carregar dados da API
async function loadDashboardData() {
    try {
        const response = await fetch('/api/top_tracks');
        if (!response.ok) {
            throw new Error('Erro ao carregar dados');
        }

        const data = await response.json();

        // Atualizar cards de estatísticas
        updateStatsCards(data);

        // Criar gráficos
        createPopularityChart(data.tracks);
        createArtistsChart(data.artists_count);
        createYearsChart(data.years_count);
        createPopularityByYearChart(data.avg_popularity_by_year);

        // Mostrar dashboard e esconder loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('dashboardContent').style.display = 'block';

    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('loading').innerHTML = `
            <p style="color: #ff6b6b;">❌ Erro ao carregar dados. Tente fazer login novamente.</p>
            <a href="/login" style="color: ${SPOTIFY_COLORS.green};">Reconectar</a>
        `;
    }
}

// Atualizar cards de estatísticas
function updateStatsCards(data) {
    const topArtistEntry = Object.entries(data.artists_count)[0];

    // Card 1: Total de Tracks
    document.getElementById('totalTracks').textContent = data.total_tracks;

    // Card 2: Música Mais Popular (NOVO)
    if (data.most_popular_track) {
        const trackName = data.most_popular_track.name.length > 30 
            ? data.most_popular_track.name.substring(0, 30) + '...'
            : data.most_popular_track.name;

        document.getElementById('mostPopularTrack').textContent = trackName;
        document.getElementById('mostPopularArtist').textContent = data.most_popular_track.artist;
    } else {
        document.getElementById('mostPopularTrack').textContent = '-';
        document.getElementById('mostPopularArtist').textContent = 'Nenhuma música encontrada';
    }

    // Card 3: Artista Favorito
    document.getElementById('topArtist').textContent = topArtistEntry ? topArtistEntry[0] : '-';
}

// Gráfico de Popularidade (Top 10)
function createPopularityChart(tracks) {
    const chart = echarts.init(document.getElementById('popularityChart'));

    // Top 10 por popularidade
    const sortedTracks = [...tracks].sort((a, b) => b.popularity - a.popularity).slice(0, 10);

    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            backgroundColor: SPOTIFY_COLORS.darkGray,
            borderColor: SPOTIFY_COLORS.green,
            textStyle: { color: SPOTIFY_COLORS.white }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { color: SPOTIFY_COLORS.lightGray },
            splitLine: { lineStyle: { color: SPOTIFY_COLORS.gray, type: 'dashed' } }
        },
        yAxis: {
            type: 'category',
            data: sortedTracks.map(t => `${t.name.substring(0, 25)}...`).reverse(),
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { color: SPOTIFY_COLORS.lightGray }
        },
        series: [{
            type: 'bar',
            data: sortedTracks.map(t => t.popularity).reverse(),
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                    { offset: 0, color: SPOTIFY_COLORS.green },
                    { offset: 1, color: '#1ed760' }
                ]),
                borderRadius: [0, 5, 5, 0]
            },
            label: {
                show: true,
                position: 'right',
                color: SPOTIFY_COLORS.white,
                fontWeight: 'bold'
            }
        }]
    };

    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
}

// Gráfico de Artistas
function createArtistsChart(artistsCount) {
    const chart = echarts.init(document.getElementById('artistsChart'));

    const data = Object.entries(artistsCount).map(([name, value]) => ({
        name: name,
        value: value
    }));

    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'item',
            backgroundColor: SPOTIFY_COLORS.darkGray,
            borderColor: SPOTIFY_COLORS.green,
            textStyle: { color: SPOTIFY_COLORS.white }
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: true,
            itemStyle: {
                borderRadius: 10,
                borderColor: SPOTIFY_COLORS.black,
                borderWidth: 2
            },
            label: {
                show: true,
                color: SPOTIFY_COLORS.white,
                formatter: '{b}: {c}'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            data: data,
            color: CHART_COLORS
        }]
    };

    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
}

// Gráfico de Anos
function createYearsChart(yearsCount) {
    const chart = echarts.init(document.getElementById('yearsChart'));

    const sortedYears = Object.entries(yearsCount)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .filter(([year]) => year !== 'Unknown');

    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            backgroundColor: SPOTIFY_COLORS.darkGray,
            borderColor: SPOTIFY_COLORS.green,
            textStyle: { color: SPOTIFY_COLORS.white }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: sortedYears.map(([year]) => year),
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { 
                color: SPOTIFY_COLORS.lightGray,
                rotate: 45
            }
        },
        yAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { color: SPOTIFY_COLORS.lightGray },
            splitLine: { lineStyle: { color: SPOTIFY_COLORS.gray, type: 'dashed' } }
        },
        series: [{
            type: 'bar',
            data: sortedYears.map(([_, count]) => count),
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
                    { offset: 0, color: SPOTIFY_COLORS.green },
                    { offset: 1, color: '#1ed760' }
                ]),
                borderRadius: [5, 5, 0, 0]
            }
        }]
    };

    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
}

// Gráfico de Popularidade por Ano
function createPopularityByYearChart(avgPopByYear) {
    const chart = echarts.init(document.getElementById('popularityYearChart'));

    const sortedData = Object.entries(avgPopByYear)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .filter(([year]) => year !== 'Unknown');

    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            backgroundColor: SPOTIFY_COLORS.darkGray,
            borderColor: SPOTIFY_COLORS.green,
            textStyle: { color: SPOTIFY_COLORS.white }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: sortedData.map(([year]) => year),
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { 
                color: SPOTIFY_COLORS.lightGray,
                rotate: 45
            }
        },
        yAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: SPOTIFY_COLORS.gray } },
            axisLabel: { color: SPOTIFY_COLORS.lightGray },
            splitLine: { lineStyle: { color: SPOTIFY_COLORS.gray, type: 'dashed' } }
        },
        series: [{
            type: 'line',
            data: sortedData.map(([_, pop]) => pop),
            smooth: true,
            lineStyle: {
                color: SPOTIFY_COLORS.green,
                width: 3
            },
            itemStyle: {
                color: SPOTIFY_COLORS.green
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(29, 185, 84, 0.5)' },
                    { offset: 1, color: 'rgba(29, 185, 84, 0.1)' }
                ])
            }
        }]
    };

    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', loadDashboardData);
