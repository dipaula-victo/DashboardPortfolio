import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÕES INICIAIS E FUNÇÕES AUXILIARES ---

# Carrega a imagem da logo
logo = Image.open('img/logo.png')

# Configurações da página
st.set_page_config(
    page_title="Análise de dados",
    page_icon=logo,
    layout="wide"
)

# Funções auxiliares do script original
def format_number(n):
    if n >= 1e9: return f'{n/1e9:.0f}B'
    if n >= 1e6: return f'{n/1e6:.0f}M'
    if n >= 1e3: return f'{n/1e3:.0f}K'
    return str(n)

def format_estimated_owners(owner_range):
    parts = owner_range.replace(',', '').split(' - ')
    if len(parts) == 2:
        start, end = int(parts[0]), int(parts[1])
        return f"{format_number(start)} - {format_number(end)}"
    return owner_range.replace(',', '')

def sort_key(s):
    try:
        if ' - ' in s:
            parts = s.split(' - ')
            start = int(parts[0].replace('K', '000').replace('M', '000000').replace('B', '000000000'))
            end = int(parts[1].replace('K', '000').replace('M', '000000').replace('B', '000000000'))
            return (start, end)
        return (int(s.replace('K', '000').replace('M', '000000').replace('B', '000000000')), 0)
    except:
        return (9999999999, 9999999999)

# --- MELHORIA DE PERFORMANCE E LOGS: FUNÇÃO DE CACHE PARA CARREGAR E PROCESSAR OS DADOS ---
@st.cache_data
def load_and_process_data():
    log_messages = []
    log_messages.append("Iniciando carregamento do arquivo 'dataset/games.csv'...")
    df = pd.read_csv('dataset/games.csv')
    log_messages.append(f"Arquivo carregado com sucesso. {len(df)} linhas encontradas.")

    duplicatas = df.duplicated().sum()
    if duplicatas > 0:
        log_messages.append(f"Encontradas {duplicatas} linhas duplicadas. Removendo...")
        df.drop_duplicates(inplace=True)
        log_messages.append("Duplicatas removidas.")
    else:
        log_messages.append("Nenhuma linha duplicada encontrada.")
    
    log_messages.append("Iniciando tratamento de valores nulos para colunas indispensáveis...")
    colunas_indispensaveis = ['Price', 'Genres', 'Positive', 'Metacritic score', 'Reviews', 'Estimated owners']
    for col in colunas_indispensaveis:
        if df[col].isnull().sum() > 0:
            if df[col].dtype == 'object':
                df[col].fillna('Desconhecido', inplace=True)
            else:
                df[col].fillna(df[col].median(), inplace=True)
            log_messages.append(f"-> Valores nulos na coluna '{col}' foram tratados.")
    log_messages.append("Tratamento de valores nulos concluído.")

    log_messages.append("Iniciando tratamento de outliers para a coluna 'Price'...")
    Q1, Q3 = df['Price'].quantile(0.25), df['Price'].quantile(0.75)
    limite_superior = Q3 + 1.5 * (Q3 - Q1)
    outliers_count = (df['Price'] > limite_superior).sum()
    df['Price'] = np.where(df['Price'] > limite_superior, limite_superior, df['Price'])
    log_messages.append(f"{outliers_count} outliers de preço foram ajustados para o limite superior de ${limite_superior:.2f}.")

    log_messages.append("Iniciando engenharia de features...")
    df['Release date'] = pd.to_datetime(df['Release date'], format='%b %d, %Y', errors='coerce')
    df['Release Year'] = df['Release date'].dt.year
    df.dropna(subset=['Release Year'], inplace=True)
    df['Release Year'] = df['Release Year'].astype(int)
    log_messages.append("-> Coluna 'Release Year' criada.")
    df['Total_Reviews'] = df['Positive'] + df['Negative']
    log_messages.append("-> Coluna 'Total_Reviews' criada.")
    df['Positive_Percentage'] = np.where(df['Total_Reviews'] > 0, (df['Positive'] / df['Total_Reviews']) * 100, 0)
    log_messages.append("-> Coluna 'Positive_Percentage' criada.")
    df['Estimated owners'] = df['Estimated owners'].apply(format_estimated_owners)
    log_messages.append("-> Coluna 'Estimated owners' formatada.")
    log_messages.append("Engenharia de features concluída.")
    
    log_messages.append("Pré-processamento de dados finalizado com sucesso!")
    return df, log_messages

def data_analysis_page():
    # --- SIDEBAR ---
    with st.sidebar:
        st.image(logo, width=30)

    try:
        df, logs = load_and_process_data()
    except FileNotFoundError:
        st.error("Arquivo 'dataset/games.csv' não encontrado. Verifique o caminho do arquivo.")
        st.stop()

    st.sidebar.header("Filtros")
    df_genres_filter = df.copy()
    df_genres_filter['Genres'] = df_genres_filter['Genres'].str.split(',')
    df_genres_filter = df_genres_filter.explode('Genres')
    df_genres_filter['Genres'] = df_genres_filter['Genres'].str.strip()
    all_genres = sorted(df_genres_filter['Genres'].unique())
    selected_genres = st.sidebar.multiselect("Selecione o(s) Gênero(s):", options=all_genres, default=[])

    min_year, max_year = int(df['Release Year'].min()), int(df['Release Year'].max())
    selected_year_range = st.sidebar.slider("Selecione o Ano de Lançamento:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    if selected_genres:
        filtered_df = df[df['Genres'].apply(lambda x: any(g in x for g in selected_genres))].copy()
    else:
        filtered_df = df.copy()
    filtered_df = filtered_df[(filtered_df['Release Year'] >= selected_year_range[0]) & (filtered_df['Release Year'] <= selected_year_range[1])]
    
    st.sidebar.divider()
    st.sidebar.subheader("Resumo da Seleção")
    if filtered_df.empty:
        st.warning("Nenhum jogo encontrado com os filtros selecionados.")
        st.stop()
    
    col1_side, col2_side = st.sidebar.columns(2)
    col1_side.metric(label="Jogos Selecionados", value=f"{len(filtered_df):,}")
    col2_side.metric(label="Total de Avaliações", value=f"{format_number(filtered_df['Total_Reviews'].sum())}")
    
    # --- LAYOUT PRINCIPAL ---
    col1, col2 = st.columns([1, 9])
    with col1: st.image(logo, width=100)
    with col2: st.title("Análise de Dados de Jogos da Steam")
    st.divider()

    # --- INTRODUÇÃO VISÍVEL POR PADRÃO ---
    st.subheader("Sobre o Projeto")
    st.markdown("""
        Esta seção do dashboard foi projetada para uma análise estruturada de um conjunto de dados com cerca de 70 mil registros de jogos da Steam. O objetivo é explorar tendências, identificar padrões e extrair insights valiosos a partir dos dados.
    """)
    st.divider()

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### Sobre a Steam")
        st.markdown("""
            Steam é uma renomada plataforma de jogos digitais que serve como um hub para jogadores em todo o mundo. Desenvolvida e operada pela Valve Corporation, a Steam revolucionou a forma como os jogadores acessam e desfrutam de seus videogames favoritos. Lançada em 2003, rapidamente ganhou popularidade e se tornou a plataforma de referência para jogos de PC. Em sua essência, a Steam oferece aos usuários uma vasta biblioteca de jogos que abrangem diversos gêneros, desde títulos indie até lançamentos de sucesso. Os jogadores podem navegar e comprar jogos diretamente na plataforma, que são então adicionados à sua biblioteca digital para fácil acesso. A Steam também oferece uma maneira segura e conveniente de instalar, atualizar e gerenciar jogos, eliminando a necessidade de mídia física.
        """)
    with col2:
        st.image("img/steam_logo.png")

    with st.expander("Ver Log de Processamento de Dados"):
        for log in logs:
            st.info(log)
            
    st.subheader("Apresentação dos Dados e Tipos de Variáveis")
    st.markdown("### Sobre este Conjunto de Dados")
    st.markdown("""
        O conjunto de dados "All Steam Spiele und deren Metadaten" é uma coleção abrangente de dados que engloba diversos jogos disponíveis na plataforma Steam, juntamente com seus metadados correspondentes. Ele serve como um recurso valioso para pesquisadores, desenvolvedores e entusiastas de jogos interessados em explorar e analisar o vasto ecossistema de jogos da Steam. O conjunto de dados inclui informações sobre cada jogo, como título, data de lançamento, desenvolvedor, editora, gênero, avaliações de usuários, classificações e requisitos de sistema. Ele cobre uma ampla gama de gêneros de jogos, incluindo ação, aventura, estratégia, RPG, simulação, esportes e muito mais, fornecendo uma representação diversificada e extensa da biblioteca de jogos da Steam.
    """)
    st.dataframe(df.head())
    
    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown("### Classificação das Variáveis")
        st.markdown("""
            **Variáveis Qualitativas Nominais:**
            * `Name`, `Website`, `Support url`, `Support email`, `About the game`, `Header image`, `Metacritic url`, `Notes`, `Developers`, `Publishers`, `Categories`, `Genres`, `Tags`, `Screenshots`, `Movies`, `Supported languages`, `Full audio languages`, `Windows`, `Mac`, `Linux`.
            
            **Variáveis Qualitativas Ordinais:**
            * `Metacritic score`, `Score rank`, `User score`, `Estimated owners`.
            
            **Variáveis Quantitativas Discretas:**
            * `AppID`, `Peak CCU`, `Required age`, `DLC count`, `Reviews`, `Positive`, `Negative`, `Achievements`, `Recommendations`.
            
            **Variáveis Quantitativas Contínuas:**
            * `Release date`, `Price`, `Average playtime forever`, `Average playtime two weeks`, `Median playtime forever`, `Median playtime two weeks`.
            """)
    with col2:
        st.markdown("### Perguntas de Análise")
        st.markdown("""
            * Existe uma correlação entre o preço de um jogo e a quantidade de donos estimados?
            * A porcentagem de avaliações positivas (calculada a partir das colunas `Positive` e `Negative`) varia de acordo com o preço?
            * Quais os 10 principais gêneros (ou tags) de jogos com maior tempo de jogo médio (`Average playtime forever`)?
            * Qual a correlação entre a pontuação do Metacritic e as recomendações dos usuários?
            * Existe uma diferença significativa na média de avaliações positivas entre jogos com alto e baixo número de conquistas (`Achievements`)?
            * Como a média de preço dos jogos se comporta ao longo dos anos de lançamento? (Análise temporal usando `Release date`)
            * Existe uma faixa de preço ideal que maximiza o número de avaliações (a soma de `Positive` e `Negative`)?
            """)
    st.divider()
    
    # --- ABAS DE NAVEGAÇÃO ---
    st.header("Análise Exploratória e Inferência")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Popularidade e Gêneros", "📈 Tendências de Mercado", "🔬 Inferência Estatística", "✅ Conclusão"])

    with tab1:
        st.subheader("Análise de Popularidade vs. Preço")
        unique_owners = sorted(filtered_df['Estimated owners'].unique(), key=sort_key)
        fig_price_owners = px.box(filtered_df, x='Estimated owners', y='Price', title='Distribuição de Preço por Faixa de Donos Estimados', category_orders={"Estimated owners": unique_owners})
        fig_price_owners.update_xaxes(title_text='Faixa de Donos Estimados').update_yaxes(title_text='Preço (USD)')
        st.plotly_chart(fig_price_owners, use_container_width=True)
        st.markdown("""
        * **Preço concentrado em faixas baixas:** A maioria dos jogos, em todas as faixas de donos estimados, tem seu preço mediano abaixo de 15 USD. Isso sugere que o preço não é um fator determinante para a quantidade de donos, e que muitos jogos com grandes bases de jogadores são de baixo custo ou gratuitos.
        * **Jogos gratuitos dominam as faixas mais altas:** O gráfico mostra que as duas faixas de donos mais altas, **`20M - 50M`** e **`50M - 100M`**, têm um preço mediano igual a zero. Isso indica que, para atingir o maior número de donos, o modelo de negócios de jogos gratuitos é uma estratégia predominante.
        * **Outliers e variação de preços:** As faixas com poucos donos (`0 - 0` e `0 - 20k`) apresentam a maior variabilidade de preços, com muitos outliers que chegam a custar mais de 20 USD. Isso pode refletir jogos de nicho, versões premium ou simplesmente jogos que não alcançaram uma grande popularidade. No caso da faixa de `0 - 0`, é possível concluir que dentro da biblioteca da Steam há muitos jogos que jamais foram comprados, ou têm um número de jogadores irrelevante no dataset.
        """)

        st.subheader("Análise de Desempenho por Gênero e Tags")
        df_genres_tab = filtered_df.copy()
        df_genres_tab['Genres'] = df_genres_tab['Genres'].str.split(',')
        df_genres_tab = df_genres_tab.explode('Genres')
        df_genres_tab['Genres'] = df_genres_tab['Genres'].str.strip()
        top_genres = df_genres_tab.groupby('Genres')['Average playtime forever'].mean().nlargest(10).reset_index().sort_values('Average playtime forever', ascending=True)
        
        col1_g, col2_g = st.columns([1.5, 1])
        with col1_g:
            fig_top_genres = px.bar(top_genres, x='Average playtime forever', y='Genres', orientation='h', title='Top 10 Gêneros por Tempo Médio de Jogo')
            fig_top_genres.update_xaxes(title_text='Tempo Médio de Jogo (minutos)').update_yaxes(title_text='Gênero')
            st.plotly_chart(fig_top_genres, use_container_width=True)
        with col2_g:
            st.markdown("""
            * **Aplicativos e Ferramentas com Maior Tempo de Jogo:** As categorias com o maior tempo médio de jogo não são jogos tradicionais. O topo da lista é dominado por software de produção de áudio, publicação na web, utilitários, design e edição de vídeo. Isso indica que essas ferramentas, quando disponíveis na plataforma, são utilizadas por longos períodos.
            * **Gêneros de Jogos com Alto Engajamento:** O único gênero de jogo tradicional a entrar no top 10 é `Massively Multiplayer`, o que reforça a ideia de que jogos que incentivam a interação contínua entre jogadores possuem um alto potencial de engajamento a longo prazo.
            * **Baixo Tempo de Jogo para Educação e Desenvolvimento:** Categorias como `Education`e `Game Development` aparecem na parte inferior do ranking, com tempo médio de jogo significativamente menor. Isso sugere que, em geral, essas aplicações são usadas por períodos mais curtos do que as ferramentas de produção criativa.
            """)

    with tab2:
        st.subheader("Distribuição de Avaliações por Faixa de Preço")
        price_bins = [0, 0.01, 5.0, 10.0, 15.0, 20.0, float('inf')]
        price_labels = ['Free', '0.01 - 5', '5.01 - 10', '10.01 - 15', '15.01 - 20', 'Over 20']
        filtered_df['Price_Bins'] = pd.cut(filtered_df['Price'], bins=price_bins, labels=price_labels, right=False)
        fig_price_pos_pct = px.box(filtered_df, x='Price_Bins', y='Positive_Percentage', title='Distribuição de % de Avaliações Positivas por Faixa de Preço')
        fig_price_pos_pct.update_xaxes(title_text='Faixa de Preço', categoryorder='array', categoryarray=price_labels).update_yaxes(title_text='Porcentagem de Avaliações Positivas (%)')
        st.plotly_chart(fig_price_pos_pct, use_container_width=True)
        st.markdown("""
        * **Distribuição de avaliações em jogos pagos:** Jogos com preço acima de zero apresentam uma distribuição de avaliações muito mais consistente e positiva. A mediana da porcentagem de avaliações positivas para todas as faixas de preço pagas está consistentemente alta, por volta de 70-80%, o que sugere que ao pagar por um jogo, os jogadores tendem a ter uma expectativa de qualidade que é frequentemente atendida.
        * **Os extremos dos jogos gratuitos:** A categoria de jogos gratuitos (`Free`) apresenta a maior dispersão nas avaliações, com uma mediana mais baixa (cerca de 34%) e a maior amplitude interquartil, indicando uma alta volatilidade nos resultados. A presença de um grande número de outliers em 100% reforça a ideia de que muitos jogos gratuitos com poucas avaliações se concentram nos extremos, um fenômeno que não é tão proeminente nas faixas de preço pagas.
        * **Falta de correlação linear com o preço:** O gráfico não mostra uma tendência clara de que jogos mais caros recebem avaliações percentuais mais altas. As medianas da porcentagem de avaliações positivas permanecem estáveis em todas as faixas de preço pagas, indicando que, após o jogo ter um preço, o valor em si não é o principal fator para avaliações mais altas.
        """)

        st.subheader("Tendências de Mercado")
        df_by_year = filtered_df.groupby('Release Year')['Price'].mean().reset_index()
        col1_t, col2_t = st.columns([1.8, 1])
        with col1_t:
            selected_window = st.selectbox("Escolha o Período da Média Móvel (em anos):", options=[1, 3, 5, 7], index=1)
            df_by_year['Média Móvel'] = df_by_year['Price'].rolling(window=selected_window, min_periods=1).mean()
            fig_price_trend = go.Figure()
            fig_price_trend.add_trace(go.Scatter(x=df_by_year['Release Year'], y=df_by_year['Price'], mode='lines+markers', name='Preço Médio Original'))
            fig_price_trend.add_trace(go.Scatter(x=df_by_year['Release Year'], y=df_by_year['Média Móvel'], mode='lines', name=f'Média Móvel ({selected_window} anos)', line=dict(color='blue', width=3)))
            fig_price_trend.update_layout(title='Preço Médio dos Jogos ao Longo dos Anos', xaxis_title='Ano de Lançamento', yaxis_title='Preço Médio (USD)', legend_title='Séries')
            st.plotly_chart(fig_price_trend, use_container_width=True)
        with col2_t:
            st.markdown("""
            * **Pico Histórico de Preço:** A linha de média móvel confirma que o preço médio dos jogos na Steam atingiu seu pico histórico na década dos anos 2000, superando os 10 USD. Isso pode refletir o período em que jogos de PC eram majoritariamente lançados por grandes estúdios, com preços mais elevados.
            * **Tendência de Queda Acelerada:** O gráfico suavizado pela média móvel demonstra de forma robusta uma tendência de queda constante no preço médio dos jogos, que se acentuou significativamente a partir de 2022. Essa queda reflete a crescente popularidade e o grande volume de jogos gratuitos e de baixo custo que entram na plataforma, além do fim dos registros do dataset.
            * **Estabilização Temporária:** A média móvel mostra um período de relativa estabilidade no preço médio entre 2018 e 2022, antes da queda recente. Isso sugere que o mercado se estabilizou por um tempo, mas a tendência de longo prazo de barateamento dos jogos continua.
            """)

        st.markdown("<br><br>", unsafe_allow_html=True)
        df_by_price_bin = filtered_df.groupby('Price_Bins', observed=False)['Total_Reviews'].mean().reset_index()
        col1_pb, col2_pb = st.columns([1, 1])
        with col2_pb:
            fig_price_bin = px.bar(df_by_price_bin, x='Price_Bins', y='Total_Reviews', title='Número Médio de Avaliações por Faixa de Preço')
            fig_price_bin.update_xaxes(title_text='Faixa de Preço', type='category').update_yaxes(title_text='Número Médio de Avaliações')
            st.plotly_chart(fig_price_bin, use_container_width=True)
        with col1_pb:
            st.markdown("""
            * **Relação de Avaliações em Faixas de Preço Baixas:** A faixa de preço `Free` tem um número médio de avaliações significativamente maior do que a faixa de `0.01 - 5` USD. Isso sugere que, embora o modelo gratuito atraia um grande volume de avaliações, a faixa mais baixa de jogos pagos pode ter menos visibilidade e um público menos propenso a deixar feedback.
            * **Relação Positiva e Acelerada:** Para jogos com preço acima de 5 USD, há uma relação positiva e acelerada: quanto maior a faixa de preço, maior o número médio de avaliações que ele recebe. O número de avaliações cresce consistentemente a cada faixa de preço mais alta.
            * **Pico de Engajamento em Jogos Mais Caros:** A categoria de jogos com preço `Over 20` USD recebe o maior número médio de avaliações, superando 6.000 por jogo. Isso indica que os jogos mais caros são, em média, os mais populares ou os que mais geram engajamento e feedback dos jogadores na plataforma.
            """)

    with tab3:
        st.subheader("Comparação de Avaliações e Métrica de Sucesso")
        corr_value = filtered_df[['Metacritic score', 'Recommendations']].corr().iloc[0,1]
        st.metric(label="Correlação entre Metacritic Score e Recomendações", value=f"{corr_value:.3f}")
        fig_metacritic_rec = px.scatter(filtered_df.sample(min(1000, len(filtered_df))), x='Metacritic score', y='Recommendations', title='Metacritic Score vs. Recomendações', trendline='ols', hover_data=['Name'], range_y=[0, 25000])
        st.plotly_chart(fig_metacritic_rec, use_container_width=True)
        st.markdown("""
        * **Correlação Fraca:** A correlação positiva de `0.124` demonstra uma relação muito fraca entre a pontuação do Metacritic e as recomendações dos usuários. Embora um Metacritic Score mais alto possa ter uma pequena tendência a gerar mais recomendações, a relação não é forte.
        * **Distribuição de Pontos:** A visualização mostra que a maioria dos jogos tem pontuações e recomendações baixas, com alguns outliers em ambas as variáveis, que podem representar jogos de grande sucesso.
        """)
        
        st.subheader("Intervalo de Confiança para a Média do Metacritic Score")
        st.markdown("""
            O `Metacritic score` foi escolhido para aplicar o Intervalo de Confiança por ser uma variável quantitativa e um dos indicadores mais importantes da qualidade e recepção crítica de um jogo. Ele nos permite fazer inferências sobre a população inteira de jogos da Steam a partir da sua amostra.
        """)
        
        selected_confidence = st.selectbox("Escolha o Nível de Confiança (%)", options=[70, 80, 90, 95, 99], index=3)
        metacritic_data = filtered_df['Metacritic score'].dropna()
        if len(metacritic_data) > 1:
            conf_interval = stats.t.interval(confidence=selected_confidence/100, df=len(metacritic_data)-1, loc=metacritic_data.mean(), scale=stats.sem(metacritic_data))
            st.info(f"Temos {selected_confidence}% de confiança de que a pontuação média real do Metacritic para os jogos selecionados está entre **{conf_interval[0]:.2f} e {conf_interval[1]:.2f}**.")

        st.subheader("Teste de Hipótese para Conquistas nos Jogos")
        st.markdown("""
            A escolha de conquistas (`Achievements`) para o teste de hipótese foi motivada por ser uma métrica que pode estar diretamente ligada ao esforço de desenvolvimento e à longevidade de um jogo. A hipótese é que um jogo com mais conquistas pode ser visto como mais completo, oferecendo mais conteúdo, o que poderia se traduzir em melhores avaliações.

            O teste de hipótese nos permite verificar se essa suposição é estatisticamente válida.
        """)
        
        median_achievements = filtered_df['Achievements'].median()
        high_ach_data = filtered_df[filtered_df['Achievements'] > median_achievements]['Positive'].dropna()
        low_ach_data = filtered_df[filtered_df['Achievements'] <= median_achievements]['Positive'].dropna()
        if not high_ach_data.empty and not low_ach_data.empty:
            t_stat_ach, p_value_ach = stats.ttest_ind(high_ach_data, low_ach_data, equal_var=False, nan_policy='omit')
            st.write(f"**Estatística T:** `{t_stat_ach:.2f}` | **Valor p:** `{p_value_ach:.4f}`")
            if p_value_ach < 0.05:
                st.success("O p-valor é menor que 0.05, indicando uma diferença estatisticamente significativa na média de avaliações positivas entre os dois grupos.")
            else:
                st.warning("O p-valor não é menor que 0.05. Não há evidência de uma diferença estatisticamente significativa.")

            fig_achievements_bp = px.box(filtered_df, x=np.where(filtered_df['Achievements'] > median_achievements, 'Acima da Mediana', 'Abaixo da Mediana'), y='Positive', title='Distribuição de Avaliações Positivas por Grupo de Conquistas', range_y=[0, 350])
            fig_achievements_bp.update_xaxes(title_text='Grupo de Conquistas').update_yaxes(title_text='Avaliações Positivas')
            st.plotly_chart(fig_achievements_bp, use_container_width=True)
            st.markdown("""
            * **Diferença de Médias:** O teste t com um p-valor de `0.0000` indica uma diferença estatisticamente significativa na média de avaliações positivas entre os dois grupos. O box plot, ao limitar o eixo Y, mostra claramente que a mediana de avaliações do grupo "Acima da Mediana" é superior.
            * **Distribuição de Dados:** A distribuição das avaliações do grupo "Acima da Mediana" é mais concentrada e tem uma mediana mais alta do que o grupo "Abaixo da Mediana", embora ambos os grupos tenham um grande número de outliers positivos, que podem ser melhor vistos ajustando a escala do gráfico.
            """)

    with tab4:
        st.markdown('### Conclusão Geral das Análises')
        st.markdown("""
            O dashboard demonstra uma abordagem analítica estruturada e aprofundada sobre o ecossistema de jogos da Steam, revelando insights valiosos sobre tendências de mercado, engajamento do usuário e percepção de qualidade, ainda que com as limitações da base de dados utilizada.
            
            A análise de tendência de preço ao longo dos anos mostra uma clara e acelerada tendência de queda no preço médio dos jogos desde 2012, impulsionada pelo crescimento exponencial de títulos free-to-play e de baixo custo. A visualização da distribuição de avaliações por faixa de preço revela uma dinâmica interessante: enquanto jogos gratuitos atraem um grande número de avaliações, os jogos pagos de baixo custo recebem menos feedback, e o número de avaliações aumenta drasticamente nas faixas de preço mais altas.

            O estudo do tempo de jogo médio por gênero revelou que as categorias com maior engajamento de longo prazo não são jogos tradicionais, mas sim softwares de produtividade e ferramentas criativas, como `Audio Production` e `Utilities`. No universo dos jogos, o gênero `Massively Multiplayer` se destaca como o único com um alto tempo de jogo médio. A análise de inferência estatística reforça essas descobertas, demonstrando que jogos com mais conquistas tendem a ter um número significativamente maior de avaliações positivas, sugerindo que o investimento do desenvolvedor em conteúdo se correlaciona com uma melhor recepção do público.

            A correlação entre o Metacritic Score e as recomendações é muito fraca, indicando que a pontuação da crítica não é um forte preditor de recomendações diretas dos usuários. Por fim, o Intervalo de Confiança para a média do `Metacritic Score` nos permite estimar o verdadeiro score médio da plataforma, fornecendo um parâmetro robusto para entender a percepção de qualidade do mercado de forma geral.
        """)

    st.divider()
    st.markdown("""
        <div style="text-align: center;">
            <p>
                <b>Contato:</b><br>
                📞 Telefone: (11) 91032-7240  | 📧 E-mail: dipaula.victo@gmail.com  | 🔗 <a href="https://github.com/dipaula-victo">GitHub</a><br>
            </p>
                <b>© 2025</b>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    data_analysis_page()