import numpy as np
import scipy.signal

#Define 2D kernels for diagonal, vertical and horizontal lines 
KERNELS = [
        np.eye(4,dtype=np.uint8),# 2d arr of diagonal 1s \
        np.eye(4,dtype=np.uint8)[::-1],# 2d arr of diagonal 1s /
        np.ones((4,1),dtype=np.uint8), #2d arr of verticle 1s
        np.ones((1,4),dtype=np.uint8) # 2d arr of horizontal 1s
      ]


# Define ConnectFour class to initialize game
class ConnectFour:
    def __init__(self):
        # Define grid size
        self.w,self.h = 7,6
        # Create a grid of zeros
        self.grid = np.zeros(shape=(self.h,self.w),dtype=np.uint8)
        # Initialize the game state as true or ongoing
        self.game = True

    # Define function to make a copy of the current board
    def copy(self):
        boardCopy = ConnectFour()
        boardCopy.grid = 1*self.grid
        return boardCopy
  
    # Define function to drop a piece in a column
    def drop(self,col):
        # Check if the column is full
        row = self.h-1-list(self.grid[:, col][::-1]).index(0)
        # Drop the piece
        self.grid[row][col] = (self.grid.sum()+1)%3
        return row

    # Define function to simulate a drop
    def simDrop(self,col):
        # Make a copy of the board
        copyBoard = self.copy()
        # Drop the piece
        copyBoard.drop(col)
        # Return the copy
        return copyBoard
    
    # Define function to get available moves
    def getAvailableMoves(self):
        # Return the indices of the columns that are not full
        return np.where(self.grid[0]==0)[0]
      
    # Define function to get huristic value
    def getHuristic(self,kernels,d):
      a=0
      b=0
      for kernel in kernels:
        # Correlate the grid with the kernel to find any matching sequences of 1s or 2s
        onesVals=scipy.signal.correlate2d(self.grid==1, kernel,"valid")
        twosVals=scipy.signal.correlate2d(self.grid==2, kernel,"valid")
        # Create a map of 1s and 0s to indicate which cells are part of a sequence
        oneColorMap = 1-(onesVals>0)*(twosVals>0) 
        # Add a large positive score if there is a winning sequence of 1s
        if onesVals.max()==4:
          a+=10000-d
        # Add a large negative score if there is a winning sequence of 2s
        if twosVals.max()==4:
          b+=10000-d
        # Add a score proportional to the length of the matching sequences of 1s or 2s
        a += (onesVals**2*oneColorMap).sum()
        b += (twosVals**2*oneColorMap).sum()
      # Switch scores depending on whose turn it is
      if (self.grid>0).sum()%2==1:
        a,b=b,a
      
      # return the difference between the scores
      return a-b
  
    # Define function to print the board
    def prettyPrint(self):
      print("\033[H\033[J", end="")
      print("|[ "+"  ".join([f"{i}" for i in range(1,8)])+"]|",end="\n")
      for row in self.grid:
        print("|",end="")
        print(np.array2string(row).replace("1","🔴").replace("2","🟡").replace("0","⚪"),sep="|",end="")
        print("|",end="\n")
      print("|[ "+"  ".join([f"{i}" for i in range(1,8)])+"]|")

# Define negamax function
def negamax(board,depth,alpha,beta):
  '''
  to-do:
  add or sub depth to win faster
  '''
  # Get huristic value
  h=board.getHuristic(KERNELS,depth)
  # Check if the game is over or the depth is 0
  if depth == 0 or abs(h)>=10000:
    return (None,h)
  v = -10000
  bm=None
  # Loop through all available moves
  for move in board.getAvailableMoves():  
    nextBoard=board.simDrop(int(move))
    # Get the huristic value of the next board
    _,nextV=negamax(nextBoard,depth-1,-alpha,-beta)
    nextV*=-1

    # Check if the huristic value is greater than the current value
    if nextV>v:
      v=nextV
      bm=move

    # alpha beta pruning (not working)

    # alpha = min(alpha,v)
    
    # if alpha >= beta:
    #   break

  # return the best move and the huristic value
  return bm,v

if __name__ == "__main__":
  board = ConnectFour()
  col,row = 0,0
  m = -1
  v = 0
  while 1:
    board.prettyPrint()
    print(v)
    if m:
      print(f"Last Bot Move: {m+1}")
    try:
      col = int(input("Column To Drop At: "))
    except:
      continue
    if col-1 not in board.getAvailableMoves():
      continue
    row = board.drop(col-1)
    if (board.grid>0).sum()%2==1:
      m,v = negamax(board,4,-10000,10000)
      board.drop(m)
    if v > 10000 or v<-10000:
      break

  board.prettyPrint()
  print(f"Lost on Col: {m+1}")