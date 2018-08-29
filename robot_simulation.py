class Position:
	# x and y position
	DEF_POS = 0

	MIN_POS = 0
	MAX_POS = 4

	# facing position
	DEF_F_POS = 'NORTH'

	FACE_LIST = ['NORTH', 'SOUTH', 'EAST', 'WEST']

	F_NORTH = 'NORTH'
	F_SOUTH = 'SOUTH'
	F_EAST = 'EAST'
	F_WEST = 'WEST'

	def __init__(self):
		self.set_def_position()

	def get_x_position(self):
		return self.x_pos

	def get_y_position(self):
		return self.y_pos

	def get_f_position(self):
		return self.f_pos.upper()

	def set_def_position(self):
		self.x_pos = self.DEF_POS
		self.y_pos = self.DEF_POS
		self.f_pos = self.DEF_F_POS

	def set_x_position(self, x_pos):
		self.x_pos = int(x_pos)

	def set_y_position(self, y_pos):
		self.y_pos = int(y_pos)

	def set_f_position(self, f_pos):
		self.f_pos = f_pos.upper()

	def validate_place_position(self, x_pos, y_pos, f_pos):
		x_pos = int(x_pos)
		y_pos = int(y_pos)

		if x_pos < 0 or x_pos > 4:
			print('X position should be between 0 - 4')
			return False

		if y_pos < 0 or y_pos > 4:
			print('Y position should be between 0 - 4')
			return False

		if not f_pos.upper() in self.FACE_LIST:
			print('Face position shoud be NORTH, EAST, SOUTH, and WEST')
			return False

		return True

	def move_to_front(self):
		if self.f_pos == self.F_NORTH:
			self.set_y_position(self.y_pos + 1)
			return

		if self.f_pos == self.F_SOUTH:
			self.set_y_position(self.y_pos - 1)
			return

		if self.f_pos == self.F_EAST:
			self.set_x_position(self.x_pos + 1)
			return

		if self.f_pos == self.F_WEST:
			self.set_x_position(self.x_pos - 1)
			return

	def check_front(self):
		# check if robot can move forward. 
		if self.f_pos == self.F_NORTH and self.y_pos + 1 > self.MAX_POS:
			return False

		if self.f_pos == self.F_SOUTH and self.y_pos - 1 < self.MIN_POS:
			return False	

		if self.f_pos == self.F_EAST and self.x_pos + 1 > self.MAX_POS:
			return False

		if self.f_pos == self.F_WEST and self.x_pos - 1 < self.MIN_POS:
			return False

		return True

	def rotate_left(self):
		if self.f_pos == self.F_NORTH:
			self.set_f_position(self.F_WEST)
			return

		if self.f_pos == self.F_SOUTH:
			self.set_f_position(self.F_EAST)
			return

		if self.f_pos == self.F_EAST:
			self.set_f_position(self.F_NORTH)
			return

		if self.f_pos == self.F_WEST:
			self.set_f_position(self.F_SOUTH)
			return

	def rotate_right(self):
		if self.f_pos == self.F_NORTH:
			self.set_f_position(self.F_EAST)
			return

		if self.f_pos == self.F_SOUTH:
			self.set_f_position(self.F_WEST)
			return

		if self.f_pos == self.F_EAST:
			self.set_f_position(self.F_SOUTH)
			return

		if self.f_pos == self.F_WEST:
			self.set_f_position(self.F_NORTH)
			return


class Command:
	#commands
	COMMAND_LIST = ['PLACE', 'MOVE', 'LEFT', 'RIGHT', 'REPORT']

	COMM_PLACE = 'PLACE'
	COMM_MOVE = 'MOVE'
	COMM_LEFT = 'LEFT'
	COMM_RIGHT = 'RIGHT'
	COMM_REPORT = 'REPORT'

	def __init__(self, position):
		self.position = position	

	def verify_command(self, command):
		try:
			comm_array = command.split(' ')
			comm = comm_array[0].upper()

			if not comm in self.COMMAND_LIST:
				print('Command not found.')
				raise Exception

			if comm == self.COMM_PLACE:
				params = comm_array[1].split(',')

				if len(params) != 3:
					print("Expecting 3 parameters separated by ','. e.g., PLACE X,Y,F")
					raise Exception

				if not self.position.validate_place_position(params[0], params[1], params[2]):
					raise Exception
					
			return True
		except Exception:
			return False

	def execute(self, command):
		comm_array = command.split(' ')
		comm = comm_array[0].upper()

		if comm == self.COMM_PLACE:
			params = comm_array[1].split(',')
			self.position.set_x_position(params[0])
			self.position.set_y_position(params[1])
			self.position.set_f_position(params[2].upper())	
			return

		if comm == self.COMM_MOVE:
			if self.position.check_front():
				self.position.move_to_front()
			return

		if comm == self.COMM_LEFT:
			self.position.rotate_left()
			return

		if comm == self.COMM_RIGHT:
			self.position.rotate_right()
			return

		if comm == self.COMM_REPORT:
			print(str(self.position.get_x_position()) + ',' + str(self.position.get_y_position()) + ',' + str(self.position.get_f_position()))
			return


import sys

def main():
	position = Position()
	command = Command(position)

	try: # run commands in the file accepted as an argument.
		file = open(sys.argv[1], "r")

		if file.mode == 'r':
			contents = file.readlines()

			for content in contents:
				content = content.rstrip() # remove newlines

				if command.verify_command(content):
					command.execute(content)
	except: # accept commands if there is no argument submitted.
		while True:
			input_comm = input('Enter command: ')

			if command.verify_command(input_comm):
				command.execute(input_comm)
		

if __name__ == '__main__':
	main()