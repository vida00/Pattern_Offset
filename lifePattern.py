#!/usr/bin/env python3
# based on: https://github.com/ickerwx/pattern/blob/master/pattern

import struct, sys

def grey(str): print('\033[1;90m'+str+'\033[0;0m')

def pattern_create(lenght):
	if not isinstance(lenght, int):	
		lenght = int(lenght, 10)

	pattern = '' 
	charset = ['A', 'a', '0']

	while len(pattern) != lenght:
		pattern += charset[len(pattern) % 3]

		if len(pattern) % 3 == 0:
			charset[2] = chr(ord(charset[2]) + 1)

			if charset[2] > '9':
				charset[2] = '0'
				charset[1] = chr(ord(charset[1]) + 1)
				
				if charset[1] > 'z':
					charset[1] = 'a'
					charset[0] = chr(ord(charset[1]) + 1)
				
					if charset[0] > 'Z':
						charset[0] = 'A'
	return pattern

def pattern_offset(value, lenght, arch):
	sub = False
	if value.startswith('0x'):
		try:
			if arch == 'x32':
				value = struct.pack('<I', int(value, 16)).decode('utf-8')
				sub = True
		except ValueError:
			grey('unknow format')
			sys.exit(1)

	if arch == 'x32': 
		arch = int(4)
		if(sub):
			arch = int(0)
	if arch == 'x64':
		arch = int(0)

	pattern = pattern_create(lenght)

	try:
		return pattern.index(str(value)) - arch
	except ValueError:
		grey('not found')
		sys.exit(1)

def help(): 
	grey('''
		create - create pattern
		offset - find offset

		example: create 50
		example: offset Aa1 50 x64 | x32
		example: offset 0x4141 50 x32
		obs: find offset with hex is only x32 architecture

		extra: copy - copy to transfer area
		example: create 50 copy
		obs: dependencie - clipboard ; pip3 install clipboard
		
	''')
	sys.exit(1)

def main():
	if len(sys.argv) <= 2 or sys.argv[1].lower() not in ['create', 'offset']:
		help()

	option = sys.argv[1].lower()

	if option == 'create':
		lenght = sys.argv[2]
		pattern = pattern_create(lenght)
		if len(sys.argv) == 4 and sys.argv[3].lower() == 'copy':
			import clipboard
			clipboard.copy(pattern)
		grey(pattern)

	elif option == 'offset':
		if len(sys.argv) != 5: help()

		value = sys.argv[2]
		lenght = sys.argv[3]
		arch = sys.argv[4]

		if str(arch) not in ['x32', 'x64']:
			help()

		offset = pattern_offset(value, lenght, arch)
		grey(str(offset))

if __name__ == '__main__':
	main()
