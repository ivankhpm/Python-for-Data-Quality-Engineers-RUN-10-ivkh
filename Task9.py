import datetime as dt
import os
import csv
import re
import json
import xml.etree.ElementTree as ET


##Class for NewsFeed
class NewsFeed:
    def __init__(self):
        self.records = []

## to save all inputs
    def add_record(self, record):
        self.records.append(record)

    def remove_all(self):
        self.records.clear()

## to add all inputs to file
    def publish_records(self):
        with open("news_feed.txt", "a") as file:
            for record in self.records:
                file.write(record.publish())

# Class for NEWS
class News:
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.date = dt.datetime.now().strftime('%d/%m/%Y %H.%M')

##publish news
    def publish(self):
        return f"----News -------------------------\n{self.text}\n{self.city}, {self.date}\n\n"



#Class for Private Ad
class PrivateAd:
    def __init__(self, text, expiration_date):
        self.text = text
        try:
            self.expiration_date = dt.datetime.strptime(expiration_date, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Expiration Date should be in 'DD-MM-YYYY' format")
        self.days_left = self.calculate_days_left()

##Day left calculation
    def calculate_days_left(self):
        today = dt.datetime.now().date()
        ##expiration_date = dt.datetime.strptime(self.expiration_date, "%d-%m-%Y").date()
        return (self.expiration_date - today).days

##publish PrivateAd
    def publish(self):
        return f"----Private Ad -------------------\n{self.text}\nActual until: {self.expiration_date}, {self.days_left} days left\n\n"



##Class for custom class BirthNotification
class BirthNotification:
    def __init__(self, user_name, date_of_birth):
        self.user_name = user_name
        try:
            self.date_of_birth = dt.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Date of Birth should be in 'DD-MM-YYYY' format")
        self.date_of_birth = self.calculate_days_to_birthday()

    def calculate_days_to_birthday(self):
        today = dt.datetime.today().date()
        this_year_birthday = self.date_of_birth.replace(year=today.year)

        # in case bday already was in current year check next year for this person
        if this_year_birthday < today:
            this_year_birthday = this_year_birthday.replace(year=today.year + 1)

        return (this_year_birthday - today).days

##publish BirthNotification
    def publish(self):
        return f"----IT IS BIRTHDAY SOON! ---------\nUser {self.user_name} has bday in {self.date_of_birth} day(s)\n\n"



###Class for working in file:
##Sample of processed data:
# 1; Test1; Kyiv
# 1; Test2; Kyiv
# 2; PrivateAd Test; 11-01-2022
# 2; PrivateAd Test1; 11-01-2022
# 3; User1; 11-01-2022

## file mask news_<date>.txt

class File:
    def __init__(self):
        input_prompt = "Enter the path to the directory containing the news file (Enter for default): "
        input_path = input(input_prompt).strip()

        # default root directory
        self.folder_path = input_path if input_path else "./"

        # if incorrect path, use defualt
        if not os.path.isdir(self.folder_path):
            print("Warning: Using the default directory instead, as PATH IS NOT VALID")
            self.folder_path = "./"

        # add date for news file
        date_prompt = "Please enter the date for the news file in DDMMYYYY format: "
        date_input = input(date_prompt).strip()

        # file format txt or json
        filetype_prompt = "Please enter the file extension for the news file; txt, json or xml only: "
        filetype_input = input(filetype_prompt).strip()

        self.file_name = f"news_{date_input}.{filetype_input}"
        self.file_path = os.path.join(self.folder_path, self.file_name)
        self.filetype_input = filetype_input

    def read_records(self, news_feed):
        # file exists?
        if not os.path.exists(self.file_path):
            print("File does not exist or file extension input is incorrect")
            return

        with open(self.file_path, "r") as file:
            if self.filetype_input == 'txt':
                lines = file.readlines()
            elif self.filetype_input == 'json':
                lines = json.load(file)
            elif self.filetype_input == 'xml':
                tree = ET.parse(file)
                lines = tree.getroot()
            else:
                print("GOOD NEWS: Your file exists \nBAD NEWS: only TXT or JSON or XMLfiles are allowed. Please add correct file")

            self.process_lines(lines, news_feed)


    def process_lines(self, lines, news_feed):
        #describe types of news to select proper class
        data_mapping = {
            '1': {'class': News, 'length': 3},
            '2': {'class': PrivateAd, 'length': 3},
            '3': {'class': BirthNotification, 'length': 3}
        }

        temp_news_feed = []
        error_occurred = False
        if self.filetype_input == 'txt':
            ##iter every record
            for line in lines:
                # split data by separator
                data = line.strip().split(';')
                # get data type of each row
                data_type = data[0].strip()

                # check that type is correct and required field amount correct
                if data_type in data_mapping and len(data) == data_mapping[data_type]['length']:
                    # helper for getting class
                    record_class = data_mapping[data_type]['class']
                    try:
                        if record_class is News:
                            text, city = capitalized_sentences(data[1].strip()), data[2].strip()
                            news_feed.add_record(News(text, city))
                        elif record_class is PrivateAd:
                            text, expiration_date = capitalized_sentences(data[1].strip()), data[2].strip()
                            news_feed.add_record(PrivateAd(text, expiration_date))
                        elif record_class is BirthNotification:
                            user_name, date_of_birth = capitalized_sentences(data[1].strip()), data[2].strip()
                            news_feed.add_record(BirthNotification(user_name, date_of_birth))
                    except ValueError:
                        print(f"Error in record '{line.strip()}': {ValueError}. File was not processed")
                        error_occurred = True
                else:
                    print(f"Incorrect record type or data structure: {line.strip()}. File was not processed")
                    error_occurred = True


        ### HM8 JSON
        elif self.filetype_input == 'json':
            for line in lines:
                data_type = line.get('type')

                # check that type is correct and required field amount correct
                if data_type in data_mapping and len(line) == data_mapping[data_type]['length']:
                    # helper for getting class
                    record_class = data_mapping[data_type]['class']
                    try:
                        if record_class is News:
                            text, city = capitalized_sentences(line.get('text')), line.get('city')
                            news_feed.add_record(News(text, city))
                        elif record_class is PrivateAd:
                            text, expiration_date = capitalized_sentences(line.get('text')), line.get('expiration_date')
                            news_feed.add_record(PrivateAd(text, expiration_date))
                        elif record_class is BirthNotification:
                            user_name, date_of_birth = capitalized_sentences(line.get('user_name')), line.get(
                                'date_of_birth')
                            news_feed.add_record(BirthNotification(user_name, date_of_birth))
                    except ValueError:
                        print(f"Error in record '{json.dumps(line)}': {ValueError}. File was not processed")
                        error_occurred = True
                else:
                    print(f"Incorrect record type or data structure: {json.dumps(line)}. File was not processed")
                    error_occurred = True

        ### HM9 XML
        elif self.filetype_input == 'xml':
            for news_element in lines.findall('news'):
                data_type = news_element.find('type').text

                if data_type in data_mapping and len(list(news_element)) == data_mapping[data_type]['length']:
                    record_class = data_mapping[data_type]['class']

                    try:
                        if record_class is News:
                            text = capitalized_sentences(news_element.find('text').text)
                            city = news_element.find('city').text
                            news_feed.add_record(News(text, city))
                        elif record_class is PrivateAd:
                            text = capitalized_sentences(news_element.find('text').text)
                            expiration_date = news_element.find('expiration_date').text
                            news_feed.add_record(PrivateAd(text, expiration_date))
                        elif record_class is BirthNotification:
                            user_name = capitalized_sentences(news_element.find('user_name').text)
                            date_of_birth = news_element.find('date_of_birth').text
                            news_feed.add_record(BirthNotification(user_name, date_of_birth))
                    except ValueError as e:
                        print(f"Error in record '{ET.tostring(news_element, 'unicode')}': {e}. File was not processed")
                        error_occurred = True
                else:
                    print(
                        f"Incorrect record type or data structure: {ET.tostring(news_element, 'unicode')}. File was not processed")
                    error_occurred = True

        if not error_occurred:
            # Remove file after processing
            os.remove(self.file_path)
            print("Processed and removed the input file:", self.file_path)
            return news_feed
        else:
            return news_feed.remove_all()



### HM7 CSV
class FileCsv:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_and_process_text(self):
        # Read the file and return the text
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def calculate_word_count(self, text):
        # Calculate word frequency in the text (lowercase), removed also any other symbols except letetrs and numbers
        words = text.lower().split()
        word_count = {}
        for word in words:
            cleaned_word = re.sub(r'[^a-z0-9]', '', word)
            if cleaned_word:
                word_count[cleaned_word] = word_count.get(cleaned_word, 0) + 1
        return word_count

    def write_word_count_csv(self, word_count):
        # write word count
        with open("word_count.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Word', 'Frequency'])
            for word, frequency in word_count.items():
                csv_writer.writerow([word, frequency])

    def count_letters(self, text):
        # Count the total and uppercase letters
        count_all = 0
        count_uppercase = 0
        for char in text:
            if char.isalpha():
                count_all += 1
                if char.isupper():
                    count_uppercase += 1
        return count_all, count_uppercase

    def write_letter_count_csv(self, count_all, count_uppercase):
        # Write the letter count to a CSV file
        percentage = (count_uppercase / count_all) * 100 if count_all else 0
        with open("letters_count.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Total Letters', 'Uppercase Letters', 'Uppercase Percentage'])
            csv_writer.writerow([count_all, count_uppercase, percentage])

    def process_text_and_output_csvs(self):
        # Process the text and output the results to CSV files
        text = self.read_and_process_text()

        word_count = self.calculate_word_count(text)
        self.write_word_count_csv(word_count)

        count_all, count_uppercase = self.count_letters(text)
        self.write_letter_count_csv(count_all, count_uppercase)


##### USAGE ######
def capitalized_sentences(text):
    sentences = text.split('.')
    capitalized = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
    normalized_text = '.\n'.join(capitalized) + '.'
    return normalized_text



def get_input():
    data_type = input("Select the data type (1 for News, 2 for Private Ad, 3 for Bday Notification): ")
    if data_type == "1":
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return News(text, city)
    elif data_type == "2":
        text = input("Enter the ad text: ")
        expiration_date = input("Enter the expiration date (IMPORTANT!!! DD-MM-YYYY): ")
        return PrivateAd(text, expiration_date)
    elif data_type == "3":
        user = input("Enter the user name: ")
        date_of_birth = input("Enter the birthday date (IMPORTANT!!! DD-MM-YYYY): ")
        return BirthNotification(user, date_of_birth)
    else:
        print("Invalid data type")
        return None


def main():
    news_feed = NewsFeed()
    user_choice = input("File load or manual input? (type 'file' or 'manual'): ")

    if user_choice.lower() == 'file':
        file_handler = File()
        file_handler.read_records(news_feed)
        news_feed.publish_records()
    elif user_choice.lower() == 'manual':
        while True:
            record = get_input()
            if record:
                news_feed.add_record(record)
            cont = input("Do you want to add more records? (yes/no): ")
            if cont.lower() != "yes":
                break
        news_feed.publish_records()
    else:
        print("Invalid choice")
        return

    csv = FileCsv("news_feed.txt")
    csv.process_text_and_output_csvs()

if __name__ == "__main__":
    main()

