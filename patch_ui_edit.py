import re

with open('index.html', 'r') as f:
    content = f.read()

# Add button to map editor modal
old_tools = '''                        <button id="btn-toggle-remove" onclick="toggleRemoveMode()" class="flex-1 bg-gray-600 hover:bg-gray-500 text-white px-2 py-3 rounded-lg font-bold shadow-lg transition text-xs">
                            <i class="fa-solid fa-minus"></i> Удалить
                        </button>
                    </div>'''

new_tools = '''                        <button id="btn-toggle-remove" onclick="toggleRemoveMode()" class="flex-1 bg-gray-600 hover:bg-gray-500 text-white px-2 py-3 rounded-lg font-bold shadow-lg transition text-xs">
                            <i class="fa-solid fa-minus"></i> Удалить
                        </button>
                        <button id="btn-toggle-config" onclick="toggleConfigMode()" class="flex-1 bg-gray-600 hover:bg-gray-500 text-white px-2 py-3 rounded-lg font-bold shadow-lg transition text-xs" title="Настроить клетку">
                            <i class="fa-solid fa-gear"></i> Данные
                        </button>
                    </div>'''

content = content.replace(old_tools, new_tools)

with open('index.html', 'w') as f:
    f.write(content)
