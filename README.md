# Player AI for Reversi
### Guilherme Franco, Gabriel Vargas, George Rappel

Para o funcionamento dos nossos players, devem ser adicionados os seguintes arquivos nas pastas:

models/players/**best_player.py**

models/players/**largura_player.py**

models/players/**playNode.py**


Além disso, deve se instalar o pacote [AnyTree](https://github.com/c0fec0de/anytree) com ```pip install anytree```.

O jogador **best_player.py** gera a árvore de jogadas usando busca em profundidade definida em 3.

O jogador **largura_player.py** gera a árvore de jogadas usando busca em largura sem profundidade definida mas levando em conta o tempo, para que a operação toda de escolher a melhor jogada não passe de 3 segundos.

O jogador escolhido para o campeonato é o **largura_player.py**.

Os dois jogadores usam a mesma função heurística (que é uma mistura de heurísticas, cada uma com um peso) e possuem uma checagem: caso o tempo da jogada esteja chegando em 3 segundos, a mobilidade (número de jogadas possíveis a partir do tabuleiro atual) não é calculada. Isso é feito somente para garantir que não passe de 3 segundos, pois a mobilidade é cara para ser calculada.
