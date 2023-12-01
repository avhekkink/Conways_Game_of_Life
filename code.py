import numpy as np

def htmlize(array):
    s = []
    for row in array:
        for cell in row:
            s.append('▓▓' if cell else '░░')
        s.append('\n')
    return ''.join(s)
    

def get_generation(cells, generations):
    # initialise current array of size (n, m)
    arr = np.array(cells)
    
    # initialise array to track changes
    new_arr = arr
    
    # initialise array to count the number of neighbours of size (n+2, m+2)
    nhbrs = np.zeros((arr.shape[0]+2, arr.shape[1]+2), np.int8)
    
    # track the generations
    gen = 0
    
    while gen < generations:
        # get co-ords of where the live/dead cells are
        live_coords = np.nonzero(arr)
        dead_coords = np.nonzero(arr==0)
        
        # re-initialise neighbour array of new size
        nhbrs = np.zeros((arr.shape[0]+2, arr.shape[1]+2), np.int8)
        
        # count the no. neighbours each cell has
        for (x,y) in zip(*live_coords):
            for i in range(3):
                for j in range(3):
                    nhbrs[x+i, y+j] += 1
            # correct for cell not being its own nhbr
            nhbrs[x+1,y+1] -= 1
        
        # re-initialise the next generation and then update according to the rules
        new_arr = np.zeros_like(nhbrs)
        
        # first update the live cells
        for (x,y) in zip(*live_coords):
            r, c = x+1, y+1
            if nhbrs[r,c] < 2:
                # cell dies due to undercrowding
                new_arr[r,c] = 0
            elif nhbrs[r,c] > 3:
                # cell dies due to overcrowding
                new_arr[r,c] = 0
            else:
                # cell has 2 or 3 neighbours, so lives on
                new_arr[r,c] = 1
            
        # then update the dead cells, first the originals
        for (x,y) in zip(*dead_coords):
            r,c = x+1, y+1
            if nhbrs[r,c] == 3:
                # cell becomes alive by repoduction
                new_arr[r,c] = 1
                
        # now update the dead cells on the perimeter
        for r in [0, nhbrs.shape[0]-1]:
            for c in range(nhbrs.shape[1]):
                if nhbrs[r,c] == 3:
                    new_arr[r,c] = 1
        for c in [0, nhbrs.shape[1]-1]:
            for r in range(1,nhbrs.shape[0]-1):
                if nhbrs[r,c] == 3:
                    new_arr[r,c] = 1
                    
        # set the array as the new array
        arr = new_arr
        
        # check if we need to delete any empty rows or cols on the perimeter
        while np.all(arr[0,:]==0):
            arr = np.delete(arr, 0, axis=0)
        while np.all(arr[-1,:]==0):
            arr = np.delete(arr, -1, axis=0)
        while np.all(arr[:,0]==0):
            arr = np.delete(arr, 0, axis=1)
        while np.all(arr[:,-1]==0):
            arr = np.delete(arr, -1, axis=1)
            
        # print the current universe
        print(htmlize(arr))
        # increment the generation
        gen += 1
        
    
    # convert back from numpy array to list
    cells = arr.tolist()
    return cells
    
    
    
# Three examples for starting arrays...

start1 = [[0,0,0],
         [1,1,1],
         [0,0,0]]

# Gosper glider gun
start2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# Pulsar, period 3
start3 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,0],
         [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0],
         [0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0],
         [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0],
         [0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0],
         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]



# Demonstration...

get_generation(start3, 12)
