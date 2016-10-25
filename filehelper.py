f = open("timesData.csv", 'r')
pts = open("universities.points", 'w')
lbls = open("universities.labels", 'w')
meta = open("metadata.txt", 'w')

ct = 0
max_num_students = 0
max_stud_staff_ratio = 0.0
for line in f.readlines():
	csplit = line.rstrip().split(',')
	if csplit[0] == "world_rank":
		continue
	else:
		new_line = []
		skip_until = 0
		for i in range(len(csplit)):
			if i <= skip_until:
				continue
			if '"' in csplit[i]:
				new_elt = csplit[i]
				j = i+1
				while '"' not in csplit[j]:
					j += 1
				new_elt = "".join(csplit[i:j+1]).strip('"')
				new_line.append(new_elt)
				skip_until = j
			else:
				new_line.append(csplit[i])

		try:
			num_students = int(new_line[len(new_line)-5])
			student_staff_ratio = float(new_line[len(new_line)-4])
			if num_students > max_num_students:
				max_num_students = num_students
			if student_staff_ratio > max_stud_staff_ratio:
				max_stud_staff_ratio = student_staff_ratio
		except:
			continue

meta.write("max_num_students: %d\n" % (max_num_students))
meta.write("max_stud_staff_ratio: %f\n" % (max_stud_staff_ratio))

f.close()
f = open("timesData.csv", 'r')

for line in f.readlines():
	csplit = line.rstrip().split(',')
	if csplit[0] == "world_rank":
		continue
	else:
		new_line = []
		skip_until = 0
		for i in range(len(csplit)):
			if i <= skip_until:
				continue
			if '"' in csplit[i]:
				new_elt = csplit[i]
				j = i+1
				while '"' not in csplit[j]:
					j += 1
				new_elt = "".join(csplit[i:j+1]).strip('"')
				new_line.append(new_elt)
				skip_until = j
			else:
				new_line.append(csplit[i])
		try:
			num_students = float(new_line[len(new_line)-5])/max_num_students
			student_staff_ratio = 1.0 - (float(new_line[len(new_line)-4])/max_stud_staff_ratio)
			name = new_line[0]
			teaching_score = float(new_line[2])/100
			tot_score = new_line[len(new_line)-6]
			lbls.write(name+"\n")
			try:
				tot_score = float(tot_score)/100
			except:
				tot_score = teaching_score
			pts.write(str(tot_score) +" "+ str(num_students) +" "+ str(student_staff_ratio) + "\n")
		except:
			continue

f.close()
pts.close()
lbls.close()
meta.close()
