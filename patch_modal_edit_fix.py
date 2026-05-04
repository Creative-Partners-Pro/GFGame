import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix toggle mode for Config brush so it closes map settings and opens cells to click
old_toggle_config = '''        function toggleConfigMode() {
            const wasActive = isConfiguringMap;
            resetAllEditorModes();
            if (!wasActive) {
                isConfiguringMap = true;
                document.getElementById('btn-toggle-config').classList.replace('bg-gray-600', 'bg-green-600');
                Object.values(cellElements).forEach(el => { el.style.cursor = 'pointer'; el.classList.add('border-yellow-500'); });
                document.getElementById('editor-hint').innerText = "Кликните по клетке, чтобы настроить её.";
            }
        }'''

new_toggle_config = '''        function toggleConfigMode() {
            const wasActive = isConfiguringMap;
            resetAllEditorModes();
            if (!wasActive) {
                isConfiguringMap = true;
                document.getElementById('btn-toggle-config').classList.replace('bg-gray-600', 'bg-green-600');
                Object.values(cellElements).forEach(el => { el.style.cursor = 'pointer'; el.classList.add('border-yellow-500'); });
                document.getElementById('editor-hint').innerText = "Кликните по клетке, чтобы настроить её. Закройте это окно.";
            }
        }'''

content = content.replace(old_toggle_config, new_toggle_config)

with open('index.html', 'w') as f:
    f.write(content)
