# This script is written by ShadowDara
# Github: https://github.com/shadowdara

import os
import fnmatch
import re
import time

def display_menu():
    while True:
        print("\n === Search Machine Menu ===")
        print(" ")
        print("   0) Exit Programm")
        print("   1) Search for a Word")
        print("   2) Search for a Filename")
        print("   3) Search for a Foldername")
        print("   4) Search for large Files")
        print("   5) Search with File extension / edit Time")

        choice = input("\n Select a version or type 0 to exit: ").strip()

        if choice == '0':
            print(" Exiting program. Goodbye!")
            break
        elif choice == '1':
            print("\n Searching for Words...\n")
            run_search_word()
        elif choice == '2':
            print("\n Searching for Filenames...\n")
            run_search_filenames()
        elif choice == '3':
            print("\n Searching for Foldernames...\n")
            run_search_folder()
        elif choice == '4':
            print("\n Searching for large Files...\n")
            run_largest_files()
        elif choice == '5':
            print("\n Searching with File extension / edit Time\n")
            run_search_by_file_type()
        elif choice == '5027':
            hack()
        else:
            print(" Invalid input. Please select a valid option.")

def run_search_word():
    directory = os.path.dirname(os.path.abspath(__file__))

    while True:
        search_word = input("\n Enter the word to search for (or type '/exit' to quit): ").strip()

        if search_word.lower() == '/exit':
            break

        search_results = search_word_in_files(directory, search_word)
        search_word_print_results(search_results)

def search_word_in_files(directory, search_word, file_types=('*.txt', '*.md', '*.html', '*.htm', '*.json', '*.mcfunction', '*.log')):
    """
    Search for a word in multiple .txt .md .html .htm .json . mcfunction .log files in a directory and its subdirectories.

    :param directory: The directory to search.
    :param search_word: The word to search for.
    :param file_types: The types of files to search
    :return: A dictionary with filenames as keys and lists of results as values.
    """
    results = {}

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        # Filter files based on the file_types pattern
        for file_type in file_types:
            for filename in fnmatch.filter(files, file_type):
                filepath = os.path.join(root, filename)

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.readlines()

                # Search for the word in each line
                for line_number, line in enumerate(content, start=1):
                    # Use regex to find whole words (adjust pattern if partial match is acceptable)
                    if re.search(rf'\b{search_word}\b', line, re.IGNORECASE):
                        if filepath not in results:
                            results[filepath] = []
                        results[filepath].append((line_number, line.strip()))
    
    return results

def search_word_print_results(results):
    """
    Print the search results in a readable format.

    :param results: The dictionary with search results.
    """
    if not results:
        print("No matches found.")
    else:
        for filepath, matches in results.items():
            print(f"\nIn file: {filepath}")
            for line_number, line in matches:
                print(f"  Line {line_number}: {line}")

def run_search_folder():
    directory = os.path.dirname(os.path.abspath(__file__))
    while True:
        search_word = input("\n Enter the word to search for in folder names (or type '/exit' to quit): ").strip()
        if search_word.lower() == '/exit':
            return
        search_results = search_folders(directory, search_word)
        search_folders_print_results(search_results)

def search_folders(directory, search_word):
    """
    Search for folder names that contain the search_word in a directory and its subdirectories.

    :param directory: The directory to search.
    :param search_word: The word to search for in folder names.
    :return: A list of folder paths that match the search_word in their name.
    """
    results = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        # Check each directory name
        for foldername in dirs:
            # Check if the search_word is in the folder name (case-insensitive)
            if search_word.lower() in foldername.lower():
                folderpath = os.path.join(root, foldername)
                results.append(folderpath)
    
    return results

def search_folders_print_results(results):
    """
    Print the search results in a readable format.

    :param results: The list of folder paths.
    """
    if not results:
        print(" No matches found.")
    else:
        for folderpath in results:
            print(f" Folder found: {folderpath}")

def run_largest_files():
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = input(f" Enter the directory to search (or press Enter for current directory: {directory}): ").strip() or directory
    top_n = 100
    largest_files = get_largest_files(directory, top_n)
    print_largest_files(largest_files)
    input("\n Press Enter to return to the menu...")

def get_largest_files(directory, top_n=100):
    """
    Find the largest files in a directory and its subdirectories.

    :param directory: The directory to search.
    :param top_n: The number of largest files to return (default is 100).
    :return: A list of tuples containing file sizes and their paths, sorted by size.
    """
    file_sizes = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            try:
                # Get the size of the file
                file_size = os.path.getsize(filepath)
                # Add the file size and path to the list
                file_sizes.append((file_size, filepath))
            except OSError as e:
                print(f" Error accessing file {filepath}: {e}")

    # Sort the list by file size in descending order
    file_sizes.sort(reverse=True, key=lambda x: x[0])

    # Return the top 'n' largest files
    return file_sizes[:top_n]

def print_largest_files(file_sizes):
    """
    Print the largest files in a readable format, showing size first and then the file path.

    :param file_sizes: A list of tuples with file sizes and paths.
    """
    if not file_sizes:
        print(" No files found.")
    else:
        print(f"\n The {len(file_sizes)} largest files are:")
        for size, filepath in file_sizes:
            print(f"{size / (1024 * 1024):.2f} MB - {filepath}")

def run_search_by_file_type():
    """
    Führt die Suche nach Dateien eines bestimmten Typs aus und sortiert nach Änderungsdatum.
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = input(f" Enter the directory to search (or press Enter for current directory: {directory}): ").strip() or directory
    file_type = input(" Enter the file type to search for (e.g., *.txt, *.log) or press Enter for all files: ").strip() or "*.*"
    top_n = 50  # Anzahl der neuesten Dateien
    files = get_newest_files_by_type(directory, file_type, top_n)
    print_files_by_type(files)

    # Warte auf Benutzereingabe, bevor das Menü zurückkehrt
    input("\n Press Enter to return to the menu...")

def get_newest_files_by_type(directory, file_type="*.*", top_n=50):
    """
    Findet die neuesten Dateien eines bestimmten Typs in einem Verzeichnis und dessen Unterverzeichnissen.

    :param directory: Das Verzeichnis, in dem gesucht werden soll.
    :param file_type: Der Dateityp, nach dem gesucht werden soll (z.B. *.txt).
    :param top_n: Anzahl der zurückgegebenen Dateien.
    :return: Eine Liste der neuesten Dateien sortiert nach Änderungsdatum.
    """
    file_dates = []

    # Durchlaufe das Verzeichnis und Unterverzeichnisse
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, file_type):  # Filtere nach dem Dateityp
            filepath = os.path.join(root, filename)
            try:
                file_mtime = os.path.getmtime(filepath)  # Änderungsdatum
                file_dates.append((file_mtime, filepath))
            except OSError as e:
                print(f"Error accessing file {filepath}: {e}")

    # Sortiere nach dem Änderungsdatum (neuste zuerst)
    file_dates.sort(reverse=True, key=lambda x: x[0])

    # Gib nur die top_n neuesten Dateien zurück
    return file_dates[:top_n]

def print_files_by_type(file_dates):
    """
    Gibt die Dateien eines bestimmten Typs in einem lesbaren Format aus.
    """
    if not file_dates:
        print("No files found.")
    else:
        print(f"\nThe {len(file_dates)} newest files of the specified type are:")
        for mtime, filepath in file_dates:
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            print(f"{formatted_time} - {filepath}")

def search_filenames(directory, search_term):
    """
    Search for filenames that contain the search_term in a directory and its subdirectories.

    :param directory: The directory to search.
    :param search_term: The term to search for in filenames.
    :return: A list of matching file paths.
    """
    results = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the search term is in the filename (case-insensitive)
            if search_term.lower() in filename.lower():
                results.append(os.path.join(root, filename))

    return results

def search_filenames_print_results(results):
    """
    Print the search results in a readable format.

    :param results: The list of matching file paths.
    """
    if not results:
        print("No matches found.")
    else:
        print(f"\n{len(results)} match(es) found:")
        for filepath in results:
            print(f" - {filepath}")

def run_search_filenames():
    # Automatically get the directory where this script is located
    directory = os.path.dirname(os.path.abspath(__file__))

    # Loop to allow continuous searching
    while True:
        # Get the search term from the user
        search_term = input("\nEnter the term to search for in filenames (or type '/exit' to quit): ").strip()

        # Exit if the user types 'exit'
        if search_term.lower() == '/exit':
            print("Exiting the program. Goodbye!")
            return

        # Perform the search
        search_results = search_filenames(directory, search_term)

        # Print the results
        search_filenames_print_results(search_results)

def hack():
    # secret Area
    print("\n You discovered the secret Area!")
    print("\n So, tell me, my friend.")
    print("\n How much is ah life worth if you cant be yourself?")

    choice = input("\n ").strip()

    if choice == '0':
        print("\n Ah, i see, we have a similar mindset!\n")
        input()

# Run the program
if __name__ == '__main__':
    print(" ")
    print(" Search Engine - By ShadowDara - 6.4.0")
    display_menu()
    input("\n Press Enter to exit...")
