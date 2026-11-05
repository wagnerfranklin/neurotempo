import os

base_dir = r"c:\Users\wfran\Documents\Antigravity\Mestrado UFMG"
bib_path = os.path.join(base_dir, "bibliografia_mestrado.bib")

entries = [
    {
        "key": "izhikevich2007dynamical",
        "type": "book",
        "title": "Dynamical Systems in Neuroscience: The Geometry of Excitability and Bursting",
        "author": "Izhikevich, Eugene M.",
        "year": "2007",
        "publisher": "MIT Press",
        "file": os.path.join(base_dir, "livros", "Izhikevich - Dynamical Systems in Neuroscience.pdf"),
        "note": "BIBLIA DO ENGENHEIRO: Nao leia tudo de uma vez. Use como consulta de alto nivel. Va direto ao Capitulo 3 (Phase Portraits: entenda o que sao nullclines e trajetorias) e Capitulo 8 (Izhikevich Model: as duas equacoes diferenciais simples que substituem Hodgkin-Huxley)."
    },
    {
        "key": "izhikevich2003simple",
        "type": "article",
        "title": "Simple model of spiking neurons",
        "author": "Izhikevich, Eugene M.",
        "journal": "IEEE Transactions on Neural Networks",
        "volume": "14",
        "number": "6",
        "pages": "1569--1572",
        "year": "2003",
        "doi": "10.1109/TNN.2003.820440",
        "file": os.path.join(base_dir, "artigos_nnc", "[2003] - Simple model of spiking neurons - Izhikevich.pdf"),
        "note": "ARTIGO FUNDAMENTAL (4 paginas): Leia as equacoes (1) e (2) na pagina 1569. Olhe a Figura 1 e a Tabela 1: veja como os parametros a, b, c, d modelam neuronios de CA3 (regular spiking) e interneuronios (fast spiking)."
    },
    {
        "key": "stimberg2019brian2",
        "type": "article",
        "title": "Brian 2, an intuitive and efficient neural simulator",
        "author": "Stimberg, Marcel and Brette, Romain and Goodman, Dan F. M.",
        "journal": "eLife",
        "volume": "8",
        "pages": "e47314",
        "year": "2019",
        "doi": "10.7554/eLife.47314",
        "file": os.path.join(base_dir, "artigos_nnc", "[2019] - Brian 2, an intuitive and efficient neural simulator.pdf"),
        "note": "O SIMULADOR: Foco na secao 'Model descriptions' (como declarar equacoes diferenciais com unidades fisicas em Python) e na secao 'Synapses and plasticity' (exemplo de codigo para STDP)."
    },
    {
        "key": "xavier2026distinct",
        "type": "article",
        "title": "Distinct Patterns of Temporally Coded Electrical Stimulation Interfere With Long-Range Interhemispheric Coupling in a Focal Model of Epilepsy",
        "author": "Xavier, Larissa Samara Santos and Montalvao, Thiago Moreira Maia and Guarnieri, Leonardo de Oliveira and Carvalho-Moreira, Joao Pedro and Passos, Matheus Costa and Cota, Vinicius Rosa and Moraes, Marcio Flavio Dutra",
        "journal": "Neuromodulation / NNC Publications",
        "year": "2026",
        "doi": "10.1016/j.neurom.2025.08.414",
        "file": os.path.join(base_dir, "artigos_nnc", "[2026] - Distinct Patterns of Temporally Coded Electrical Stimulation Interfere With Long....pdf"),
        "note": "DO SEU LABORATORIO (PROF. MARCIO): Veja a secao 'Materials and Methods -> Electrical stimulation protocols'. Entenda como o NNC usa estimulacao periodica (PS) e nao-periodica (NPS) e como calculam a causalidade e acoplamento entre canais."
    },
    {
        "key": "cota2023temporal",
        "type": "article",
        "title": "On temporal scale-free non-periodic stimulation and its mechanisms as an infinite improbability drive of the brain's functional connectogram",
        "author": "Cota, Vinicius Rosa and Cancado, Sergio Augusto Vieira and Moraes, Marcio Flavio Dutra",
        "journal": "Frontiers in Neuroinformatics",
        "volume": "17",
        "pages": "1173597",
        "year": "2023",
        "doi": "10.3389/fninf.2023.1173597",
        "file": os.path.join(base_dir, "artigos_nnc", "[2023] - On temporal scale-free non-periodic stimulation and its mechanisms as an infinit....pdf"),
        "note": "TEORIA DO PROF. MARCIO: Artigo conceitual profundo sobre por que a sintaxe temporal da estimulacao eletrica reorganiza redes neuronais e nao apenas 'bloqueia' sinapses."
    },
    {
        "key": "buzsaki2006rhythms",
        "type": "book",
        "title": "Rhythms of the Brain",
        "author": "Buzsaki, Gyorgy",
        "year": "2006",
        "publisher": "Oxford University Press",
        "note": "O LIVRO DO RITMO TETA: O Prof. Marcio adora este livro. Nao leia do comeco ao fim; consulte o Ciclo 8 e o Ciclo 9 quando tiver duvida sobre o que e oscilacao teta (7 Hz) e acoplamento teta-gama no hipocampo."
    },
    {
        "key": "dix1999extending",
        "type": "article",
        "title": "Extending the spontaneous preference test of recognition: Evidence of object-location and object-context recognition",
        "author": "Dix, S. L. and Aggleton, J. P.",
        "journal": "Behavioural Brain Research",
        "volume": "99",
        "number": "2",
        "pages": "191--200",
        "year": "1999",
        "doi": "10.1016/S0166-4328(98)00079-5",
        "note": "O TESTE BIOLOGICO ORIGINAL: Leia especificamente o 'Experiment 3: Object-Context Recognition' (paginas 194-196). E exatamente esse teste empirico que voce tentou rodar com animais e que nos vamos transpor para a simulacao in silico."
    },
    {
        "key": "mourao2022fully",
        "type": "article",
        "title": "A Fully Adapted Headstage With Custom Electrode Arrays Designed for Electrophysiological Experiments",
        "author": "Mourao, Flavio Afonso Goncalves and Guarnieri, Leonardo de Oliveira and Amaral Junior, Paulo Aparecido and Carvalho, Vinicius Rezende and Mendes, Eduardo Mazoni Andrade Marcal and Moraes, Marcio Flavio Dutra",
        "journal": "Frontiers in Neuroscience",
        "volume": "15",
        "pages": "691788",
        "year": "2022",
        "doi": "10.3389/fnins.2021.691788",
        "file": os.path.join(base_dir, "artigos_nnc", "[2022] - A Fully Adapted Headstage With Custom Electrode Arrays Designed for Electrophysi....pdf"),
        "note": "O CAPACETE E CIRURGIA DO NNC: Mostra como o laboratorio projeta o headstage e eletrodos. Importante para voce citar na introducao ao justificar os desafios biomecanicos enfrentados pelos animais."
    },
    {
        "key": "kandel2013principles",
        "type": "book",
        "title": "Principios de Neurociencias",
        "author": "Kandel, Eric R. and Schwartz, James H. and Jessell, Thomas M. and Siegelbaum, Steven A. and Hudspeth, A. J.",
        "edition": "5",
        "publisher": "AMGH Editora / McGraw-Hill",
        "year": "2014",
        "note": "SUA ENCICLOPEDIA BIOLOGICA DE CONSULTA TOP-DOWN: Consulte apenas: Cap. 6 (Canais Ionicos), Cap. 7 (Potencial de Membrana), Cap. 8 (Potencial de Acao) e Cap. 67 (Mecanismos Celulares de Aprendizado e Memoria / LTP)."
    }
]

with open(bib_path, "w", encoding="utf-8") as f:
    for e in entries:
        f.write(f"@{e['type']}{{{e['key']},\n")
        f.write(f"  title = {{{e['title']}}},\n")
        f.write(f"  author = {{{e['author']}}},\n")
        f.write(f"  year = {{{e['year']}}},\n")
        for k in ["journal", "volume", "number", "pages", "publisher", "edition", "doi"]:
            if k in e:
                f.write(f"  {k} = {{{e[k]}}},\n")
        if "file" in e and os.path.exists(e["file"]):
            escaped_file = e["file"].replace("\\", "/")
            f.write(f"  file = {{{escaped_file}}},\n")
        if "note" in e:
            f.write(f"  note = {{{e['note']}}},\n")
        f.write("}\n\n")

print(f"Sucesso: {len(entries)} referencias gravadas em {bib_path}")
