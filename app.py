import tkinter as tk
from PIL import Image, ImageTk
import requests  # Importing requests for API calls

# Sample character data (you can extend this as needed)
CHARACTER_DATA = {
    "Harry Potter": {
        "Name": "Harry Potter",
        "House": "Gryffindor",
        "Wand": "11\" Holly, Phoenix Feather",
        "Patronus": "Stag"
    },
    "Hermione Granger": {
        "Name": "Hermione Granger",
        "House": "Gryffindor",
        "Wand": "10¾\" Vine Wood, Dragon Heartstring",
        "Patronus": "Otter"
    },
    "Ron Weasley": {
        "Name": "Ron Weasley",
        "House": "Gryffindor",
        "Wand": "14\" Willow, Unicorn Hair",
        "Patronus": "Jack Russell Terrier"
    },
    "Albus Dumbledore": {
        "Name": "Albus Dumbledore",
        "House": "Gryffindor",
        "Wand": "15\" Elder, Thestral Tail Hair (Elder Wand)",
        "Patronus": "Phoenix"
    },
}

class HarryPotterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Harry Potter App")
        self.geometry("800x600")  # Adjusted to make it more responsive

        # Main container for pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for F in (StartPage, HomePage, FavouritesPage, CharacterPage, InfoPage,): 
        # Ensure BooksPage is included
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def fetch_data(self, endpoint):
        """Fetch data from the API."""
        base_url = "https://api.potterdb.com/"
        try:
            response = requests.get(base_url + endpoint)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the JSON data
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to the API: {e}")
            return None

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#004d99')
        self.controller = controller
        
        label = tk.Label(self, text="Welcome to the Harry Potter App!", font=("Helvetica", 24), bg='#004d99', fg='white')
        label.pack(pady=20)

        # Adding a front image
        try:
            front_image = Image.open("image1.jpg")
            front_image = front_image.resize((400, 300), Image.LANCZOS)
            self.front_photo = ImageTk.PhotoImage(front_image)
            front_image_label = tk.Label(self, image=self.front_photo, bg='#ffcc00')
            front_image_label.pack(pady=10)  # Moved above the start button

        except FileNotFoundError:
            error_label = tk.Label(self, text="Error: 'image1.jpg' not found.", bg='#ffcc00', fg='red')
            error_label.pack(pady=20)
        except Exception as e:
            error_label = tk.Label(self, text=f"Error loading front image: {str(e)}", bg='#ffcc00', fg='red')
            error_label.pack(pady=20)

        start_button = tk.Button(self, text="Start Exploring", command=lambda: controller.show_frame("HomePage"), 
                                 font=("Helvetica", 14), bg='#ff6600', fg='white')
        start_button.pack(pady=20)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#004d99')
        self.controller = controller
        
        # Left-side navigation panel (buttons)
        nav_frame = tk.Frame(self, bg='#00264d')
        nav_frame.pack(side="left", fill="y")
        
        # Navigation buttons
        button1 = tk.Button(nav_frame, text="Home", command=lambda: controller.show_frame("HomePage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button1.pack(pady=10)
        
        button2 = tk.Button(nav_frame, text="Favourites", command=lambda: controller.show_frame("FavouritesPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button2.pack(pady=10)
        
        button3 = tk.Button(nav_frame, text="Character Details", command=lambda: controller.show_frame("CharacterPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button3.pack(pady=10)

        button4 = tk.Button(nav_frame, text="Info", command=lambda: controller.show_frame("InfoPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button4.pack(pady=10)

        # Adding the new Books button
        button5 = tk.Button(nav_frame, text="Books", command=lambda: controller.show_frame("BooksPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button5.pack(pady=10)

        # Main content area (center)
        content_frame = tk.Frame(self, bg='#004d99')
        content_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)
        
        label = tk.Label(content_frame, text="Welcome to the Harry Potter App", font=("Helvetica", 24), bg='#ffcc00', fg='black')
        label.pack(pady=20)

        # Adding a start button
        start_button = tk.Button(content_frame, text="Explore Characters", command=lambda: controller.show_frame("CharacterPage"), 
                                 font=("Helvetica", 14), bg='#ff6600', fg='white')
        start_button.pack(pady=20)

        # Adding a back button to Start Page
        back_button = tk.Button(content_frame, text="Back to Start Page", command=lambda: controller.show_frame("StartPage"), 
                                font=("Helvetica", 14), bg='#ff6600', fg='white')
        back_button.pack(pady=20)

class FavouritesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#004d99')
        self.controller = controller
        
        # Left-side navigation panel (buttons)
        nav_frame = tk.Frame(self, bg='#00264d')
        nav_frame.pack(side="left", fill="y")
        
        # Navigation buttons
        button1 = tk.Button(nav_frame, text="Home", command=lambda: controller.show_frame("HomePage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button1.pack(pady=10)
        
        button2 = tk.Button(nav_frame, text="Favourites", command=lambda: controller.show_frame("FavouritesPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button2.pack(pady=10)
        
        button3 = tk.Button(nav_frame, text="Character Details", command=lambda: controller.show_frame("CharacterPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button3.pack(pady=10)

        # Main content area (center)
        content_frame = tk.Frame(self, bg='#004d99')
        content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        label = tk.Label(content_frame, text="Your Favourite Characters", font=("Helvetica", 24), bg='#004d99', fg='white')
        label.pack(pady=20)

        # Frame to hold images in a grid
        self.image_frame = tk.Frame(content_frame, bg='#004d99')
        self.image_frame.pack(fill="both", expand=True)

        # List of image paths
        self.image_paths = ["image4.jpg", "image5.jpg", "image6.jpg", "image7.jpg", "image8.jpg"]
        self.image_labels = []

        # Bind the window resize event
        self.bind("<Configure>", self.resize_images)
        
        self.load_images()

    def load_images(self):
        """Load and display images in a grid layout.""" 
        for index, img_path in enumerate(self.image_paths):
            try:
                image = Image.open(img_path)
                # Initially resize image to a default size
                image = image.resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                image_label = tk.Label(self.image_frame, image=photo, bg='#004d99')
                image_label.photo = photo  # Keep a reference to prevent garbage collection
                image_label.grid(row=index // 3, column=index % 3, padx=10, pady=10)  # Arrange images in 3 columns

                self.image_labels.append(image_label)

            except Exception as e:
                error_label = tk.Label(self.image_frame, text=f"Error loading {img_path}", bg='#004d99', fg='red')
                error_label.grid(row=index // 3, column=index % 3, padx=10, pady=10)

    def resize_images(self, event):
        """Resize images when the window size changes.""" 
        window_width = event.width
        window_height = event.height
        new_size = min(window_width // 4, window_height // 4)  # Calculate new size based on window size
        
        for index, img_path in enumerate(self.image_paths):
            try:
                # Resize each image dynamically based on the window size
                image = Image.open(img_path)
                image = image.resize((new_size, new_size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Update the image on the label
                self.image_labels[index].config(image=photo)
                self.image_labels[index].photo = photo  # Keep a reference to prevent garbage collection

            except Exception as e:
                pass  # Handle exceptions, like image not found or load errors

class CharacterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#004d99')
        self.controller = controller
        
        # Left-side navigation panel (buttons)
        nav_frame = tk.Frame(self, bg='#00264d')
        nav_frame.pack(side="left", fill="y")
        
        # Navigation buttons
        button1 = tk.Button(nav_frame, text="Home", command=lambda: controller.show_frame("HomePage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button1.pack(pady=10)
        
        button2 = tk.Button(nav_frame, text="Favourites", command=lambda: controller.show_frame("FavouritesPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button2.pack(pady=10)

        # Main content area (center)
        content_frame = tk.Frame(self, bg='#004d99')
        content_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)
        
        label = tk.Label(content_frame, text="Character Details", font=("Helvetica", 24), bg='#004d99', fg='white')
        label.pack(pady=20)

        # Search bar for entering character name
        self.entry = tk.Entry(content_frame, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        # Button to search for the character
        search_button = tk.Button(content_frame, text="Search", command=self.show_character_details, 
                                  font=("Helvetica", 14), bg='#ff6600', fg='white')
        search_button.pack(pady=10)

        # Display area for character details
        self.character_info = tk.Text(content_frame, height=10, width=50, font=("Helvetica", 12), bg='#003366', fg='white')
        self.character_info.pack(pady=20)

        # Clear button to clear the text area
        self.clear_button = tk.Button(content_frame, text="Clear", command=self.clear_text, font=("Helvetica", 14), bg='#ff6600', fg='white')
        self.clear_button.pack(pady=10)

    def show_character_details(self):
        """Show details of the entered character."""
        character_name = self.entry.get()
        try:
            # Perform API request or lookup
            if character_name in CHARACTER_DATA:
                character_info = CHARACTER_DATA[character_name]
                # Update the text area with character details
                self.character_info.delete("1.0", tk.END)
                details = f"Name: {character_info['Name']}\nHouse: {character_info['House']}\nWand: {character_info['Wand']}\nPatronus: {character_info['Patronus']}"
                self.character_info.insert(tk.END, details)
            else:
                self.character_info.delete("1.0", tk.END)
                self.character_info.insert(tk.END, "Character not found.")
        except Exception as e:
            self.character_info.delete("1.0", tk.END)
            self.character_info.insert(tk.END, f"Error: {str(e)}")

    def clear_text(self):
        """Clear the character details text box.""" 
        self.character_info.delete("1.0", tk.END)

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#004d99')
        self.controller = controller
        
        # Left-side navigation panel (buttons)
        nav_frame = tk.Frame(self, bg='#00264d')
        nav_frame.pack(side="left", fill="y")
        
        # Navigation buttons
        button1 = tk.Button(nav_frame, text="Home", command=lambda: controller.show_frame("HomePage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button1.pack(pady=10)
        
        button2 = tk.Button(nav_frame, text="Favourites", command=lambda: controller.show_frame("FavouritesPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button2.pack(pady=10)

        button3 = tk.Button(nav_frame, text="Character Details", command=lambda: controller.show_frame("CharacterPage"), 
                            font=("Helvetica", 14), bg='#ff6600', fg='white', width=15)
        button3.pack(pady=10)

        # Main content area (center)
        content_frame = tk.Frame(self, bg='#004d99')
        content_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)
        
        label = tk.Label(content_frame, text="Information Page", font=("Helvetica", 24), bg='#004d99', fg='white')
        label.pack(pady=20)

        info_text = tk.Label(content_frame, text="The Harry Potter universe, created by author J. K. Rowling, is a fictional reality.", 
                             font=("Helvetica", 14), bg='#004d99', fg='white')
        info_text.pack(pady=20)

    def mainloop(self):
        """Start the Tkinter event loop.""" 
        super().mainloop()

if __name__ == "__main__":
    app = HarryPotterApp()
    app.mainloop()  # Added to start the Tkinter event loop
