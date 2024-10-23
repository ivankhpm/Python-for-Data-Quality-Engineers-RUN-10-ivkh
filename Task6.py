import datetime as dt
import os


##Class for NewsFeed
class NewsFeed:
    def __init__(self):
        self.records = []

## to save all inputs
    def add_record(self, record):
        self.records.append(record)

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

        self.file_name = f"news_{date_input}.txt"
        self.file_path = os.path.join(self.folder_path, self.file_name)

    def read_records(self, news_feed):
        # file exists?
        if not os.path.exists(self.file_path):
            print("File does not exist.")
            return

        with open(self.file_path, "r") as file:
            lines = file.readlines()

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

        ##iter every record
        for line in lines:
            # split data by separator
            data = line.strip().split(';')
            # get data type of each row
            data_type = data[0].strip()

            #check that type is correct and required field amount correct
            if data_type in data_mapping and len(data) == data_mapping[data_type]['length']:
                #helper for getting class
                record_class = data_mapping[data_type]['class']
                try:
                    if record_class is News:
                        text, city = capitalized_sentences(data[1].strip()), data[2].strip()
                        temp_news_feed.append(News(text, city))
                    elif record_class is PrivateAd:
                        text, expiration_date = capitalized_sentences(data[1].strip()), data[2].strip()
                        temp_news_feed.append(PrivateAd(text, expiration_date))
                    elif record_class is BirthNotification:
                        user_name, date_of_birth = capitalized_sentences(data[1].strip()), data[2].strip()
                        temp_news_feed.append(BirthNotification(user_name, date_of_birth))
                except ValueError:
                    print(f"Error in record '{line.strip()}': {ValueError}. File was not processed")
                    error_occurred = True
            else:
                print(f"Incorrect record type or data structure: {line.strip()}. File was not processed")
                error_occurred = True

        if not error_occurred:
            final_news_feed = NewsFeed()
            for record in temp_news_feed:
                final_news_feed.add_record(record)
            # Remove file after processing
            os.remove(self.file_path)
            print("Processed and removed the input file:", self.file_path)

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

if __name__ == "__main__":
    main()

