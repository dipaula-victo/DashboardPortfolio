import streamlit as st
from PIL import Image

# Carrega a imagem da logo
logo = Image.open('img/logo.png')

# Configurações da página, incluindo o ícone da aba do navegador
st.set_page_config(
    page_title="Skills",
    page_icon=logo,
    layout="wide"
)

def skills_page():
    # Adiciona a logo na sidebar
    with st.sidebar:
        st.image(logo, width=30)

    col1, col2 = st.columns([1, 9])

    with col1:
        # Coloca a logo na primeira coluna
        st.image(logo, width=100)

    with col2:
        # Título
        st.title("Habilidades e Competências")

    st.divider()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Habilidades Técnicas")
        
        st.markdown("""
        * **Linguagens e Ferramentas de Programação:**
            * Lógica de programação
            * Python - Nível Intermediário
            * Pandas
            * Matplotlib
            * Google Colab
        """)

        st.markdown("""
        * **Conhecimentos Específicos:**
            * Data Science
            * Programação Dinâmica
            * Pacote Office
            * Edição de imagem e vídeo
            * Produção musical e edição de áudio
        """)

    with col2:
        st.subheader("Soft Skills")
        st.markdown("""
        * Autodidatismo
        * Criatividade
        * Organização
        * Trabalho em equipe
        * Comunicação interpessoal
        * Facilidade com novas tecnologias e aprendizados
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
    skills_page()