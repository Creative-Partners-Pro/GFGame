import re

with open('index.html', 'r') as f:
    content = f.read()

# Make tooltip clickable by setting pointer-events
old_tt = '''        <div id="cell-tooltip" class="fixed hidden bg-gray-800 border-2 border-yellow-500 rounded-xl p-4 shadow-2xl z-[100] text-sm w-64 pointer-events-none transform -translate-x-1/2 -translate-y-full mt-[-10px] transition-opacity duration-200">'''
new_tt = '''        <div id="cell-tooltip" class="fixed hidden bg-gray-800 border-2 border-yellow-500 rounded-xl p-4 shadow-2xl z-[100] text-sm w-64 transform -translate-x-1/2 -translate-y-full mt-[-10px] transition-opacity duration-200">'''
content = content.replace(old_tt, new_tt)


# Change tooltip logic to use mousedown instead of mouseenter
old_handlers = '''                // Тултип логика
                el.addEventListener('mouseenter', (e) => {
                    if (isEditingMap || isLinkingMap || isAddingMap || isRemovingMap || activeDragEl) return;

                    const tooltip = document.getElementById('cell-tooltip');
                    const cellData = cellsData.find(c => c.cell_id === cell.cell_id);
                    if(!cellData) return;

                    document.getElementById('tt-title').innerText = `${cellData.zone_name} (Клетка ${cellData.cell_id})`;
                    document.getElementById('tt-type').innerText = cellData.task_type === 'None' ? 'Отдых' : cellData.task_type;
                    document.getElementById('tt-win').innerText = cellData.max_points;
                    document.getElementById('tt-loss').innerText = cellData.penalty_points || 0;
                    document.getElementById('tt-diff').innerText = cellData.difficulty || '—';

                    const repeatEl = document.getElementById('tt-repeat');
                    if(cellData.is_repeatable) repeatEl.classList.remove('hidden');
                    else repeatEl.classList.add('hidden');

                    const rect = el.getBoundingClientRect();
                    tooltip.style.left = `${rect.left + rect.width / 2}px`;
                    tooltip.style.top = `${rect.top - 10}px`;
                    tooltip.classList.remove('hidden');
                });

                el.addEventListener('mouseleave', () => {
                    document.getElementById('cell-tooltip').classList.add('hidden');
                });'''

new_handlers = '''                // Тултип логика (клик)
                el.addEventListener('mousedown', (e) => {
                    if (isEditingMap || isLinkingMap || isAddingMap || isRemovingMap || activeDragEl) return;
                    e.stopPropagation(); // Prevent document click from immediately closing it

                    const tooltip = document.getElementById('cell-tooltip');
                    const cellData = cellsData.find(c => c.cell_id === cell.cell_id);
                    if(!cellData) return;

                    document.getElementById('tt-title').innerText = `${cellData.zone_name} (Клетка ${cellData.cell_id})`;
                    document.getElementById('tt-type').innerText = cellData.task_type === 'None' ? 'Отдых' : cellData.task_type;
                    document.getElementById('tt-win').innerText = cellData.max_points;
                    document.getElementById('tt-loss').innerText = cellData.penalty_points || 0;
                    document.getElementById('tt-diff').innerText = cellData.difficulty || '—';

                    const repeatEl = document.getElementById('tt-repeat');
                    if(cellData.is_repeatable) repeatEl.classList.remove('hidden');
                    else repeatEl.classList.add('hidden');

                    const rect = el.getBoundingClientRect();
                    tooltip.style.left = `${rect.left + rect.width / 2}px`;
                    tooltip.style.top = `${rect.top - 10}px`;
                    tooltip.classList.remove('hidden');
                });'''

content = content.replace(old_handlers, new_handlers)

# Global document click to close tooltip
global_click = '''
        document.addEventListener('mousedown', (e) => {
            const tooltip = document.getElementById('cell-tooltip');
            if (!tooltip.classList.contains('hidden')) {
                // Check if click is outside tooltip and outside cells
                if (!e.target.closest('#cell-tooltip') && !e.target.closest('.cell')) {
                    tooltip.classList.add('hidden');
                }
            }
        });
'''
content = content.replace('        const svgLines = document.getElementById(\'svg-lines\');', '        const svgLines = document.getElementById(\'svg-lines\');\n' + global_click)


with open('index.html', 'w') as f:
    f.write(content)
