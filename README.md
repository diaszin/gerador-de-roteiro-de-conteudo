## Dashboard
Para iniciar o dashboard com algumas analises que fizemos internamente. Basta executar o comando:
```bash
python dashboard.py
```

e abri em `localhost:5002`


## Gerador de Roteiro
Já para gerar um roteiro, é necessário criar um arquivo `.env` para inserir a chave de API do Gemini com o seguinte nome:
```
GEMINI_API_KEY=<chave-da-api>
```

Após isso, rode o comando:

```bash
python generate-document.py
```

Pronto! O arquivo será criado com o nome **Roteiro criado.pdf** na pasta em que foi executado o código !