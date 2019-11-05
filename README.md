# Player AI for Reversi
### Guilherme Franco, Gabriel Vargas, George Rappel

Para o funcionamento dos nossos players, devem ser adicionados os seguintes arquivos nas pastas:

models/players/**mobility_player.py**

models/players/**no_mobility_player.py**

models/players/**playNode.py**


Além disso, deve se instalar o pacote [AnyTree](https://github.com/c0fec0de/anytree) com ```pip install anytree```.


O jogador **largura_player.py** gera a árvore de jogadas usando busca em largura e levando em conta o tempo, para que a operação toda de escolher a melhor jogada não passe de 3 segundos.

O jogador **best_player.py** gera a árvore de jogadas usando busca em profundidade definida em profundidade 3.
