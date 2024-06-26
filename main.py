import threading
import State as ST
import AgentSnake_GBF as GBFS
import AgentSnake as simple
import BFS_ALgorithm as BFS
import AgentSnake_AStar as AStar
import time
import View as V


class Main:	
	def __init__(self, State, AgentSnake, SnakeSpeed=30):
		self.State = State
		self.AgentSnake = AgentSnake
		self.View = V.SnakeViewer(self.State,SnakeSpeed)
		
	def setDirection(self, k):
		if(k == 0):
			self.State.snake.HeadDirection.X = 0
			self.State.snake.HeadDirection.Y = -1
		elif(k == 6):
			self.State.snake.HeadDirection.X = 0
			self.State.snake.HeadDirection.Y = 1
		elif(k == 3):
			self.State.snake.HeadDirection.X = 1
			self.State.snake.HeadDirection.Y = 0
		elif(k == 9):
			self.State.snake.HeadDirection.X = -1
			self.State.snake.HeadDirection.Y = 0	
	
	def ExecutePlan(self, Plan):
		for k in Plan:
			self.setDirection(k)		
			self.State.snake.moveSnake(self.State)
			if(self.State.snake.isAlive == False):
				break
			time.sleep(1/self.View.SPEED)
			self.View.UpdateView()	
	
	def StartSnake(self):
		if(self.State.snake.isAlive == False):
			return
		PlanIsGood = True
		Message = "Game Over"
		while(self.State.snake.isAlive and PlanIsGood):
			ScoreBefore = self.State.snake.score
			
			Plan = self.AgentSnake.SearchSolution(self.State)
			self.ExecutePlan(Plan)
			
			ScoreAfter = self.State.snake.score
			
			if(ScoreAfter == ScoreBefore):
				PlanIsGood = False
			self.State.generateFood()
			time.sleep(1/2)

		if(self.State.snake.isAlive):
			Message = Message + "  HAS A BAD PLAN"
		else:
			Message = Message + " HAS HIT A WALL"
		self.View.ShowGameOverMessage(Message)
	def Play(self):
		t1 = threading.Thread(target=self.StartSnake)
		t1.start()
		t2 = threading.Thread(target= self.View.top.mainloop())	
		t2.start()
		t1.join()
		t2.join()	
			
def main():
    state = ST.SnakeState('red', 10, 10, 0, 1, "Maze.txt")

    print("\nChoose an agent:\n")
    print("1. A Star\n")
    print("2. BFS\n")
    print("3. GFS\n")
    print("4. Simple\n")
    choice = input("Enter your choice (1, 2, 3, or 4): ")
    
    if choice == "1":
        Agent = AStar.AgentSnake_AStar()
    elif choice == "2":
        Agent = BFS.BFS_ALgorithm()
    elif choice == "3":
        Agent = GBFS.AgentSnake_GBF()
    elif choice == "4":
        Agent = simple.AgentSnake() 
    else:
        print("Invalid choice. Defaulting to AgentSnake_AStar.")
        Agent = AStar.AgentSnake_AStar()
    
    Game = Main(state, Agent)
    Game.Play()

if __name__ == '__main__':
    main()


