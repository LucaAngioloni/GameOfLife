# GameOfLife
## Overview
The **Game of Life** was invented in 1970 by the British mathematician John Horton Conway. Conway developed an interest in a problem which was made evident in the 1940’s by mathematician John von Neumann, who aimed to find a hypothetical machine that had the ability to create copies of itself and was successful when he discovered a mathematical model for such a machine with very complicated rules on a rectangular grid. Thus, the Game of Life was Conway’s way of simplifying von Neumann’s ideas. It is the best-known example of a cellular automaton which is any system in which rules are applied to cells and their neighbors in a regular grid. Martin Gardner popularized the Game of Life by writing two articles for his column “Mathematical Games” in the journal Scientific American in 1970 and 1971.

## Rules of the Game
The game is played on a two-dimensional grid (or board). Each grid location is either empty or populated by a single cell. A location’s **neighbors** are any cells in the surrounding **eight adjacent locations**. The simulation of starts from an initial state of populated locations and then **progresses through time**. The evolution of the board state is governed by a few simple rules:
1. Each populated location with one or zero neighbors dies (from loneliness).
2. Each populated location with four or more neighbors dies (from overpopulation).
3. Each populated location with two or three neighbors survives.
4. Each unpopulated location that becomes populated if it has exactly **three** populated neighbors. 
5. All updates are performed simultaneously **in parallel**.

This figure illustrates the rules for cell death, survival, and birth:
[![Go_LRules.png](https://s2.postimg.org/3vwxjhzp5/Go_LRules.png)](https://postimg.org/image/ra4wvfhmd/)

## Implementation
The game was implemnted using Python:
  - Numpy for the state of the game (model, updates, evolution...) (a couple of lines use Scipy)
  - PyQt5 for the GUI
 
### The Model
The model has been implemented in the `GameOfLife` Class.

This class contains the game state and the rules of the game.

It provides methods to get, set, modify and evolve the state following the rules.
It also provides methods to load and save the state from and to file.

Attributes:
- mat = current state of the game
- heatmap = weighted average of past states (history of past states)
- do_heatmap = boolean value defining what to return in get_state (the state or the heatmap)
- x, y = current board dimensions
- initial_state = backed up initial state that becomes the state when/if reset

### The game loop
The game loop has been implemented subclassing the `QTimer` class from the Qt Framework to create a custom timer that times out accordingly to a specific speed (duration) set live at runtime.

This is the `GolLoop` class:

Attributes:
- going = bool value representing the state of the game
- currentTimer = value of time between GoL steps in ms

It fires a timeout signal every currentTimer ms.

All the update methods of the GUI elements and of the Model are connected to the time out signal emitted from this class.

### The GUI
The GUI is composed of a main window (`MainWindow` class) containing some stock widgets and some custom widget developed for this game.

#### GolViewer
This is the custom widget designed to show and edit (with mouse events) the state of the Game of Life.

It can receive as imput 1 channel images (the state of the game or the current heat map) or color (color+alpha) images (maybe for a different representation of the state of the game).

Attributes:
- gol = reference to an object of class GameOfLife (the model)
- drawing = bool value to keep track of mouse button long press and movement
- V_margin = dimension of right and left margin in window (widget) coordinates for the image
- H_margin = dimension of top and bottom margin in window (widget) coordinates for the image
- h = board (gol state) height
- w = board (gol state) height
- lastUpdate = time of the last view update
- pixmap = image representing the state of the game (QPixmap object) (self.pixmap())

## Functionalities
The game can be launched from the `main.py` script:
```
$ python3 main.py
```
### Main window
The Main window presents itself like this:
[![Gui.png](https://s2.postimg.org/6c3cauu89/Gui.png)](https://postimg.org/image/8tf3i4e4l/)

### Play/Pause
The user can play/pause or reset the board using the push buttons at the bottom.
Moreover the speed (framerate) of the simulation can be changed using the dedicated slider even during the simulation.

### Draw and delete
The user can draw new cells on the board using the **Left Click** of the mouse, and delete cells using **Right Click** (In both cases dragging the mouse while clicking is allowed and behaves like expected).

This can be done also while the simulation is running.

### Load known patterns
From the drop down menu at the top, the user can choose between some well known patterns to load and play.

### Heatmap
This implementation of Game of Life implements also a Heatmap (History) of the past game states. To visualize it just check the check button at the top right. (example in the picture below)
[![Heatmap.png](https://s2.postimg.org/idyq50b6h/Heatmap.png)](https://postimg.org/image/bni8vko0l/)

### Save and Load
Finally the user can save his own creations and load them using the Load and Save buttons at the bottom right.
A modal window will popup so that the user can choose where to save or what to load.

The game states are saved in PNG format (1 channel images \[0 dead cells, 255 living cells\])

### Game demonstration

<img src="https://s1.gifyu.com/images/demonstration.gif" alt="Demonstration Gif" data-load="full">

## Requirements
| Software       | Verison        | Required |
| -------------- |:--------------:| --------:|
| **Python**     |     >= 3.5     |    Yes   |
| **PyQt5**      |     >= 5.1     |    Yes   |
| **Numpy**      |Tested on v1.13 |    Yes   |
| **Scipy**      |Tested on v1.0.0|    Yes   |
| QDarkStylesheet|    >= 2.3.1    | Optional |

QDarkStylesheet was used for a better looking GUI (highly recommended) and can be found in [this GitHub Repo](https://github.com/ColinDuquesnoy/QDarkStyleSheet)

## Future developements
Maybe implement **Pan and Zoom** functionalities with fixed board size (big) not depending on the pattern loaded.
