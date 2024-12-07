import tkinter as tk
from tkinter import messagebox
import psycopg2
from tkinter import ttk

# Database connection configuration
db_password = "Asd1010420"

def search_database(search_term, search_type):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="Listen",
            user="postgres",
            host="localhost",
            port="5433",
            password=db_password
        )
        with conn:
            with conn.cursor() as cur:
                # Perform search based on selected type
                if search_type == "Song":
                    query = """
                        SELECT 
                            s.Song_id, 
                            s.Title, 
                            a.Name AS Artist, 
                            s.Audio_file AS URL 
                        FROM SONG s
                        JOIN ARTIST a ON s.Artist_id = a.Artist_id
                        WHERE s.Title ILIKE %s
                    """
                elif search_type == "Album":
                    query = "SELECT Album_id, Title FROM ALBUM WHERE Title ILIKE %s"
                elif search_type == "Artist":
                    query = "SELECT Artist_id, Name FROM ARTIST WHERE Name ILIKE %s"
                else:
                    messagebox.showerror("Error", "Invalid search type!")
                    return
                
                cur.execute(query, (f"%{search_term}%",))
                results = cur.fetchall()

                # Display results
                display_results(results, search_type)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def display_results(results, search_type):
    # Clear previous results
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Display clickable results
    if not results:
        tk.Label(
            scrollable_frame, text="No results found.", font=("Arial", 14)
        ).pack(fill="x", pady=10)
    else:
        for result in results:
            if search_type == "Song":
                display_text = f"{result[1]} by {result[2]}"
            else:
                display_text = f"{result[1]}"

            # Create a block for each result
            result_frame = tk.Frame(scrollable_frame, width=385, bd=1, relief="solid", padx=10, pady=10)
            result_frame.pack(fill="x", expand=True, padx=0, pady=0)  # No margins between blocks

            result_label = tk.Label(result_frame, text=display_text, font=("Arial", 14), anchor="w", justify="left")
            result_label.pack(fill="x")

            # Bind a click event to the result block
            result_frame.bind("<Button-1>", lambda e, r=result, st=search_type: result_clicked(r, st))
            result_label.bind("<Button-1>", lambda e, r=result, st=search_type: result_clicked(r, st))

def result_clicked(result, search_type):
    if search_type == "Song":
        # Update the right-side music player with the clicked song's details
        song_id, title, artist, url = result
        update_player((song_id, title, artist, url))  # Pass the song details to the player update function

    else:
        # Handle non-song search types (Album, Artist)
        messagebox.showinfo(
            f"{search_type} Selected",
            f"You selected: {result[1]} (ID: {result[0]})"
        )

def on_search(*args):
    search_term = search_input.get().strip()
    search_type = search_type_var.get()
    if not search_term:
        # Clear results if search term is empty
        display_results([], search_type)
        return
    search_database(search_term, search_type)

# Mock function for playing/stopping songs
def toggle_play():
    if play_button["text"] == "Play":
        play_button["text"] = "Stop"
    else:
        play_button["text"] = "Play"

def update_player(song_details):
    # Update player UI elements with song details
    song_title_label.config(text=song_details[1])
    artist_label.config(text=f"by {song_details[2]}")
    # Simulate loading a cover image (use a placeholder for this example)
    cover_image_label.config(text="🎵", font=("Arial", 50))  # Placeholder emoji
    time_bar["value"] = 0

# Enable mouse wheel scrolling
def on_mouse_wheel(event):
    # Adjust scrolling for the canvas, ensuring compatibility for both directions
    # print(event.delta, event.num)
    if event.delta:  # For Windows and macOS
        results_canvas.yview_scroll(-1* event.delta, "units")

        
# GUI setup
app = tk.Tk()
app.title("Music Database Search")
app.geometry("800x400")  # Increased width for player

# Search section
search_frame = tk.Frame(app, width=400, relief="solid", bd=1)
search_frame.pack(side="left", fill="both", expand=True)


tk.Label(search_frame, text="Search Term:", font=("Arial", 12)).pack(pady=5)
search_input = tk.Entry(search_frame, font=("Arial", 12), width=30)
search_input.pack(pady=5)
# Bind the input change event to the `on_search` function
search_input.bind("<KeyRelease>", on_search)


search_type_var = tk.StringVar(value="Song")
tk.Label(search_frame, text="Search Type:", font=("Arial", 12)).pack(pady=5)
search_type_menu = tk.OptionMenu(search_frame, search_type_var, "Song", "Album", "Artist")
search_type_menu.pack(pady=5)

# Scrollable results frame setup
results_canvas = tk.Canvas(search_frame, height=400, highlightbackground="black", highlightthickness=1)
scrollable_frame = tk.Frame(results_canvas)

# Add the scrollbar inside the canvas
scrollbar = tk.Scrollbar(results_canvas, orient="vertical", command=results_canvas.yview)
results_canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame.bind(
    "<Configure>",
    lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
)
results_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Bind mouse wheel scrolling to the canvas
results_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Pack the canvas and scrollbar inside the same frame
results_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Music player section
player_frame = tk.Frame(app, width=400, relief="solid", bd=1, bg="white")
player_frame.pack(side="right", fill="both", expand=True)

cover_image_label = tk.Label(player_frame, text="🎵", font=("Arial", 50), bg="white")
cover_image_label.pack(pady=10)

song_title_label = tk.Label(player_frame, text="Song Title", font=("Arial", 14), bg="white")
song_title_label.pack(pady=5)

artist_label = tk.Label(player_frame, text="by Artist", font=("Arial", 12), bg="white", fg="gray")
artist_label.pack(pady=5)

time_bar = ttk.Progressbar(player_frame, orient="horizontal", mode="determinate", length=300)
time_bar.pack(pady=10)

play_button = tk.Button(player_frame, text="Play", command=toggle_play, font=("Arial", 12))
play_button.pack(pady=5)

volume_label = tk.Label(player_frame, text="Volume", font=("Arial", 12), bg="white")
volume_label.pack(pady=5)

volume_scale = ttk.Scale(player_frame, from_=0, to=100, orient="horizontal")
volume_scale.set(50)  # Default volume level
volume_scale.pack(pady=5)

app.mainloop()