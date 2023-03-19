import csv
import random
import tkinter as tk

# Read in the CSV file and store the questions, answers, and decoys
questions = []
with open('questions.csv') as file:
    reader = csv.reader(file)
    next(reader) # Skip the header row
    for row in reader:
        question = row[0]
        answer = row[1]
        decoys = row[2:]
        question_dict = {'question': question, 'answer': answer, 'decoy1': decoys[0], 'decoy2': decoys[1], 'decoy3': decoys[2]}
        questions.append(question_dict)

# Randomize the order of the questions
random.shuffle(questions)

# Initialize variables to keep track of score and current question
score = 0
current_question = 0

#Create global variables for options and option labels
option = None
option_labels = []

# Create a function to check the user's answer and update the score
def check_answer():
    global score
    global current_question
    global option

    # Check whether an option has been selected
    if option is None:
        return
    
    # Get the user's answer from the selected radio button
    selected = option.get()
    user_answer = option_labels[selected-1]['text']
    
    # Get the correct answer for the current question
    correct_answer = questions[current_question]['answer']
    
    # If the user's answer is correct, increment the score
    if user_answer == correct_answer:
        score += 1
    
    # Move to the next question
    current_question += 1
    
    # Set option to None to show the next question
    option = None
    
    # If there are more questions, display the next one
    if current_question < len(questions):
        display_question()
    # If all questions have been asked, display the final score
    else:
        question_label.config(text='Quiz complete! Final score: {}'.format(score))
        option_frame.destroy()
        score_label.destroy()
        next_button.destroy()


def display_question():
    global option
    global score
    global option_labels
    
    # Clear the answer options from the previous question
    option_labels.clear()

    if option is not None:
        for label in option_frame.winfo_children():
            label.destroy()

    # Get the current question and answer options
    current = questions[current_question]
    q = current['question']
    answer = current['answer']
    decoy1 = current['decoy1']
    decoy2 = current['decoy2']
    decoy3 = current['decoy3']
    
    # Randomize the order of the answer options
    options = [answer, decoy1, decoy2, decoy3]
    random.shuffle(options)
    
    # Display the question and answer options
    question_label.config(text=q)
    option = tk.IntVar()
    option_labels = []
    for i in range(4):
        option_labels.append(tk.Label(option_frame, text='', width=30))
        option_labels[-1].grid(row=i, column=0, sticky='w')
        option_button = tk.Radiobutton(option_frame, variable=option, value=i+1,  command=check_answer)
        option_button.grid(row=i, column=1, sticky='w')
    
    # Update the text of the answer option labels
    for i, option_text in enumerate(options):
        option_labels[i].config(text=option_text)

    # Update the score label
    score_label.config(text='Score: {}'.format(score))


# Create the main GUI window
root = tk.Tk()
root.title('Pop Trivia Quiz')

# Create a frame for the question and answer options
question_frame = tk.Frame(root, padx=20, pady=20)
question_frame.pack()

# Create a label for the question
question_label = tk.Label(question_frame, text='')
question_label.grid(row=0, column=0, sticky='w')

# Create a frame for the answer options
option_frame = tk.Frame(question_frame, padx=20, pady=20)
option_frame.grid(row=1, column=0, sticky='w')

# Create a label for the score
score_label = tk.Label(root, text='Score: {}'.format(score))
score_label.pack()

# Create a button to move to the next question
next_button = tk.Button(root, text='Next Question', command= check_answer)

# Display the "Next Question" button
next_button.pack()

# Display the first question
display_question()

root.mainloop()