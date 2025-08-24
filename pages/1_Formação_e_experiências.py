import streamlit as st
from PIL import Image
from pathlib import Path

# Carrega a imagem da logo
logo = Image.open('img/logo.png')

# Configurações da página
st.set_page_config(
    page_title="Formação e experiências",
    page_icon=logo,
    layout="wide"
)

def education_experience_page():
    # Define o caminho raiz do projeto de forma confiável
    PROJECT_ROOT = Path(__file__).parent.parent
    CERTIFICADOS_DIR = PROJECT_ROOT / "certificados"

    # Adiciona a logo na sidebar
    with st.sidebar:
        st.image(logo, width=30)

    col1, col2 = st.columns([1, 9])
    with col1:
        st.image(logo, width=100)
    with col2:
        st.title("Formação e Experiências")
    
    st.divider()
    st.subheader("Formação Acadêmica")
    st.markdown("""
        * **Engenharia de Software** - FIAP (Faculdade de Informática e Administração Paulista) 
            * 2024 - Em andamento (2º ano) 
        * **Ensino Médio Completo** - Colégio Objetivo de Vargem Grande Paulista 
            * Concluído em 2023 
    """)

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

    st.markdown("""
    <style>
    .stDownloadButton > button {
        width: 400px;
        height: 70px;
    }
    </style>
    """, unsafe_allow_html=True)

    with col2:

        # Certificado 1
        cert_path_1 = CERTIFICADOS_DIR / "Algoritmos - Aprenda a programar.pdf"
        with open(cert_path_1, "rb") as file:
            pdf_bytes_1 = file.read() # Lê o conteúdo para uma variável
        st.download_button(
            label="Certificado - Algoritmos",
            data=pdf_bytes_1, # Passa os bytes diretamente
            file_name="certificado_de_algoritmos.pdf",
            mime="application/pdf"
        )
        
        # Certificado 2
        cert_path_2 = CERTIFICADOS_DIR / "Design Thinking - Process.pdf"
        with open(cert_path_2, "rb") as file:
            pdf_bytes_2 = file.read()
        st.download_button(
            label="Certificado - Design Thinking",
            data=pdf_bytes_2,
            file_name="certificado_de_design_thinking.pdf",
            mime="application/pdf"
        )
        
        # Certificado 3
        cert_path_3 = CERTIFICADOS_DIR / "Estruturas de Computadores.pdf"
        with open(cert_path_3, "rb") as file:
            pdf_bytes_3 = file.read()
        st.download_button(
            label="Certificado - Estruturas de Computadores",
            data=pdf_bytes_3,
            file_name="certificado_de_estrutura_de_computadores.pdf",
            mime="application/pdf"
        )
        
        # Certificado 4
        cert_path_4 = CERTIFICADOS_DIR / "Formação Social e Sustentabilidade.pdf"
        with open(cert_path_4, "rb") as file:
            pdf_bytes_4 = file.read()
        st.download_button(
            label="Certificado - Formação Social e Sustentabilidade",
            data=pdf_bytes_4,
            file_name="certificado_de_formação_social_e_sustentabilidade.pdf",
            mime="application/pdf"
        )
        
        # Certificado 5
        cert_path_5 = CERTIFICADOS_DIR / "Trilha de Treinamentos Comportamentais.pdf"
        with open(cert_path_5, "rb") as file:
            pdf_bytes_5 = file.read()
        st.download_button(
            label="Certificado - Trilha de Treinamentos Comportamentais",
            data=pdf_bytes_5,
            file_name="certificado_de_trilha_de_treinamentos_comportamentais.pdf",
            mime="application/pdf"
        )
    
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
    st.divider()
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