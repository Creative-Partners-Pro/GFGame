import re

with open('index.html', 'r') as f:
    content = f.read()

# Add tooltip div right before the main container closing (or inside main)
tooltip_html = '''
        <!-- Тултип с информацией о клетке -->
        <div id="cell-tooltip" class="fixed hidden bg-gray-800 border-2 border-yellow-500 rounded-xl p-4 shadow-2xl z-[100] text-sm w-64 pointer-events-none transform -translate-x-1/2 -translate-y-full mt-[-10px] transition-opacity duration-200">
            <h3 id="tt-title" class="text-lg font-bold text-yellow-400 border-b border-gray-600 pb-1 mb-2">Локация</h3>
            <div id="tt-content" class="space-y-1 text-gray-300">
                <p><span class="text-gray-500">Тип:</span> <span id="tt-type" class="text-white">Обычная</span></p>
                <p><span class="text-gray-500">Победа:</span> +<span id="tt-win" class="text-green-400 font-bold">0</span> pts</p>
                <p><span class="text-gray-500">Поражение:</span> -<span id="tt-loss" class="text-red-400 font-bold">0</span> pts</p>
                <p><span class="text-gray-500">Сложность:</span> <span id="tt-diff" class="text-purple-400">Легко</span></p>
                <p id="tt-repeat" class="text-blue-400 font-bold mt-2 pt-2 border-t border-gray-600 hidden">Можно повторить <i class="fa-solid fa-rotate-right"></i></p>
            </div>
        </div>
'''
content = content.replace('    </main>', tooltip_html + '\n    </main>')

# Update cell data generation models
old_gen1 = '''                cellsData.push({
                    cell_id: id,
                    zone_name: "Зона " + Math.ceil(id / 10),
                    task_type: type,
                    min_points: hasTask ? 10 + Math.floor(id / 5) : 0,
                    max_points: hasTask ? 20 + Math.floor(id / 2) : 0,
                    required_item: id === 14 ? 'grappling_hook' : null, // Пример требования
                    locked_description: id === 14 ? "Для прохода дальше требуется Абордажный крюк!" : null,
                    coordinates: { x: 0, y: 0 }, // Заполнится шаблоном
                    connections: !isBoss ? [id + 1] : [] // По умолчанию к следующей клетке
                });'''
new_gen1 = '''                let diffs = ['Легко', 'Нормально', 'Сложно', 'Безумие'];
                cellsData.push({
                    cell_id: id,
                    zone_name: isStart ? "Лавка Чудес" : (isBoss ? "Странногедон" : "Зона " + Math.ceil(id / 10)),
                    task_type: type,
                    min_points: hasTask ? 10 + Math.floor(id / 5) : 0,
                    max_points: hasTask ? 20 + Math.floor(id / 2) : 0,
                    penalty_points: hasTask ? 5 + Math.floor(id / 4) : 0,
                    is_repeatable: hasTask && Math.random() > 0.7,
                    difficulty: hasTask ? diffs[Math.floor(Math.random() * diffs.length)] : '—',
                    required_item: id === 14 ? 'grappling_hook' : null,
                    locked_description: id === 14 ? "Для прохода дальше требуется Абордажный крюк!" : null,
                    coordinates: { x: 0, y: 0 },
                    connections: !isBoss ? [id + 1] : []
                });'''
content = content.replace(old_gen1, new_gen1)

old_gen2 = '''                cellsData.push({
                    cell_id: nextId,
                    zone_name: "Зона", task_type: "Physical", min_points: 10, max_points: 20,
                    required_item: null, locked_description: null,
                    coordinates: { x: (x/rect.width)*100, y: (y/rect.height)*100 },
                    connections: []
                });'''
new_gen2 = '''                cellsData.push({
                    cell_id: nextId,
                    zone_name: "Новая Зона", task_type: "Physical", min_points: 10, max_points: 20,
                    penalty_points: 5, is_repeatable: false, difficulty: 'Нормально',
                    required_item: null, locked_description: null,
                    coordinates: { x: (x/rect.width)*100, y: (y/rect.height)*100 },
                    connections: []
                });'''
content = content.replace(old_gen2, new_gen2)

old_gen3 = '''                            cellsData.push({
                                cell_id: savedCell.id,
                                zone_name: "Зона", task_type: "None", min_points: 0, max_points: 0, required_item: null, locked_description: null,
                                coordinates: savedCell.coords, connections: savedCell.connections || []
                            });'''
new_gen3 = '''                            cellsData.push({
                                cell_id: savedCell.id,
                                zone_name: "Зона", task_type: "None", min_points: 0, max_points: 0,
                                penalty_points: 0, is_repeatable: false, difficulty: '—',
                                required_item: null, locked_description: null,
                                coordinates: savedCell.coords, connections: savedCell.connections || []
                            });'''
content = content.replace(old_gen3, new_gen3)


# Add tooltip hover logic to initMapDOM
js_tooltip_handlers = '''
                // Тултип логика
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
                });
'''

old_title_logic = '''                let titleStr = `Клетка ${cell.cell_id}\\n`;
                if(cssClass === 'cell-task') titleStr += `Задание: ${cell.task_type}`;
                else if(cssClass === 'cell-empty') titleStr += `Безопасная зона`;
                else if(cssClass === 'cell-shop') titleStr += `Магазин Стэна`;
                else if(cssClass === 'cell-boss') titleStr += `Финальный Босс`;

                el.title = titleStr;
                cellsLayer.appendChild(el);'''

new_title_logic = js_tooltip_handlers + '''                cellsLayer.appendChild(el);'''
content = content.replace(old_title_logic, new_title_logic)

with open('index.html', 'w') as f:
    f.write(content)
