#Tayja Phillips
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator."""
print("=" * 50)
FILE_NAME = "STUDENT_GRADES.TXT"
print("=" * 50)

class Student:
	"""A student and the scores used to calculate a final grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test_scores = [test1, test2, test3]
		self.average = sum(self.test_scores) / len(self.test_scores)
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		scores = "|".join(f"{score:.2f}" for score in self.test_scores)
		return f"{self.name}|{self.student_id}|{scores}|{self.average:.2f}|{self.grade}"

	@classmethod
	def from_file_line(cls, line):
		parts = line.strip().split("|")
		if len(parts) != 7:
			raise ValueError("record must contain 7 pipe-delimited fields")
		student = cls(parts[0], parts[1], float(parts[2]), float(parts[3]), float(parts[4]))
		if abs(student.average - float(parts[5])) > 0.01 or student.grade != parts[6]:
			raise ValueError("record contains incorrect calculated values")
		return student


def save_students(students):
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line() + "\n")
		print(f"✓ Saved {len(students)} student record(s) to file.")
	except OSError as error:
		print(f"Unable to save student records: {error}")


def save_and_exit(students):
	print("Saving Records...")
	save_students(students)


def load_students():
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				if not line.strip():
					continue
				try:
					students.append(Student.from_file_line(line))
				except (ValueError, IndexError) as error:
					print(f"Skipped invalid record on line {line_number}: {error}")
		print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
	except FileNotFoundError:
		print(f"No existing {FILE_NAME} file found. Starting with an empty record list.")
	except OSError as error:
		print(f"Unable to load student records: {error}")
	return students


def prompt_text(message):
	value = input(message).strip()
	if value == "\x1b":
		raise KeyboardInterrupt
	return value


def prompt_score(test_number):
	while True:
		value = prompt_text(f"Test {test_number} score (0-100): ")
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\n" + "=" * 50)
	print("ADD NEW STUDENT")
	print("=" * 50)
	try:
		name = prompt_text("Student name: ")
		student_id = prompt_text("Student ID: ")
		if not name or not student_id:
			print("Name and student ID are required.")
			return
		if "|" in name or "|" in student_id:
			print("Name and student ID cannot contain the pipe character (|).")
			return
		scores = [prompt_score(number) for number in range(1, 4)]
		students.append(Student(name, student_id, *scores))
		student = students[-1]
		print(f"Added {name}. Average: {student.average:.2f}, Grade: {student.grade}")
	except KeyboardInterrupt:
		print("\nAdd student cancelled.")


def display_students(students):
	if not students:
		print("No student records to display.")
		return
	header = f"{'Name':<22} {'ID':<14} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>5}"
	print("\n" + header)
	print("-" * len(header))
	for student in students:
		print(
			f"{student.name:<22.22} {student.student_id:<14.14} "
			f"{student.test_scores[0]:>8.2f} {student.test_scores[1]:>8.2f} "
			f"{student.test_scores[2]:>8.2f} {student.average:>9.2f} {student.grade:>5}"
		)


def display_statistics(students):
	print("\n" + "=" * 50)
	print("CLASS STATISTICS")
	print("=" * 50)
	if not students:
		print("No student records available for statistics.")
		return
	averages = [student.average for student in students]
	class_average = sum(averages) / len(averages)
	highest_average = max(averages)
	lowest_average = min(averages)
	highest_students = [student.name for student in students if student.average == highest_average]
	lowest_students = [student.name for student in students if student.average == lowest_average]
	grade_counts = {grade: 0 for grade in "ABCDF"}
	for student in students:
		grade_counts[student.grade] += 1

	print(f"Class average:   {class_average:.2f}")
	print(f"Highest average: {highest_average:.2f} ({', '.join(highest_students)})")
	print(f"Lowest average:  {lowest_average:.2f} ({', '.join(lowest_students)})")
	print()
	print("Grade Distribution:")
	for grade, count in grade_counts.items():
		print(f"{grade}: {count} student(s)")


def search_student(students):
	print("\n" + "=" * 50)
	print("SEARCH STUDENT")
	print("=" * 50)
	try:
		search_name = prompt_text("Enter student name to search: ").casefold()
	except KeyboardInterrupt:
		print("\nSearch cancelled.")
		return
	matches = [student for student in students if search_name in student.name.casefold()]
	if matches:
		display_students(matches)
	else:
		print("No student found with that name.")


def display_menu():
	print("\n" + "=" * 50)
	print("Student Grade Calculator")
	print("=" * 50)
	print("1. Add new student")
	print("2. Display All Students")
	print("3. Search student by Name")
	print("4. View Class Statistics")
	print("5. Save and Exit (or press ESC)")


def main():
	print("=" * 50)
	print("WELCOME TO STUDENT GRADE CALCULATOR")
	print("=" * 50)
	students = load_students()
	while True:
		display_menu()
		try:
			print("=" * 50)
			choice = prompt_text("Select an option (1-5) or press ESC to exit: ")
		except (KeyboardInterrupt, EOFError):
			print("\nExiting program.")
			save_and_exit(students)
			break
		if choice.casefold() in ("5", "esc", "\x1b"):
			save_and_exit(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			search_student(students)
		elif choice == "4":
			display_statistics(students)
		else:
			print("Invalid option. Please choose 1 through 5.")


if __name__ == "__main__":
	main()