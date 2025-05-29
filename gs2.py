# Nome do Projeto: Monitoramento de Riscos de Enchentes

# Integrantes do Grupo:

# Nome: Henrique Celso - RM: 559687
# Nome: Davis Junior - RM: 560723
# Nome: Jonathan Henrique - RM: 561139

import csv
import os
import api_clima
from datetime import datetime

municipios = []

def cadastrar_municipio():
    try:
        nome = input("Nome do município: ")
        volume_agua = float(input("Volume de água acumulado (mm): "))
        cobertura_vegetal = float(input("Percentual de cobertura vegetal (%): "))
        movimento_massa = float(input("Movimentação de massa detectada (0 a 10): "))

        if not (0 <= cobertura_vegetal <= 100):
            print("Erro: A cobertura vegetal deve estar entre 0 e 100.\n")
            return

        if not (0 <= movimento_massa <= 10):
            print("Erro: A movimentação de massa deve estar entre 0 e 10.\n")
            return
        coords = api_clima.pegar_Coordenadas()
        volume_chuva_previsto = 0.0
        probabilidade_media_chuva = 0.0
        nome_local_api = ""
        if coords and coords.get('lat') and coords.get('long'):
            lat = coords['lat']
            lon = coords['long']
            local_info = api_clima.obter_nome_local(lat, lon, api_clima.api_key)
            # nome local pega com base no ip da pessoa que esta usando 
            # nao sei se é interessante deixar assim ou colocar para a pessoa digitar a cidade que ela quer
            nome_local_api = local_info.get('nomeLocal', "")
            previsoes = api_clima.obter_previsao_dias(lat, lon, api_clima.api_key)
            volume_chuva_previsto = api_clima.volume_NextDays(previsoes)
            probabilidade_media_chuva = api_clima.calcula_Probabilidade(previsoes)
        else:
                print("Não foi possível obter dados de previsão de chuva da API.")

        municipio = {
            "nome": nome,
            "volume_agua": volume_agua,
            "cobertura_vegetal": cobertura_vegetal,
            "movimento_massa": movimento_massa,
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome_local_api": nome_local_api,
            "volume_chuva_previsto_api": volume_chuva_previsto,
            "prob_media_chuva_api": probabilidade_media_chuva 
        }

        municipios.append(municipio)
        print(f"Município {nome} cadastrado com sucesso!\n")

    except ValueError:
        print("Erro: insira apenas números válidos nos campos numéricos.\n")


def calcular_risco(municipio):
    risco = 0
    volume_previsto = municipio.get("volume_chuva_previsto_api", 0)
    prob_chuva = municipio.get("prob_media_chuva_api", 0)
    if municipio["volume_agua"] > 100:
        risco += 1
    if municipio["cobertura_vegetal"] < 30:
        risco += 1
    if municipio["movimento_massa"] > 5:
        risco += 1
    if volume_previsto > 50:
        risco += 2 
    if prob_chuva > 75:
        risco += 1
    if risco == 1:
        return "Baixo"
    elif risco == 2:
        return "Moderado"
    elif risco == 3:
        return "Alto"
    else:
        return "Crítico"


def gerar_relatorio():
    if not municipios:
        print("Nenhum município cadastrado ainda.\n")
        return

    for m in municipios:
        risco = calcular_risco(m)
        print(f"Município: {m['nome']} - Risco de enchente: {risco}")
    print()


def listar_municipios():
    if not municipios:
        print("Nenhum município cadastrado.\n")
        return

    for m in municipios:
        print(f"Nome: {m['nome']}")
        print(f"Volume de Água: {m['volume_agua']} mm")
        print(f"Cobertura Vegetal: {m['cobertura_vegetal']}%")
        print(f"Movimento de Massa: {m['movimento_massa']}")
        print(f"Data de Cadastro: {m['data_cadastro']}")
        print(f"  Localização da Previsão (API): {m.get('nome_local_api', '')}")
        print(f"  Volume Chuva Previsto (API): {m.get('volume_chuva_previsto_api', 'N/A'):.2f} mm")
        print(f"  Prob. Média Chuva (API): {m.get('prob_media_chuva_api', 'N/A'):.2f}%")
        print('-' * 40)
    print()


def buscar_municipio():
    nome = input("Digite o nome do município: ")
    for m in municipios:
        if m["nome"] == nome:
            print(f"\nMunicípio encontrado:")
            print(f"Nome: {m['nome']}")
            print(f"Volume de Água: {m['volume_agua']} mm")
            print(f"Cobertura Vegetal: {m['cobertura_vegetal']}%")
            print(f"Movimento de Massa: {m['movimento_massa']}")
            print(f"Data de Cadastro: {m['data_cadastro']}")
            print(f"Risco: {calcular_risco(m)}\n")
            return
    print("Município não encontrado.\n")


def salvar_dados(arquivo='dados_municipios.csv'):
    try:
        with open(arquivo, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nome", "volume_agua", "cobertura_vegetal", "movimento_massa", "data_cadastro"])
            writer.writeheader()
            for m in municipios:
                writer.writerow(m)
        if os.path.exists(arquivo):
            print(f"Dados salvos com sucesso no arquivo: {arquivo}\n")
        else:
            print("Erro: o arquivo não foi criado.\n")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")


def carregar_dados(arquivo='dados_municipios.csv'):
    try:
        with open(arquivo, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                municipios.append({
                    "nome": row["nome"],
                    "volume_agua": float(row["volume_agua"]),
                    "cobertura_vegetal": float(row["cobertura_vegetal"]),
                    "movimento_massa": float(row["movimento_massa"]),
                    "data_cadastro": row.get("data_cadastro", "Data desconhecida")
                })
        print("Dados carregados com sucesso!\n")
    except FileNotFoundError:
        print("Arquivo não encontrado. Nenhum dado carregado.\n")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}\n")


def exportar_relatorio_txt(arquivo='relatorio_risco.txt'):
    if not municipios:
        print("Nenhum município cadastrado para exportar.\n")
        return

    try:
        with open(arquivo, 'w') as f:
            for m in municipios:
                risco = calcular_risco(m)
                f.write(f"Município: {m['nome']} - Risco de enchente: {risco}\n")
        if os.path.exists(arquivo):
            print(f"Relatório exportado com sucesso no arquivo: {arquivo}\n")
        else:
            print("Erro: o arquivo do relatório não foi criado.\n")
    except Exception as e:
        print(f"Erro ao exportar relatório: {e}\n")


def main():
    while True:
        print("MONITORAMENTO DE ENCHENTES")
        print("1. Cadastrar Município")
        print("2. Gerar Relatório de Riscos")
        print("3. Salvar Dados")
        print("4. Carregar Dad7os")
        print("5. Listar Municípios Cadastrados")
        print("6. Buscar Município por Nome")
        print("7. Exportar Relatório para TXT")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_municipio()
        elif opcao == "2":
            gerar_relatorio()
        elif opcao == "3":
            salvar_dados()
        elif opcao == "4":
            carregar_dados()
        elif opcao == "5":
            listar_municipios()
        elif opcao == "6":
            buscar_municipio()
        elif opcao == "7":
            exportar_relatorio_txt()
        elif opcao == "8":
            confirmar = input("Tem certeza que deseja sair? (s/n): ")
            if confirmar == 's':
                print("Encerrando aplicação...")
                break
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()




