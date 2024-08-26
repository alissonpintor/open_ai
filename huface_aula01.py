from transformers import pipeline, Pipeline
import torch

device = torch.cuda.get_device_name(0)

# Usando o modelo rufimelo/Legal-BERTimbau-base mask=[MASK]
modelo: Pipeline = pipeline('fill-mask', model='rufimelo/Legal-BERTimbau-base', device=0)

# Usando o modelo neuralmind/bert-base-portuguese-cased mask=[MASK]
#modelo: Pipeline = pipeline('fill-mask', model='neuralmind/bert-base-portuguese-cased', device=0)

# Usando o modelo FacebookAI/xlm-roberta-base mask=<mask>
# modelo: Pipeline = pipeline('fill-mask', model='FacebookAI/xlm-roberta-base', device=0)

frase: str = 'The capital of [MASK] is Brasília.'

predicoes = modelo(frase)
for predicao in predicoes:
    resposta: str = predicao['token_str']
    score = predicao['score'] * 100
    frase = predicao['sequence']
    print(f'Predição: "{resposta.strip()}" com score {score:.2f}% -> "{frase}"')