import re

with open('index.html', 'r') as f:
    content = f.read()

# Add validMoves array
old_vars = '''        let activeDragEl = null, dragType = null, dragId = null, isEditingMap = false, isLinkingMap = false, isAddingMap = false, isRemovingMap = false, linkStartCellId = null;'''
new_vars = '''        let activeDragEl = null, dragType = null, dragId = null, isEditingMap = false, isLinkingMap = false, isAddingMap = false, isRemovingMap = false, linkStartCellId = null;
        let validMoves = new Set();'''
content = content.replace(old_vars, new_vars)

# Populate validMoves in highlightAvailableMoves
old_highlight = '''            // Highlight final possible destinations
            currentNodes.forEach(id => {
                if(cellElements[id]) cellElements[id].classList.add('highlight-move');
            });
        }'''
new_highlight = '''            // Highlight final possible destinations
            validMoves = currentNodes;
            currentNodes.forEach(id => {
                if(cellElements[id]) cellElements[id].classList.add('highlight-move');
            });
        }'''
content = content.replace(old_highlight, new_highlight)

# Check validMoves in handleTokenDrop
old_drop = '''        function handleTokenDrop(teamId, targetCell) {
            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            const team = gameState[teamId];
            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }
            if (targetCell.required_item && !team.inventory.includes(targetCell.required_item)) {
                showAlert("Доступ закрыт", targetCell.locked_description);
                updateMapDrawings(); return;
            }'''
new_drop = '''        function handleTokenDrop(teamId, targetCell) {
            const team = gameState[teamId];

            // Allow moving tokens freely in map editor mode, or restrict otherwise
            if (!isEditingMap && validMoves.size > 0 && !validMoves.has(targetCell.cell_id)) {
                showAlert("Недопустимый ход", "Вы можете переместиться только на подсвеченные клетки.");
                updateMapDrawings();
                return;
            }

            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            validMoves.clear();

            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }
            if (targetCell.required_item && !team.inventory.includes(targetCell.required_item)) {
                showAlert("Доступ закрыт", targetCell.locked_description);
                updateMapDrawings(); return;
            }'''
content = content.replace(old_drop, new_drop)

with open('index.html', 'w') as f:
    f.write(content)
