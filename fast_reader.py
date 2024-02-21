import string

class Fastify_Reader:
	'''
	Class to implement the fastify Fast Reader. The intention is to enable the users to 
	read text faster by bolding some parts of the words.
	'''
	def __init__(self, text: str):
		self.text = text
		self.offset_factor = 1.6
	
	def _get_offset(self, word: str):
		'''
		Getting the offset for the word
		'''
		word_stripped = word.translate(str.maketrans('', '', string.punctuation))
		offset = int(len(word_stripped) / self.offset_factor)
		offset_value = offset if offset != 0 else 1
		return offset_value
	
	def fastify_word(self, word: str):
		if '-' in word:
			part_1, part_2 = word.rsplit('-', 1)
			part_1 = f"**{part_1[:self._get_offset(part_1)]}**{part_1[self._get_offset(part_1):]}"
			part_2 = f"**{part_2[:self._get_offset(part_2)]}**{part_2[self._get_offset(part_2):]}"
			fastify_word = f"{part_1}-{part_2}"
		else:
			fastify_word = f"**{word[:self._get_offset(word)]}**{word[self._get_offset(word):]}"
		return fastify_word
	
	def fastify_line(self, line: str):
		fastify_line = ""
		for word in line.split():
			fastify_line += f"{self.fastify_word(word)} "
		return fastify_line.strip()
	
	def fastify(self):
		'''
		Triggering the Fastify Logic
		'''
		fastify_text = ""
		for line in self.text.split('\n'):
			fastify_text += f"{self.fastify_line(line)}\n"
		fastify_text = fastify_text.replace("****","")
		return fastify_text.strip()
