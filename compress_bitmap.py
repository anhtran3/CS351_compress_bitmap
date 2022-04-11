# Anh Tran
# CS 351
# Homework 4

def create_index(input_file, output_path,sorted):
	f_input = open(input_file, "r")
	#open the input file to read

	f_output = output_path + input_file
	#create path for output file

	input_line = f_input.readline()
	input_list = []
	output_file = open(f_output, "w")
	if (sorted == 1):
		f_output += "_sorted"
		input_list.sort()

	if (sorted == 0):
		f_output += "_unsorted"

	while input_line != "":
		input_list.append(input_line)
		input_line = f_input.readline()
	

	for line in input_list:
		line = line.split(",")
		output_line = ""

		#4 bits for 4 animals
		if line[0] == "cat":
			output_line += "1000"
		elif line[0] == "dog":
			output_line += "0100"
		elif line[0] == "turtle":
			output_line += "0010"
		elif line[0] == "bird":
			output_line += "0001"

		# 10 bits for 10 bins of age
		if int(line[1]) <= 10:
			output_line += "1000000000"
		elif int(line[1]) <= 20:
			output_line += "0100000000"
		elif int(line[1]) <= 30:
			output_line += "0010000000"
		elif int(line[1]) <= 40:
			output_line += "0001000000"
		elif int(line[1]) <= 50:
			output_line += "0000100000"
		elif int(line[1]) <= 60:
			output_line += "0000010000"
		elif int(line[1]) <= 70:
			output_line += "0000001000"
		elif int(line[1]) <= 80:
			output_line += "0000000100"
		elif int(line[1]) <= 90:
			output_line += "0000000010"
		elif int(line[1]) <= 100:
			output_line += "0000000001"

		#2 bits for boolean values of adopted
		if line[2] == "True\n":
			output_line += "10"
		elif line[2] == "False\n": 
			output_line += "01"

		output_line += "\n"
		output_file.write(output_line)

	f_input.close()
	output_file.close()

def compress_index(bitmap_index, output_path, compression_method, word_size):

	f_input = open(bitmap_index,"r")
	#open input file
	f_output = output_path + bitmap_index + "_" + compression_method + "_" + str(word_size)
	#create output path
	my_output = open(f_output, "w")

	size = word_size - 1
	num_run = 0
	num_literal = 0
	run_count = 0
	input_list = []
	for i in range(16):
		input_list.append("")

	input_line = f_input.readline()
	while input_line != "":

		for i in range(0,16):
			input_list[i] += input_line[i] #transpose every chunk 
		input_line = f_input.readline()

	if compression_method == "WAH":
		for col in input_list:  
			output_line = ""
			position = 0    #keep track the position we are

			while position + size < (len(col)+1): 
			#whie the leftover chunks fit one word
					word = col[position: (position + size)]   
					#pick a word
					if ((word == ("0" * (size))) or (word == ("1" * size))): 
					#check if the word is run of either 0s or 1s
						previous = word 
						#store current word as a reference for future
						run_count = 1   
						num_run += 1
						position += size  
						#move the position forwawrd
						word = col[position:position+ size]   
						 #pick the next word
						 
						while ((previous == word) and (run_count != (2^(word_size-2)-1))): 
						#if this new word is the same run as previous and run not full
							position += (size)   #move the head up
							run_count+= 1  
							num_run += 1
							
							if position+size >= len(col)+1:   
							#break if the leftover bits aren't enough to compress
								break
							else:  
								word = col[position:position+size]    
								#moving to next word
						run_type = previous[0]   
						#check if it's a run of 0s or 1s
						fill = format(run_count, "b")    
						#convert to a binary string
						while len(fill) < (word_size-2):  
						#if the leftover chunk doesn't fit
							fill = "0" + fill
							#fill the rightmost leftover with 0s
						output_line += "1" + run_type + fill 

					else:   
					#if the word is a literal
						position += size
						num_literal += 1
						output_line += "0" + word
						
			if col[position] != "\n":
				last = "0" + col[position:]
				num_literal += 1
				while len(last) < word_size:
					last += "0"
				output_line += last
			output_line += "\n"
			my_output.write(output_line)
			#output to a file

	print("Total runs: ", str(num_run))
	print("Total literals: ", str(num_literal))


# def main():

# 	create_index("animals_small.txt","/Users/anhtran/Desktop/CS351/output/", False)

# 	compress_index("animals.txt_sorted", "/Users/anhtran/Desktop/CS351/output/", "WAH", 16 )

# if __name__ == "__main__":
# 	main()
