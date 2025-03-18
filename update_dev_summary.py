import datetime

def add_update(update_text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    with open("development_summary.md", "r") as f:
        content = f.read()
    
    # Find the Updates Log section
    if "## Updates Log" in content:
        # Add new entry after the Updates Log heading
        updated_content = content.replace("## Updates Log", f"## Updates Log\n\n### [Date: {today}]\n- {update_text}\n")
    else:
        # Add Updates Log section if it doesn't exist
        updated_content = content + f"\n## Updates Log\n\n### [Date: {today}]\n- {update_text}\n"
    
    with open("development_summary.md", "w") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_text = input("Enter update details: ")
    add_update(update_text)
    print("Development summary updated successfully!")
