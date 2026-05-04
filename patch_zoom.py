import re

with open('index.html', 'r') as f:
    content = f.read()

# Add map-zoom-layer div
old_map = '''        <!-- Игровое поле -->
        <div class="flex-1 h-full rounded-xl custom-scrollbar flex items-center justify-center bg-gray-900 border border-gray-700 shadow-inner relative">
            <div id="map-container">
                <svg id="svg-lines"></svg>
                <div id="cells-layer"></div>
            </div>'''
new_map = '''        <!-- Игровое поле -->
        <div class="flex-1 h-full rounded-xl custom-scrollbar flex items-center justify-center bg-gray-900 border border-gray-700 shadow-inner relative overflow-hidden">
            <div id="map-container">
                <div id="map-zoom-layer" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; transition: transform 0.8s ease;">
                    <svg id="svg-lines"></svg>
                    <div id="cells-layer"></div>
                </div>
            </div>'''
content = content.replace(old_map, new_map)

# Update Token appending
old_token_append = '''            token.className = 'token';
            if (icon) {
                token.innerText = icon;
            }
            mapContainer.appendChild(token);'''
new_token_append = '''            token.className = 'token';
            if (icon) {
                token.innerText = icon;
            }
            document.getElementById('map-zoom-layer').appendChild(token);'''
content = content.replace(old_token_append, new_token_append)


# Add zoom logic to highlight moves
old_hl = '''            // Highlight final possible destinations
            validMoves = currentNodes;
            currentNodes.forEach(id => {
                if(cellElements[id]) cellElements[id].classList.add('highlight-move');
            });
        }'''
new_hl = '''            // Highlight final possible destinations
            validMoves = currentNodes;
            currentNodes.forEach(id => {
                if(cellElements[id]) cellElements[id].classList.add('highlight-move');
            });

            // Zoom effect
            const startCell = cellsData.find(c => c.cell_id === startPos);
            if (startCell) {
                const zoomLayer = document.getElementById('map-zoom-layer');
                zoomLayer.style.transformOrigin = `${startCell.coordinates.x}% ${startCell.coordinates.y}%`;
                zoomLayer.style.transform = 'scale(1.3)';
            }
        }'''
content = content.replace(old_hl, new_hl)


# Reset zoom logic on drop
old_drop2 = '''            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            validMoves.clear();

            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }'''
new_drop2 = '''            Object.values(cellElements).forEach(el => el.classList.remove('highlight-move'));
            validMoves.clear();
            document.getElementById('map-zoom-layer').style.transform = 'scale(1)'; // Reset zoom

            if(team.pos === targetCell.cell_id) { updateMapDrawings(); return; }'''
content = content.replace(old_drop2, new_drop2)

with open('index.html', 'w') as f:
    f.write(content)
