
class Trie:
    """
    Class for Trie data structure
    """
    def __init__(self):
        """
        Function description: Constructor of Trie class

        Input:  None

        Ouput:  None

        Time Complexity:    O(1)
        -Analysis: Creating the Node class object takes constant time
        Auxiliary space Complexity:O(1)
        Space Complexity:   O(1)
        """
        self.root = Node()


    def insert(self, key):
        """
        Function description:
        Inserting key to the Trie using tail recursion

        Input:  key(string)

        Ouput:  None

        Time Complexity:    O(n), where n is the length of string
        -Analysis:  The auxiliary function will call itself n times

        Auxiliary space Complexity:   O(n), where n is the length of string
        -Analysis:  The auxiliary function will call itself n times, so 
                    n spaces are needed for the run stack.

        Space Complexity: O(1)(Input) + O(n), where n is the length of string
        """
        self.insert_aux(self.root, key, 0)


    def insert_aux(self, current, key, height):
        """
        Function description:
        Auxiliary function of insert function.
        This function will create the Node if the Node does not exist.
        When it reaches the end of the key, it will create the terminal node and return it.
        When returning the terminal node, each node will decide to add the terminal node to their current ranking 
        or update the ranking base on several criterias.

        Input:
        argument1:current(Node)
        argument2:key(string)
        argument3:height(int)

        Ouput:  terminal_node(Node)

        Time Complexity:    O(n), where n is the length of string
        -Analysis:  It will call itself until height equals to length of string,
                    so it will call itself O(n) times,

        Auxiliary space Complexity:   O(n), where n is the length of string
        -Analysis:  Since it will call itself n times, it will also take n
                    spaces in the run stack.

        Space Complexity: O(1)(Inputs) + O(n), where n is the length of string
        """

        #Reach the end of the string
        if(len(key) == height):
            
            #Create the terminal node if it is not existed
            if(current.link[0] is None):
                current.link[0] = Node()
                current.link[0].string = key
                current.link[0].height = height

            #Increase the frequency
            current.link[0].freq += 1
            #Update the ranking
            self.update_ranking(current.link[0], current)
            #Maintain the order of ranking
            self.sorting(current)

            return current.link[0]  #return the terminal node
        
        index = self.scale(key[height])

        #Create the node
        if(current.link[index] is None):
            current.link[index] = Node()
            current.link[index].height = height + 1

        current = current.link[index]
        terminal_node = self.insert_aux(current, key, height + 1)

        self.update_ranking(terminal_node, current)
        self.sorting(current)
        return terminal_node
    

    def update_ranking(self, terminal_node, current):
        """
        Function description:
        This function will update the current node's ranking.

        Input: 
        argument1: terminal_node(Node)
        argument2: current(Node)

        Ouput:  None

        Time Complexity:    O(1)
        -Analysis:      
                Since the maximum size of ranking is fixed, which is always less or equal to 3.
                Therefore, the time complexity of looping through ranking is constant.
                Besides that, time complexity of comparing the pointers to terminal_node is O(1) too.
                Lastly,the function of comparing the ascii value has O(1) time complexity. 
                Therefore, this entire function's time complexity is O(1).

        Auxiliary space Complexity:   O(1)
        -Analysis: It does not create any lists or calling itself, so O(1)

        Space Complexity: O(1)(Inputs) + O(1)
        """

        #Looping through the ranking using in keyword to check this is a new terminal node
        if(terminal_node not in current.ranking):

            #If the size of ranking is less than 3, 
            #we can just add the terminal node to the ranking and sort it later
            if(len(current.ranking) < 3):
                current.ranking.append(terminal_node)
                return 
            
            #If the ranking is full, we can just compare the last item of the ranking
            #This is because the ranking is sorted, the last item always has the lowest frequency or highest ascii value
            last_node = current.ranking[-1]

            #New terminal node has higher frequency,so replace it
            if(last_node.freq < terminal_node.freq):
                current.ranking[-1] = terminal_node
            
            #Both has the same frequency, compare ascii value
            elif(last_node.freq == terminal_node.freq):
                bigger = self.compare_ascii(terminal_node, current.ranking[-1], current)

                #If the last item has bigger ascii value, replace it.
                if(bigger is current.ranking[-1]):
                    current.ranking[-1] = terminal_node


    def compare_ascii(self, terminal_node1, terminal_node2, current):
        """
        Function description:
        Comparing the terminal node's string's ascii value, and return the terminal node with higher ascii value

        Input: 
        argument1: terminal_node1(Node)
        argument2: terminal_node2(Node)
        argument3: current(Node)

        Ouput:  terminal_node, with higher ascii value

        Time Complexity:    O(1)
        -Analysis:  
                   Since the maximum size of ranking is fixed, which is only 3.
                   Looping through the ranking to check the pointer to
                   terminal node or get the index of it takes constant time.
                   Besides that, comparing two characters also takes constant time,
                   therefore this function's time complexity is O(1).

        Auxiliary space Complexity:   O(1)
        -Analysis:
                    It does not create any lists or call itself.
        
        Space Complexity: O(1)(Inputs) + O(1)
        """

        height = current.height 

        #If the current's height equals to the length of terminal_node's string,
        #means this current node's link[0] is this terminal node, which is shorter but has the same prefix
        #This string has lower ascii value base on third criteria
        if(height  == len(terminal_node1.string)):
            return terminal_node2
        elif(height == len(terminal_node2.string)):
            return terminal_node1

        #If both of them is longer than current's height, compare the character 
        if(ord(terminal_node1.string[height]) > ord(terminal_node2.string[height])):
            return terminal_node1
        elif(ord(terminal_node1.string[height]) < ord(terminal_node2.string[height])):
            return terminal_node2

        #If both of them has the same character, we reuse the ranking of that character's node.
        #For example, IDK, IDA, we are at I node. The height of I node is 1, but both of them string[1] are same, which is D.
        #Therefore, we get the next node's ranking, which is D node, to know the order of this two strings.
        
        prev = current.link[self.scale(terminal_node1.string[height])]
        
        if(prev):
            reused_ranking = prev.ranking
            p1 = None #index of terminak_node1 in previous ranking
            p2 = None #index of terminak_node1 in previous ranking

            if(terminal_node1 in reused_ranking):
                p1 = reused_ranking.index(terminal_node1)

            if(terminal_node2 in reused_ranking):
                p2 = reused_ranking.index(terminal_node2)
            
            #If both of them are inside the previous ranking
            #Compare the index
            if(p1 is not None and p2 is not None):
                if(p1 > p2): #Bigger one means it has bigger ascii value or lesser frequency
                    return terminal_node1
                return terminal_node2
            
            #The one not inside the ranking means it is definitely not important.
            elif(p1 is not None):
                return terminal_node2
            
            elif(p2 is not None):
                return terminal_node1
        

    def sorting(self, current):
        """
        Function description:
        Sort the current node's ranking base on three criterias using buble sort

        Input: current(Node)

        Ouput:  None

        Time Complexity:    O(1)
        -Analysis:
                    Buble sort's time complexity is O(n^2), where n is the number
                    of items. However, the maximum number of item in ranking
                    is fixed, which is 3. Plus the time complexity of comparing two
                    pointers takes constant time too. Therefore, this function's
                    time complexity is O(1).

        Auxiliary space Complexity:   O(1)
        -Analysis:  
                    Buble sort does not create additional lists or call itself.
        
        Space Complexity: O(1)(Input) + O(1)
        """
        done = False            #Indicating the ranking is sorted or not
        rank = current.ranking
        looping_limit = 0       #Prevent it from infinite loop, the maximum 
                                # number of looping should be 9 

        while not done and looping_limit < 10:    
            done = True
            looping_limit += 1

            for i in range(len(rank)-1):
                #Compare frequency
                if(rank[i].freq < rank[i+1].freq):
                    temp = rank[i]
                    rank[i] = rank[i+1]
                    rank[i+1] = temp
                    done = False

                #Same frequency, compare ascii value
                elif(rank[i].freq == rank[i+1].freq):
                    
                    bigger = self.compare_ascii(rank[i], rank[i+1], current)
                    
                    if(bigger is rank[i]):
                       
                        temp = rank[i]
                        rank[i] = rank[i+1]
                        rank[i+1] = temp
                        done = False
    
    def search(self, key):
        """
        Function description:
        This function will search through the Trie base on the key, and return
        maximum top 3 words.

        Input: key(string)

        Ouput:  None

        Time Complexity:    O(n), where n is the length of key
        -Analysis:  
                    n is the length of key

                    1.Call the auxiliary function :                 O(n)
                    2.Looping through lists and get top 3 words:    O(3)(max)

                    Total: O(n) + O(3) = O(n)

        Auxiliary space Complexityy:   O(n), where n is the length of key
        -Analysis:
                    n is the length of key

                    1.Auxiliary function calls itself:          O(n)
                    2.Get the top 3 words                       O(3)(max)

                    Total: O(n) + O(3) = O(n)

        Space Complexity: O(1)(Input) + O(n), where n is the length of key        
        """
        result = self.search_aux(self.root, key, [])
        if(result):
            for i in range(len(result)):
                result[i] = result[i].string
            return result
        return []
    
    def search_aux(self, current, key, lst):
        """
        Function description:
        The auxiliary function of search function. This function will call itself
        several times base on the key's valid part,then return a list that 
        contains maximum top 3 words.

        Input: 
        argument1: current(Node)
        argument2: key(string)
        argument3: lst(list)

        Ouput:  lst(list)

        Time Complexity:    O(n), where n is the length of key
        -Analysis:  In worst case scenario, the key is existed in the trie, so 
                    we need to loop through the key to reach terminal node, which
                    means this function will call itself n times, where n is the 
                    length of string

        Auxiliary space Complexity:   O(n), where n is the length of key
        -Analysis:  Same as before, if the key is existed in the trie. This function
                    will call itself n times, so this function needs n spaces in the run stack
        
        Space Complexity: O(1)(Inputs) + O(n)
        """

        #While searching, if we found that the node is not existed, we can 
        #focus on getting the top 3 words
        if(current is None):
            return lst

        #If we reach the end of string, we check index 0 of the link.
        #If it is not none, means this word is existed, so we can return empty list
        #Else we need to get the top 3 words.
        if(len(key) == current.height):
            if(current.link[0] is None):
                return current.ranking
            return None

        #Get the index of next node
        index = self.scale(key[current.height])

        #If the first character of string does not existed, we return empty list
        if(current is self.root and current.link[index] is None):
            return None
        
        lst = self.search_aux(current.link[index], key, lst)
        
        if(current is not self.root and lst is not None):
            if(len(lst) < 3):#Ensure the maximym size of returning list is 3
                for i in current.ranking:
                    #Only add the new pointers
                    if(i not in lst and len(lst) < 3):
                        lst.append(i) 
        return lst       
    
        
    def scale(self, char):
        """
        Function description:
        This function will convert the input into integer.The integer will be 
        inside the range [0, 62].

        Input: char(character)

        Ouput:  index(int)

        Time Complexity:    O(1)
        -Analysis:  This time complexity of checking the char(isdigit, isupper)
                    takes constant time.
                    Getting the ascii value of char(ord) also takes constant time
                    ,plus time complexity of arithmetic operation(+,-) is O(1).
                    Therefore, the time complexity of this function is O(1).

        Auxiliary space Complexity:   O(1)
        -Analysis: This function does not create any lists or call itself

        Space Complexity: O(1)(Input) + O(1)
        """
        #Digit
        if(char.isdigit()):
            return int(char) + 1
        #Uppercase
        if(char.isupper()):
            return ord(char) - 54
        #Lowercase
        return ord(char) - 60
    

class Node:
    """
    Class for Node of Trie
    """
    def __init__(self, size = 63):
        """
        Function description: Constructor of Node class

        Input:  size(optional)(int)

        Ouput:  None

        Time Complexity:    O(n), where n is the size
        -Analysis: Creating the link array takes n times, where n is the size

        Auxiliary space Complexity:  O(n), where n is the size
        -Analysis: Creating the link array takes n spaces, where n is the size

        Space Complexity:   O(1)(Input) + O(n)
        """
        self.link = [None]*size
        self.freq = 0
        #Store maximum 3 pointers
        self.ranking = []
        self.string = None
        self.height = 0
        #self.terminal_node = None
      
    
class SpellChecker:
    """
    Class of SpellChecker 
    """
    def __init__(self, file_name):
        """
        Function description: Constructor of SpellChecker class

        Input:  file_name(string)

        Ouput:  None

        Time complexity: O(T), where T is the number of characters of the file
        -Analysis:  T is the number of character of the file

                    Each word will be looped through 3 times.
                    1. Adding it to the word list
                    2. Using join function 
                    3. Insert the word to the trie

                In worst case,if the file only has one word, all the characters of the file will be looped through 3 times,
                so the time complexity is O(3T), which is O(T) 

        Auxiliary Space Complexity: O(T), where T is the number of character of the file.
        -Analysis:  In worst case, there is only one word in the file so the word list will
                    take T spaces to create the word, using join function will create a string that 
                    takes T spaces.After that, inserting it to the trie needs T nodes.

                    Overall, its auxiliary space complexity is O(T), where T is the number of character of the file.

        Space Complexity: O(1)(Input) + O(T), where T is the number of character of the file.

        """
        #Creating the Trie 
        self.trie = Trie() 
        file = open(file_name, "r")

        #Looping through each line of the file
        for line in file:

            word = []

            #Looping through every character of the line
            for letter in range(len(line.strip())):

                #If it is a valid character, add it to list
                if(line[letter].isalpha() or line[letter].isdigit()):
                    word.append(line[letter])

                #If we encounter invalid character, we insert the accumulated character
                # to the trie    
                elif(len(word) != 0):
                    self.trie.insert("".join(word))
                    word = []

            if(len(word) != 0):
                self.trie.insert("".join(word))
        #Close the file        
        file.close()
                   
                    
    def check(self, key):
        """
        Function description: 
        This function will take a key as argument and search through the Trie.After that,
        it will return a list that contains maximum 3 words that meets some criterias or 
        an empty list.
        
        Approach description:
        We decide to add an attribute to the Node, which is a list(I call it ranking) that contains maximum 3 words base on 3 criterias.
        Therefore, we can get the top 3 words easily when we are searching for it, do not need to traverse the entire trie.

        When we are reading the file, we insert the words to our trie using recursion. The benefit of recursion is it can return something.
        In this case, we want it to return a pointer to the terminal node. The reason we want the pointer to terminal node instead of word itself, is 
        the space complexity of the pointer is O(1), unlike word will take n spaces, where n is the length of word. Besides that, terminal node
        can store more information, such as the frequency, which we cannot know from the word. Therefore, it is logical to store the pointer to the
        terminal node inside the ranking. Besides that, each node has an attribute called height, so we can know the index of characters we should compare 
        at that node.

        When we are returning the pointer to terminal node, each node will compare this pointer to those pointer(s) inside the ranking. However, we can compare 
        this new pointer to the last pointer of the ranking because the ranking will maintain order. The last pointer is the worst among all 3 pointers. 
        In other word, if the new pointer is worse than the last pointer of the ranking, it is also worse that the other pointers. The way of comparing two pointers
        are comparing the frequency then the ascii value.Time compexity of comparing the frequency takes constant time, so we do not need to worry. The problem is the
        ascii value. We can know that the index of that character we should compare for two pointers, but there is a scenario that both of them share a long common prefix.
        For example, abbbbba, abbbbbb, and now we are at the first b node. We cannot continue comparing until the last character because the time complexity is not O(1) anymore.
        To solve this problem, we decide to reuse the ranking of previous node. We use in keyword to check the position of both pointers of the previous ranking, it will take constant
        time since the maximum size of ranking is fixed. After that, we compare their position, if one of their poisitions is none, means that pointer is worse. However, if both of
        their positions are not none, we compare the index, the bigger index means it is worse.

        After update the ranking,
        we need to maintain the order,so we sort the pointer using buble sort. The reason of using buble sort is it is inplace, no additional spaces required.
        Besides that, since the maximum size of ranking is fixed, which is always 3, so the worst case of buble sort now become O(1) too. 

        This process will make our searching easier. Because we just need to search until the end of key or encounter the node does not exist, we just get the current node's ranking
        as the returning list and returning back. If the returning list's size is lesser than 3, we get the pointers from the nearer node's ranking until it is full.

        After that, we use a for-loop, to change the pointer to the word they stored and return this list of strings.

        Input:  key(string)

        Ouput:  empty list or a list with maximum 3 strings

        Time complexity: O(M), where M is the length of key
        -Analysis:  In worst case, the key is inside the Trie, so we need to 
                    search until the end of key.

                    M is the length of key
                    1. Using strip to check key is empty or not:      O(M)
                    2. Using search function of trie:                 O(M)

                    Total: O(M) + O(M)  = O(2M)
                                        = O(M)
                        
        Auxiliary Space Complexity: O(M), where M is the length of key
        -Analysis:  Same as before, the worst case is the key is inside the Trie,
                    so the the auxiliary search function will call itself M times,
                    the calling of this function needs M spaces in run stack.

        Space Complexity:O(1)(Input) + O(M), where M is the length of key
        """
        if(key.strip() == ""):
            return []

        checking = self.trie.search(key) 

        return checking