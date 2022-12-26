"""
Facebook - BOT  functions:
A. Scrape and extract posts to excel and get Keyword
B. Scrape for desired Keyword and get posts to Whatsapp


Requested Library's to be pre-installed:
pip install selenium , customtkinter ,pandas ,pywhatkit, keyboard, tkinter


Notice:     (better to read before running the code)
A.  The extension chromedriver.exe must be installed
    to the folder from which the code will run, otherwise Selenium will not work.
    You can download the Chrome extension from the following link:
    https://chromedriver.chromium.org/
    (You must first check the version of your Chrome browser and download according to the version)

B.  A verification process through the phone of the Facebook account holder
    will be needed as part of the login process to Facebook


by: Amit Shemesh
26/12/2022
Github account: https://github.com/amit96s?tab=repositories
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import customtkinter
import pandas as pd
import pywhatkit as w
import time
import pyautogui
import keyboard as k
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class UserUi(customtkinter.CTk):
    User_Info = []
    def __init__(self):
        super(UserUi, self).__init__()

        """  Window Main Configurations  """
        self.geometry("650x520")
        self.title("Facebook BOT  - by Amit shemesh")
        self.resizable(False, False)
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)


        """  Window Fields  """
        self.Login_System_Label = customtkinter.CTkLabel(master=self.frame, text='Login System')
        self.Login_System_Label.configure(font=("Roboto", 26))
        self.Login_System_Label.pack(pady=(16, 35), padx=10)

        self.Enter_details_Label = customtkinter.CTkLabel(master=self.frame, text='Enter your Facebook login details')
        self.Enter_details_Label.configure(font=("Roboto", 15))
        self.Enter_details_Label.pack(pady=(0,6), padx=0)

        self.Email_Entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="E-mail:", width=260, height=30, font=("", 18))
        self.Email_Entry.pack(pady=(0, 8), padx=10)

        self.Password_Entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password:", show="*", width=260, height=30,font=("", 18))
        self.Password_Entry.pack(pady=(0, 8), padx=10)

        self.Group_link_Entry =customtkinter.CTkEntry(master=self.frame, placeholder_text="Requested Group Link:", width=260, height=30,font=("", 18))
        self.Group_link_Entry.pack(pady=(14, 8), padx=10)

        self.Key_word_Entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Key word:", width=260, height=30, font=("", 18))
        self.Key_word_Entry.pack(pady=(0, 8), padx=10)

        self.Phone_Entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Enter phone number:", width=260, height=30,font=("", 18))
        self.Phone_Entry.pack(pady=(0, 8), padx=10)

        self.Desired_num_of_results_Label = customtkinter.CTkLabel(master=self.frame, text='Desired number of results')
        self.Desired_num_of_results_Label.configure(font=("Roboto", 15))
        self.Desired_num_of_results_Label.pack(pady=(13, 8), padx=10)


        self.Desired_num_of_results_Checkbox = customtkinter.CTkComboBox(master=self.frame, values= ['20', '30', '35', '40', '45', '50', '55', '60', '65', '70',
                                                            '75', '80', '85', '90', '100', '110', '120', '130', '140', '150'])
        self.Desired_num_of_results_Checkbox.pack(pady=(0, 10), padx=10)

        self.Start_Button = customtkinter.CTkButton(master=self.frame, text="Start", command=self.Start, height=30, font=("", 19))
        self.Start_Button.pack(pady=(18, 0), padx=10)


    """  A function that takes the data entered by the user and login to Facebook  """
    def Start(self):
        UserUi.User_Info.extend((self.Email_Entry.get(),
                                 self.Password_Entry.get(),
                                 self.Group_link_Entry.get(),
                                 self.Key_word_Entry.get(),
                                 self.Phone_Entry.get(),
                                 self.Desired_num_of_results_Checkbox.get()))     # Insert the values entered by the user to a dict

        # Set Selenium Connection To Internet
        self.options = Options()
        self.options.headless = False
        self.options = webdriver.ChromeOptions()
        self.prefs = {"profile.default_content_setting_values.notifications": 2}
        self.options.add_experimental_option("prefs", self.prefs)

        self.website = 'https://www.facebook.com/'
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.website)
        self.driver.maximize_window()


        #Account Login
        self.Email_Login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@name, "email")]')))
        self.Email_Login.send_keys(self.User_Info[0])

        self.Password_Login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@type, "password")]')))
        self.Password_Login.send_keys(self.User_Info[1])

        self.Login_Enter = WebDriverWait(self.driver, 450).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@name, "login")]'))).click()

        # Usually at this stage there is a verification process required on the phone hence the wait
        time.sleep(20)

        # Go to the desired Facebook page
        self.driver.get(self.User_Info[2])
        time.sleep(3)


        self.List_of_posts = []     # All scraped posts will be saved here
        self.List_of_links = []     # Link to each scraped post
        self.Number_of_posts = 0

        while self.Number_of_posts < int(self.User_Info[5]):       # While the user's selection for a number of posts is less than the scraped posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")         # Scroll down in page
            time.sleep(3)

            posts = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@CLASS = 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']")))


            """  Function to scan the Facebook page for posts  """
            def Extract_Post(post):
                xpath_syntax_link = ".//li[contains(@class, 'x1rg5ohu x1emribx x1i64zmx')]/a"     # Xpath for post's link

                List_of_Xpaths_possiable = [".//div[starts-with(@id, 'jsc_c') and starts-with (@class, 'x1iorvi4 x1pi30zi')]",
                                            ".//div[contains(@CLASS, 'xzsf02u xngnso2 xo1l8bm x1qb5hxa')]/div",
                                            ".//div[starts-with(@id, 'jsc_c') and starts-with (@class, 'x1yx25j4')]/div"]     # Xpath options for post content

                for try_xpath in List_of_Xpaths_possiable:
                    try:
                        post_content = post.find_element(By.XPATH, try_xpath).get_attribute('textContent')
                        post_link = post.find_element(By.XPATH, xpath_syntax_link).get_attribute('href')
                        post_info = [post_content, post_link]
                        return post_info
                    except:
                        pass


            for post in posts:
                self.post_info = Extract_Post(post)
                try:
                    if self.post_info is not None:       # Check if we get any values from post
                        if self.post_info[0] not in self.List_of_posts:    # Make sure post is not already in fainl list
                            if len(self.post_info[0]) > 2:        # Filter "single-icon" posts
                                self.List_of_posts.append(self.post_info[0])      # Add posts content into a list
                                split_for_link = str(self.post_info[1]).split("?comment")
                                self.List_of_links.append(split_for_link[0])    # Add post link's into a list
                                self.Number_of_posts += 1
                        else:
                            pass
                except:
                    pass

        """   Save all scraped posts to excel  """
        save_to_excel = pd.DataFrame({"Post": self.List_of_posts ,
                                      "Post link": self.List_of_links})
        save_to_excel.to_csv(f'Facebook BOT - {self.User_Info[3]}.csv', index=False, encoding='utf-8')


        """ Filter Keywords and send relevant post to Whatsapp """
        posts_with_key_word = []
        count_founds = 0
        for key in self.List_of_posts:
            try:
                if str(self.User_Info[3]).lower() in key or str(self.User_Info[3]).title() in key or str(self.User_Info[3]).upper() in key:         # Check for each post if Keyword exists
                    count_founds += 1
                    posts_with_key_word.extend((count_founds, key, f'{self.List_of_links[self.List_of_posts.index(key)]}'))
            except:
                pass


        """  Send the relevant posts with the KEYWORD to Whatsapp"""
        w.sendwhatmsg_instantly(self.User_Info[4],f'Hi {self.User_Info[0]}, \n according to the key words'
                                                  f' you selected ({self.User_Info[3]}) we found {int(len(posts_with_key_word) / 3)} matches'
                                                  f' for you: \n \n {posts_with_key_word}',10)
        pyautogui.click()
        time.sleep(0.5)
        k.press_and_release('enter')


        messagebox.showinfo(title="Process Finished Successfully", message="Process Finished Successfully")



if __name__ == '__main__':
    bot = UserUi()
    bot.mainloop()