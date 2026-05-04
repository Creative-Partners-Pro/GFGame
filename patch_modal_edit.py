import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix modal visibility by removing modal from container properly
old_open = '''        function openCellEditModal(cellId) {
            const cellData = cellsData.find(c => c.cell_id === cellId);
            if (!cellData) return;

            document.getElementById('cell-edit-title').innerHTML = `<i class="fa-solid fa-gear"></i> Настройка клетки ${cellId}`;'''

new_open = '''        function openCellEditModal(cellId) {
            const cellData = cellsData.find(c => c.cell_id === cellId);
            if (!cellData) return;

            document.getElementById('modal-map-settings').classList.add('hidden');

            document.getElementById('cell-edit-title').innerHTML = `<i class="fa-solid fa-gear"></i> Настройка клетки ${cellId}`;'''

content = content.replace(old_open, new_open)


old_close = '''        function closeCellEditModal() {
            document.getElementById('modal-cell-edit').classList.add('hidden');
        }'''
new_close = '''        function closeCellEditModal() {
            document.getElementById('modal-cell-edit').classList.add('hidden');
            document.getElementById('modal-map-settings').classList.remove('hidden');
        }'''

content = content.replace(old_close, new_close)

with open('index.html', 'w') as f:
    f.write(content)
