import re

with open('index.html', 'r') as f:
    content = f.read()

# Add the new modal HTML right before the shop modal
modal_html = '''    <!-- Модальное окно: Редактор Клетки -->
    <div id="modal-cell-edit" class="fixed inset-0 bg-black/80 z-[160] hidden flex items-center justify-center backdrop-blur-sm">
        <div class="bg-gray-800 border-2 border-yellow-500 rounded-xl w-full max-w-md shadow-2xl p-6">
            <div class="flex justify-between items-center mb-6 border-b border-gray-700 pb-2">
                <h2 class="text-2xl text-white font-bold" id="cell-edit-title"><i class="fa-solid fa-gear"></i> Настройка клетки</h2>
                <button onclick="closeCellEditModal()" class="text-gray-400 hover:text-white"><i class="fa-solid fa-times text-2xl"></i></button>
            </div>

            <div class="space-y-4">
                <input type="hidden" id="edit-cell-id">

                <div>
                    <label class="block text-sm text-gray-400 mb-1">Название локации:</label>
                    <input type="text" id="edit-cell-name" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white outline-none focus:border-yellow-500">
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm text-gray-400 mb-1">Тип задания:</label>
                        <select id="edit-cell-type" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white outline-none focus:border-yellow-500">
                            <option value="None">Отдых (None)</option>
                            <option value="Physical">Physical</option>
                            <option value="Audio-interactive">Audio</option>
                            <option value="Screen-based">Screen-based</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm text-gray-400 mb-1">Сложность:</label>
                        <select id="edit-cell-diff" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white outline-none focus:border-yellow-500">
                            <option value="—">—</option>
                            <option value="Легко">Легко</option>
                            <option value="Нормально">Нормально</option>
                            <option value="Сложно">Сложно</option>
                            <option value="Безумие">Безумие</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm text-gray-400 mb-1 text-green-400">Награда (Победа):</label>
                        <input type="number" id="edit-cell-win" min="0" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white outline-none focus:border-green-500">
                    </div>
                    <div>
                        <label class="block text-sm text-gray-400 mb-1 text-red-400">Штраф (Поражение):</label>
                        <input type="number" id="edit-cell-loss" min="0" class="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white outline-none focus:border-red-500">
                    </div>
                </div>

                <div class="flex items-center gap-3 pt-2">
                    <input type="checkbox" id="edit-cell-repeat" class="w-5 h-5 accent-yellow-500 cursor-pointer">
                    <label class="text-gray-300 cursor-pointer" for="edit-cell-repeat">Можно выполнять повторно (фарм)</label>
                </div>

                <div class="pt-4 mt-2 border-t border-gray-700">
                    <button onclick="saveCellData()" class="w-full bg-green-600 hover:bg-green-500 text-white py-3 rounded-lg font-bold shadow-lg transition">Сохранить изменения</button>
                </div>
            </div>
        </div>
    </div>
'''

content = content.replace('    <!-- Магазин и Оповещения -->', modal_html + '\n    <!-- Магазин и Оповещения -->')

with open('index.html', 'w') as f:
    f.write(content)
