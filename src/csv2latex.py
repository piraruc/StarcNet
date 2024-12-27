import pandas as pd
def table_transform(csv):
    # Converter para um DataFrame
    data = pd.read_csv(csv)

    # Gerar tabela LaTeX
    table_latex = data.to_latex(index=False)

    # Salvar como arquivo LaTeX
    with open("output/table.tex", "w") as f:
        f.write(table_latex)

    print("Tabela convertida para LaTeX e salva em output/table.tex")

if __name__ == "__main__":
    table = 'output/total.csv'
    table_transform(table)