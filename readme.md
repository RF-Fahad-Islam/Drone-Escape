**Drone Escape 🚁**
====================

A fast-paced Flappy-Bird--style arcade game built with **Python + Pygame**, featuring a flying drone, dynamic obstacles, power-ups, and increasing difficulty.

🎮 **About the Game**
---------------------

**Drone Escape** is a side-scrolling survival game where you control a drone navigating through gaps, avoiding obstacles, and collecting power-ups.\
The world scrolls continuously, pipes spawn at random heights, and the game becomes harder the longer you survive.

Your goal: **Fly as far as you can and get the highest score!**

* * * * *

✨ **Features**
--------------

### 🕹️ **Core Gameplay**

-   Smooth drone physics (gravity, jump/flap mechanics)

-   Flappy Bird--style gap obstacles (pipes)

-   Dynamic ground scrolling

-   Increasing difficulty (pipe gap shrinks + speed increases over time)

### ⚡ **Power-Ups**

-   **Shield** --- protects you from one collision\
    (More can be added easily)

### 🚧 **Obstacles**

-   Fire shoot

### 🔊 **Sound Effects**

-   Flap sound

-   Scoring sound

-   Game-over sound

### 📈 **Scoring System**

-   +1 point for every pipe pair passed

-   +5 points for collecting a power-up

-   Difficulty scales as score increases

* * * * *

🖼️ **Screens**
---------------

-   **Welcome Screen** --- Press SPACE to start

-   **Game Running** --- Pipes, obstacles, power-ups spawn as you fly

-   **Game Over Screen** --- Press SPACE to restart

* * * * *

🧩 **Folder Structure**
-----------------------

`📦 drone-escape
├── assets/
│   ├── bg.png
│   ├── ground.png
│   ├── font.ttf
│   ├── sfx/
│   │   ├── flap.wav
│   │   ├── score.wav
│   │   └── dead.wav
│   └── sprites/
│       ├── drone.png
│       ├── powerups/
│       └── obstacles/
├── sprites/
│   ├── drone.py
│   ├── pipe.py
│   ├── obstacle.py
│   └── power.py
├── main.py
└── README.md`

* * * * *

🚀 **How to Run**
-----------------

### **1. Install dependencies**

`pip install pygame`

### **2. Run the game**

`python game.py`

* * * * *

🧠 **Controls**
---------------

| Key | Action |
| --- | --- |
| **SPACE** | Flap / Jump |
| **SPACE (on Game Over)** | Restart |

* * * * *

🛠️ **Built With**
------------------

-   **Python**

-   **Pygame**

-   Custom pixel sprites and animations


❤️ **Credits**
--------------

Developed by **Fahad Islam**\
Sprites, SFX, and game logic made manually for this project.
