# artificial-arcade-gamer
A generic 2D arcade gamer that with just simple settings, can learn to play in any arcade game using NEAT model


Recommended games:
Flappy Bird
T-Rex game


Algoirithm:
Our program works like this-
1. It take each frame and turn it to a black-white image of objects and background using.
2. Every frame divided in to 16x16 slots with each slot is an input node of the genome.
3. Each genome calc every frame using is own network and decide what output to generate
   where the possible outputs are the game keys.
4. After a genome loses, he check his score using ocr and than the next genome runs his turn.
5. After all the population (which default is 15 genomes) run their turn, a new smarter generation get going.
6. when the last generation ends (which default is generation 30), the winning genome's net presented.


Notes:
Starting key - starting key is a key that start the game after the restart button pressed (not every needs).
    example: the key 'd' in snake game

Game's window - the game's window needs to be opened before running the program

Mouse - the algorithm does not work so well in games that plays by the mouse