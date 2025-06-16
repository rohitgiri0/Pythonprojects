import json

# YouTube Video Manager Program
# This program allows users to manage a list of YouTube videos by adding, listing,
# updating, and deleting video entries stored in a JSON file.

# File name where video data is stored
yt_file = "yt_info.txt"

# Load video data from file, return empty list if file doesn't exist or is invalid
def load_data():
    """
    Loads video data from the yt_info.txt file.
    Returns a list of video dictionaries.
    """
    try:
        with open(yt_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save video data to file
def save_data(videos):
    """
    Saves the current video list to the yt_info.txt file in JSON format.
    """
    with open(yt_file, 'w') as file:
        json.dump(videos, file)

# List all videos with their index, name, and duration
def list_all(videos):
    """
    Displays all videos in the list with their name and duration.
    """
    if not videos:
        print("No videos found.")
        return 
    print("\nAll YouTube Videos:")
    for index, video in enumerate(videos, start=1):
        print(f"{index}. Name: {video.get('name', 'Unknown')}, Duration: {video.get('duration', 'Unknown')}")

# Add a new video to the list
def add_video(videos):
    """
    Prompts user to enter video name and duration, then adds it to the list.
    """
    name = input("Enter video name: ")
    duration = input("Enter the duration of your video: ")
    videos.append({"name": name, "duration": duration})
    save_data(videos)
    print("Video added successfully.")

# Update existing video information
def update_video(videos):
    """
    Prompts user to update the name and/or duration of a selected video.
    """
    list_all(videos)
    if not videos:
        return
    try:
        index = int(input("Enter the number of the video to update: ")) - 1
        if 0 <= index < len(videos):
            name = input("Enter new name (leave blank to keep current): ")
            duration = input("Enter new duration (leave blank to keep current): ")
            if name:
                videos[index]["name"] = name
            if duration:
                videos[index]["duration"] = duration
            save_data(videos)
            print("Video updated successfully.")
        else:
            print("Invalid video number.")
    except ValueError:
        print("Please enter a valid number.")

# Delete a video from the list
def delete_video(videos):
    """
    Prompts user to select a video to delete from the list.
    """
    list_all(videos)
    if not videos:
        return
    try:
        index = int(input("Enter the number of the video to delete: ")) - 1
        if 0 <= index < len(videos):
            del videos[index]
            save_data(videos)
            print("Video deleted successfully.")
    except ValueError:
        print("Please enter a valid number.")

# Main application loop
def main():
    """
    Main function that shows a menu and handles user interaction.
    """
    videos = load_data()
    while True:
        print("\nYouTube Manager | Choose an option:")
        print("1. List all YouTube videos")
        print("2. Add a YouTube video")
        print("3. Update a YouTube video")
        print("4. Delete a YouTube video")
        print("5. Exit")
        choice = input("Enter your choice: ")
        match choice:
            case '1':
                list_all(videos)
            case '2':
                add_video(videos)
            case '3':
                update_video(videos)
            case '4':
                delete_video(videos)
            case '5':
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter a number from 1 to 5.")

# Entry point
if __name__ == "__main__":
    main()