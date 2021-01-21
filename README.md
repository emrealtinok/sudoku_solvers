# sudoku_solvers
### Attempting to solve Sudoku puzzles with three separate AIs

In order to test the performance of my AIs, I generated [1000 Sudoku puzzles](https://github.com/emrealtinok/sudoku_solvers/blob/main/1000Sudokus%20-%20Sheet1.csv) via [this website](https://qqwing.com/generate.html).  
I also tried to solve the [world's hardest Sudoku puzzle](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html).  

This as an ongoing side project to practice what I learn and explore how I can implement and adapt various AI methods to solve Sudoku puzzles. All my code is written in Python.

## AI #1: Translating Sudoku solving techniques into code

File name: [SudokuHumanTechniques.py](https://github.com/emrealtinok/sudoku_solvers/blob/main/SudokuHumanTechniques.py)

In order to implement this AI, I made use of object-oriented programming. The Sudoku grid is a two dimensional Numpy array of 81 objects that represent each unit of the Sudoku puzzle. Each object has properties that represent the value of the unit and a probability dictionary that holds the binary probabilities of the unit getting each value. 

The codified 'human' techniques scan the grid, assign values and re-adjust probabilities according to the new values and probabilities until the puzzle is finished.

After implemeting most of the basic and medium level techniques, I found out that this approach is not very efficient as it uses a lot of for-loops to scan the grid and to alter  the properties. As the techniques got more advanced, the code got exponentially more computantionally expensive and the AI significantly slowed down. 

I stopped building on it at around 500 lines of code with 14 human techniques.

It was able to solve 594 of the 1000 test puzzles and it couldn't solve the world's hardest Sudoku puzzle.


## AI #2: Using a backtracking algorithm with Sudoku constraints

File name: [SudokuBacktracking.py](https://github.com/emrealtinok/sudoku_solvers/blob/main/SudokuBacktracking.py)

This AI only has around 50 lines of code. I used a recurrent backtracking function that tries numbers from 1 to 9 one by one if they satisfy the basic constraints/rules of the Sudoku puzzle. If the algorithm gets stuck, it takes a step back and tries the next possible number until it solves the puzzle.

It was able to solve all 1000 test puzzles, and it was able to solve the world's hardest Sudoku puzzle in 5 seconds.  

This AI is by far the most efficient and accurate one. 

## AI #3: Building a densely connected deep convolutional neural network

File Name: [SudokuDenseNet.ipynb](https://github.com/emrealtinok/sudoku_solvers/blob/main/SudokuDenseNet.ipynb)

I also wanted to see if neural networks can learn to solve Sudoku puzzles. I used TensorFlow and Google Colab to have access to GPUs.

I imported 3 million puzzles to train my model from [this website](https://www.kaggle.com/radcliffe/3-million-sudoku-puzzles-with-ratings).

For this AI, I tried a variety of architectures to see how they perform. I built vanilla deep networks with only Dense layers, simple convolutional networks, convolutional networks with residual blocks or inception blocks and recurrent neural networks with LSTM blocks. I even tried using all of them at the same time by concatenating each architecture before the last layer or placing them one after the other.

Finally what worked best was a densely connected 721-layer deep network with an Adam optimizer that had a learning rate of 0.003. For the prediction layer, I used a convolutional softmax layer with 10 filters representing the numbers from 0 to 9 (0 means an empty unit). I used sparse categorical crossentropy for the loss function and a mini batch size of 64.

After 16 hours of training, Colab ended my session, so I loaded the model from the last checkpoint and kept on training it with Stochastic Gradient Descent for another 6 hours. I used SGD as many researchers suggest that it can converge better towards the end of the training.

When I evaluated the model on the test puzzles, it got an accuracy of 94%. However, to actually see how many test puzzles the model can solve I used a step by step inference method where the model predicts the probabilities of each number being in each unit and assigns the value to the to the empty unit with the highest overall probability. It repeats this process until the Sudoku puzzle is finished. 

It was able to solve 907 of the 1000 test puzzles. It couldn't solve the world's hardest Sudoku puzzle.

In conclusion, the final model was quite good at learning, and it definitely has more room to grow. With more processing power, deeper or wider networks, more precise hyperparameters and longer learning time I believe that neural networks can come close to being 100% accurate at solving Sudoku puzzles. 

Next up, I will use TPUs to train this network and see how it improves the learning curve.






