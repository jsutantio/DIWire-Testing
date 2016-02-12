#Test file for running python
#practice for Jess to get reacquainted

text = 'We all live in a Yellow Submarine. A Big Paper is Due.'

def repeatCaps(text):
	uppers = ""
	for word in text:
		for letter in word:
			if letter.isupper():
				uppers += letter
	return uppers

print repeatCaps(text)
