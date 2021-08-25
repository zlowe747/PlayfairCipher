from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class MainLayout(GridLayout):
	encryptMode = BooleanProperty(True)
	replaceX = BooleanProperty(False)
	message = StringProperty('')
	changedMessage = StringProperty('')
	table = []
	tableText = StringProperty('')

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.createTable('')

	def toggleMode(self):
		self.encryptMode = not self.encryptMode
		self.encrypt() if self.encryptMode else self.encrypt(-1)

	def createTable(self, key):
		uniqueLetters = []
		key = key.upper().replace('J', 'I')
		for letter in key:
			if letter in letters and letter not in uniqueLetters:
				uniqueLetters.append(letter)
		for letter in letters:
			if letter not in uniqueLetters:
				uniqueLetters.append(letter)
		self.tableText = ''.join(uniqueLetters)
		self.table = [[], [], [], [], []]
		for i in range(0, 25):
			self.table[int(i / 5)].append(uniqueLetters[i])
		self.encrypt() if self.encryptMode else self.encrypt(-1)

	def setMessage(self, widget):
		self.message = widget.text
		self.encrypt() if self.encryptMode else self.encrypt(-1)
		
	def encrypt(self, modifier = 1):
		cleanMessage = self.message.upper().replace('J', 'I')
		decryptedPairs = []
		pair = ''
		for letter in cleanMessage:
			if letter in letters:
				if pair == '':
					pair += letter
				elif pair[0] == letter:
					pair += 'X'
					decryptedPairs.append(pair)
					pair = letter
				else:
					pair += letter
					decryptedPairs.append(pair)
					pair = ''
		if len(pair) == 1:
			pair += 'X'
			decryptedPairs.append(pair)

		encryptedPairs = []
		for dPair in decryptedPairs:
			x1 = y1 = x2 = y2 = 0
			ePair = ''
			for row in self.table:
				if dPair[0] in row:
					x1 = row.index(dPair[0])
					y1 = self.table.index(row)
				if dPair[1] in row:
					x2 = row.index(dPair[1])
					y2 = self.table.index(row)
			if x1 == x2:
				y1 = y1 + modifier
				if y1 > 4:
					y1 = 0
				elif y1 < 0:
					y1 = 4
				y2 = y2 + modifier
				if y2 > 4:
					y2 = 0
				elif y2 < 0:
					y2 = 4
			elif y1 == y2:
				x1 = x1 + modifier
				if x1 > 4:
					x1 = 0
				elif x1 < 0:
					x1 = 4
				x2 = x2 + modifier
				if x2 > 4:
					x2 = 0
				elif x2 < 0:
					x2 = 4
			if x1 == x2 or y1 == y2:
				ePair += self.table[y1][x1]
				ePair += self.table[y2][x2]
			else:
				ePair += self.table[y1][x2]
				ePair += self.table[y2][x1]
			encryptedPairs.append(ePair)
		
		self.changedMessage = ''.join(encryptedPairs)
	
	
class MainApp(App):
	pass


MainApp().run()
