import csv
import time
import os

DATA_FILE = "storage.csv"

#Utility Functions

def create_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["topic", "slide_number", "title", "prompt"])

def load():
    data = {}
    if not os.path.exists(DATA_FILE):
        return data
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = row["topic"]
            if topic not in data:
                data[topic] = []
            data[topic].append({
                "slide_number": int(row["slide_number"]),
                "title": row["title"],
                "prompt": row["prompt"]
            })
    return data

def save(data):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["topic", "slide_number", "title", "prompt"])
        for topic, slides in data.items():
            for slide in slides:
                writer.writerow([
                    topic,
                    slide["slide_number"],
                    slide["title"],
                    slide["prompt"]
                ])

def generate_prompt(slide_title):
    title = slide_title.lower()
    if "intro" in title:
        return "Introduce the topic and explain why it is important."
    elif "application" in title:
        return "Discuss real-world applications with examples."
    elif "advantage" in title:
        return "Explain benefits and positive impacts."
    elif "disadvantage" in title:
        return "Explain limitations or challenges."
    elif "conclusion" in title:
        return "Summarize key points and give a closing statement."
    elif "definition" in title:
        return "Define the concept clearly with examples."
    elif "types" in title:
        return "Explain different types with brief descriptions."
    elif "outro" in title:
        return "End the Presentation with some closing thoughts."
    else:
        return "Explain this slide clearly with key details."

def create(data):
    topic = input("Enter presentation topic: ").strip().lower()
    if not topic:
        print("Topic cannot be empty.")
        return
    if topic in data:
        print("Presentation already exists.")
        return
    try:
        n = int(input("Enter number of slides: "))
    except ValueError:
        print("Invalid input.")
        return
    slides = []
    for i in range(n):
        title = input(f"Enter title for Slide {i+1}: ").strip()
        slides.append({
            "slide_number": i + 1,
            "title": title,
            "prompt": generate_prompt(title)
        })
    data[topic] = slides
    save(data)
    print("\nPresentation created successfully.\n")

def view(data):
    if not data:
        print("No presentations found.")
        return
    print("\nAvailable Presentations:")
    for i, topic in enumerate(data.keys(), 1):
        print(f"{i}. {topic}")

def view_notes(data):
    view(data)
    topic = input("\nEnter topic name to view notes: ").strip().lower()
    if topic not in data:
        print("Presentation not found.")
        return
    print(f"\nNotes for: {topic}\n")
    for slide in sorted(data[topic], key=lambda x: x["slide_number"]):
        print(f"Slide {slide['slide_number']}: {slide['title']}")
        print(f"Prompt: {slide['prompt']}\n")

def timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Time left: {i}s", end="\r")
        time.sleep(1)
    print("\nTime's up.\n")

def practice(data):
    view(data)
    topic = input("\nEnter topic name to practice: ").strip().lower()
    if topic not in data:
        print("Presentation not found.")
        return
    try:
        duration = int(input("Enter time per slide (in seconds): "))
    except ValueError:
        print("Invalid input.")
        return
    print("\nPractice Mode Starting...\n")
    input("Press Enter to begin...")
    for slide in sorted(data[topic], key=lambda x: x["slide_number"]):
        print(f"\nSlide {slide['slide_number']}: {slide['title']}")
        print(f"Prompt: {slide['prompt']}")
        timer(duration)

def delete(data):
    view(data)
    topic = input("\nEnter topic name to delete: ").strip().lower()
    if topic not in data:
        print("Presentation not found.")
        return
    confirm = input("Are you sure you want to delete? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return
    del data[topic]
    save(data)
    print("Presentation deleted.")

#Main Menu

def main():
    create_file()
    data = load()
    while True:
        print("\n====== Smart Presentation Assistant ======")
        print("1. Create Presentation")
        print("2. View Presentations")
        print("3. View Notes")
        print("4. Practice Mode")
        print("5. Delete Presentation")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            create(data)
            data = load()
        elif choice == "2":
            view(data)
        elif choice == "3":
            view_notes(data)
        elif choice == "4":
            practice(data)
        elif choice == "5":
            delete(data)
            data = load()
        elif choice == "6":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()