import re

with open('index.html', 'r') as f:
    content = f.read()

# Update modal-dice wrapper to catch clicks outside
old_dice_html = '''    <!-- Модальное окно: Бросок кубиков -->
    <div id="modal-dice" class="fixed inset-0 bg-black/80 z-[60] hidden flex items-center justify-center backdrop-blur-sm">
        <div class="bg-gray-800 border-4 border-blue-500 rounded-3xl w-full max-w-md shadow-2xl p-8 text-center relative overflow-hidden">'''

new_dice_html = '''    <!-- Модальное окно: Бросок кубиков -->
    <div id="modal-dice" onclick="if(event.target === this) closeDiceModal()" class="fixed inset-0 bg-black/80 z-[60] hidden flex items-center justify-center backdrop-blur-sm">
        <div class="bg-gray-800 border-4 border-blue-500 rounded-3xl w-full max-w-md shadow-2xl p-8 text-center relative overflow-hidden">'''

content = content.replace(old_dice_html, new_dice_html)

with open('index.html', 'w') as f:
    f.write(content)
