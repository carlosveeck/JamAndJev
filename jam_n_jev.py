import os
import json
import requests
import time
import random
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Carrega as chaves
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY")

JEV_API_URL = "https://api.typesafe.ai/v1/systemone"
client = genai.Client(api_key=GEMINI_API_KEY)

def gerar_fusao(iteracao):
    # Dicionários de aleatoriedade para forçar o Gemini a sair do padrão
    continentes = ["África Subsaariana", "Leste Europeu", "Extremo Oriente", "América Latina", "Oriente Médio", "Oceania e Polinésia", "Celtas/Nórdicos"]
    epocas = ["Antiguidade Clássica", "Idade Média", "Anos 80", "Futuro Distópico", "Século XIX", "Era de Ouro do Rádio", "Idade Contemporânea"]
    
    foco_1 = random.choice(continentes)
    foco_2 = random.choice(epocas)
    
    # ALTERNADOR DE ESTILO: Ímpar = Bizarro/Underground | Par = Comercial/Rádio
    is_comercial = (iteracao % 2 == 0)
    
    if is_comercial:
        perfil = "um mega-produtor musical de hits globais, focado em criar tendências que tocam na rádio e viralizam"
        objetivo = "unir dois gêneros musicais de forma muito inovadora, mas criando uma música ACESSÍVEL, POP e AGRADÁVEL ao grande público"
        vibe = "Crie uma fusão grounded e altamente comercial. Tem que ser inovadora, mas com estrutura cativante e pronta para estourar nas paradas de sucesso."
    else:
        perfil = "um agente de criatividade musical de vanguarda e curador de bizarrices estéticas"
        objetivo = "criar o 'Concept Blending' de dois gêneros musicais diametralmente opostos — de épocas, culturas e instrumentações que nunca deveriam se cruzar"
        vibe = "Crie uma fusão coerente, mas absurdamente excêntrica, caótica e underground."

    prompt = f"""
    Você é {perfil}.
    Sua missão é {objetivo}.
    
    [DIRETRIZ DE ALEATORIEDADE]: Para garantir que você não repita ideias, nesta iteração ({iteracao}) tente buscar inspiração em ritmos da região '{foco_1}' e estéticas da época '{foco_2}'. Não precisa ser literal, use como semente criativa!
    
    {vibe}
    
    Retorne APENAS um JSON válido e estrito com esta estrutura exata:
    {{
      "genero_1": "Primeiro gênero original",
      "genero_2": "Segundo gênero original",
      "nome_da_fusao": "Nome criativo e impactante da mistura",
      "descricao": "Descreva em 1 parágrafo intenso como soa essa música. Detalhe os instrumentos colidindo, o andamento, a textura sonora e a atmosfera."
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=1.8, # Continua alto para manter a criatividade
        )
    )
    return json.loads(response.text)

def criticar_com_jev(fusao):
    state_text = f"Fusão: {fusao['nome_da_fusao']}. Mistura de {fusao['genero_1']} e {fusao['genero_2']}. Descrição: {fusao['descricao']}"
    
    # ESTRUTURA EXATA DA DOCUMENTAÇÃO DO JEV
    payload_jev = {
        "model": "jev-latest",
        "state": state_text,
        "questions": {
            "ambiente_ideal": {
                "type": "choice",
                "instructions": "Em qual ambiente essa música faria mais sentido?",
                "criteria": {
                    "Festa": "Lugar animado, festivo e descontraído",
                    "Igreja": "Ambiente religioso, solene ou meditativo",
                    "Rave": "Festa eletrônica com batidas repetitivas e intensas",
                    "Moshpit": "Rodinha punk, caos e agressividade sonora",
                    "Quarto_Escuro": "Música introspectiva e experimental para ouvir sozinho"
                }
            },
            "nivel_energia": {
                "type": "score",
                "instructions": "Qual o nível de agitação e energia dessa música?",
                "criteria": [
                    "Calmaria absoluta ou música de ninar",
                    "Tranquilo, relaxante",
                    "Moderado, dá para dançar de leve",
                    "Muito agitado, ritmo acelerado",
                    "Caos total, roda punk, agressivo"
                ]
            },
            "potencial_de_radio": {
                "type": "noul",
                "instructions": "Uma pessoa comum conseguiria ouvir essa música no rádio do carro sem mudar de estação?"
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {TYPESAFE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(JEV_API_URL, headers=headers, json=payload_jev)
    
    if not response.ok:
        print(f"\n❌ Erro na API do Jev: {response.text}")
        response.raise_for_status() 
        
    return response.json()

if __name__ == "__main__":
    print("🎵 Jam n' Jev: Iniciando Geração em Lote...\n")
    
    resultados_finais = []
    
    for i in range(1, 6):
        print(f"--- Gerando Fusão {i}/5 ---")
        try:
            nova_fusao = gerar_fusao(i) # Passando a iteração para o prompt dinâmico
            print(f"🎸 CRIADO: {nova_fusao['genero_1']} + {nova_fusao['genero_2']} = {nova_fusao['nome_da_fusao']}")
            
            print("⚖️ Avaliando com Jev...")
            critica = criticar_com_jev(nova_fusao)
            
            # Navegando no JSON de resposta exatamente como a documentação mostrou
            res_jev = critica.get('answers', {})
            
            ambiente = res_jev.get('ambiente_ideal', {}).get('choice', 'Desconhecido')
            energia = res_jev.get('nivel_energia', {}).get('score', 0)
            
            # O Noul retorna um valor entre 0 e 1.
            noul_prob = res_jev.get('potencial_de_radio', {}).get('noul', 0)
            sucesso = "Sim!" if noul_prob > 0.5 else "Não."
            
            resultado_completo = {
                "musica": nova_fusao,
                "avaliacao_jev": {
                    "ambiente_ideal": ambiente,
                    "energia": energia,
                    "sucesso_comercial": sucesso,
                    "noul_bruto": noul_prob 
                }
            }
            resultados_finais.append(resultado_completo)
            
            print(f"   📍 Ambiente: {ambiente.replace('_', ' ')}")
            print(f"   🔋 Energia (0 a 4): {energia}")
            print(f"   📻 Comercial: {sucesso}")
            print("✅ Concluído.\n")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"⚠️ Erro na iteração {i}: {e}")
            time.sleep(3)
        
    nome_arquivo = "resultados_jam_n_jev.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(resultados_finais, f, ensure_ascii=False, indent=4)
        
    print(f"🎉 Sucesso! As {len(resultados_finais)} fusões foram salvas no arquivo '{nome_arquivo}'.")