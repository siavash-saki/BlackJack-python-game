from random import shuffle, choice, randrange

def new_deck():
    
    return [(x,y) for x in ['heart','sapde','club','diamond'] for y in range(1,14)]

card_deck=new_deck()


def pick_a_card():


	while True:
	    
		

	    if card_deck==[]:
	        card_deck=new_deck()
	        
	    else:
	        card_suit, card_num = choice(card_deck)
	        card_deck.remove((card_suit, card_num))
	        break

	return (card_suit,card_num)




def card_num_image(card_num):

    if card_num==1:
        return 'A '    
    elif card_num==10:
        return '10'     
    elif card_num==11:
        return 'J '      
    elif card_num==12:
        return 'Q '      
    elif card_num==13:
        return 'K '        
    else:
        return str(card_num)+' '
    
def card_suit_image(card_suit):
    
    if card_suit=='heart':
        return b'\xe2\x99\xa5'.decode("utf-8", "ignore")
    elif card_suit=='spade':
        return b'\xe2\x99\xa0'.decode("utf-8", "ignore")
    elif card_suit=='club':
        return b'\xe2\x99\xa3'.decode("utf-8", "ignore")
    elif card_suit=='diamond':
        return b'\xe2\x99\xa6'.decode("utf-8", "ignore")

def card_image():

    num_image=card_num_image(card_num)
    suit_image=card_suit_image(card_suit)
    
    r1=' _____'
    r2='|     |'
    r3=f'|{num_image}  {suit_image}|'
    r4='|_____|'

    return [r1,r2,r3,r4]