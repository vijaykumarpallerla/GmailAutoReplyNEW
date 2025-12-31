import os

file_path = r'c:\Users\Palle\OneDrive\Desktop\Gmail Auto Reply\templates\rule_edit_ui.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the modal
start_idx = -1
for i, line in enumerate(lines):
    if '<!-- Email Editor Modal (hidden by default) -->' in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find modal start")
    exit(1)

# Find the end of the modal section (before </form>)
# We know the modal is followed by </form> (line 244 in previous view)
# We want to remove everything from start_idx up to the line before </form>
end_idx = -1
form_close_idx = -1
for i in range(start_idx, len(lines)):
    if '</form>' in lines[i]:
        form_close_idx = i
        end_idx = i # We stop right before </form>
        break

if end_idx == -1:
    print("Could not find form close tag")
    exit(1)

# Extract the modal block
modal_lines = lines[start_idx:end_idx]

# Remove the modal block from the original lines
# This also removes the extra </div> if it was in that block
del lines[start_idx:end_idx]

# Find where to insert (after .main-content closes)
# The .main-content closing div should be the one after </form>
# Since we removed the lines before </form>, the form_close_idx has shifted.
# We need to find </form> again in the modified lines.
new_form_close_idx = -1
for i, line in enumerate(lines):
    if '</form>' in line:
        new_form_close_idx = i
        break

if new_form_close_idx == -1:
    print("Could not find form close tag after deletion")
    exit(1)

# The .main-content closing div is likely the next line
insert_idx = new_form_close_idx + 2 # +1 for </form>, +1 for </div>

# Modify the modal styles
modified_modal_lines = []
for line in modal_lines:
    # Remove the extra closing div if it was captured (it likely was, as we took everything up to </form>)
    # The block ends with </div> (modal outer), </div> (extra).
    # We want to keep the modal outer div, but discard the extra one.
    # But wait, we are moving the *entire* block.
    # If the block has an extra </div> at the end, we should remove it from the *end* of the list.
    pass

# Check the last few lines of modal_lines for the extra div
# We expect: ... </div> (inner), </div> (outer), </div> (extra)
# Let's print them to be sure in the script execution, or just strip the last line if it is just whitespace and </div>
# But safer to just inspect and clean.

# Let's just update the CSS first
for i, line in enumerate(modal_lines):
    if 'id="emailEditorModal"' in line:
        # Update outer modal styles
        modal_lines[i] = line.replace('align-items:flex-start;justify-content:center;overflow:auto;', 'align-items:center;justify-content:center;overflow:hidden;')
    if 'margin:40px auto 0 auto;' in line:
        # Update inner modal styles
        modal_lines[i] = line.replace('margin:40px auto 0 auto;', 'max-height:95vh;overflow-y:auto;')

# Now handle the extra </div>
# We assume the last non-empty line in modal_lines is the extra </div>
# Let's iterate backwards
lines_to_keep = []
found_extra = False
for line in reversed(modal_lines):
    if not found_extra and '</div>' in line and len(line.strip()) == 6:
        # This is likely the extra div
        found_extra = True
        continue # Skip it
    lines_to_keep.insert(0, line)

if not found_extra:
    print("Warning: Did not find the expected extra </div>. Inserting original block.")
    lines_to_keep = modal_lines

# Insert the modified modal lines
lines[insert_idx:insert_idx] = lines_to_keep

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Successfully moved and updated email editor modal.")
