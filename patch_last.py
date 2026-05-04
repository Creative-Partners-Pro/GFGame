import re

with open('index.html', 'r') as f:
    content = f.read()

# Add functions properly
js_logic = '''        function saveLastLayout() {
            const layout = cellsData.map(c => ({ id: c.cell_id, coords: c.coordinates, connections: c.connections }));
            localStorage.setItem('gf_last_layout', JSON.stringify(layout));
        }

        function loadLastLayout() {
            const saved = localStorage.getItem('gf_last_layout');
            if (!saved) return false;
            try {
                const layout = JSON.parse(saved);
                layout.forEach(savedCell => {
                    const cell = cellsData.find(c => c.cell_id === savedCell.id);
                    if(cell) {
                        cell.coordinates = savedCell.coords;
                        cell.connections = savedCell.connections || [];
                    } else {
                        // Restore missing cells to keep full layout intact
                        let diffs = ['Легко', 'Нормально', 'Сложно', 'Безумие'];
                        cellsData.push({
                            cell_id: savedCell.id,
                            zone_name: "Зона",
                            task_type: "Physical",
                            min_points: 10, max_points: 20, penalty_points: 5,
                            is_repeatable: false, difficulty: 'Нормально',
                            required_item: null, locked_description: null,
                            coordinates: savedCell.coords,
                            connections: savedCell.connections || []
                        });
                    }
                });

                // Remove cells that were deleted in last layout
                const savedIds = layout.map(c => c.id);
                cellsData = cellsData.filter(c => savedIds.includes(c.cell_id));
                return true;
            } catch(e) {
                return false;
            }
        }
'''

content = content.replace('// --- 1. СТАРТ ИГРЫ И ГЕНЕРАЦИЯ КЛЕТОК ---', '// --- 1. СТАРТ ИГРЫ И ГЕНЕРАЦИЯ КЛЕТОК ---\n' + js_logic)


# Update start Game logic
old_start = '''            const timerMins = parseInt(document.getElementById('set-timer').value) || 30;
            startTimer(timerMins);

            initMapDOM();


            logEvent(`Игра началась! Поле сгенерировано: ${totalCells} клеток, вероятность заданий ${taskPct}%.`);
            updateHUDStyle();
        }'''

new_start = '''            const timerMins = parseInt(document.getElementById('set-timer').value) || 30;
            startTimer(timerMins);

            const hasLastLayout = loadLastLayout();
            if (hasLastLayout) {
                initMapDOM(true);
            } else {
                initMapDOM();
                saveLastLayout(); // Save snake layout initially
            }


            logEvent(`Игра началась! Поле сгенерировано: ${totalCells} клеток, вероятность заданий ${taskPct}%.`);
            updateHUDStyle();
        }'''
content = content.replace(old_start, new_start)


# Update close editor
old_close = '''function closeMapSettings() { document.getElementById('modal-map-settings').classList.add('hidden'); }'''
new_close = '''function closeMapSettings() { saveLastLayout(); document.getElementById('modal-map-settings').classList.add('hidden'); }'''

content = content.replace(old_close, new_close)

with open('index.html', 'w') as f:
    f.write(content)
