import os
import glob

def apagar_arquivos_sql_csv(pasta='.'):
    arquivos = glob.glob(os.path.join(pasta, '*.sql')) + glob.glob(os.path.join(pasta, '*.csv'))
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f"Apagado: {arquivo}")
    print("Todos os arquivos .sql e .csv foram removidos.")

if __name__ == "__main__":
    apagar_arquivos_sql_csv('.')
