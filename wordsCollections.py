from config import BOT_NAME

TRIGGERS = {BOT_NAME.lower(), f'{BOT_NAME}'}

greetMessages = [
    f"Hello, Vlady. {BOT_NAME} is online and ready to serve!",
    "Greetings, Vlady. How can I assist you today?",
    "Welcome back, Vlady. It's good to hear you again.",
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
    'make a screenshot'         : 'takeScreenshot click clack',
    'write the text'            : 'writeTheNote alright , what do you want to   write? ',
    'write the notes'           : 'writeTheNote alright , what do you want to   write? ',
    'make system sleep'         : 'sleepComputer ok, preparing system to sleep',
    'turn computer off'         : 'offPc ok, preparing to turn off PC',
    'show me the weather'       : 'getCurrentWeather allright, im checking...',
    'what is the weather outside' : 'getCurrentWeather one moment, fetching...',
    'hey, '                     : 'passive greetings, i am ready to serve',
    'are you there'             : 'passive yes, im here',
    'i need your help!'         : 'passive yes, master? how can i help?',
    'how are you doing'         : 'passive just working in background',
    'hello'                     : 'passive hello, sir, what would u like me to do ?',
    'who is Natalia'            : 'showNatalia she is a director of Backend on S2S, but she is lazy as hell',
    'tell me more about Natalia': 'passive she dont like Penises in chat of KRYSY, and she can make you gloves ',
    'who is my best friend?'    : 'passive he is troll',
    'what is his name?'         : 'passive Val, Valera the badminton champion who dont like fat liashki',
    'stop working'              : 'offBot all right, im doing, good bye!',
    'shut down yourself'        : 'offBot oy kay im doing, see you!',
    'restart yourself'          : 'restartBot oy kay im preparing to restart, be right back!',
    'restart bot'               : 'restartBot yes im restarting, tou will not miss me',
    'mute yourself'             : 'muteBot',
    'mute mode'                 : 'muteBot',
    'activate sound'            : 'unmuteBot',
    'speak mode'                : 'unmuteBot',
    'ask chatGPT'               : 'askGPT what do you want to know?',
    'i have a question'         : 'askGPT what are you interested in?',

}

# check doble recognising
# make Evernote api
# check askGpt
# make Extrime abort function