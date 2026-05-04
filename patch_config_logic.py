import re

with open('index.html', 'r') as f:
    content = f.read()

# Variables & Toggles
old_vars = '''        let activeDragEl = null, dragType = null, dragId = null, isEditingMap = false, isLinkingMap = false, isAddingMap = false, isRemovingMap = false, linkStartCellId = null;
        let validMoves = new Set();'''
new_vars = '''        let activeDragEl = null, dragType = null, dragId = null, isEditingMap = false, isLinkingMap = false, isAddingMap = false, isRemovingMap = false, isConfiguringMap = false, linkStartCellId = null;
        let validMoves = new Set();'''
content = content.replace(old_vars, new_vars)

old_reset = '''        function resetAllEditorModes() {
            isEditingMap = false; isLinkingMap = false; isAddingMap = false; isRemovingMap = false; linkStartCellId = null;
            document.getElementById('btn-toggle-edit').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-link').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-add').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-remove').classList.replace('bg-green-600', 'bg-gray-600');'''

new_reset = '''        function resetAllEditorModes() {
            isEditingMap = false; isLinkingMap = false; isAddingMap = false; isRemovingMap = false; isConfiguringMap = false; linkStartCellId = null;
            document.getElementById('btn-toggle-edit').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-link').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-add').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-remove').classList.replace('bg-green-600', 'bg-gray-600');
            document.getElementById('btn-toggle-config').classList.replace('bg-green-600', 'bg-gray-600');'''
content = content.replace(old_reset, new_reset)

js_toggles = '''
        function toggleConfigMode() {
            const wasActive = isConfiguringMap;
            resetAllEditorModes();
            if (!wasActive) {
                isConfiguringMap = true;
                document.getElementById('btn-toggle-config').classList.replace('bg-gray-600', 'bg-green-600');
                Object.values(cellElements).forEach(el => { el.style.cursor = 'pointer'; el.classList.add('border-yellow-500'); });
                document.getElementById('editor-hint').innerText = "Кликните по клетке, чтобы настроить её.";
            }
        }
'''
content = content.replace('        function resetAllEditorModes() {', js_toggles + '\n        function resetAllEditorModes() {')


# Click Logic
old_mouse = '''            if (isRemovingMap && cellEl) {
                const cellId = parseInt(cellEl.innerText);
                cellsData = cellsData.filter(c => c.cell_id !== cellId);
                cellsData.forEach(c => {
                    if (c.connections) {
                        c.connections = c.connections.filter(id => id !== cellId);
                    }
                });
                initMapDOM(true);
                toggleRemoveMode(); toggleRemoveMode();
                return;
            }'''

new_mouse = '''            if (isRemovingMap && cellEl) {
                const cellId = parseInt(cellEl.innerText);
                cellsData = cellsData.filter(c => c.cell_id !== cellId);
                cellsData.forEach(c => {
                    if (c.connections) {
                        c.connections = c.connections.filter(id => id !== cellId);
                    }
                });
                initMapDOM(true);
                toggleRemoveMode(); toggleRemoveMode();
                return;
            }

            if (isConfiguringMap && cellEl) {
                const cellId = parseInt(cellEl.innerText);
                openCellEditModal(cellId);
                return;
            }'''
content = content.replace(old_mouse, new_mouse)


# Modal Logic implementation
modal_logic = '''
        function openCellEditModal(cellId) {
            const cellData = cellsData.find(c => c.cell_id === cellId);
            if (!cellData) return;

            document.getElementById('cell-edit-title').innerHTML = `<i class="fa-solid fa-gear"></i> Настройка клетки ${cellId}`;
            document.getElementById('edit-cell-id').value = cellId;
            document.getElementById('edit-cell-name').value = cellData.zone_name;
            document.getElementById('edit-cell-type').value = cellData.task_type;
            document.getElementById('edit-cell-diff').value = cellData.difficulty || '—';
            document.getElementById('edit-cell-win').value = cellData.max_points;
            document.getElementById('edit-cell-loss').value = cellData.penalty_points || 0;
            document.getElementById('edit-cell-repeat').checked = !!cellData.is_repeatable;

            document.getElementById('modal-cell-edit').classList.remove('hidden');
        }

        function closeCellEditModal() {
            document.getElementById('modal-cell-edit').classList.add('hidden');
        }

        function saveCellData() {
            const cellId = parseInt(document.getElementById('edit-cell-id').value);
            const cellData = cellsData.find(c => c.cell_id === cellId);
            if (!cellData) return;

            cellData.zone_name = document.getElementById('edit-cell-name').value;
            cellData.task_type = document.getElementById('edit-cell-type').value;
            cellData.difficulty = document.getElementById('edit-cell-diff').value;
            cellData.max_points = parseInt(document.getElementById('edit-cell-win').value) || 0;
            cellData.penalty_points = parseInt(document.getElementById('edit-cell-loss').value) || 0;
            cellData.is_repeatable = document.getElementById('edit-cell-repeat').checked;

            closeCellEditModal();
            initMapDOM(true); // Redraw to update classes
            showAlert("Сохранено", `Данные клетки ${cellId} обновлены.`);
        }
'''

content = content.replace('// --- ЛОГ, МОДАЛКИ, ЗАДАНИЯ ---', '// --- ЛОГ, МОДАЛКИ, ЗАДАНИЯ ---\n' + modal_logic)

with open('index.html', 'w') as f:
    f.write(content)
