from cx_Freeze import setup, Executable

setup(
    name="Drogaria",
    version="1.0",
    description="Sistema de Caixa para Drogaria",
    executables=[Executable("app.py")],
    options={
        "build_exe": {
            "packages": ["flask", "sqlite3"],
            "include_files": [
                "Templates/",  # Inclua o diretório dos templates
                "static/",     # Inclua o diretório dos arquivos estáticos
                "database.db", # Inclua o banco de dados, se desejar distribuir já preenchido
            ],
        }
    }
)