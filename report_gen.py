# report_gen.py

from template_proc import is_blank_or_comment, extract_item_and_folder_status  # Ensure these are imported if used

# Function to compile the formatted line
def compile_line(item, comment, is_folder):
    """Compile a formatted line from item details."""
    line = item
    if comment:
        line += f" | {comment}"
    if is_folder:
        line += " (ƒ)"
        line = f"**{line}**"
    return f"- {line}"

def process_template(template_path, dot_items_dict):
    """Process the template and return formatted output for the report."""
    formatted_output = []
    unmatched_in_home = set(dot_items_dict.keys())
    matched_in_template = set()
    template_items = set()

    with open(template_path, "r") as template_file:
        for line in template_file:
            stripped_line = line.strip()
            if is_blank_or_comment(stripped_line):
                formatted_output.append(line.rstrip())
                continue

            item_name, comment, is_folder = extract_item_and_folder_status(stripped_line)
            template_items.add(item_name)

            # Check if the item exists in the dot items dictionary
            if item_name in dot_items_dict:
                matched_in_template.add(item_name)
                unmatched_in_home.discard(item_name)
                is_folder = dot_items_dict[item_name]
            formatted_line = compile_line(item_name, comment, is_folder)
            formatted_output.append(formatted_line)

    unmatched_in_template = template_items.difference(matched_in_template)

    return formatted_output, unmatched_in_home, unmatched_in_template

def post_process_output(formatted_output, unmatched_in_home, unmatched_in_template, dot_items_dict, template_dict):
    """Post-process the output to handle unmatched items."""
    # Add unmatched items in home to the beginning of the formatted output
    if unmatched_in_home:
        formatted_output.insert(0, "### _$HOME dot items not found in Template_")
        for item in sorted(unmatched_in_home):
            is_folder = dot_items_dict.get(item, False)
            line = compile_line(item, "", is_folder)
            formatted_output.insert(1, line)
    
    # Add unmatched items in template to the end of the formatted output
    if unmatched_in_template:
        formatted_output.append("### _Template Items Not Found in $HOME_")
        for item in sorted(unmatched_in_template):
            comment, is_folder = template_dict.get(item, ("", False))
            line = compile_line(item, comment, is_folder)
            formatted_output.append(line)
    
    return formatted_output

def write_output_file(output_path, formatted_output):
    """Write the formatted output to a file."""
    with open(output_path, "w") as dest:
        for line in formatted_output:
            dest.write(line + "\n")