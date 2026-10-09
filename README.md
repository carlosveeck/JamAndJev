# Jam n' Jev 🎵⚖️

Experimento de Criatividade Computacional desenvolvido para a disciplina da faculdade, explorando a interseção entre geração procedural de conteúdo e avaliação estruturada por IA (LLM-as-a-Judge).

## Aposta Inicial
A ideia inicial era aprender a utilizar o JEV e entender as nuances do seu funcionamento, além de exercitar sistemas multiagentes. Como eu estava muito interessado no conceito de fusão conceitual de músicas — devido ao projeto autoral da minha equipe, o Recifusão —, decidi enveredar por algo nesse caminho.

## O que foi usado?
* **Ferramentas e Modelos:** API do Google Gemini (`gemini-3.5-flash-lite`), TypeSafe API (System One / Jev), Python 3.8, VS Code e ambiente virtual (`venv`).
* **Abordagem:** Sistemas Multiagentes (Gerador vs. Crítico), *Concept Blending*, Prompts dinâmicos com controle de temperatura (`1.8`) e injeção de aleatoriedade geográfica e temporal.

## O que aconteceu?
A princípio, tive dificuldades para me comunicar com a API do Jev, mas a boa documentação deles ajudou bastante a ajustar a estrutura das requisições. Também enfrentei problemas com as versões iniciais do prompt, já que o agente criativo do Gemini tendia a repetir muitos gêneros musicais ou gerar misturas que o avaliador sempre considerava inviáveis comercialmente. O que surpreendeu positivamente foi ver o sistema multiagente funcionando de forma integrada, o que consegui solucionar ajustando a temperatura do modelo e criando um alternador dinâmico de perfis no prompt para equilibrar propostas underground e comerciais.

## O que eu aprendi?
Aprendi que o Jev é uma ferramenta extremamente útil e barata para estruturar classificações automatizadas, embora seja importante lembrar que ele funciona estritamente como um classificador e não como um gerador de texto livre. Também aprofundei bastante o aprendizado sobre a construção de prompts em sistemas multiagentes, entendendo como alinhar a criatividade de um modelo com a avaliação de outro. Para a próxima peça, fica o aprendizado de alinhar melhor o papel de cada agente e o formato dos dados logo no início, para evitar retrabalho e fazer tudo encaixar mais rápido.

---

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/carlosveeck/JamAndJev.git
   cd JamAndJev
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:
   ```bash
   pip install google-genai requests python-dotenv
   ```

4. Configure suas chaves de API:
   * Renomeie o arquivo `.env.example` para `.env`
   * Insira suas chaves do Gemini e da TypeSafe.

5. Execute o script:
   ```bash
   python jam_n_jev.py
   ```