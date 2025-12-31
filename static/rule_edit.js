// alert removed for cleaner UX
// Main logic for rule editor: dynamic conditions/actions, AJAX submit, etc.

// --- Condition row logic ---
function createConditionRow(index, fieldValue, condValue, keywordsValue, andOrValue) {
    const row = document.createElement('div');
    row.className = 'filter-row';
    row.style.display = 'flex';
    row.style.alignItems = 'stretch';
    row.style.gap = '10px';
    row.style.marginBottom = '14px';
    // Filter field select
    const field = document.createElement('select');
    field.name = 'filter_field_' + index;
    field.style.width = '220px';
    field.style.height = '44px';
    field.style.background = '#23283a';
    field.style.color = '#fff';
    field.style.border = '1px solid #31374a';
    field.style.padding = '0 10px';
    field.style.borderRadius = '5px';
    field.style.fontSize = '16px';
    field.style.boxSizing = 'border-box';
    field.style.lineHeight = '44px';
    [
        'Sender email address',
        'Recipient email address',
        'Cc email address',
        'Bcc email address',
        'Email subject',
        'Email body',
        'Email time',
        'Email date',
        'Conversation assignee',
        'Conversation status',
        'Marked as SPAM',
        'Attachment'
    ].forEach(opt => {
        const o = document.createElement('option');
        o.textContent = opt;
        field.appendChild(o);
    });
    if (fieldValue) field.value = fieldValue;
    // Condition select
    const cond = document.createElement('select');
    cond.name = 'filter_condition_' + index;
    cond.style.width = '160px';
    cond.style.height = '44px';
    cond.style.background = '#23283a';
    cond.style.color = '#fff';
    cond.style.border = '1px solid #31374a';
    cond.style.padding = '0 10px';
    cond.style.borderRadius = '5px';
    cond.style.fontSize = '16px';
    cond.style.boxSizing = 'border-box';
    cond.style.lineHeight = '44px';
    [
        'contains',
        'is exactly',
        'does not contain',
        'starts with',
        'ends with'
    ].forEach(opt => {
        const o = document.createElement('option');
        o.textContent = opt;
        cond.appendChild(o);
    });
    if (condValue) cond.value = condValue;
    // Keywords input
    const keywords = document.createElement('input');
    keywords.type = 'text';
    keywords.name = 'filter_value_' + index;
    keywords.className = 'filter-value';
    keywords.placeholder = 'Keywords (comma separated)';
    keywords.style.width = '180px';
    keywords.style.height = '44px';
    keywords.style.background = '#23283a';
    keywords.style.color = '#fff';
    keywords.style.border = '1px solid #31374a';
    keywords.style.padding = '0 10px';
    keywords.style.borderRadius = '5px';
    keywords.style.fontSize = '16px';
    keywords.style.boxSizing = 'border-box';
    keywords.style.lineHeight = '44px';
    keywords.value = keywordsValue || '';
    // Store AND/OR value for potential future logic (optional)
    row.dataset.andOr = andOrValue || 'AND';
    console.log('createConditionRow: keywordsValue for row', index, '=', keywords.value);
    row.appendChild(field);
    row.appendChild(cond);
    row.appendChild(keywords);
    // Delete button
    const delBtn = document.createElement('button');
    delBtn.type = 'button';
    delBtn.textContent = 'Delete';
    delBtn.style.background = '#2d2f3a';
    delBtn.style.color = '#ff5c5c';
    delBtn.style.border = 'none';
    delBtn.style.padding = '0 18px';
    delBtn.style.height = '44px';
    delBtn.style.borderRadius = '5px';
    delBtn.style.fontWeight = '600';
    delBtn.style.fontSize = '15px';
    delBtn.style.cursor = 'pointer';
    delBtn.addEventListener('click', function () {
        const filterConditionsContainer = document.getElementById('filterConditionsContainer');
        if (row.previousSibling && row.previousSibling.className === 'and-or-row') {
            filterConditionsContainer.removeChild(row.previousSibling);
        } else if (row.nextSibling && row.nextSibling.className === 'and-or-row') {
            filterConditionsContainer.removeChild(row.nextSibling);
        }
        filterConditionsContainer.removeChild(row);
    });
    row.appendChild(delBtn);
    return row;
}

function createAndOrSelector(index) {
    const wrapper = document.createElement('div');
    wrapper.className = 'and-or-row';
    wrapper.style.display = 'flex';
    wrapper.style.justifyContent = 'center';
    wrapper.style.marginBottom = '14px';
    const select = document.createElement('select');
    select.name = 'and_or_' + index;
    select.style.width = '100px';
    select.style.height = '36px';
    select.style.background = '#23283a';
    select.style.color = '#fff';
    select.style.border = '1px solid #31374a';
    select.style.padding = '0 10px';
    select.style.borderRadius = '5px';
    select.style.fontSize = '15px';
    select.style.boxSizing = 'border-box';
    select.style.textAlign = 'center';
    select.style.fontWeight = '600';
    ['AND', 'OR'].forEach(opt => {
        const o = document.createElement('option');
        o.textContent = opt;
        select.appendChild(o);
    });
    wrapper.appendChild(select);
    return wrapper;
}

// Initial condition row creation is handled by rule_edit_prepopulate.js
// (AJAX submit and action logic would go here)
