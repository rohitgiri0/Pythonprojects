import random

def main():
    questions = [
        # Easy (1-4)
        ["kaisa laga game🤡?", "Mast", "Bohat mast", "Best game ever made", "Bekar", "Best game ever made"],
        ["I speak without a mouth and hear without ears. What am I?", "Echo", "Shadow", "Wind", "Light", "Echo"],
        ["What gets wetter as it dries?", "Towel", "Sponge", "Soap", "Rain", "Towel"],
        ["What has a face and two hands but no arms or legs?", "Clock", "Mirror", "Robot", "Painting", "Clock"],

        # Medium (5-8)
        ["What comes once in a minute, twice in a moment, but never in a thousand years?", "Letter M", "Sunrise", "Full Moon", "Leap Year", "Letter M"],
        ["What can travel around the world while staying in a corner?", "Stamp", "Shadow", "Wind", "Compass", "Stamp"],
        ["What has cities, but no houses; forests, but no trees; and water, but no fish?", "Map", "Dream", "Book", "Painting", "Map"],
        ["What is so fragile that saying its name breaks it?", "Silence", "Glass", "Egg", "Promise", "Silence"],

        # Challenging (9-12)
        ["I am not alive, but I can grow. I don't have lungs, but I need air. What am I?", "Fire", "Plant", "Cloud", "Shadow", "Fire"],
        ["What can fill a room but takes up no space?", "Light", "Air", "Sound", "Shadow", "Light"],
        ["The more you take, the more you leave behind. What are they?", "Footsteps", "Memories", "Time", "Shadows", "Footsteps"],
        ["What belongs to you, but other people use it more than you do?", "Your name", "Your phone", "Your car", "Your house", "Your name"],

        # Difficult (13-16)
        ["What has many teeth, but can't bite?", "Comb", "Saw", "Zipper", "Fork", "Comb"],
        ["What is always in front of you but can’t be seen?", "Future", "Air", "Shadow", "Wind", "Future"],
        ["What word is spelled incorrectly in every dictionary?", "Incorrectly", "Dictionary", "Misspelled", "Wrong", "Incorrectly"],
        ["Do you want 1 crore rupees🫣", "Yes", "No", "Khud kama lega", "khud toh kamaunga tab kamaunga abhi dedo", "khud toh kamaunga tab kamaunga abhi dedo"]
    ]


    for q in questions:
        options = q[1:5]
        random.shuffle(options)
        q[1:5] = options

    score = 0

    for i,question in enumerate(questions,start=1):
        print(f"{question[0]}")
        print(f"a .{question[1]}")
        print(f"b .{question[2]}")
        print(f"c .{question[3]}")
        print(f"d .{question[4]}")

        u_ans=input("Enter your answer: ")
        if u_ans.lower() == ['a', 'b', 'c', 'd'][[question[1], question[2], question[3], question[4]].index(question[5])]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {question[5]}\n")
            break
            
    score_levels = [
        0, 1000, 2000, 5000, 10000, 20000, 40000, 80000,
        100000, 150000, 320000, 640000, 1280000, 2500000,
        5000000, 10000000, 70000000
    ]

    print(f"You won {score_levels[score]} rupees🤑.")
    
if __name__=="__main__":
    main()