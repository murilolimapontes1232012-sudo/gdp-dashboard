import os
import streamlit as st
from groq import Groq

# Configuração da página do Streamlit
st.set_page_config(
    page_title="App de Nutrição e Fitness com IA",
    page_icon="💪",
    layout="centered"
)

# Título principal
st.title("💪 Assistente de Nutrição e Treino com IA")
st.write("Calcula as tuas necessidades diárias e tira dúvidas sobre dieta e exercício com Inteligência Artificial.")

# Inicializar o cliente da Groq usando os secrets do Streamlit
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ A chave `GROQ_API_KEY` não foi encontrada nos Secrets do Streamlit! Por favor, configura os Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Barra lateral para navegação
st.sidebar.header("Navegação")
opcao = st.sidebar.selectbox("Escolhe uma ferramenta:", ["Calculadora de Calorias/Macros", "Chat com Nutricionista IA"])

if opcao == "Calculadora de Calorias/Macros":
    st.subheader("📊 Calculadora de Necessidades Diárias")
    
    col1, col2 = st.columns(2)
    with col1:
        peso = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, value=60.0)
        altura = st.number_input("Altura (cm):", min_value=100.0, max_value=230.0, value=170.0)
    with col2:
        idade = st.number_input("Idade:", min_value=10, max_value=100, value=14)
        objetivo = st.selectbox("Objetivo:", ["Hipertrofia (Ganhar Massa)", "Emagrecimento (Perder Gordura)", "Manutenção"])

    if st.button("Calcular Dieta"):
        # Estimativa simples de calorias e proteínas
        if objetivo == "Hipertrofia (Ganhar Massa)":
            calorias = (peso * 24) + 400
            proteina = peso * 2.0
        elif objetivo == "Emagrecimento (Perder Gordura)":
            calorias = (peso * 24) - 400
            proteina = peso * 2.2
        else:
            calorias = peso * 24
            proteina = peso * 1.8

        st.success("✅ Cálculo efetuado com sucesso!")
        st.metric("Calorias Diárias Estimadas", f"{int(calorias)} kcal")
        st.metric("Consumo Recomendado de Proteína", f"{int(proteina)} g")
        
        st.info("💡 Dica: Mantém a consistência no treino e consome água suficiente todos os dias!")

elif opcao == "Chat com Nutricionista IA":
    st.subheader("💬 Pergunta ao Especialista em Nutrição e Treino")
    st.write("Tira dúvidas sobre alimentos, substituições de refeições ou rotinas de exercício.")

    # Caixa de texto para a pergunta do usuário
    pergunta_usuario = st.text_input("Escreve a tua dúvida aqui:", placeholder="Ex: O que posso comer pré-treino para ter mais energia?")

    if st.button("Enviar Pergunta"):
        if pergunta_usuario.strip() == "":
            st.warning("Por favor, escreve uma pergunta antes de enviar.")
        else:
            with st.spinner("A IA está a pensar na resposta..."):
                try:
                    # Chamada à API da Groq
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "És um nutricionista e personal trainer especializado em ajudar jovens e atletas com treinos de hipertrofia, dietas práticas e alimentação saudável."
                            },
                            {
                                "role": "user",
                                "content": pergunta_usuario
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                    )
                    
                    resposta_ia = chat_completion.choices[0].message.content
                    st.markdown("### Resposta:")
                    st.write(resposta_ia)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao comunicar com a IA: {e}")
    
    


   



        
