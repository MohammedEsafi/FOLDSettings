import sqlite3
import os.path
import hashlib
import sys

usage = '''drive. keep your files in sync
usage: python drive.py push                sync your files to your locale database.
       python drive.py [options] restore   restore the files to your system.
       python drive.py -h --help           show this help message.
       python drive.py --version           show version.
options:
       -f --force   force every question asked to be answered with "Yes".
'''

query = {
	"CREATE": "CREATE TABLE IF NOT EXISTS 'Files' (realpath TEXT NOT NULL, content BLOB NOT NULL)",
	"INSERT": "INSERT INTO 'Files' (realpath, content) VALUES (?, ?)",
	"UPDATE": "UPDATE 'Files' SET content = ? WHERE realpath = ?",
	"SELECT": "SELECT * FROM 'Files'",
	"GET": "SELECT * FROM 'Files' WHERE realpath = ?"
}

class style: 
	reset='\033[0m'
	bold='\033[01m'
	disable='\033[02m'
	italic='\033[03m'
	underline='\033[04m'
	strikethrough='\033[09m'
	red='\033[31m'
	green='\033[32m'
	yellow='\033[33m'
	light_yellow='\033[93m'

def reader(filename):
	# convert digital data to binary format
	with open(filename, 'rb') as file:
		blob = file.read()
	return blob

def writer(content, filename):
	# convert binary data to proper format and write it on file
	with open(filename, 'rb') as file:
		md5Checksum = hashlib.md5(file.read()).hexdigest()
	with open(filename, 'wb') as file:
		if md5Checksum != hashlib.md5(content).hexdigest():
			file.write(content)

def opt(argv):
	options = ['push', 'restore', '--help', '--version', '--force', '-h', '-f']
	args = dict()
	for item in options:
		if item in argv:
			args[item] = True
		else:
			args[item] = False
	return (args)

def main():
	# get the command line args
	argv = sys.argv
	args = opt(argv)

	# usage
	if args["--help"] or args["-h"] or (len(argv) - 1 == 0):
		print(usage, end='')
		sys.exit(0)

	# --version opt
	if args["--version"]:
		print('v1.0.0')
		sys.exit(0)

	# if we want to answer drive with "yes" for each question
	if args["--force"] or args["-f"]:
		__FORCE = True
	else:
		__FORCE = False

	database = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale.db')

	# connect to the database
	connection = sqlite3.connect(database)
	if connection is None:
		print("Error! cannot create the database connection.")
		sys.exit(0)

	# instantiate a cursor obj
	cursor = connection.cursor()

	# get user home directory to shorten paths
	if args["push"] or args["restore"]:
		user = os.path.expanduser('~')

	# baCkup (push opt)
	if args["push"]:
		# create Files table if not exists
		cursor.execute(query["CREATE"])

		# read `~/.config.ini` file containing full path of source files to backup
		source_paths = None
		with open(os.path.expanduser('~/.config.ini'), 'r') as file:
			source_paths = file.read().splitlines()

		source_paths = list(os.path.expanduser(item).rstrip('/') for item in source_paths[1:])

		# push files
		for item in source_paths:
			relpath = "~/" + os.path.relpath(item, user)
			error = "{}{}‣{} {}{}{}{}".format(style.bold, style.red, style.reset, style.italic, style.strikethrough, relpath, style.reset)
			if not os.path.exists(item):
				print(error)
			elif os.path.isdir(item):
				print(error)
			else:
				try:
					cursor.execute(query["GET"], tuple([item]))
					record = cursor.fetchone()

					content = reader(item)
					if record is None:
						cursor.execute(query["INSERT"], tuple([item, content]))
					else:
						cursor.execute(query["UPDATE"], tuple([content, item]))
				except:
					# Failed to insert FILES into sqlite table
					print(error)
				else:
					connection.commit()
					# Files inserted successfully as a BLOB into a table
					print("{}{}‣{} {}{}{}".format(style.bold, style.green, style.reset, style.italic, relpath, style.reset))

	# restore opt
	elif args["restore"]:
		try:
			cursor.execute(query["SELECT"])
			record = cursor.fetchall()
			for realpath, content in record:
				if not __FORCE:
					relpath = "~/" + os.path.relpath(realpath, user)
					print("{}{}?{} Do you want to replace {}{}{}{} with the newer one you're restart? {}(Y/N){} "\
					.format(style.bold, style.green, style.reset, style.italic, style.yellow, relpath, style.reset, style.disable, style.reset), end="")
					response = input()
				if __FORCE or response == 'Y' or response == 'y':
					dirname = os.path.dirname(realpath)
					if not os.path.exists(dirname):
						os.makedirs(dirname, exist_ok=True)
					writer(content, realpath)
		except sqlite3.Error as error:
			# Failed to restore the FILES to your system
			print("{}{}!{} Failed to restore the FILES to your system".format(style.bold, style.red, style.reset))
			print("  {}Error:{} {}".format(style.red, style.reset, error))

	else:
		print(usage, end='')

	if connection:
		connection.close()
		print("{}{}i{} The sqlite connection is closed.".format(style.bold, style.green, style.reset))

if __name__ == '__main__':
	main()
