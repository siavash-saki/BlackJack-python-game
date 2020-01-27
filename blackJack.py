"""
Black Jack Game
"""

from time import sleep

#clear the screen

print (100*'\n')



#Printing Banner

from art import text2art

welcome=text2art('Welcome')
to=text2art(10*" "+'to')
blackjack=text2art(20*" "+'Black Jack')
print(welcome+to+blackjack)


#Introduction

print('You play against the computer dealer.\nYour starting money is = 100$')

from sys import exit

while True:
    
    ready_or_not= input('\n\n Are you ready to Play? (y/n) ')
    
    if ready_or_not == 'y':
        break
    elif ready_or_not== 'n':
        exit('\n\n   ------ Come back when you are ready! ------ \n\n')
    else:
        print ('\nPlease chose only "y" or "n"!' )

print (100*'\n')

###########################################################################################


from random import shuffle, choice, randrange
from termcolor import colored


###########################################################################################

#Classes

class card():


    def __init__(self,card_suit_num):
        self.card_suit,self.card_num = card_suit_num[0],card_suit_num[1]

    def card_score(self):
        if self.card_num == 1:
            return 11
        if self.card_num > 10:
            return 10
        else:
            return self.card_num    

    def card_num_image(self):

        if self.card_num==1:
            return 'A '    
        elif self.card_num==10:
            return '10'     
        elif self.card_num==11:
            return 'J '      
        elif self.card_num==12:
            return 'Q '      
        elif self.card_num==13:
            return 'K '        
        else:
            return str(self.card_num)+' '
        
    def card_suit_image(self):
        
        if self.card_suit=='heart':
            return b'\xe2\x99\xa5'.decode("utf-8", "ignore")
        elif self.card_suit=='spade':
            return b'\xe2\x99\xa0'.decode("utf-8", "ignore")
        elif self.card_suit=='club':
            return b'\xe2\x99\xa3'.decode("utf-8", "ignore")
        elif self.card_suit=='diamond':
            return b'\xe2\x99\xa6'.decode("utf-8", "ignore")

    def card_image(self):
        
        num_image=self.card_num_image()
        suit_image=self.card_suit_image()

        if self.card_suit in ['heart','diamond']:
            
            r1= colored('  _____ ','red')
            r2= colored(' |     |','red')
            r3= colored(f' |{num_image}  {suit_image}|','red')
            r4= colored(' |_____|','red')

        else:
            r1='  _____ '
            r2=' |     |'
            r3=f' |{num_image}  {suit_image}|'
            r4=' |_____|'

        return [r1,r2,r3,r4]

    def __str__(self):

        str_of_card=''
        for i in self.card_image():
            str_of_card += i+'\n'
        return str(str_of_card)

class Hidden_card():

    card_num=0
    def card_image(self):
        r1='  _____ '
        r2=' |     |'
        r3=' |     |'
        r4=' |_____|'
        return [r1,r2,r3,r4]
    
class Empty_space():
    
    card_num=0
    def card_image(self): 
        r1=r2=r3=r4=10*' '
        return [r1,r2,r3,r4]    

    def card_score(self):
        return 0

###########################################################################################

#Functions

def new_deck():
      
    return [(x,y) for x in ['heart','spade','club','diamond'] for y in range(1,14)]

def pick_a_card(deck):

    while True:

        if deck == []:
            deck = new_deck()

        else:
            card_suit_num = choice(deck)
            deck.remove(card_suit_num)
            break

    return card_suit_num

def score(hand):
    # score=0
    # for i in hand:
    #     score += i.card_score()
    # if 
    # return score

    score_lst=[]
    for i in hand:
        score_lst.append(i.card_score())
    while sum(score_lst)>21 and 11 in score_lst:
            score_lst.remove(11)
            score_lst.append(1)
    return sum(score_lst) 

def print_hand(hand):

    print_list=[]
    
    for x in range(4):
        print_row=[]
        for y in hand:
            print_row.append(y.card_image()[x])
        print_list.append(print_row)

    for i in print_list:
        klm=''
        for q in i:
            klm += q
        print(klm)

def print_table():
    
    print (100*'\n')
    print(' '*10,"Dealer's hand: ")
    print_hand(dealer)
    print(f'\n\n Money: {player_money}$\n BET: {bet}$\n Your Hand:')
    print_hand(player)
    
###########################################################################################

player_money=100
game_deck=new_deck()


while player_money>0:
    
    #placing the bet
    while True:
        try:
            print(f'\nBank :{player_money}$')
            bet=int(input('\nPlace your bet: '))
            if bet<=0:
                print("Please place a valid bet")
                continue

            elif bet <= player_money:
                break

            else:
                print(f"You don't have enough money to bet {bet}$")
                continue
        except:
            print("Please place a valid bet")

        
    player=[card(pick_a_card(game_deck)),card(pick_a_card(game_deck))]
    dealer=[Empty_space(),card(pick_a_card(game_deck)),Hidden_card()]


    while True:

        print_table()
        
        player_score=score(player)
        
        if player_score==21:
            print(f'\nBLACKJACK! You just won {bet}$!')
            player_money += bet
            break
        
        elif player_score>21:
            print(f'\nBUST! You just lost {bet}$!')
            player_money -= bet
            break
        
        else:
            while True:      
                request=input('\nHit or Stand: ')
                if request.lower() in ['hit','stand','h','s']:
                    break
                else:
                    print('Please enter only Hit or Stand!!!\n')
        
        if request.lower() in ['hit','h']:
            player.append(card(pick_a_card(game_deck)))
            continue
            
        elif request.lower() in ['stand','s']:
            
            dealer.pop()
            dealer.append(card(pick_a_card(game_deck)))
            
            
            while True:
                
                sleep(1)
                print_table()
                dealer_score = score(dealer)
                
                if dealer_score>21:
                    sleep(1)
                    print(f'\nYou just won {bet}$!')
                    player_money += bet
                    break

                elif 16<dealer_score==player_score:
                    sleep(1)
                    print('\nPUSH!')
                    break

                elif dealer_score>player_score:
                    sleep(1)
                    print(f'\nYou just lost {bet}$!')
                    player_money -= bet
                    break                
                
                else:
                    dealer.append(card(pick_a_card(game_deck)))
                    
                    
        break


        
print(text2art('YOU    LOST!'))

