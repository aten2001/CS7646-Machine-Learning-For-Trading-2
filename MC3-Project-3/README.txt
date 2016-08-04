In this project you will implement the Q-Learning and Dyna-Q solutions to the reinforcement learning problem. You will apply them to two problems: 1) Navigation, and 2) Trading. The reason for working with the navigation problem first is that, as you will see, navigation is an easy problem to work with and understand. In the last part of the assignment you will apply Q-Learning to stock trading.

Note that your Q-Learning code really shouldn't care which problem it is solving. The difference is that you need to wrap the learner in different code that frames the problem for the learner as necessary.

For the navigation problem we have created testqlearner.py that automates testing of your Q-Learner in the navigation problem. We also provide teststrategylearner.py to test your strategy learner. In order to apply Q-learning to trading you will have to implement an API that calls Q-learning internally.

Overall, your tasks for this project include:

Code a Q-Learner
Code the Dyna-Q feature of Q-Learning
Test/debug the Q-Learner in navigation problems
Build a strategy learner based on your Q-Learner
Test/debug the strategy learner on specific symbol/time period problems
