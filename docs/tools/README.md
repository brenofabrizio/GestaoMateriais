# Geração de PDFs

Instalar as dependências:

```bash
python -m pip install -r docs/tools/requirements.txt
```

Gerar os cinco PDFs:

```bash
backend/.venv/Scripts/python.exe docs/tools/generate_pdfs.py
```

Os arquivos são gerados em:

```text
docs/pdf/
```

A fonte oficial continua sendo o Markdown em `docs/`. Os PDFs são artefatos de visualização e devem ser regenerados quando a documentação mudar.
