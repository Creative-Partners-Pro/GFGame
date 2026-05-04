import re

with open('index.html', 'r') as f:
    content = f.read()

# Update startGame to load last layout if it exists
old_start_game = '''        function startGame() {
            totalCells = parseInt(document.getElementById('set-total').value) || 50;
            if (totalCells < 10) totalCells = 10;
            if (totalCells > 100) totalCells = 100;

            const taskPct = parseInt(document.getElementById('set-task-pct').value) || 0;

            // Обработка фона
            const file = document.getElementById('set-map-bg').files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (ev) => { mapContainer.style.backgroundImage = `url(${ev.target.result})`; };
                reader.readAsDataURL(file);
            }

            // Генерация данных клеток
            cellsData = [];
            const taskTypes = ['Physical', 'Audio-interactive', 'Screen-based'];

            for (let i = 0; i < totalCells; i++) {
                let id = i + 1;
                let isStart = (id === 1);
                let isBoss = (id === totalCells);

                // Определение: есть ли задание
                let hasTask = (!isStart && !isBoss) ? (Math.random() * 100 < taskPct) : false;
                let type = hasTask ? taskTypes[Math.floor(Math.random() * taskTypes.length)] : 'None';

                let diffs = ['Легко', 'Нормально', 'Сложно', 'Безумие'];
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
                });
            }

            document.getElementById('modal-start').classList.add('hidden');
            document.getElementById('game-log').innerHTML = ''; // Очистка лога

            const timerMins = parseInt(document.getElementById('set-timer').value) || 30;
            startTimer(timerMins);

            initMapDOM();

            logEvent(`Игра началась! Поле сгенерировано: ${totalCells} клеток, вероятность заданий ${taskPct}%.`);
            updateHUDStyle();
        }'''

new_start_game = '''        function saveLastLayout() {
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
                    }
                });
                return true;
            } catch(e) {
                return false;
            }
        }

        function startGame() {
            totalCells = parseInt(document.getElementById('set-total').value) || 50;
            if (totalCells < 10) totalCells = 10;
            if (totalCells > 100) totalCells = 100;

            const taskPct = parseInt(document.getElementById('set-task-pct').value) || 0;

            // Обработка фона
            const file = document.getElementById('set-map-bg').files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (ev) => { mapContainer.style.backgroundImage = `url(${ev.target.result})`; };
                reader.readAsDataURL(file);
            }

            // Генерация данных клеток
            cellsData = [];
            const taskTypes = ['Physical', 'Audio-interactive', 'Screen-based'];

            for (let i = 0; i < totalCells; i++) {
                let id = i + 1;
                let isStart = (id === 1);
                let isBoss = (id === totalCells);

                // Определение: есть ли задание
                let hasTask = (!isStart && !isBoss) ? (Math.random() * 100 < taskPct) : false;
                let type = hasTask ? taskTypes[Math.floor(Math.random() * taskTypes.length)] : 'None';

                let diffs = ['Легко', 'Нормально', 'Сложно', 'Безумие'];
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
                });
            }

            document.getElementById('modal-start').classList.add('hidden');
            document.getElementById('game-log').innerHTML = ''; // Очистка лога

            const timerMins = parseInt(document.getElementById('set-timer').value) || 30;
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

content = content.replace(old_start_game, new_start_game)


# Save layout on closing map settings
old_close = '''function closeMapSettings() { document.getElementById('modal-map-settings').classList.add('hidden'); }'''
new_close = '''function closeMapSettings() { saveLastLayout(); document.getElementById('modal-map-settings').classList.add('hidden'); }'''

content = content.replace(old_close, new_close)


with open('index.html', 'w') as f:
    f.write(content)
