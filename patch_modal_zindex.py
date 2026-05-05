import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix modal visibility by increasing z-index of modal-cell-edit to make sure it is clickable and visible above backdrop
old_modal = '''    <!-- Модальное окно: Редактор Клетки -->
    <div id="modal-cell-edit" class="fixed inset-0 bg-black/80 z-[160] hidden flex items-center justify-center backdrop-blur-sm">'''
new_modal = '''    <!-- Модальное окно: Редактор Клетки -->
    <div id="modal-cell-edit" class="fixed inset-0 bg-black/80 z-[300] hidden flex items-center justify-center backdrop-blur-sm">'''

content = content.replace(old_modal, new_modal)

with open('index.html', 'w') as f:
    f.write(content)
