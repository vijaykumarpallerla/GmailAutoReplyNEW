// Pre-populate conditions using hidden inputs (preferred) or fallback to JSON script tag.
console.log('rule_edit_prepopulate.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('filterConditionsContainer');
    if (!container) return;
    container.innerHTML = '';

    const fields = Array.from(document.querySelectorAll('#initialConditionsInputs input[name="initial_filter_field"]'));
    const conds  = Array.from(document.querySelectorAll('#initialConditionsInputs input[name="initial_filter_condition"]'));
    const vals   = Array.from(document.querySelectorAll('#initialConditionsInputs input[name="initial_filter_value"]'));
    const andors = Array.from(document.querySelectorAll('#initialConditionsInputs input[name="initial_and_or"]'));
    const count = Math.max(fields.length, conds.length, vals.length);

    if (count > 0) {
        for (let i = 0; i < count; i++) {
            const andOrValue = andors[i] ? andors[i].value : 'AND';
            if (i > 0 && typeof window.createAndOrSelector === 'function') {
                const connector = window.createAndOrSelector(i);
                // Set the AND/OR selector to stored value
                const select = connector.querySelector('select');
                if (select) select.value = andOrValue;
                container.appendChild(connector);
            }
            const row = window.createConditionRow ? window.createConditionRow(
                i,
                fields[i] ? fields[i].value : '',
                conds[i] ? conds[i].value : '',
                vals[i] ? vals[i].value : '',
                andOrValue
            ) : null;
            if (row) container.appendChild(row);
        }
    } else {
        // Fallback to JSON in script tag
        let initialConditions = [];
        const conditionsScript = document.getElementById('rule-conditions');
        if (conditionsScript && conditionsScript.textContent.trim()) {
            try { initialConditions = JSON.parse(conditionsScript.textContent); } catch (e) { initialConditions = []; }
        }
        if (initialConditions.length) {
            initialConditions.forEach((cond, idx) => {
                const andOrValue = cond.and_or || 'AND';
                if (idx > 0 && typeof window.createAndOrSelector === 'function') {
                    const connector = window.createAndOrSelector(idx);
                    const select = connector.querySelector('select');
                    if (select) select.value = andOrValue;
                    container.appendChild(connector);
                }
                const row = window.createConditionRow ? window.createConditionRow(idx, cond.field, cond.condition, cond.value, andOrValue) : null;
                if (row) container.appendChild(row);
            });
        } else {
            container.appendChild(createConditionRow(0, '', '', '', 'AND'));
        }
    }

    // Delegated delete handler
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('delete-condition')) {
            e.preventDefault();
            const row = e.target.closest('.filter-row');
            if (!row) return;
            const filterConditionsContainer = document.getElementById('filterConditionsContainer');
            if (row.previousSibling && row.previousSibling.className === 'and-or-row') {
                filterConditionsContainer.removeChild(row.previousSibling);
            } else if (row.nextSibling && row.nextSibling.className === 'and-or-row') {
                filterConditionsContainer.removeChild(row.nextSibling);
            }
            row.remove();
        }
    });
});
