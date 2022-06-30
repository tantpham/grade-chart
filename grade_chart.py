import pandas as pd
import numpy as np
import statistics
import os
import matplotlib.pyplot as plt
import csv as reader


def print_menu():
    """
    print the menu, ask for the options from the main menu
    :args:
        None
    @return:
        user choice (integer)
    """
    print("*************************Main Menu***************************\n", )
    print("1. Read CSV file of grades")
    print("2. Generate student report file")
    print("3. Generate student report charts")
    print("4. Generate class report file")
    print("5. Generate class report charts")
    print("6. Quit")
    print("*************************************************************\n")
    user_choice = int(input("Enter the choice number: "))
    while user_choice < 1 or user_choice > 6:
        user_choice = int(input("Enter the choice number: "))
    return user_choice


def score_to_letter_grade(score):
    """
    convert to score 0-100 to A, B, C , D, F
    :args:
        score (float)
    @return:
        letter grade (char)
    """
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def check_UIN_format(UIN):
    """
    check UIN format
    10 digits only
    :args:
        UIN unique identification number
    @return:
        true/false
    """
    if len(UIN) != 10:
        return False
    # check digit
    for ch in UIN:
        if not ch.isdigit():
            return False
    return True


def calculate_score(exam_1, exam_2, exam_3, labs_mean, quizzes_mean, reading_activities_mean, project):
    """
    calculate score
    :args:
        exam_1: exam 1 (float)
        exam_2: exam 2 (float)
        exam_3: exam 3 (float)
        labs_mean: labs mean (float)
        quizzes_mean: quizzes mean (float)
        reading_activities_mean: reading activities mean (float)
        project: project (float)

    @return:
        score (float)
    """
    return (
                   exam_1 * 15 + exam_2 * 15 + exam_3 * 15 + labs_mean * 25 + quizzes_mean * 10 + reading_activities_mean * 10 + project * 10) / 100.0


def generate_student_report_file(df):
    """
    Generate student report file
    The function generates the "<UIN>.txt" file

    Exams mean: ...
    Labs mean: ...
    Quizzes mean: ...
    Reading activities mean: ...
    Score: ...%
    Letter grade: ...

    :args:
        pandas.DataFrame df
    """
    # ask for UIN until valid
    while True:
        UIN = input('Please enter UIN: ')
        while not check_UIN_format(UIN):
            print("UIN should be ten digits and contains numbers only")

            # ask for UIN
            UIN = input('Please enter UIN: ')

        # retrieving row
        row = df.loc[df['UIN'] == int(UIN)]
        if len(row) == 0:
            print('UIN not found!')
        else:

            # print(float(row['exam 1']))

            # exams
            exam_1 = float(row['exam 1'])
            exam_2 = float(row['exam 2'])
            exam_3 = float(row['exam 3'])

            # exams mean
            exams_mean = (exam_1 + exam_2 + exam_3) / 3.0
            # labs mean
            labs_mean = (float(row['lab 1']) + float(row['lab 2']) + float(row['lab 3']) + float(
                row['lab 4']) + float(row['lab 5']) + float(row['lab 6'])) / 6.0
            # quizzes mean
            quizzes_mean = (float(row['quiz 1']) + float(row['quiz 2']) + float(row['quiz 3']) + float(
                row['quiz 4']) + float(row['quiz 5']) + float(row['quiz 6'])) / 6.0
            # reading activities mean
            reading_activities_mean = (float(row['reading 1']) + float(row['reading 2']) + float(
                row['reading 3']) + float(row['reading 4']) + float(row['reading 5']) + float(
                row['reading 6'])) / 6.0
            # project
            project = float(row['project'])

            # calculate score
            score = calculate_score(exam_1, exam_2, exam_3, labs_mean, quizzes_mean, reading_activities_mean, project)

            # calculate letter grade
            letter_grade = score_to_letter_grade(score)

            # write to file
            file = open(UIN + ".txt", "w")  # write mode

            file.write(f"Exams mean: {format(exams_mean, '.1f')}\n")
            file.write(f"Labs mean: {format(labs_mean, '.1f')}\n")
            file.write(f"Quizzes mean: {format(quizzes_mean, '.1f')}\n")
            file.write(f"Reading activities mean: {format(reading_activities_mean, '.1f')}\n")
            file.write(f"Score: {format(score, '.1f')}%\n")
            file.write(f"Letter grade: {letter_grade}\n")

            # close file
            file.close()

            break


def generate_student_report_charts(df):
    """
    Generate student report charts

    :args:
        df:
        pandas dataframe in which desired file is want to be read

    """
    # ask for UIN until valid
    while True:
        UIN = input('Please enter UIN: ')
        while not check_UIN_format(UIN):
            print("UIN should be ten digits and contains numbers only")

            # ask for UIN
            UIN = input('Please enter UIN: ')

        # retrieving row
        row = df.loc[df['UIN'] == int(UIN)]
        if len(row) == 0:
            print('UIN not found!')
        else:

            # create folder
            if not os.path.exists(UIN):
                os.mkdir(UIN)

            # exams
            exam_1 = float(row['exam 1'])
            exam_2 = float(row['exam 2'])
            exam_3 = float(row['exam 3'])

            exams = [exam_1, exam_2, exam_3]
            index = ['Exam 1', 'Exam 2', 'Exam 3']

            df = pd.DataFrame({'Exam': exams}, index=index)
            ax = df.plot.bar(rot=0)
            ax.get_figure().savefig(UIN + '/exams.png')

            # labs
            lab_1 = float(row['lab 1'])
            lab_2 = float(row['lab 2'])
            lab_3 = float(row['lab 3'])
            lab_4 = float(row['lab 4'])
            lab_5 = float(row['lab 5'])
            lab_6 = float(row['lab 6'])

            labs = [lab_1, lab_2, lab_3, lab_4, lab_5, lab_6]
            index = ['Lab 1', 'Lab 2', 'Lab 3', 'Lab 4', 'Lab 5', 'Lab 6']

            df = pd.DataFrame({'Lab': labs}, index=index)
            ax = df.plot.bar(rot=0)
            ax.get_figure().savefig(UIN + '/labs.png')

            # quizzes
            quiz_1 = float(row['quiz 1'])
            quiz_2 = float(row['quiz 2'])
            quiz_3 = float(row['quiz 3'])
            quiz_4 = float(row['quiz 4'])
            quiz_5 = float(row['quiz 5'])
            quiz_6 = float(row['quiz 6'])

            quizzes = [quiz_1, quiz_2, quiz_3, quiz_4, quiz_5, quiz_6]
            index = ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4', 'Quiz 5', 'Quiz 6']

            df = pd.DataFrame({'quiz': quizzes}, index=index)
            ax = df.plot.bar(rot=0)
            ax.get_figure().savefig(UIN + '/quizzes.png')

            # reading activities
            reading_1 = float(row['reading 1'])
            reading_2 = float(row['reading 2'])
            reading_3 = float(row['reading 3'])
            reading_4 = float(row['reading 4'])
            reading_5 = float(row['reading 5'])
            reading_6 = float(row['reading 6'])

            reading_activities = [reading_1, reading_2, reading_3, reading_4, reading_5, reading_6]
            index = ['Reading 1', 'Reading 2', 'Reading 3', 'Reading 4', 'Reading 5', 'Reading 6']

            df = pd.DataFrame({'Reading': reading_activities}, index=index)
            ax = df.plot.bar(rot=0)
            ax.get_figure().savefig(UIN + '/reading_activities.png')

            break


def generate_class_report(df):
    """Creates a .txt file with various data from a csv file

    Calculates each row's overall grade and stores information
    into a list. Then uses integrated list functions in order to find
    the specified data wanted.

    A txt file with various data values such as:
                Max score of the class
                Min score of the class
                Median score of the class
                Mean score of the class
                Standard deviation of the class

    :args:
        df:
        pandas dataframe in which desired file is want to be read

    @return:
        A txt file with specified data - reports.txt
            Contains:
                Max score of the class
                Min score of the class
                Median score of the class
                Mean score of the class
                Standard deviation of the class
    """
    num_students = len(df.index) - 1
    student_averages = []

    # iterate through each UIN and take the average for each student and append to list

    for row in range(1, num_students):
        # exams
        exam_1 = float(df.iloc[row, 19])
        exam_2 = float(df.iloc[row, 20])
        exam_3 = float(df.iloc[row, 21])

        # labs mean
        labs_mean = (float(df.iloc[row, 1]) + float(df.iloc[row, 2]) + float(df.iloc[row, 3]) + float(
            df.iloc[row, 4]) + float(df.iloc[row, 5]) + float(df.iloc[row, 6])) / 6.0
        # quizzes mean
        quizzes_mean = (float(df.iloc[row, 7]) + float(df.iloc[row, 8]) + float(df.iloc[row, 9]) + float(
            df.iloc[row, 10]) + float(df.iloc[row, 11]) + float(df.iloc[row, 12])) / 6.0
        # reading activities mean
        reading_activities_mean = (float(df.iloc[row, 13]) + float(df.iloc[row, 14]) + float(
            df.iloc[row, 15]) + float(df.iloc[row, 16]) + float(df.iloc[row, 17]) + float(
            df.iloc[row, 18])) / 6.0

        # project
        project = float(df.iloc[row, 22])

        score = calculate_score(exam_1, exam_2, exam_3, labs_mean, quizzes_mean, reading_activities_mean, project)
        student_averages.append(score)

        max_score = max(student_averages)
        min_score = min(student_averages)
        median_score = statistics.median(student_averages)
        mean_score = statistics.mean(student_averages)
        std_dev = statistics.pstdev(student_averages)

    file = open("report.txt", "w")

    file.write(f"Total number of students: {format(num_students)}\n")
    file.write(f"Minimum score: {format(min_score, '.1f')}\n")
    file.write(f"Maximum score: {format(max_score, '.1f')}\n")
    file.write(f"Median score: {format(median_score, '.1f')}\n")
    file.write(f"Mean score: {format(mean_score, '.1f')}\n")
    file.write(f"Standard deviation: {format(std_dev, '.1f')}\n")


def generate_class_report_charts(df):
    """Generate two class report charts (pie and bar)

    Iterates through each row and finds the total average
    of each student. Then will use the score_to_letter function
    to convert the score into its correct letter. Then graphs the
    pie and bar chart according to the amount of letters were present
    amongst the overall data in the csv.

    A directory(class_charts):
            two png files named:
                bar_chart.png
                pie_chart.png

    :args:
        df:
        pandas dataframe in which desired file is want to be read

    @return:
        New file directory - /class_charts
            two png files:
                bar_chart.png
                pie_chart.png
    """

    num_students = len(df.index) - 1

    grade_letter = []

    # iterate through each UIN and take the average for each student and append to list

    for row in range(1, num_students):
        # exams
        exam_1 = float(df.iloc[row, 19])
        exam_2 = float(df.iloc[row, 20])
        exam_3 = float(df.iloc[row, 21])

        # labs mean
        labs_mean = (float(df.iloc[row, 1]) + float(df.iloc[row, 2]) + float(df.iloc[row, 3]) + float(
            df.iloc[row, 4]) + float(df.iloc[row, 5]) + float(df.iloc[row, 6])) / 6.0
        # quizzes mean
        quizzes_mean = (float(df.iloc[row, 7]) + float(df.iloc[row, 8]) + float(df.iloc[row, 9]) + float(
            df.iloc[row, 10]) + float(df.iloc[row, 11]) + float(df.iloc[row, 12])) / 6.0
        # reading activities mean
        reading_activities_mean = (float(df.iloc[row, 13]) + float(df.iloc[row, 14]) + float(
            df.iloc[row, 15]) + float(df.iloc[row, 16]) + float(df.iloc[row, 17]) + float(
            df.iloc[row, 18])) / 6.0
        # project
        project = float(df.iloc[row, 22])

        score = calculate_score(exam_1, exam_2, exam_3, labs_mean, quizzes_mean, reading_activities_mean, project)
        letter = score_to_letter_grade(score)
        grade_letter.append(letter)

    count_a = grade_letter.count('A')
    count_b = grade_letter.count('B')
    count_c = grade_letter.count('C')
    count_d = grade_letter.count('D')
    count_f = grade_letter.count('F')

    labels = ['A', 'B', 'C', 'D', 'F']
    data = [count_a, count_b, count_c, count_d, count_f]
    y2 = data
    # figure out how to store into file
    present = os.path.isdir('./class_charts')
    if present is True:
        os.chdir('class_charts')
    else:
        os.mkdir('class_charts')
        os.chdir('class_charts')
    plt.pie(data, labels=labels, autopct='%.1f%%')
    plt.title("Letter Grade Distribution")
    plt.savefig('pie_chart.png')
    plt.close()
    plt.bar(labels, y2)
    plt.title("Letter Grade Distribution")
    plt.savefig('bar_chart.png')


def main():
    """Main function as the starting point of Python application
    @Return:
        None
    """
    # print the menu, ask for the choice and return it
    user_choice = print_menu()
    #
    df = None

    while user_choice != 6:

        if user_choice == 1:  # Read CSV file of grades
            fn = input("Enter file name: ")  # "grades.csv
            try:
                df = pd.read_csv(fn)
            except:
                print('Could not read ' + fn)  # THROW AN ERROR!!
        elif user_choice == 2:

            if df is None:
                print('Please choose option 1 to read CSV file of grades')
            else:
                # Generate student report file
                generate_student_report_file(df)
        elif user_choice == 3:

            if df is None:
                print('Please choose option 1 to read CSV file of grades')
            else:
                # Generate student report charts
                generate_student_report_charts(df)
        elif user_choice == 4:

            if df is None:
                print('Please choose option 1 to read CSV file of grades')
            else:
                # Generate student report charts
                generate_class_report(df)
        elif user_choice == 5:

            if df is None:
                print('Please choose option 1 to read CSV file of grades')
            else:
                # Generate student report charts
                generate_class_report_charts(df)
        print()
        # print the menu, ask for the choice and return it
        user_choice = print_menu()


main()