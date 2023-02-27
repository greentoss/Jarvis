from config import BOT_NAME

TRIGGERS = {BOT_NAME.lower(), f'{BOT_NAME}'}

greetMessages = [
    f"Hello, Vlady. {BOT_NAME} is online and ready to serve!",
    "Greetings, Vlady. How can I assist you today?",
    "Welcome back, Vlady. It's good to hear from you again.",
    "Hi there, Vlady. How may I be of assistance?",
    "Good day, Vlady. How can I help you?",
    "Hello again, Vlady. What can I do for you?",
    "Nice to see you again, Vlady. What can I assist you with?",
    "Howdy, Vlady. What do you need help with today?",
    "Hello, Vlady. I'm at your service. How can I assist you?",
    "Hey there, Vlady. What can I do for you today?"
]

phrases_printNote = [
    "All right, any other note?",
    "Okay, What else?",
    "Do you have any other notes?",
    "Ready for the next note."
]

data_set = {
    'open browser'              : 'chrome opening browser chrome',
    'open google'               : 'chromeGoogle yes i am opening google.com',
    'open chatGPT'              : 'chromeChatGPT yes i am opening chatGPT',
    'turn on browser'           : 'chrome just a moment, i am doing',
    'open telegram'             : 'openTelegram just a moment, opening telegram',
    'close telegram'            : 'closeTelegram yes, i am doing, closing telegram',
    'start OBS recording'       : 'startObsRecording just a moment, starting the OBS recording',
    'stop OBS recording'        : 'stopObsRecording just a moment, terminating the OBS recording',
    'make a screenshot'         : 'takeScreenshot click clack',
    'record the text'            : 'writeTheNote alright im doing, what do you want to   write? ',
    # 'make system sleep'       : 'sleepComputer ok, preparing to sleep',
    # 'what is the weather'     : 'checkWeather allright, im checking...',
    # 'what weather is outside' : 'checkWeather one moment, fetching...',
    'hey, '                     : 'passive yes, master',
    'are you there'             : 'passive hello, sir, what would u like me to do ?',
    'hey you!'                  : 'passive greetings, i am ready to serve',
    'how are you doing'         : 'passive just working in background',
    'hello'                     : 'passive yes ya im here',
    'what can you do?'          : 'passive well, i can speak, thats good, right? ok, i can unswer simple words, can turn on '
                                  'browser, can shutdown myself, can tell you my list of functionality, i guess thats all',
    'who is my best friend?'    : 'passive he is troll',
    'what is his name?'         : 'passive Val, Valera the badminton champion who dont like fat liashki',
    'stop working'              : 'offBot all right, im doing, good bye!',
    'shut down yourself'        : 'offBot oy kay im doing, see you!',
}
