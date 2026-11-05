"""
Gera painel 2x2 com imagens reais da arena aberta para os 4 testes de preferência de objetos.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

# Configuração de caminhos das imagens no HD
BASE_HD = Path(r"D:\NNC\COMPORTAMENTO\Animais serios\Teste de preferencia")

TESTES = [
    {
        "letra": "A",
        "num": "Teste 1",
        "titulo": "Teste 1: Prisma Circular vs. Prisma Pentagonal",
        "material": "Material: Impresso 3D (PLA)",
        "path": BASE_HD / "#2 Teste 1" / "#22 Teste" / "#t1" / "cx11a1-t1.jpg"
    },
    {
        "letra": "B",
        "num": "Teste 2",
        "titulo": "Teste 2: Frasco Tampa Vermelha vs. Tampa Branca",
        "material": "Material: Plástico (PET)",
        "path": BASE_HD / "#2 Teste 1" / "#22 Teste" / "#t2" / "cx11a1-t2.jpg"
    },
    {
        "letra": "C",
        "num": "Teste 3",
        "titulo": "Teste 3: Prisma Triangular vs. Prisma Quadrangular",
        "material": "Material: Impresso 3D (PLA)",
        "path": BASE_HD / "#3 Teste 2" / "#32 Teste" / "cx11a1-t1.jpg"
    },
    {
        "letra": "D",
        "num": "Teste 4",
        "titulo": "Teste 4: Garrafa Roxa vs. Quadrangular Transparente",
        "material": "Material: Vidro",
        "path": BASE_HD / "#3 Teste 2" / "#32 Teste" / "cx11a1-t2.jpg"
    }
]

# Configura figura com proporções equilibradas
fig, axes = plt.subplots(2, 2, figsize=(11, 11.5), dpi=300)
plt.subplots_adjust(top=0.86, bottom=0.03, left=0.04, right=0.96, hspace=0.22, wspace=0.08)

# Título principal e subtítulo com espaçamento vertical perfeito
fig.suptitle(
    "Disposição dos Objetos nos Testes de Preferência na Arena Aberta",
    fontsize=16,
    fontweight="bold",
    color="#0f172a",
    y=0.965
)
fig.text(
    0.5,
    0.925,
    "Vista superior da arena exibindo os pares de objetos posicionados nas diagonais (sessão com animais naive)",
    ha="center",
    fontsize=11.5,
    color="#475569"
)

for ax, info in zip(axes.flat, TESTES):
    if not info["path"].exists():
        raise FileNotFoundError(f"Imagem não encontrada: {info['path']}")
    
    img = Image.open(info["path"])
    ax.imshow(img)
    
    # Título do subplot em duas linhas bem espaçadas
    ax.set_title(
        f"{info['titulo']}\n{info['material']}",
        fontsize=11.5,
        fontweight="bold",
        color="#1e293b",
        pad=10,
        linespacing=1.25
    )
    
    # Badge moderno com a letra do painel no canto superior esquerdo
    ax.text(
        0.035,
        0.95,
        info["letra"],
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        color="white",
        bbox=dict(
            boxstyle="square,pad=0.28",
            facecolor="#124076",
            edgecolor="none",
            alpha=0.92
        ),
        va="top",
        ha="left"
    )
    
    # Remove eixos e adiciona contorno suave
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#cbd5e1")
        spine.set_linewidth(1.2)

# Salva na pasta de figuras do relatório
OUTPUT_RELATORIO = Path(r"c:\Users\wfran\Documents\Antigravity\Mestrado_UFMG\relatorios\figuras\painel_objetos_testes_preferencia.png")
OUTPUT_RELATORIO.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_RELATORIO, dpi=300, facecolor="white", edgecolor="none")
plt.close(fig)

print(f"[OK] Painel gerado com sucesso em: {OUTPUT_RELATORIO}")
