#!/usr/bin/env python3
import sys
import random
import argparse

def contains_only(str, chars):
	for c in str:
		if c not in chars:
			return False

	return True


def generate(wordlist, args):
	for _ in range(args.amount):
		skipped = 0

		while skipped < 100:
			if skipped > 0:
				print("skipped")

			pw = generate_password(wordlist, args)

			if len(pw) < args.minlen:
				skipped += 1
				continue

			if len(pw) > args.maxlen:
				skipped += 1
				continue

			yield pw
			break

		if skipped == 100:
			print("ERROR: Could not generate a valid password 100 times in a row")
			sys.exit(1)


def generate_password(wordlist, args):
	password = ""
	next_random = False

	for c in args.format:
		if next_random:
			if bool(random.getrandbits(1)):
				continue

			next_random = False

		if c == "w":
			password += random.choice(wordlist).title()
		elif c == "n":
			password += random.randint(0, 9)
		elif c == "s":
			password += random.choice(args.symbols)
		else:
			next_random = True

	return password


def main(args):
	if args.amount <= 0:
		print("ERROR: You need to generate at least one password!")
		sys.exit(1)

	if args.minlen > args.maxlen:
		print("ERROR: Min length is greater than the max length")
		sys.exit(1)

	if len(args.format) <= 0:
		print("ERROR: Please provide a format. See help for more information")
		sys.exit(1)

	if not contains_only(args.format, ['w', 'n', 's', '?']):
		print("ERROR: Format is incorrect. See help for more information")
		sys.exit(1)

	if args.seed:
		random.seed(args.seed)

	try:
		wordlist = []

		with open(args.wordlist) as f:
			for line in f:
				wordlist.append(line.rstrip())
	except FileNotFoundError:
		print('ERROR: Wordlist file not found')
		sys.exit(1)

	random.shuffle(wordlist)

	for password in generate(wordlist, args):
		print(password)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='pwgen')

	parser.add_argument('wordlist', help='input wordlist')
	parser.add_argument('format', help='password format. w = word; n = number; s = symbol; ? = optional')

	parser.add_argument('--symbols', help='symbols to use', type=list, default='!@$^*().,;')
	parser.add_argument('--amount', help='amount of passwords to generate', type=int, required=True)
	parser.add_argument('--minlen', help='min password length', type=int, default=7)
	parser.add_argument('--maxlen', help='max password length', type=int, default=20)

	parser.add_argument('--seed', help='seed for randomness')

	main(parser.parse_args())