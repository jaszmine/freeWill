import time
import sys
import random
from pydub import AudioSegment
from pydub.playback import play
import threading

# get ready for the greatest code you've ever seen absolutely LITTERED with sprinkles of joy (comments)

tree = [
    "          *  ",
    "         ***  ",
    "        *****  ",
    "       *******  ",
    "       *******  ",
    "      *********  ",
    "      *********  ",
    "     ***********  ",
    "     ***********  ",
    "    *************   ",
    "    *************  ",
    "   ***************  ",
    "   ***************  ",
    "  *****************  ",
    "  *****************  ",
    " ******************* ",
    "*********************",
    "         |||        ",
    "         |||        ",
]

# time in seconds from start and the text
the_actual_gospel = [
    # start at 2:42 in music video
    (0.0, "A crowded room, friends with tired eyes"),
    (5.0, "I'm hiding from you and your soul of ice"),
    (8.7, "My god I thought you were someone to rely onh"),
    (12.5, "Me? ........... I guess I was a shoulder to cry on"),
    (15.5, ""),
    (17.0, "A   face on a lover with a fire in his heart      "),
    (22.0, "A man under cover but you toooooooooooooooore meeeee aaapaaaaaaaaaaaaaaart"),
    (28.0, "ooooooooohhhhhhhhhh"),
    (30.0, "Now I've found a real love you'll never fool me again"),
    (34.8, ""),
    (35.9, "Last Christmas, I gave you my heart"),
    (39.0, "But the \033[4mvery\033[0m \033[4mnext\033[0m \033[4mday\033[0m, you gave it away, u gave it away :("),
    (44.0, "Thiiiiiis yearrrrr, to save me from tears"),
    (48.0, "I'll give it to someone special,          specialll"),
    (51.0, ""),
    (53.0, "Last Christmas, I gave you my heaaaaaart"),
    (57.0, "But the very next day, you gaaaaaaaaaave meeeee awaaaaaaaaaaay"),
    (62.0, "This yearrr,    to save - me  -  from   -   tears"),
    (66.0, "I'll give it to someone special, speciallllllllll"),
    (68.5, ""),
    (71.0, "A face on a lover with a fire in his heart"),
    (75.0, "A man under cover but you tore him apart"),
    (80.0, "Maybe ... next year ........... "),
    (84.0, "I'll give it to someone"),
    (87.0, "I'll give it to someone ssssspecialllll"),
    (90.0, "speciAaAaalll .....    "),
    (94.0, "someoneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"),
    (97.0, "     "),
]

the_most_insane_way_to_reference_colors = {
    'R': "\033[31m", # Red
    'G': "\033[32m", # Green
    'Y': "\033[33m", # Yellow
    'B': "\033[34m", # Blue 
    'M': "\033[35m", # Magenta
    'C': "\033[36m", # Cyan i think?? who knows tbh
}
reset_color = "\033[0m"


# Animation parameters (they're capitalized bc they're important bro)

# (1 / 0.05 = 20) --> screen updates 20 times per second
LYRIC_TICK_DELAY = 0.05   # Controls how frequently the screen updates and lyrics advance (Fast for smooth typing)

# colors of the tree update time
COLOR_UPDATE_DELAY = 0.5  # Controls how frequently the tree colors flicker (Slower, independent rate)

# characters of the lyric updates per tick
CHARACTERS_PER_FRAME = 1  # Typing speed (characters per LYRIC_TICK_DELAY)

# load and trim audio at 2:42 (162 seconds)
try:
    full_audio = AudioSegment.from_wav("wamalama.wav")
    trimmed_audio = full_audio[162.5*1000:]  # convert seconds to milliseconds
    audio_loaded = True
except Exception as e:
    print(f" - Audio file error: {e}")
    print("- Continuing without audio...")
    audio_loaded = False

# play audio in a separate thread
def play_audio(audio_segment):
    play(audio_segment)

# clears console screen and resets the cursor.
def clear_console():
    sys.stdout.write("\033c")
    sys.stdout.flush()

# generates one tree row w/ randomly colored lights. (color logic)
def get_random_colored_row(row, colors, reset_color):
    colored_row = ""
    for char in row:
        if char == '*':
            # randomly pick color for the light
            color_key = random.choice(list(colors.keys()))
            colored_row += colors[color_key] + char + reset_color
        else:
            colored_row += char
    return colored_row

# generates a list representing the entire tree with randomized colors
def generate_colored_tree(tree_data, colors, reset_color):
    return [get_random_colored_row(row, colors, reset_color) for row in tree_data]

# prints final screen, duh
def print_outro(colors, reset_color):
    clear_console()
    
    # use the color logic for the final star! <3
    star = get_random_colored_row(" * ", colors, reset_color)
    
    print(f"          {star.strip()}  ")
    print("         ***  ")
    print("        *****  ")
    print("       *******  ")
    print("       *******  ")
    print("      *********  ")
    print("      *********  ")
    print("     ***********                  Merry   ")
    print("     ***********                  Christmas!!   ")
    print("    *************   ")
    print("    *************                 (DONT go giving someone's heart away)")
    print("   ***************  ")
    print("   ***************  ")
    print("  *****************  ")
    print("  *****************  ")
    print(" ******************* ")
    print("*********************")
    print("         |||        ")
    print("         |||        ")

# handles main animation loop, coordinating tree color & lyric display
# main timing and rendering logic
def run_animation(tree_data, lyrics_data, colors, reset_color, lyric_tick_delay, color_update_delay, chars_per_frame):
    
    # start audio at exactly 2:42 ish
    if audio_loaded:
        # play audio in a separate thread so animation continues
        audio_thread = threading.Thread(target=play_audio, args=(trimmed_audio,))
        audio_thread.daemon = True
        audio_thread.start()
    
    start_time = time.time()
    
    # state & color vars
    start_time = time.time()
    lyric_index = 0
    char_index = 0  
    displayed_lyrics = []
    last_color_update_time = 0.0
    current_colored_tree = generate_colored_tree(tree_data, colors, reset_color) # initial color generation
    
    clear_console() 
    
    try:
        while True:
            current_time = time.time() - start_time
            current_lyric_text = ""
            
            # --- color Update Logic (separately timed) ---
            # check if enough time has passed to update the colors
            if current_time >= last_color_update_time + color_update_delay:
                current_colored_tree = generate_colored_tree(tree_data, colors, reset_color)
                last_color_update_time = current_time
            
            # --- lyric typing logic (reads timing data) ---
            if lyric_index < len(lyrics_data):
                if current_time >= lyrics_data[lyric_index][0]:
                    
                    # advance character index (typing progress)
                    char_index += chars_per_frame
                    
                    # determine the partially typed lyric
                    full_line = lyrics_data[lyric_index][1]
                    current_lyric_text = full_line[:char_index]
                    
                    # check if the line is finished typing
                    if char_index >= len(full_line):
                        # if yerp, add it to history and move to the next lyric
                        if full_line:
                            displayed_lyrics.append(full_line)
                            # keep only last few lyrics to fit screen
                            if len(displayed_lyrics) > len(tree_data): 
                                displayed_lyrics.pop(0)
                                
                        lyric_index += 1
                        char_index = 0
            
            # --- render(ing that) logic silly goose ---
            
            clear_console()
            
            # render the pre-colored tree and history
            for i, colored_row in enumerate(current_colored_tree):
                # add the completed lyric lines next to the tree
                lyric_display = ""
                if i < len(displayed_lyrics):
                    lyric_display = displayed_lyrics[i]
                
                print(colored_row + f"    {lyric_display}")

            # print the currently typing lyric below the tree
            print() 
            print(current_lyric_text)
            
            if lyric_index >= len(lyrics_data) and not current_lyric_text:
                break
            
            # --- wait for next frame (uses the lyric tick delay) ---
            time.sleep(lyric_tick_delay)

    except KeyboardInterrupt:
        pass

# ya i do write main like __main__ we been knew girlie pop
if __name__ == "__main__":
    # pass params to the animation function
    run_animation(
        tree, 
        the_actual_gospel, 
        the_most_insane_way_to_reference_colors, 
        reset_color, 
        LYRIC_TICK_DELAY, 
        COLOR_UPDATE_DELAY,
        CHARACTERS_PER_FRAME
    )
    print_outro(the_most_insane_way_to_reference_colors, reset_color)