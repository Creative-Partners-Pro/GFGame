import re

with open('index.html', 'r') as f:
    content = f.read()

# Update drag mousedown rules
old_mouse = '''            if (tokenEl && !isEditingMap) {
                Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
                activeDragEl = tokenEl; dragType = 'token'; dragId = tokenEl.id.replace('token-', '');
                tokenEl.classList.add('dragging');
            } else if (cellEl && isEditingMap) {'''

new_mouse = '''            if (tokenEl && !isEditingMap) {
                const tokenId = tokenEl.id.replace('token-', '');
                if (tokenId !== gameState.currentTurn) {
                    showAlert("Не ваш ход", "Сейчас ходит другая команда.");
                    return;
                }
                // Do NOT clear highlight on drag start
                activeDragEl = tokenEl; dragType = 'token'; dragId = tokenId;
                tokenEl.classList.add('dragging');
            } else if (cellEl && isEditingMap) {'''
content = content.replace(old_mouse, new_mouse)


# Update drop rules
old_drop = '''        function handleTokenDrop(teamId, targetCell) {
            const team = gameState[teamId];

            // Allow moving tokens freely in map editor mode, or restrict otherwise
            if (!isEditingMap && validMoves.size > 0 && !validMoves.has(targetCell.cell_id)) {
                showAlert("Недопустимый ход", "Вы можете переместиться только на подсвеченные клетки.");
                updateMapDrawings();
                return;
            }

            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            validMoves.clear();
            document.getElementById('map-zoom-layer').style.transform = 'scale(1)'; // Reset zoom

            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }
            if (targetCell.required_item && !team.inventory.includes(targetCell.required_item)) {
                showAlert("Доступ закрыт", targetCell.locked_description);
                updateMapDrawings(); return;
            }'''

new_drop = '''        function handleTokenDrop(teamId, targetCell) {
            const team = gameState[teamId];

            // If dropping on same cell, just snap back, don't clear moves
            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }

            // Strict movement checks
            if (!isEditingMap) {
                if (validMoves.size === 0) {
                    showAlert("Сначала бросьте кубик!", "Чтобы походить, нужно кинуть кубик.");
                    updateMapDrawings();
                    return;
                }
                if (!validMoves.has(targetCell.cell_id)) {
                    showAlert("Недопустимый ход", "Вы можете переместиться только на подсвеченные клетки.");
                    updateMapDrawings();
                    return;
                }
            }

            // Move is valid and happening
            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            validMoves.clear();
            document.getElementById('map-zoom-layer').style.transform = 'scale(1)'; // Reset zoom

            if (targetCell.required_item && !team.inventory.includes(targetCell.required_item)) {
                showAlert("Доступ закрыт", targetCell.locked_description);
                updateMapDrawings(); return;
            }'''
content = content.replace(old_drop, new_drop)

with open('index.html', 'w') as f:
    f.write(content)
