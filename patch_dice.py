import re

with open('index.html', 'r') as f:
    content = f.read()

# Hide second dice
old_dice_html = '''            <div class="flex justify-center gap-6 mb-8 relative z-10">
                <div id="dice1" class="w-24 h-24 bg-white text-black text-5xl flex items-center justify-center rounded-2xl shadow-inner font-bold border-4 border-gray-300 transform transition-transform">?</div>
                <div id="dice2" class="w-24 h-24 bg-white text-black text-5xl flex items-center justify-center rounded-2xl shadow-inner font-bold border-4 border-gray-300 transform transition-transform">?</div>
            </div>'''
new_dice_html = '''            <div class="flex justify-center gap-6 mb-8 relative z-10">
                <div id="dice1" class="w-24 h-24 bg-white text-black text-5xl flex items-center justify-center rounded-2xl shadow-inner font-bold border-4 border-gray-300 transform transition-transform">?</div>
                <div id="dice2" class="hidden w-24 h-24 bg-white text-black text-5xl flex items-center justify-center rounded-2xl shadow-inner font-bold border-4 border-gray-300 transform transition-transform">?</div>
            </div>'''
content = content.replace(old_dice_html, new_dice_html)


# Update JS roll logic to 1 dice
old_perform = '''        function performRoll() {
            const btnRoll = document.getElementById('btn-roll-action');
            btnRoll.classList.add('hidden'); // Скрываем кнопку броска, чтобы не нажимали дважды

            const d1El = document.getElementById('dice1');
            const d2El = document.getElementById('dice2');

            // Анимация броска
            let counter = 0;
            const interval = setInterval(() => {
                d1El.innerText = Math.floor(Math.random() * 6) + 1;
                d2El.innerText = Math.floor(Math.random() * 6) + 1;
                d1El.style.transform = `rotate(${Math.random() * 360}deg) scale(1.1)`;
                d2El.style.transform = `rotate(${Math.random() * 360}deg) scale(1.1)`;
                counter++;
                if (counter > 10) {
                    clearInterval(interval);
                    finalizeRoll();
                }
            }, 50);
        }

        function useOfflineDice() {
            const val = parseInt(document.getElementById('offline-dice-val').value);
            if (!val || val < 1) { showAlert("Ошибка", "Введите корректное число."); return; }
            const d1El = document.getElementById('dice1');
            const d2El = document.getElementById('dice2');
            d1El.innerText = val; d2El.innerText = '?';
            const team = gameState[gameState.currentTurn];
            let msg = `Офлайн кубики: ${val}. У вас ${val} шагов!`;
            document.getElementById('dice-result').innerText = msg;
            document.getElementById('btn-dice-close').classList.remove('hidden');
            logEvent(`${team.name} вводит результат офлайн: ${val}.`);
            highlightAvailableMoves(team.pos, val);
        }

        function highlightAvailableMoves(startPos, steps) {'''

new_perform = '''        function performRoll() {
            const btnRoll = document.getElementById('btn-roll-action');
            btnRoll.classList.add('hidden'); // Скрываем кнопку броска, чтобы не нажимали дважды

            const d1El = document.getElementById('dice1');

            // Анимация броска
            let counter = 0;
            const interval = setInterval(() => {
                d1El.innerText = Math.floor(Math.random() * 6) + 1;
                d1El.style.transform = `rotate(${Math.random() * 360}deg) scale(1.1)`;
                counter++;
                if (counter > 10) {
                    clearInterval(interval);
                    finalizeRoll();
                }
            }, 50);
        }

        function useOfflineDice() {
            const val = parseInt(document.getElementById('offline-dice-val').value);
            if (!val || val < 1) { showAlert("Ошибка", "Введите корректное число."); return; }
            const d1El = document.getElementById('dice1');
            d1El.innerText = val;
            const team = gameState[gameState.currentTurn];
            let msg = `Офлайн кубик: ${val}. У вас ${val} шагов!`;
            document.getElementById('dice-result').innerText = msg;
            document.getElementById('btn-dice-close').classList.remove('hidden');
            logEvent(`${team.name} вводит результат офлайн: ${val}.`);
            highlightAvailableMoves(team.pos, val);
        }

        function highlightAvailableMoves(startPos, steps) {'''

content = content.replace(old_perform, new_perform)


# Update finalizeRoll
old_finalize = '''        function finalizeRoll() {
            const d1 = Math.floor(Math.random() * 6) + 1;
            const d2 = Math.floor(Math.random() * 6) + 1;
            const d1El = document.getElementById('dice1');
            const d2El = document.getElementById('dice2');

            d1El.innerText = d1; d2El.innerText = d2;
            d1El.style.transform = 'rotate(0deg) scale(1)';
            d2El.style.transform = 'rotate(0deg) scale(1)';

            const team = gameState[gameState.currentTurn];
            let move = d1 + d2;

            let msg = `Выпало: ${d1} и ${d2}. У вас ${move} шагов!`;
            document.getElementById('dice-result').innerText = msg;

            document.getElementById('btn-dice-close').classList.remove('hidden');
            logEvent(`${team.name} бросает кубики: ${d1} и ${d2}. Ждем перемещения.`);
            highlightAvailableMoves(team.pos, move);
        }'''

new_finalize = '''        function finalizeRoll() {
            const d1 = Math.floor(Math.random() * 6) + 1;
            const d1El = document.getElementById('dice1');

            d1El.innerText = d1;
            d1El.style.transform = 'rotate(0deg) scale(1)';

            const team = gameState[gameState.currentTurn];
            let move = d1;

            let msg = `Выпало: ${d1}. У вас ${move} шагов!`;
            document.getElementById('dice-result').innerText = msg;

            document.getElementById('btn-dice-close').classList.remove('hidden');
            logEvent(`${team.name} бросает кубик: ${d1}. Ждем перемещения.`);
            highlightAvailableMoves(team.pos, move);
        }'''

content = content.replace(old_finalize, new_finalize)

with open('index.html', 'w') as f:
    f.write(content)
