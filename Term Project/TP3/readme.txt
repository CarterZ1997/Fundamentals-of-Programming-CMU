Play Pool!!!

The project that I've been working on for the last week is this MVC achieved, user friendly pool game. 

Once you open up the .py file, the home screen will be presented to you, where you will get excited already. And from the home screen, you can go to either the help mode(which is highly recommended!!!) or the play mode. I imported images for these modes just to make things prettier.

In the help mode, you will be instructed of the rules and the basics of the game. And then it's time to play!

One thing to note before we get started: I did not use any module but tkinter, so the primary methods I used are those from 15112.

Once you are inside the play mode, you can see a pool table, on which there're 11 balls: one cue ball ten color balls. You will note at the top of the screen, there's "Steps you made:", where you will be counted by the times you hit the cue ball, and "Best Game steps" where the best game you ever played number of steps is showed. Quick note here, I keep the best game in a text file which means I can still access the best game even if I close and reopen the game. 

Time to experience the game now. You will use the mouse to rotate the cue stick in order to decide the direction from which you're about to hit the cue. Once you decided, you'll drag the cue stick, by pressing mouse of course, for a certain distance, to get the force you will apply on the cue, and then release. The cue will be moving then. Quick note again: drawing the rotating cue stick cost me a whole afternoon, the math to draw the polygon was hard. 

Now comes the most important part of my game --- collision. I don't feel like explaining what you will see for collision. But there're two main types of collision. The easier one is the wall-ball collision. And the much more difficult one is the ball-ball collision. For the ball-ball collision, I encoutered by dividing into two groups of collision. And it took me two days to finally have a working collision that you can see now. 

The game will end if you finish all the color balls with the black ball being pocketed last. If you accidentally pot your cue, it will go back to its original position.

I really hope you enjoy my pool game!