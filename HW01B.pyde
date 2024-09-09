class FadingWord:
    # this serves as the constructor method, always executed when the class is being initiated
    def __init__(self, _word, _wordDelay):
        # self serves as the current instance of the class
        self.word = _word # word stored 
        self.alpha = 255 # transparency of the word
        self.startTime = millis() # time created 
        self.letterDelay = _wordDelay / len(self.word) # letter delay time based on the word length

        self.red = 0 # red component of the word color
        self.font = "sans-serif"
        self.size = minTextSize 
        self.yOffset = 0 # offset the word vertically
        self.fadeVel = -0.3 # fading speed
        
        if self.word.lower() == "glitch" or random(1) > 0.95: 
            self.word = self.word.upper()
            self.red = 200
            self.font = "monospace"
            self.size = maxTextSize
            self.yOffset = -self.size / 6
            self.fadeVel = -0.01

        # textFont() sets the current font that will be drawn with the text() function
        # createFont() creates the fonts before they can be used
        textFont(createFont(self.font, self.size))

        self.width = textWidth(self.word) # pixel width of the word

        global cx, cy
        # update cx and cy and set this.x and this.y
        # if placing the next word on this line causes overflow
        if cx + textWidth(self.word) > width - MARGIN:
            # reset x, increment y
            cx = MARGIN
            cy += lineHeight
            
            # if larger than canvas
            if cy > height - MARGIN:
                cy = MARGIN

        self.x = cx
        self.y = cy

        # update cx for next word
        cx += self.width + spaceWidth

    def update(self):
        self.alpha += self.fadeVel

    def draw(self):
        elapsed = millis() - self.startTime # time since the word was created
        lastLetter = min(int(elapsed / self.letterDelay), len(self.word)) # how many letter should display
        letters = self.word[:lastLetter] # slicing [start:end]

        fill(self.red, 0, 0, self.alpha)
        textFont(createFont(self.font, self.size))

        text(letters, self.x, self.y + self.yOffset)

phrase = ("Glitch is something that extends beyond the most literal technological mechanics: it helps us to celebrate failure as a generative force, a new way to take on the world.")

MARGIN = 40

words = []
drawnWords = []

wordCount = 0
nextUpdateMillis = 0

minTextSize = 20
maxTextSize = 30

cx = 0
cy = 0

spaceWidth = 0
lineHeight = 0

def setup():
    global cx, cy, spaceWidth, lineHeight

    size(displayWidth, displayHeight)
    words.extend(phrase.split(" ")) # use space as the delimiter to split all the words from phrase
    
    cx = MARGIN
    cy = MARGIN

    textAlign(LEFT, TOP)
    textFont(createFont("sans-serif", minTextSize))
    textSize(minTextSize)

    spaceWidth = textWidth(" ")
    lineHeight = 1.5 * minTextSize

# returns true or false depending on if a word is still visible
def isVisible(fw):
    return fw.alpha > 0

def draw():
    global wordCount, nextUpdateMillis, drawnWords

    background(220)

    # filter(function, sequence)
    drawnWords = filter(isVisible, drawnWords)

    # iterate over drawn words, update and draw them
    for nextWord in drawnWords:
        nextWord.update()
        nextWord.draw()

    # check if it's time to add a new FadingWord to array
    if millis() > nextUpdateMillis:
        nextWordIndex = wordCount % len(words)
        nextWord = words[nextWordIndex]

        # add new word to array
        wordDelay = random(450, 600)
        drawnWords.append(FadingWord(nextWord, wordDelay))

        # always increment the word count
        wordCount += 1

        # next update time in millis, with some variation
        nextUpdateMillis = millis() + 1.2 * wordDelay
