# Player AI for Reversi
### Guilherme Franco, Gabriel Vargas, George Rappel

Para o funcionamento dos nossos players, devem ser adicionados os seguintes arquivos nas pastas:

models/players/**mobility_player.py**

models/players/**no_mobility_player.py**

models/players/**playNode.py**


Além disso, deve se instalar o pacote [AnyTree](https://github.com/c0fec0de/anytree) com ```pip install anytree```.


O jogador **mobility_player.py** gera a árvore de jogadas usando busca em largura e levando em conta o tempo, para que a operação toda de escolher a melhor jogada não passe de 3 segundos. Além disso, leva em conta a mobilidade (número de jogadas possíveis no tabuleiro atual) para calcular o valor da função heurística.

O jogador **no_mobility_player.py** gera a árvore de jogadas usando busca em profundidade definida em profundidade 4, porém não leva em conta a mobilidade para calcular o valor da função heurística para poder economizar tempo.
