import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
from pytrends.request import TrendReq
import pandas as pd
from dicio import Dicio
import openai

def reescrever_frase_com_palavras_chave(frase_original, palavras_chave):
    # Limite de tokens permitidos no plano gratuito
    limite_de_tokens = 2048
    
    # Construa o prompt incluindo as palavras-chave, mas mantenha-o dentro do limite de tokens
    prompt = f"Reescreva a frase a seguir, usando as palavras: {', '.join(palavras_chave)}\n'{frase_original}'"
    prompt = prompt[:limite_de_tokens]  # Limite o prompt ao máximo de tokens permitidos

    # Solicitação à API para reescrever a frase
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,  # Limite o número máximo de tokens na resposta
        temperature=0.7,  # Ajuste a temperatura conforme necessário
    )

    # Extraindo a frase reescrita da resposta da API
    frase_reescrita = response.choices[0].text.strip()

    return frase_reescrita
# tentativa sem sucesso de usar GPT3
#///////////////////////////////////////////////////////////////////////////////


warnings.simplefilter(action='ignore', category=FutureWarning)

def check_word_synonyms(word):
    synonyms_list=list(())
    synonyms=[]
    # Create a Dicio object
    dicio = Dicio()
    # Search for "word" and return an object Word
    word_object = dicio.search(word)
    if word_object: synonyms = word_object.synonyms
    if synonyms:
        if len(synonyms) > 1:
            for synonym in synonyms[:2]:
                synonyms_list.append(str(synonym.word))
        else:
            for synonym in synonyms:
                synonyms_list.append(str(synonym.word))
    # Print the word, the url and the meaning
    # print(word, word.url, word.meaning)
    # Print a list of synonyms
    # Print a list of examples
    # print(word.examples)
    # Print extra informations
    #for chave, valor in word.extra.items():
    #    print(chave, "=>", valor)
    # Load information about the first synonym
    # Print the word, the URL and the meaning of the first synonym
    #word.synonyms[0].load()
    #print(word.synonyms[0], word.synonyms[0].url, word.synonyms[0].meaning
    return list(synonyms_list)

def rank_by_popularity(word_list,original_word):
    ranking=[]
    pytrends = TrendReq(hl='pt-BR', tz=360)
    pytrends.build_payload([original_word], timeframe='now 1-d') 
    data_original = pytrends.interest_over_time()    
    pytrends.build_payload(word_list, timeframe='now 1-d') 
    data = pytrends.interest_over_time()
    for word in word_list:
        ##print(f'{data_original[original_word].sum()} vs {data[word].sum()}')
        if data_original[original_word].sum() < data[word].sum():
            ranking.append([word,data[word].sum()])
    return ranking

def main(key):
    openai.api_key = key
    text = " Desenvolvendo o protagonismo profissional " + \
    "com estratégias assertivas em busca da recolocação no mercado. " + \
    "Programas personalizados de acordo com o perfil profissional " + \
    "do cliente, seguindo etapas que propõem o autoconhecimento, apoio, " + \
    "reflexão, orientação, fortalecimento e desenvolvimento do profissional " + \
    "para a busca do emprego em uma empresa que esteja ao encontro de seu " + \
    "propósito de vida e carreira. Atendimento on-line. "
    
    #print(word_tokenize(text))
    #trychatGPT
    #sentencas = sent_tokenize(text)

   # for sentenca in sentencas:
   #     print("Sentença Original:", sentenca)
   #     palavras_chave = word_tokenize(sentenca)  # Tokenize a sentença em palavras-chave
   #     #trocar essa lista pelas sinonimos melhores rankeados e mandar pra API do chat reescrever.
   #     print(palavras_chave)
   #     frase_reescrita = reescrever_frase_com_palavras_chave(sentenca, palavras_chave)
   #     
   #     print("Sentença reescrita:", frase_reescrita)

    
    for word in word_tokenize(text):
        print(word)
        ranked_word_list = []
        synonyms = check_word_synonyms(word)
        if synonyms: ranked_word_list = rank_by_popularity(synonyms,word)
        if ranked_word_list: 
            print("-----------------------------------------")
            for synonym in ranked_word_list: 
                print(f'\033[37;41m suggested change {word} -> {synonym[0]} \033[0m')
            print("-----------------------------------------")
    return main()

main()
# try:
#     main()
# except:
#     print("ERROR")
