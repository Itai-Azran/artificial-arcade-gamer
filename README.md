# artificial-arcade-gamer
A generic 2D arcade gamer that requires simple configuration, can learn to play any arcade game.


Recommended games:   
Flappy Bird   
T-Rex game


Algorithm:
1. Take a screenshot from the chosen window, and turn it to black and white.
2. Every frame is then divided in to slots (default 16x16 slots) where each slot is an input node of the NEAT genome.
3. The genome generate the which key to press for the given frame.
4. After a genome loses, he check his score using OCR and the the next genome runs in a new game.
5. After all the population (default 15 genomes) run their turn, a new generation, which is improved based on the result of the last one, playes.
6. When the last generation ends (default 30 generations), the winning genome is presented.


Notes:   
Starting key - starting key is the key that should be pressed to start the game after the restart button was pressed.   
for example the key 'd' in snake.

Game's window - the game's window needs to be open before running the program.

Mouse - at the moment the mouse functionality is not fully supported yet.
