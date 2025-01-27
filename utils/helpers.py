
def save_to_csv(df, filename):
    '''Save data to a CSV file'''
    try:
        df.to_csv(filename, sep=';', index=False)
        print(f"Data saved to {filename}")
    except PermissionError:
        print("Error: Permission denied. Please close the file if it is open.")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def save_to_excel(df, filename):
    '''Save data to an Excel file'''
    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data saved to {filename}")
    except PermissionError:
        print("Error: Permission denied. Please close the file if it is open.")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def save_to_markdown(posts, titles, metadescriptions, final_keywords, internal_links):
    '''Save data to a Markdown file'''
    try:
        for i, post in enumerate(posts):
            with open(f'./outputs/blog_post_{i}.md', 'w', encoding='utf-8') as f:
                f.write(f"{titles[i]}\n\n")
                f.write(f"{metadescriptions[i]}\n\n")
                f.write(post)
                f.write("\n\n")
                f.write("Keywords: " + ", ".join(final_keywords[i]))
                f.write("\n\n")
                f.write("Internal Links: " + ", ".join(internal_links[i]))
        print("Markdown files saved successfully.")
    except PermissionError:
        print("Error: Permission denied. Please close the files if they are open.")
    except Exception as e:
        print(f"Error saving markdown files: {str(e)}")