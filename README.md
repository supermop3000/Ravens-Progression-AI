# Ravens Progression AI

## Overview
Ravens Progression AI is a knowledge based AI program designed to analyze and simulate progression patterns using advanced algorithms. This project is inspired by Raven's Progressive Matrices, aiming to study and replicate progression patterns effectively.

## Features
- **Pattern Recognition**: Identifies progression patterns in data sets.
- **Data Visualization**: Offers tools to visualize progression patterns.
- **AI Agent for Problem Solving**: A specialized AI agent designed to solve Raven's Progressive Matrices by analyzing visual and logical patterns.

---

## AI Agent Overview

### Purpose of the AI Agent
The AI agent is the core of this project and is specifically designed to solve **Raven's Progressive Matrices**, a type of visual puzzle used to test abstract reasoning. The agent uses image processing and logical reasoning to determine the correct answer by analyzing the relationships and transformations between visual figures.

### Core Methods and Workflow
#### **1. Solving Problems**
- **`Solve(problem)` Method**:
  - The primary entry point for the agent to solve a given puzzle.
  - Determines whether the problem is a `2x2` or `3x3` matrix.
  - Calls helper methods to analyze transformations and relationships between figures.

#### **2. Image Comparison and Transformation**
- **Image Processing Methods**:
  - `checkSame`: Compares two images pixel-by-pixel to measure similarity.
  - `checkMirrorHoriz` and `checkMirrorVert`: Detects horizontal and vertical mirroring transformations by flipping the images.
  - `checkRotate90` and `checkRotate270`: Identifies rotational transformations by rotating the images by 90° or 270° and comparing them.

- **Transformational Methods**:
  - `checkAdd`: Detects added elements between two images using image subtraction and comparison.
  - `checkDelete`: Identifies removed elements by reversing the addition logic.

#### **3. Transformation Mapping**
- **`getAllTransforms(problem)` Method**:
  - Analyzes transformations between all possible pairs of figures (e.g., A → B, A → C).
  - Returns a dictionary of transformations for further analysis.

#### **4. Optimal Solution Selection**
- **`getHeroTransform(all_trans)` Method**:
  - Combines and evaluates all possible transformations to determine the "hero transformation," or the best match for solving the puzzle.
  - Uses weighted scoring to rank and select the most likely solution based on transformation similarities.

### Example Workflow
1. **Load a Problem**:
   The agent begins by receiving a `problem` object containing figures (e.g., A, B, C, and possible answers).

2. **Analyze Transformations**:
   It computes transformations between pairs of figures, such as rotations, mirrors, or additions.

3. **Compare Patterns**:
   The agent compares transformations between the given figures and the answer choices.

4. **Select the Best Match**:
   Based on the highest scoring transformation, the agent returns the most probable answer.

### Summary of Key Methods

| Method                   | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `__init__`               | Initializes the agent and prepares necessary tools and libraries.           |
| `Solve(problem)`         | Main method for solving a Raven's Progressive Matrix problem.               |
| `getAllTransforms()`     | Analyzes all transformations between figures in the problem.                |
| `getHeroTransform()`     | Selects the best answer based on transformation analysis.                   |
| `checkSame()`            | Compares two images for pixel-level similarity.                             |
| `checkMirrorHoriz()`     | Detects horizontal mirroring transformations.                               |
| `checkMirrorVert()`      | Detects vertical mirroring transformations.                                 |
| `checkRotate90()`        | Detects 90° rotations.                                                      |
| `checkRotate270()`       | Detects 270° rotations.                                                     |
| `checkAdd()`             | Identifies added elements in the transformation.                            |
| `checkDelete()`          | Identifies removed elements in the transformation.                          |

---

