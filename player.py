C = False #coopirate
D = True  #defact

class MyPlayer:
    '''combination of two strategies depending on number_of_iterations'''

    def __init__(self,payoff_matrix,number_of_iterations=20):
        self.payoff_matrix=payoff_matrix
        self.number_of_iterations=number_of_iterations
        self.opponent_last_move=-1
        self.moves_count=0
        # The memory matrix is a matrix that, based on the last 2 moves of the opponent 
        # and its last move, chooses how to moove. Characterizes strategies.
        self.matrix_mem=( ((C,C),(C,C)),((C,C),(C,C)) ) 
        
    def choose_strategy(self):
        self.moves_count+=1

        # 1 defect, 2 cooperate, then 1 receives the Temptation payoff T,
        T=self.payoff_matrix[D][C][0]
        # while 2 receives the "sucker's" payoff S.
        S=self.payoff_matrix[D][C][1]
        # If both players cooperate, they both receive the reward R for cooperating.
        R=self.payoff_matrix[C][C][0]
        # If both players defect, they both receive the punishment payoff P.
        P=self.payoff_matrix[D][D][0]
        
        if(T>R>P>S):
            if(self.number_of_iterations >100):
                if(self.moves_count>100):
                    self.matrix_mem=self.spiteful_cc()
                elif(self.moves_count>50):
                    self.matrix_mem=self.tft_spiteful()
                else: 
                    self.matrix_mem= self.winer12()
            elif(self.number_of_iterations<40):
                if(self.moves_count>10):
                    self.matrix_mem=self.spiteful_cc()
                else:
                    self.matrix_mem=self.winer12()
            else:
                if(self.moves_count>50):
                    self.matrix_mem=self.spiteful_cc()
                else:
                    self.matrix_mem=self.tft_spiteful()

            if (self.moves_count<=2):
                 return C
            else: 
                return self.matrix_mem[self.my_last_move][self.opponent_penultimat][self.opponent_last_move]
        elif(P>R and P>S and P>T):
            return D
        elif(T>=R and T>=S and T>=P):
            return D
        elif(R>=P and R>=S and R>=T):
            return C
        else: 
            return C

    def spiteful_cc(self):
        # plays CC at the beginning and then plays spiteful
        return ( ((C,D),(D,D)),((D,D),(D,D)) )
    
    def tft_spiteful(self):
        # plays tit_for_tat unless she has been defacted two times consecutively, in which case she always defact
        return ( ((C,C),(C,D)),((D,D),(D,D)) )

    def winer12(self):
        # at the beginning plays c,c. Defects only if both the players did not agree 
        # on the previous move or when she was betrayed twice
        return ( ((C,D),(C,D)),((D,C),(D,D)) )

    def move (self):
        return self.choose_strategy()

    def record_last_moves(self, my_last_move, opponent_last_move):
        self.opponent_penultimat=self.opponent_last_move
        self.my_last_move = my_last_move
        self.opponent_last_move = opponent_last_move
