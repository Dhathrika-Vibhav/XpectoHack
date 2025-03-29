import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageDraw
import os

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Welcome to ByteBuddy")
        self.splash.configure(bg='#1E1E1E')
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            icon = tk.PhotoImage(file=icon_path)
            self.splash.iconphoto(False, icon)
        except Exception as e:
            print(f"Could not load window icon: {e}")
        
        # Adjust window size to fit content better
        window_width = 500  # Increased width to accommodate the quote
        window_height = 350  # Slightly increased height for better spacing
        
        # Center the window on screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create logo frame with adjusted padding
        logo_frame = tk.Frame(self.splash, bg='#1E1E1E')
        logo_frame.pack(pady=30)  # Increased padding
        
        # Fancy logo with adjusted size
        logo_text = "ByteBuddy"
        logo_label = tk.Label(logo_frame, 
                            text=logo_text,
                            font=('Comic Sans MS', 36, 'bold'),  # Increased font size
                            fg='#00ff00',
                            bg='#1E1E1E')
        logo_label.pack()
        
        # Decorative underline with adjusted width
        underline = tk.Frame(logo_frame, bg='#00ff00', height=3, width=300)  # Increased width
        underline.pack(pady=10)
        
        # Tagline with adjusted spacing
        tagline = tk.Label(logo_frame,
                          text="Not just an AI, your digital ally",
                          font=('Comic Sans MS', 16, 'italic'),  # Increased font size
                          fg='white',
                          bg='#1E1E1E')
        tagline.pack(pady=20)
        
        # Use button with adjusted position
        self.use_button = tk.Button(self.splash,
                                  text="Use ByteBuddy",
                                  command=self.launch_main_app,
                                  bg='#4CAF50',
                                  fg='white',
                                  font=('Comic Sans MS', 14, 'bold'),  # Increased font size
                                  padx=25,
                                  pady=12)
        self.use_button.pack(pady=30)  # Increased padding
        
    def launch_main_app(self):
        self.splash.destroy()
        root = tk.Tk()
        app = ByteBuddy(root)
        root.mainloop()

class ByteBuddy:
    """A class that implements a chat interface using Google's Gemini 1.5 Flash model"""
    
    def __init__(self, root):
        self.window = root
        self.window.title("ByteBuddy")
        self.window.configure(bg='#1E1E1E')
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.png")
            icon = tk.PhotoImage(file=icon_path)
            self.window.iconphoto(True, icon)
        except Exception as e:
            print(f"Could not load window icon: {e}")
        
        self.window.minsize(800, 800)
        
        self.api_key = "AIzaSyBezEr0nat_ri_mV8gtTk3UgIyWW66WbE8"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Animation state
        self.animation_running = True
        
        # Create top frame for animation and new chat button
        top_frame = tk.Frame(self.window, bg='#1E1E1E')
        top_frame.pack(side=tk.TOP, anchor='ne', padx=20, pady=10)
        
        # New Chat button
        self.new_chat_button = tk.Button(top_frame,
                                       text="New Chat",
                                       command=self.open_new_chat,
                                       bg='#4CAF50',
                                       fg='white',
                                       activebackground='#45a049',
                                       activeforeground='white',
                                       font=('Comic Sans MS', 12),
                                       padx=15,
                                       pady=5)
        self.new_chat_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create animation frame with specific size
        self.animation_frame = tk.Frame(top_frame, bg='#1E1E1E', width=150, height=150)
        self.animation_frame.pack(side=tk.LEFT)
        
        # Load running animation
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.running_man_frames = self.load_animation(os.path.join(script_dir, "running_man.gif"))
            
            self.animation_label = tk.Label(self.animation_frame, bg='#1E1E1E')
            self.animation_label.place(relx=1.0, rely=0.0, anchor='ne')
            self.animation_label.configure(bg='#1E1E1E')
            
            # Add "Running..." text below the animation
            self.running_text = tk.Label(self.animation_frame, 
                                       text="Running...", 
                                       bg='#1E1E1E', 
                                       fg='white',
                                       font=('Comic Sans MS', 10))
            self.running_text.place(relx=1.0, rely=1.0, anchor='se')
            
            self.animate_running_man(0)
            
        except Exception as e:
            print(f"Could not load animation: {e}")
        
        # Create main frame for chat
        self.main_frame = tk.Frame(self.window, bg='#1E1E1E')
        self.main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.main_frame, text="Welcome to ByteBuddy!", bg='#1E1E1E', fg='#FFFFFF', 
                             font=('Comic Sans MS', 14))
        self.label.pack(anchor='w')

        self.chat_history = scrolledtext.ScrolledText(self.main_frame, state='disabled', width=70, height=20,
                                                     bg='#2D2D2D', fg='#FFFFFF', font=('Comic Sans MS', 12))
        self.chat_history.pack(anchor='w', fill=tk.BOTH, expand=True, pady=5)

        self.entry_label = tk.Label(self.main_frame, text="Enter your prompt:", bg='#1E1E1E', fg='#FFFFFF',
                                   font=('Comic Sans MS', 12))
        self.entry_label.pack(anchor='w')

        self.user_input = tk.Entry(self.main_frame, width=70, bg='#2D2D2D', fg='#FFFFFF', 
                                  insertbackground='#FFFFFF', font=('Comic Sans MS', 12))
        self.user_input.pack(anchor='w', fill=tk.X, pady=(5, 10))
        self.user_input.bind('<Return>', self.process_input)

        self.send_button = tk.Button(self.main_frame, text="Send", command=self.process_input,
                                   bg='#4CAF50', fg='white', activebackground='#45a049', 
                                   activeforeground='white', font=('Comic Sans MS', 12),
                                   padx=20, pady=5)
        self.send_button.pack(anchor='w', pady=(0, 10))

    def load_animation(self, image_path):
        frames = []
        image = Image.open(image_path)
        
        try:
            while True:
                frame = image.copy()
                frame = frame.resize((80, 50), Image.Resampling.LANCZOS)
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                data = frame.getdata()
                newData = []
                for item in data:
                    if item[3] > 100 and sum(item[0:3]) < 500:
                        newData.append((255, 255, 255, 255))
                    else:
                        newData.append((0, 0, 0, 0))
                frame.putdata(newData)
                
                frames.append(ImageTk.PhotoImage(frame))
                image.seek(len(frames))
        except EOFError:
            pass
        
        return frames

    def animate_running_man(self, frame_index):
        if hasattr(self, 'running_man_frames') and self.running_man_frames:
            if not self.animation_running:
                self.running_text.configure(text="Thinking...")
                return
            
            self.animation_label.configure(image=self.running_man_frames[frame_index])
            self.running_text.configure(text="Running...")
            next_frame = (frame_index + 1) % len(self.running_man_frames)
            self.window.after(100, self.animate_running_man, next_frame)

    def toggle_animation(self, running=True):
        self.animation_running = running
        if running:
            self.animate_running_man(0)

    def process_input(self, event=None):
        user_query = self.user_input.get()
        if not user_query.strip():
            return

        self.toggle_animation(False)  # Pause animation and show "Thinking..."
        
        self.user_input.delete(0, tk.END)
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"\nYou: {user_query}\n", 'user')
        self.chat_history.insert(tk.END, f"\nBytebuddy: ", 'assistant')
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')
        self.chat_history.update()

        try:
            response = self.model.generate_content(user_query)
            response_text = response.text
        except Exception as e:
            response_text = f"An error occurred: {str(e)}"

        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{response_text}\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')
        
        self.toggle_animation(True)  # Resume animation and show "Running..."
    
    def open_new_chat(self):
        """Clear chat history for a new conversation"""
        self.chat_history.configure(state='normal')
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.insert(tk.END, "Starting a new chat...\n", 'system')
        self.chat_history.tag_configure('system', foreground='#FFD700')
        self.chat_history.configure(state='disabled')

    def get_response(self, query):
        """Get response from the model"""
        try:
            # Check for identity-related questions
            identity_keywords = ["who are you", "what are you", "tell me about yourself", 
                              "your creator", "who made you", "who created you"]
            
            if any(keyword in query.lower() for keyword in identity_keywords):
                return "I am ByteBuddy, an AI assistant created by Vibhav. I'm here to help you with any questions or tasks you may have!"
            
            response = self.model.generate_content(query)
            return response.text
        except Exception as e:
            return f"An error occurred: {str(e)}"

def create_icon():
    img = Image.new('RGBA', (48, 48), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    draw.line([(8, 8), (8, 40)], fill=(0, 0, 0, 255), width=3)
    draw.line([(40, 8), (40, 40)], fill=(0, 0, 0, 255), width=3)
    points = [(16, 12), (24, 36), (32, 12)]
    draw.line(points, fill=(0, 0, 0, 255), width=3)
    
    img.save('icon.png')

create_icon()

if __name__ == "__main__":
    splash = SplashScreen()
    splash.splash.mainloop()
