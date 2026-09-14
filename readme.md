### Project 2: Search and Optimization

#### Due: Sept 24, 2026. 11:59pm

**Grading rubric:** 

- Exemplary: Exemplary on all tasks.
- Satisfactory: Satisfactory (or better) on all tasks
- Unsatisfactory: At least one task unsatisfactory.

Each task will be evaluated as follows:

- Exemplary: All subtasks completed according to spec, code is well-organized and documented, 
test cases provided to demonstrate correctness. Writtern answers are clear. Graphics are constructed with care, and labeled appropriately.
- Satisfactory: Subtasks mostly completed, but one or more significant components is missing or 
not working correctly. Documentation is uneven. Written answers or figures are lacking in detail.
- Unsatisfactory: More than one significant component missing or incomplete. Poor documentation or testing.


### Task 1. A* - Romania. 

**This task should be done by yourself without the use of any AI assistance**

To begin, you will complete the A* implementation on the Romania graph. I've provided the following:
- A Graph class (in Graph.py) that implements graphs as an adjacency list.
- sld.py, which creates a pandas dataframe with the straight-line distances between all cities.
- RomaniaState.py, which implements a State in the Romania domain.
- a_star.py, which contains a working implementation of A*.

Right now, we've hard-coded the start state and the goal state, which is sloppy.
1. Modify main to prompt the user for a start state and goal state.
2. Modify the heuristic function and the goal function to use the inputted goal state.
3. Also, we don't handle missing cities well. Modify the main loop to deal with cases 
  where the goal state can't be reached.

### Task 2. A* Word Ladder.

**This task should be done by yourself without the use of any AI assistance**

A *word ladder* is a puzzle in which you try to find a sequence of words from a start word to
a goal word, replacing only one letter at a time. For example, cold -> cord -> word -> ward -> warm. 
We'll stick to four-letter words for this problem.

In this task, you'll use A* to solve this. I've given you the skeleton of a WordState class. 
You can change or modify this as much as you want. You should not have to modify the a_star algorithm

Specifically, you will need to implement:
1. successors() - for a current word, what are all the possible one-letter changes? You can find all valid
words in the file four_letter_words.
2. a heuristic function. Our h for this will be the number of letters that are different between a word and
the goal word. So if our goal was "cold", a state with the word "bolt" would have h=2, and "hold" would have h=1.

You should also provide unit tests for each of these functions, and a main that allows the user to test it out.

### Task 3: Optimization with OR-Tools - Kidney matching

**You may use AI assistance for this task** 

This is a real-world problem; the approach here is actually used in production. 

You may use AI tools such as Claude to help you with this question.

The problem is this: Often, when a patient A needs a kidney transplant, they have a potential donor
who is willing to help them, but is biologically incompatible. There might be another patient B who is 
in a similar situation, and so we could perform a swap in which A's donor gives their kidney to patient B and 
B's donor gives their kidney to patient A. We could even extend this to longer cycles, such as A->B->C->A.

What we'd like to do is find the matching that maximizes the number of successful exchanges, potentially
weighted by:
- compatibility quality (some matches are better than others).
- Patient priority/urgency. (Some patients are higher risk)

I've provided a basic setup that uses OR-tools to solve this problem. It generates an 
adjacency matrix of (i,j) pairs, where the edge is True if i is compatible with j. (note that
this relationship is not symmetric.) It then solves to find the length-2 and length-3 cycles in the graph
that maximize the number of successful exchanges.

To begin, run this code and vary the number of patients from 15-30 and the compatibility probability from 
0.1-0.9. Generate a visualization that shows the percentage of patients successfully matched as these vary.

Next, add in compatibility. Currently the weights are 1 for all matches. Have Claude help you 
extend the code to use weights account for blood types. 

- Type O Recipients: Can receive a kidney only from Type O donors. 
- Type A Recipients: Can receive a kidney from Type A or Type O donors
- Type B Recipients: Can receive a kidney from Type B or Type O donors.
- Type AB Recipients: Can receive a kidney from Type A, B, AB, or O

Vary the number of patients from 15-30, and use the fraction of blood types in the US population:
O: 45%, A: 40%, B:11%, AB: 4%. Generate a visualization that shows the percentage of patients successfully matched.

Last, add in patient sensitivity. In real life, some patients have a hard time finding a transplant
due to immune system sensitivity. We want to prioritize them when we have a successful match, as 
there are so few. 

I've included a function generate_pairs_with_priority to create this data. Sensitized patients wind up 
getting far fewer incoming edges. 

I've also added a function generate_match_quality to capture the notion that some matches might be 
better than others. Now we have two things to consider - getting the best matches, and prioritizing 
sensitized donors.

Have Claude take this code and create a solver that maximizes 
base transplant count + quality + sensitized bonus

Now, let's evaluate it. With Claude's help, solve the same instance with sensitivity bonus=0 and 
sensitivity bonus 10 and display the number of successful matches for sensitized patients.

Lastly, create a visualization that shows sensitized bonus (0,1,2,5,10,20) on the x-axis and total 
matches and sensitized matches (two separate lines) on the y-axis. 

Include all of your data and visualizations in a PDF included in your repo. 

### Task 4: Deep Blue and AlphaGo

**Note: This task is required for students in CS562, and optional for students in CS362. 
For students in CS362, you can complete this for either 2 tokens or 2 quizzes. Please indicate in your assignment which you prefer.**

In the late 90s, Deep Blue shocked the world by becoming the first computer to beat a human grandmaster, Garry Kasparov. 
[This paper](https://www.sciencedirect.com/science/article/pii/S0004370201001291?ref=pdf_download&fr=RR-2&rr=851930c31a9617ea) 
describes how Deep Blue was constructed - it took advantage of specialized hardware, 
along with hand-crafted heuristics and many optimizations of the alpha-beta pruning technique we've learned about.

20 years later, the Google team has re-revolutionized game search with the development of AlphaZero, 
which is described [in this paper](https://arxiv.org/pdf/1712.01815.pdf).

AlphaZero uses a very different approach - specifically, a deep neural network is used to learn heuristic functions 
through self-play. (We'll look at reinforcement learning later in the semester). This allows the program to learn to 
play any game, as long as it knows the state space, a goal function, and the legal actions.

These articles are both pretty dense, and I don't expect you to grasp every nuance, but you should be able to read the 
introductions and get the gist of things.

In your written answers, please address the following questions: 

a) What were the engineering advances that led to Deep Blue's success? Which of them can be transferred to other problems, 
and which are specific to chess?

b) AlphaZero is compared to a number of modern game-playing programs, such as StockFish, which work similarly to Deep Blue. 
The paper shows that AlphaZero is able to defeat StockFish even when it is given only 1/100 of the computing time. 
Why is that? Please frame your answer in terms of search and the number of nodes evaluated.

**Optional question for CS562 students. This is worth either two tokens or two quizzes. 
Please indicate in your assignment which you prefer.**

AlphaZero uses an algorithm called Monte Carlo Tree Search to search for moves to make. 
**In your own words**, explain how Monte Carlo Tree Search works and how you would implement it
within our standard search queue model. What are the successors? How are they ordered in the queue?
How are state values updated? Be as specific as possible. Feel free to provide pseudocode if it helps.

You are welcome to use any resources you like to learn about this, but your answer should be your own.



