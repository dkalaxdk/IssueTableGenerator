import PySimpleGUI as sg
import json
import gui_functions as gf

# on submit: First read all the stuff from the inputs, then validate it, then write the whole thing to a json config file
def on_submit(data):
  data['repositories'] = gf.csvToList(data['repositories'])
  with open('ConfigFile.json', 'w') as outfile:
    json.dump(data, outfile)

sg.theme('DarkAmber')  # No gray windows please!

# STEP 1 define the layout
layout = [ 
            [sg.Text('This is a very basic PySimpleGUI layout')],
            [sg.Text('Token'), sg.InputText(key='token')],
            [sg.Text('Repositories ( separated by commas)'), sg.InputText(key='repositories')],
            [sg.Text('From date ( year-month-day )'), sg.InputText(key='from_date')],
            [sg.Text('To date ( year-month-day )'), sg.InputText(key='to_date')],
            [sg.Text('State'), sg.InputText(key='state')],
            [sg.Text('Language'), sg.InputText(key='language')],
            [sg.Button('Ok'), sg.Button('Exit')]
         ]

#STEP 2 - create the window
window = sg.Window('My new window', layout, grab_anywhere=True)

# STEP3 - the event loop
while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'Ok':
      print('Creating configuration file')
      on_submit(values)
      break
window.close()
