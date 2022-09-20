import string
import random

class PasswordGenerator:
	
	alphabets = list(string.ascii_letters)
	digits = list(string.digits)
	special_characters = list("!@#$%^&*()")
	characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

	@staticmethod
	def generate_random_password(password_length: int, alphabets_count: int, digits_count: int, special_characters_count: int):
		characters_count = alphabets_count + digits_count + special_characters_count

		password = []
		
		for i in range(alphabets_count):
			password.append(random.choice(PasswordGenerator.alphabets))
		
		for i in range(digits_count):
			password.append(random.choice(PasswordGenerator.digits))
		
		for i in range(special_characters_count):
			password.append(random.choice(PasswordGenerator.special_characters))

		if characters_count < password_length:
			random.shuffle(PasswordGenerator.characters)
			for i in range(password_length - characters_count):
				password.append(random.choice(PasswordGenerator.characters))

		random.shuffle(password)

		return str().join(password)