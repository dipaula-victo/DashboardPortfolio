import streamlit as st
from PIL import Image

# Carrega a imagem da logo
logo = Image.open('img/logo.png')

# Configurações da página, incluindo o ícone da aba do navegador
st.set_page_config(
    page_title="Formação e experiências",
    page_icon=logo,
    layout="wide"
)

def education_experience_page():
    
    # Adiciona a logo na sidebar
    with st.sidebar:
        st.image(logo, width=30)

    col1, col2 = st.columns([1, 9])

    with col1:
        # Coloca a logo na primeira coluna
        st.image(logo, width=100)

    with col2:
        # Título
        st.title("Formação e Experiências")
    
    # Seção de Formação Acadêmica
    st.divider()

    st.subheader("Formação Acadêmica")
    st.markdown("""
        * **Engenharia de Software** - FIAP (Faculdade de Informática e Administração Paulista) 
            * 2024 - Em andamento (2º ano) 
        * **Ensino Médio Completo** - Colégio Objetivo de Vargem Grande Paulista 
            * Concluído em 2023 
    """)

    # Seção de Cursos e Conhecimentos Adicionais
    st.subheader("Cursos e Conhecimentos Adicionais")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            * Curso de Robótica - SESI, 2017 
            * Curso de Inglês - FISK, 2021 - Fluente
            * Estudo informal de Francês - Iniciante 
            * Curso de algoritmos - FIAP, 2025
            * Curso de Design Thinking - FIAP, 2024
            * Curso de estrutura de computadores - FIAP, 2024
            * Curso de formação social e sustentabilidade - FIAP, 2024
            * Trilha de treinamentos comportamentais - Programa LevelUP (Logicalis), 2025
        """)
        st.markdown("Conhecimentos por interesse próprio:")
        st.markdown("""
            * Design gráfico (Photoshop) 
            * Produção musical (FL Studio, Ableton Live) 
            * Edição de vídeo (VEGAS, Davinci Resolve) 
            * Computação (hardware, software, sistemas operacionais em nível intermediário) 
        """)

    # Adiciona o CSS personalizado para os botões
    st.markdown("""
    <style>
    .stDownloadButton > button {
        width: 400px;
        height: 70px;
    }
    </style>
    """, unsafe_allow_html=True)

    with col2:
        cert_path_1 = "../certificados/Algoritmos - Aprenda a programar.pdf"
        with open(cert_path_1, "rb") as file:
            btn = st.download_button(
                label="Certificado - Algoritmos",
                data=file,
                file_name="certificado_de_algoritmos.pdf",
                mime="application/pdf"
            )
        
        cert_path_2 = "../certificados/Design Thinking - Process.pdf"
        with open(cert_path_2, "rb") as file:
            btn = st.download_button(
                label="Certificado - Design Thinking",
                data=file,
                file_name="certificado_de_design_thinking.pdf",
                mime="application/pdf"
            )
        
        cert_path_3 = "../certificados/Estruturas de Computadores.pdf"
        with open(cert_path_3, "rb") as file:
            btn = st.download_button(
                label="Certificado - Estruturas de Computadores",
                data=file,
                file_name="certificado_de_estrutura_de_computadores.pdf",
                mime="application/pdf"
            )
        
        cert_path_4 = "../certificados/Formação Social e Sustentabilidade.pdf"
        with open(cert_path_4, "rb") as file:
            btn = st.download_button(
                label="Certificado - Formação Social e Sustentabilidade",
                data=file,
                file_name="certificado_de_formação_social_e_sustentabilidade.pdf",
                mime="application/pdf"
            )
        
        cert_path_5 = "../certificados/Trilha de Treinamentos Comportamentais.pdf"
        with open(cert_path_5, "rb") as file:
            btn = st.download_button(
                label="Certificado - Trilha de Treinamentos Comportamentais",
                data=file,
                file_name="certificado_de_trilha_de_treinamentos_comportamentais.pdf",
                mime="application/pdf"
            )
    
    # Seção de Projetos Acadêmicos
    st.subheader("Projetos Acadêmicos")
    st.markdown("""
        * **[Análise Descritiva de Dados em Futebol](https://github.com/dipaula-victo/futebol-analise-estatistica-clubes-brasileiros) (Data Science)**
            * **Ferramentas:** Google Colab, Python, Pandas, Matplotlib
            * **Descrição:** Desenvolvimento de um notebook interativo para análise de dados estatísticos em partidas de futebol. O projeto envolveu coleta, limpeza e visualização de dados, com foco em identificar padrões de desempenho de jogadores e times.
    """)
    st.markdown("""
        * **[Otimização da Distribuição de Produtos Essenciais](https://github.com/dipaula-victo/urban-resource-optimization) (Programação Dinâmica)**
            * **Ferramentas:** Google Colab, Python
            * **Descrição:** Implementação de uma solução baseada em programação dinâmica para otimizar a logística de distribuição de produtos essenciais em grandes cidades, considerando variáveis como distância, prioridade e recursos limitados.
    """)
        
    
    # Adicionando o rodapé
    st.divider() # Adiciona uma linha horizontal para separar o conteúdo do rodapé
    st.markdown(f"""
        <div style="text-align: center;">
            <p>
                <b>Contato:</b><br>
                📞 Telefone: (11) 91032-7240  | 📧 E-mail: dipaula.victo@gmail.com  | 🔗 <a href="https://github.com/dipaula-victo">GitHub</a><br>
            </p>
                <b>© 2025</b>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    education_experience_page()
