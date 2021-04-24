#import useful libraries
import json #import library for handling json files
import os #import library to list all files in directory
import datetime #import library used to produce unique values never to appear again

from kivymd.app import MDApp #import MDApp files
from kivy.core.window import Window #import Window files
from kivy.lang import Builder #import code to build kivy files
from kivy.uix.button import Button #import code to display buttons
from kivy.uix.scrollview import ScrollView #import code for scrolling
from kivy.uix.gridlayout import GridLayout #import code for grid layouts
from kivy.uix.label import Label #import code for labels
from kivy.uix.popup import Popup #import code for kivy popups
from kivy.uix.textinput import TextInput #import code for text input boxes
from kivy.clock import Clock #import code for scheduling events


def countBoards():

    global Boards

    Boards = [] #Stores the filename and internal flag title for every board in the system

    files = os.listdir(__file__.replace("\\main.py", "") + "\\boards") #create array of filenames in given directory
    for file in files: #for every filename stored in the files aray
        with open(r"C:\Users\thoma\Desktop\programming project\code\boards\\" + str(file)) as board: #open the board input
            boardData = json.load(board) #save the contents of the board to a dictionary
        board.close() #close the board file as it is not in use anymore
        Boards.append((file, list(boardData.values())[0])) #add file tuple (filename, title flag) to Boards array


def verifyTitle(title): #function to verify if board title exists in Board array

    for board in range(0, len(Boards)): #loop through all boards
        if Boards[board][1] == title: #if stored title = title input into function
                return Boards[board][0] #return filename of associated board
    return False #if title not in array, return false


def returnNoteFilename(noteTitle): #function to verify if note title exists in currently loaded notes

    for note in range(0, len(currentBoardNotes)): #loop through all notes in currentBoardNotes
        if currentBoardNotes[note].title == noteTitle: #check if the title matches the title input into function
            return currentBoardNotes[note].filename #return note filename     
    return False #if note isn't found, return false


def loadBoard(boardName): #Take a board title, load its flags into an object, then load every note into a list of objects

    global currentBoard
    global currentBoardNotes
    boardFilename = str()

    currentBoardNotes = [] #array to store the notes loaded into memory

    class BOARD: #create class datatype to store the flags for the currently in use board
        def __init__(self, name, notes):
            self.name = name #name of board
            self.notes = notes #all the notes this board links to
        
    class NOTE: #create class datatype to store the flags for the currently in use notes
        def __init__(self, filename, parent, title, content, deadline):
            self.filename = filename #filename of note
            self.parent = parent #parent board of note
            self.title = title  #name of note
            self.content = content #content of note
            self.deadline = deadline #content of note

    if boardName != -1:

        boardFilename = verifyTitle(boardName) #get board filename from Boards list

        if boardFilename != False: 
            with open(__file__.replace("\\main.py", "") + "\\boards\\" + boardFilename) as board: #open the board input
                boardData = json.load(board) #save the contents of the board to a dictionary
            board.close() #close the board file as it is not in use anymore

            currentBoard = BOARD(list(boardData.values())[0], list(boardData.values())[1]) #parse the values of name and notes saved in boardData into the board class

            for note in range(0, len(currentBoard.notes)): #loop through all the note titles that the board class links to
                with open(__file__.replace("\\main.py", "") + "\\notes\\" + currentBoard.notes[note] + ".json") as currentNote: #open note file using the file stored in the board class
                    noteData = json.load(currentNote) #save the contents of the note to a dictionary
                currentBoardNotes.append(NOTE(currentBoard.notes[note], list(noteData.values())[0], list(noteData.values())[1], list(noteData.values())[2], list(noteData.values())[3])) #parse filename, parent and title and content into the board class, which is added to the notes list
                currentNote.close #close the note file as it is not in use anymore
            
            return True #Returns true if boardFilename exists

        else:
            print("board does not exist")

    else:
        currentBoard = BOARD("", None)
        currentBoardNotes = []


def createBoard(tempBoardNameInput): #function to create a board based on a name the user inputs

    with open(__file__.replace("\\main.py", "") + "\\boards\\" + str(hash(datetime.datetime.now())) + ".json", "w") as newBoard: #filename is hashed current date + time
        json.dump({"name":tempBoardNameInput, "notes":[]}, newBoard) #add name flag and empty notes flag to board
    newBoard.close() #close the board file as it is not in use anymore
    countBoards() #add this new board to the array containing all board filenames and titles


def createNote(noteName): #function to create a note based on a name the user inputs

    if currentBoard.notes != None:

        tempNoteFilename = str(hash(datetime.datetime.now())) #filename is hashed current date + time
        with open(__file__.replace("\\main.py", "") + "\\notes\\" + tempNoteFilename + ".json", "w") as newNote: #create note file
            json.dump({"parent":currentBoard.name, "title":noteName, "content":"", "deadline":""}, newNote) #add parent, title, content and deadline flag
        newNote.close() #close the note file as it is not in use anymore

        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "r") as board: #open the current board as a read-only
            fileData = json.load(board) #load board's data
        board.close() #close board as no longer needed
        
        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "w") as board: #open the current board as a write-only
            fileData["notes"].append(tempNoteFilename) #add the new note filename to the current board's notes flag
            json.dump(fileData, board) #add the appended data to the note
        board.close() #close board as no longer needed

        loadBoard(currentBoard.name) #re-open the board to load new note into program

    
def deleteNote(tempNoteNameInput): #function to delete a note

    if returnNoteFilename(tempNoteNameInput) != False: #if note title exists....
        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "r") as board: #open the current board as a read-only
            fileData = json.load(board) #load board's data
        board.close() #close board as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "w") as board: #open the current board as a write-only
            fileData["notes"].remove(returnNoteFilename(tempNoteNameInput)) #remove the note filename from the list
            json.dump(fileData, board) #add the appended data to the note
        board.close() #close board as no longer needed

        #PLACEHOLDER SECTION FOR CODE TO REMOVE DATA FROM RELATED FLAGS WHEN IMPLIMENTED

        os.remove(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json") #remove file from directory

        loadBoard(currentBoard.name)

    else:
        print("Note does not exist in array") #if note is not found, print this


def deleteBoard(tempBoardNameInput): #function to delete a board

    if verifyTitle(tempBoardNameInput) != False: #if board title exists....
        loadBoard(tempBoardNameInput) #reload the board to make sure all notes are accounted for

        for note in range(0, len(currentBoardNotes)): #loop through every loaded note
            os.remove(__file__.replace("\\main.py", "") + "\\notes\\" + currentBoardNotes[note].filename + ".json") #remove associated note from directory

            #PLACEHOLDER SECTION FOR CODE TO REMOVE DATA FROM RELATED FLAGS WHEN IMPLIMENTED

        os.remove(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(tempBoardNameInput)) #remove associated board from directory
        Boards.remove((verifyTitle(tempBoardNameInput), tempBoardNameInput)) #remove associated board from Boards array

    else:
        print("Board does not exist in array") #if board is not found, print this


def addNoteContent(tempNoteNameInput, tempNoteContent): #add text to content flag of a note

    if returnNoteFilename(tempNoteNameInput) != False: #if note exists....
        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "r") as currentNote: #open the current note as a read-only
            fileData = json.load(currentNote) #load note's data
        currentNote.close() #close note as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "w") as currentNote: #open the current note as a write-only
            fileData["content"] = tempNoteContent #add the content to the note's content flag
            json.dump(fileData, currentNote) #add the appended data to the note
        currentNote.close() #close note as no longer needed

    else:
        print("Note does not exist in array") #if note is not found, print this

    loadBoard(currentBoard.name)


def editNoteTitle(tempNoteNameInput, tempNewNoteName): #edit the title of a note

    if returnNoteFilename(tempNoteNameInput) != False: #if note exists....
        
        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "r") as currentNote: #open the current note as a read-only
            fileData = json.load(currentNote) #load note's data
        currentNote.close() #close note as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "w") as currentNote: #open the current note as a write-only
            fileData["title"] = tempNewNoteName #swap the title flag to the new value input
            json.dump(fileData, currentNote) #add the appended data to the note
        currentNote.close() #close note as no longer needed

    else:
        print("Note does not exist in array") #if note is not found, print this

    loadBoard(currentBoard.name) #reload notes so that new note title is loaded into memory


def editBoardTitle(tempNewBoardName): #edit the title of a board

    if currentBoard.notes != None:

        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "r") as board: #open the current board as a read-only
            fileData = json.load(board) #load board's data
        board.close() #close board as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\boards\\" + verifyTitle(currentBoard.name), "w") as board: #open the current board as a write-only
            fileData["name"] = tempNewBoardName #swap the name flag to the new value input
            json.dump(fileData, board) #add the appended data to the board
        board.close() #close board as no longer needed

        for board in range(0, len(Boards)): #search through Boards array for item containing previous title of this board
            if Boards[board][1] == currentBoard.name:
                Boards[board] = (Boards[board][0], tempNewBoardName) #update array position of this board to contain new name

        loadBoard(tempNewBoardName) #refresh this boards' data into memory

        for note in range(0, len(currentBoardNotes)): #loop through each note associated with this board
            with open(__file__.replace("\\main.py", "") + "\\notes\\" + currentBoardNotes[note].filename + ".json", "r") as currentNote: #open the current note as a read-only
                fileData = json.load(currentNote) #load note's data
            currentNote.close() #close note as no longer needed

            with open(__file__.replace("\\main.py", "") + "\\notes\\" + currentBoardNotes[note].filename + ".json", "w") as currentNote: #open the current note as a write-only
                fileData["parent"] = tempNewBoardName #add the content to the note's content flag
                json.dump(fileData, currentNote) #add the appended data to the note
            currentNote.close() #close note as no longer needed


def addNoteDeadline(tempNoteNameInput, tempDeadline):

    if returnNoteFilename(tempNoteNameInput) != False: #if note exists....
        
        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "r") as currentNote: #open the current note as a read-only
            fileData = json.load(currentNote) #load note's data
        currentNote.close() #close note as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(tempNoteNameInput) + ".json", "w") as currentNote: #open the current note as a write-only
            fileData["deadline"] = tempDeadline #swap the deadline flag to the new value input
            json.dump(fileData, currentNote) #add the appended data to the note
        currentNote.close() #close note as no longer needed

    else:
        print("Note does not exist in array") #if note is not found, print this

    loadBoard(currentBoard.name) #reload notes so that new note title is loaded into memor

def removeNoteDeadline(noteTitle): #function to verify if note title exists in currently loaded notes

    if returnNoteFilename(noteTitle) != False: #if note exists....
        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(noteTitle) + ".json", "r") as currentNote: #open the current note as a read-only
            fileData = json.load(currentNote) #load note's data
        currentNote.close() #close note as no longer needed

        with open(__file__.replace("\\main.py", "") + "\\notes\\" + returnNoteFilename(noteTitle) + ".json", "w") as currentNote: #open the current note as a write-only
            fileData["deadline"] = "" #add the content to the note's content flag
            json.dump(fileData, currentNote) #add the appended data to the note
        currentNote.close() #close note as no longer needed

    else:
        print("Note does not exist in array") #if note is not found, print this

    loadBoard(currentBoard.name)


class NoteApp(MDApp): #create class for user interface to be run from

    Window.size = (450, 800) #set the size of the window opened

    def build(self): #build the code for the app)

        return Builder.load_file(__file__.replace("\\main.py", "") + "\\formatting.kv") #load the user interface formatting file


    def scheduledList(self, dt): #run this code as scheduled
        self.displayNotes()
        self.root.ids.topBar.title = currentBoard.name #change title of toolbar with id topBar


    def on_start(self): #run this code when the app is launched

        Clock.schedule_interval(self.scheduledList, 1) #create a clock object that runs the scheduledList function every 2 seconds

        countBoards() #add all boards to Boards array
        if len(Boards) != 0: #if boards array is not empty...
            loadBoard(Boards[0][1]) #load the first board in the Boards array
            self.root.ids.topBar.title = currentBoard.name #change title of toolbar with id topBar
        else: #else, run special case
            loadBoard(-1)

    def displayNotes(self):

        self.root.ids.noteSection.clear_widgets()

        layout = GridLayout(cols=1, spacing=-2, size_hint_y=None) #create layout for widgets to be added to
        layout.bind(minimum_height=layout.setter('height')) 

        for note in range(0, len(currentBoardNotes)): #loop through every stored note

            titleLabel = Button( #create a button with the following parameters:
                text=currentBoardNotes[note].title,  
                size_hint_y = None,
                font_name = 'Roboto',
                bold = "True",
                color = [1,1,1,1],
                background_color = [0, 0.5, 1, 0.5],
                height = 35,
                text_size = (self.root.width, 20),
                font_size = '20sp',
                padding_x = 5,
                padding_y = 0,
                on_press = self.noteEditing
                )

            layout.add_widget(titleLabel) #add titleLabel to layout
 
            contentLabel = Button( #create a button with the following parameters:
                text = currentBoardNotes[note].content, 
                font_name = 'Roboto',
                size_hint_y = None, 
                color = [1,1,1,1], 
                background_color = [0, 0.5, 1, 0.4],
                text_size = (self.root.width, None),
                padding_x = 6,
                height = len(currentBoardNotes[note].content) * 0.335 + 35
                )

            layout.add_widget(contentLabel) #add contentLabel to layout

            if currentBoardNotes[note].deadline != "":

                self.currentDate = datetime.datetime.now().date() #get current date
                self.currentTime = datetime.datetime.now().time() #cet current time
                self.inputDate = datetime.date(int(currentBoardNotes[note].deadline[0][0 : 4]), int(currentBoardNotes[note].deadline[0][5 : 7]), int(currentBoardNotes[note].deadline[0][8 : 10]))
                self.inputTime = datetime.time(int(currentBoardNotes[note].deadline[1][0 : 2]), int(currentBoardNotes[note].deadline[1][3 : 5]), datetime.datetime.now().time().second, datetime.datetime.now().time().microsecond)

                if self.currentDate == self.inputDate: #if the current date and input date are the same....

                    if self.currentTime <= self.inputTime: #a check needs to be done on the time input, to check the time input isn't less than the current time

                        self.deadlineColour = [1, 1, 1, 1]

                    else:
                    
                        self.deadlineColour = [1, 0, 0, 1]

                elif self.currentDate <= self.inputDate:  #check that the current date is less than the input date

                    self.deadlineColour = [1, 1, 1, 1]

                else:
                    
                    self.deadlineColour = [1, 0, 0, 1]

                deadlineLabel = Button(
                    text = "Deadline: " + currentBoardNotes[note].deadline[0][8 : 10] + currentBoardNotes[note].deadline[0][4 : 8] + currentBoardNotes[note].deadline[0][0 : 4] + " at " + currentBoardNotes[note].deadline[1][0 : 5],
                    font_name = 'Roboto',
                    bold = "True",
                    size_hint_y = None, 
                    height = 35,
                    color = self.deadlineColour, 
                    background_color = [0, 0.5, 1, 0.5],
                    text_size = (self.root.width, None),
                    padding_x = 6,
                )

                layout.add_widget(deadlineLabel) #add deadlineLabel to layout 

            paddingLabel = Label( #create a label with the following parameters:
                text="",   
                size_hint_y = None,
                color=[1,1,1,0], 
                height=25,
                text_size = (self.root.width, None),
                font_size = '20sp',
                padding_x = 5,
                padding_y = 0
                )
             
            layout.add_widget(paddingLabel) #add paddingLabel to layout 

        self.root.ids.noteSection.add_widget(layout)

    def boardEditing(self): #run this code when the button is pressed on the board title toolbar
        self.boardEditingMenu = boardEditingPopup() #create a variable to hold the popup class object
        self.boardEditingMenu.title = "Editing " + currentBoard.name #Edit the title flag of the board to be Editing >BOARDNAME<
        self.boardEditingMenu.open() #open the popup

    def changeBoard(self): #run this code when the button is pressed on the change board toolbar
        self.changeBoardMenu = boardChangingPopup() #create a variable to hold the popup class object
        self.changeBoardMenu.open() #open the popup

    def noteEditing(self, obj): #run this code when the title of any note is pressed
        global currentEditedNote
        currentEditedNote = obj.text
        self.noteEditingMenu = noteEditingMenu() #create a variable to hold the popup class object
        self.noteEditingMenu.title = "Editing " + obj.text
        self.noteEditingMenu.open() #open the popup


class boardEditingPopup(Popup): #class for popup for board editing

    def UIcreateNote(self): #code to run when Add Note button pressed
        self.dismiss() #hide this popup
        self.newNoteInputMenu = newNoteInputBox() #create instance of newNoteInputMenu popup
        self.newNoteInputMenu.open() #run instance of newNoteInputMenu popup

    def UIchangeBoardTitle(self): #code to run when Change Title button pressed
        self.dismiss() #hide this popup
        self.renameBoardInputBox = renameBoardInputBox() #create instance of renameBoardInputBox popup
        self.renameBoardInputBox.open() #run instance of renameBoardInputBox popup
        
    def UIdeleteBoard(self): #code to run when Delete Board button is pressed
        self.dismiss() #hide this popup
        self.confirmBoardDeletionPopup = confirmBoardDeletionPopup() #create instance of confirmBoardDeletionPopup popup
        self.confirmBoardDeletionPopup.open() #run instance of renameBoardInputBox popup


class newNoteInputBox(Popup): #class for popup for entering name of new note
    
    def on_open(self): #when popup is opened

        self.tempNewNoteName = TextInput( #create text input box with following parameters
            text = "", 
            multiline = False,
            size_hint = (0.2, None),
            height = 30,
            )

        self.confirmButton = Button( #create button with following parameters
            text = "Create Note",
            font_name = 'Roboto',
            font_size = 22,
            on_press = self.submitNote #when button pressed, run this function
        )

        self.ids.popupContent.add_widget(self.tempNewNoteName) #add text input box to popup
        self.ids.popupContent.add_widget(self.confirmButton) #add confirmation box to popup

    def submitNote(self, obj): #code to submit note title 
        self.dismiss() #hide popup
        createNote(self.tempNewNoteName.text) #create file in storage system for new note

class renameBoardInputBox(Popup): #class for popup for changing title of board
    
    def on_open(self): #when popup is opened

        self.tempNewNoteName = TextInput( #create text input box with following parameters
            text = "", 
            multiline = False,
            size_hint = (0.2, None),
            height = 30,
            )

        self.confirmButton = Button( #create button with following parameters
            text = "Change Title",
            font_name = 'Roboto',
            font_size = 22,
            on_press = self.changeBoardTitle #when button pressed, run this function
        )

        self.ids.popupContent.add_widget(self.tempNewNoteName) #add text input box to popup
        self.ids.popupContent.add_widget(self.confirmButton) #add confirmation box to popup

    def changeBoardTitle(self, obj): #code to submit note title 
        self.dismiss() #hide popup
        editBoardTitle(self.tempNewNoteName.text) #create file in storage system for new note


class boardChangingPopup(Popup): #popup that enables users to switch and create boards

    def on_open(self): #run this code when app opened

        layout = GridLayout(cols=1, spacing=-2, size_hint_y=None) #create layout for widgets to be added to
        layout.bind(minimum_height=layout.setter('height')) 

        for board in range(0, len(Boards)): #loop through every board in Boards array

            if Boards[board][1] != currentBoard.name: #check that current board in array isn't current board loaded

                self.swapBoardButton = Button( #create a button with with title current board in list
                    text = Boards[board][1],
                    size_hint = (1, None),
                    height = 60,
                    on_press = self.swapBoard
                )

                self.bufferBoard = Button( #create invisible button to add gap between items in list
                    text = "",
                    size_hint = (1, None),
                    height = 15,
                    background_color = (0, 0, 0, 0)
                )

                layout.add_widget(self.swapBoardButton) #add board button to layout
                layout.add_widget(self.bufferBoard) #add buffer to layout

        self.addBoardButton = Button( #create a button that enables users to create new boards
            text = "Add Board",
            size_hint = (1, None),
            height = 60,
            on_press = self.addBoard
        )

        layout.add_widget(self.addBoardButton) #add new board button to layout

        self.ids.swapBoardScroll.add_widget(layout) #add layout to scrollview

    def addBoard(self, obj): #function that closes this popup and opens an input window for creating new board

        self.dismiss() #close this function
        self.newBoardInputBox = newBoardInputBox() #create new popup object
        self.newBoardInputBox.open() #open new popup

    def swapBoard(self, obj):
        self.dismiss() #hide this popup
        loadBoard(obj.text) #load the board that has the same name as the button that was pressed


class newBoardInputBox(Popup): #class for popup for entering name of new board
    
    def on_open(self): #when popup is opened

        self.tempNewBoardName = TextInput( #create text input box with following parameters
            text = "", 
            multiline = False,
            size_hint = (0.2, None),
            height = 30,
            )

        self.confirmButton = Button( #create button with following parameters
            text = "Create Board",
            font_name = 'Roboto',
            font_size = 22,
            on_press = self.UIcreateBoard #when button pressed, run this function
        )

        self.ids.popupContent.add_widget(self.tempNewBoardName) #add text input box to popup
        self.ids.popupContent.add_widget(self.confirmButton) #add confirmation box to popup
        
    def UIcreateBoard(self, obj): #function that closes this oppup and opens an input window for creating new board

        self.dismiss() #close this function
        createBoard(self.tempNewBoardName.text) #open new popup


class confirmBoardDeletionPopup(Popup):
    
    def deleteLoadedBoard(self): #run this code when Confirm button is pressed
        self.dismiss() #hide the confirmation popup
        deleteBoard(currentBoard.name) #delete the currently open board
        if len(Boards) != 0:
            loadBoard(Boards[0][1]) #display the first board in the boards array
        else:
            loadBoard(-1)


class noteEditingMenu(Popup): #menu with options to edit notes

    def confirmNoteDeletion(self): #confirm user wishes to delete note
        self.dismiss() #hide this menu
        self.confirmNoteDeletionPopup = confirmNoteDeletionPopup() #create variable with confirmNoteDeletionPopup popup
        self.confirmNoteDeletionPopup.open() #run confirmNoteDeletionPopup box popup

    def displayNoteContentPopup(self):
        self.dismiss() #hide this menu
        self.noteContentPopup = noteContentPopup() #create variable that stores instance of noteContentPopup class
        self.noteContentPopup.open() #run confirmation box popup

    def changeNoteTitlePopup(self):
        self.dismiss() #hide this menu
        self.changeNoteTitlePopup = changeNoteTitlePopup() #create variable that stores instance of noteContentPopup class
        self.changeNoteTitlePopup.open() #run confirmation box popup

    def changeNoteDeadlinePopup(self):
        self.dismiss() #hide this menu
        self.changeNoteDeadlinePopup = changeNoteDeadlinePopup() #create variable that stores instance of changeNoteDeadlinePopup class
        self.changeNoteDeadlinePopup.open() #open changeNoteDeadlinePopup popup

    def removeNoteDeadlinePopup(self):
        self.dismiss() #hide this menu
        self.confirmDeadlineRemovalPopup = confirmDeadlineRemovalPopup() #create variable that stores instance of changeNoteDeadlinePopup class
        self.confirmDeadlineRemovalPopup.open() #open changeNoteDeadlinePopup popup

class confirmNoteDeletionPopup(Popup): #confirmation box that user wishes to delete a note

    def deleteSelectedNote(self): #function run when confirmation button pressed
        self.dismiss()  #hide this popup
        deleteNote(currentEditedNote) #delete current edited note


class noteContentPopup(Popup): #text box for user to input note content
    
    def on_open(self): #run when note created

        for note in range(0, len(currentBoardNotes)): #loop through every note
            if currentBoardNotes[note].title == currentEditedNote: #look for array index that contains note information
                self.boxText = currentBoardNotes[note].content #load the content flag of this into a variable
                break

        self.tempNoteContent = TextInput( #create text input box with following parameters
            text = self.boxText, #content that is already in note is put into text box
            multiline = True,
            size_hint = (0.2, 0.8),
            )

        confirmButton = Button( #create button with following parameters
            text = "Edit Content",
            font_name = 'Roboto',
            font_size = 22,
            size_hint = (0.2, 0.2),
            on_press = self.commitNoteContent
        )

        self.ids.popupContent.add_widget(self.tempNoteContent) #add text input box to popup
        self.ids.popupContent.add_widget(confirmButton) #add confirmation box to popup

    def commitNoteContent(self, obj): #run when confirmation button pressed
        self.dismiss() #hide current note
        addNoteContent(currentEditedNote, self.tempNoteContent.text) #add content to note
        

class changeNoteTitlePopup(Popup): #popup that allows user to change title of note
    
    def on_open(self): #when popup is opened

        self.tempNewNoteTitle = TextInput( #create text input box with following parameters
            text = "", 
            multiline = False,
            size_hint = (0.2, None),
            height = 30,
            )

        self.confirmButton = Button( #create button with following parameters
            text = "Change note title",
            font_name = 'Roboto',
            font_size = 22,
            on_press = self.changeNoteTitle
        )

        self.ids.popupContent.add_widget(self.tempNewNoteTitle) #add text input box to popup
        self.ids.popupContent.add_widget(self.confirmButton) #add confirmation box to popup

    def changeNoteTitle(self, obj): #function to be run when confirmButton is pressed
        self.dismiss() #hide this popup
        editNoteTitle(currentEditedNote, self.tempNewNoteTitle.text) #run editNoteTitle function using text input


class changeNoteDeadlinePopup(Popup):
    
    def addDeadline(self):

        try: #try to set current date and time as datetime objects - if date or time is invalid, run except function
            
            self.inputDate = datetime.date(int(self.ids.Year.text) + 2000, int(self.ids.Month.text), int(self.ids.Day.text)) #create datetime object of current date
            self.inputTime = datetime.time(int(self.ids.Hour.text), int(self.ids.Minute.text), datetime.datetime.now().time().second, datetime.datetime.now().time().microsecond) #create datetime object of current time
            
            self.validateDateTime()

        except:

            self.dismiss() #hide this popup
            self.runInvalidDeadlinePopup() #open invalid data popup

    def validateDateTime(self):

        self.currentDate = datetime.datetime.now().date() #get current date
        self.currentTime = datetime.datetime.now().time() #cet current time


        if self.currentDate == self.inputDate: #if the current date and input date are the same....

            if self.currentTime <= self.inputTime: #a check needs to be done on the time input, to check the time input isn't less than the current time

                addNoteDeadline(currentEditedNote, (str(self.inputDate), str(self.inputTime)))

            else:
            
                self.dismiss() #hide this popup
                self.runInvalidDeadlinePopup() #open invalid data popup

        elif self.currentDate <= self.inputDate:  #check that the current date is less than the input date

                addNoteDeadline(currentEditedNote, (str(self.inputDate), str(self.inputTime)))

        else:

            self.dismiss() #hide this popup
            self.runInvalidDeadlinePopup() #open invalid data popup

        self.dismiss() #hide this popup

    def runInvalidDeadlinePopup(self):

        self.dismiss() #hide this popup
        self.invalidDeadlinePopup = invalidDeadlinePopup() #create instance of invalidDeadlinePopup popup
        self.invalidDeadlinePopup.open() #open instance of invalidDeadlinePopup popup


class invalidDeadlinePopup(Popup): #popup that appears if an invalid deadline is input
    
    def closePopup(self): #run on press of button
        self.dismiss() #hide popup


class confirmDeadlineRemovalPopup(Popup): #popup that appears to confirm deletion of deadline
    
    def removeDeadline(self): #function to be run when confirmation button is pressed
        
        self.dismiss() #hide this popup
        removeNoteDeadline(currentEditedNote) #remove deadline from note


NoteApp().run()
            