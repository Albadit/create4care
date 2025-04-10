import os

def generate_structure(folder, prefix=''):
    try:
        items = sorted(os.listdir(folder))
    except Exception as e:
        return f"Error: {e}\n"
    
    # Filter out excluded folders, files, and extensions
    filtered = [
        item for item in items 
        if not (
            (os.path.isdir(os.path.join(folder, item)) and item in EXCLUDED_FOLDERS) or
            (os.path.isfile(os.path.join(folder, item)) and 
            (item in EXCLUDED_FILES or os.path.splitext(item)[1].lower() in EXCLUDED_EXTENSIONS))
        )
    ]
    
    structure = ""
    for i, item in enumerate(filtered):
        connector = "└── " if i == len(filtered)-1 else "├── "
        structure += f"{prefix}{connector}{item}\n"
        path = os.path.join(folder, item)
        if os.path.isdir(path):
            new_prefix = prefix + "    " if i == len(filtered)-1 else prefix + "│   "
            structure += generate_structure(path, new_prefix)
    return structure

def copy_contents(folder, parent=''):
    content = ""
    try:
        items = sorted(os.listdir(folder))
    except Exception as e:
        return f"Error: {e}\n"
    
    for item in items:
        path = os.path.join(folder, item)
        rel_path = f"{parent}/{item}" if parent else item
        
        if os.path.isdir(path):
            if item in EXCLUDED_FOLDERS:
                continue
            content += copy_contents(path, rel_path)
        elif os.path.isfile(path):
            ext = os.path.splitext(item)[1].lower()
            if item in EXCLUDED_FILES or ext in EXCLUDED_EXTENSIONS:
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                ext_clean = ext[1:] if ext else 'txt'
                content += f"\n## {rel_path}\n```{ext_clean}\n{file_content}\n```\n"
            except:
                content += f"\n## {rel_path}\n```\nError reading file.\n```\n"
    return content

def save_md(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# EXCLUDED_FOLDERS = {'node_modules', '__pycache__', '.git', 'controllers'}
EXCLUDED_FOLDERS = {'__pycache__', 'bin', 'obj', 'Platforms', 'Resources', 'Docs', 'Icon'}
EXCLUDED_FILES = {'.gitignore'}
EXCLUDED_EXTENSIONS = {}

# Specify the target folder
folder_path = r"C:\Users\ardit\Documents\GitHub\School\year_3\sem6\create4care\create4care"

# Define the output Markdown file path
output_md = os.path.join(os.path.dirname(os.path.abspath(__file__)), "folder_structure.md")

# Generate folder structure and file contents
structure = generate_structure(folder_path)
contents = copy_contents(folder_path)

# Merge and save the content to Markdown
merge_content = f"# Folder structure\n```\n{folder_path}\n{structure}```\n{contents}"
save_md(merge_content, output_md)

# Optional: Print the folder structure
print(structure)
