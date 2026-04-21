// Game state
let gameState = {
    initialized: false,
    gameOver: false,
    outcome: null,
    turn: 0
};

const outcomeMessages = {
    'escaped': '✓ ESCAPED: You made it out alive.',
    'player_dead': '✗ KILLED: You were killed by the killer.',
    'killer_dead': '✓ JUSTICE: You killed the killer.',
    'killer_restrained': '✓ CAPTURED: You restrained the killer for backup.',
    'victim_rescued': '✓ RESCUE: You saved the victim!',
    'victim_dead': '✗ TOO LATE: The victim died.'
};

const outcomeColors = {
    'escaped': '#4ade80',
    'player_dead': '#ef4444',
    'killer_dead': '#4ade80',
    'killer_restrained': '#4ade80',
    'victim_rescued': '#4ade80',
    'victim_dead': '#ef4444'
};

// DOM Elements
const briefingSection = document.getElementById('briefing-section');
const gameSection = document.getElementById('game-section');
const startButton = document.getElementById('start-button');
const actionForm = document.getElementById('action-form');
const actionInput = document.getElementById('action-input');
const submitButton = actionForm.querySelector('button');
const sceneContent = document.getElementById('scene-content');
const turnCounter = document.getElementById('turn-counter');
const gameOverScreen = document.getElementById('game-over-screen');
const loadingIndicator = document.getElementById('loading-indicator');
const restartButton = document.getElementById('restart-button');

// Event Listeners
startButton.addEventListener('click', startGame);
actionForm.addEventListener('submit', submitAction);
restartButton.addEventListener('click', restartGame);

async function startGame() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/start-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            alert('Error starting game: ' + (error.error || 'Unknown error'));
            showLoading(false);
            return;
        }

        const data = await response.json();
        
        gameState.initialized = true;
        gameState.turn = 1;
        
        // Update UI
        briefingSection.style.display = 'none';
        gameSection.style.display = 'flex';
        gameOverScreen.style.display = 'none';
        
        displayScene(data.scene);
        updateStats();
        
        // Enable input
        actionInput.disabled = false;
        submitButton.disabled = false;
        actionInput.focus();
        
        showLoading(false);
    } catch (error) {
        alert('Error starting game: ' + error.message);
        showLoading(false);
    }
}

async function submitAction(event) {
    event.preventDefault();
    
    const action = actionInput.value.trim();
    if (!action) {
        return;
    }

    try {
        // Disable input while processing
        actionInput.disabled = true;
        submitButton.disabled = true;
        showLoading(true);
        
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action })
        });

        if (!response.ok) {
            const error = await response.json();
            alert('Error processing action: ' + (error.error || 'Unknown error'));
            actionInput.disabled = false;
            submitButton.disabled = false;
            showLoading(false);
            return;
        }

        const data = await response.json();
        
        // Update game state
        gameState.gameOver = data.game_over;
        gameState.outcome = data.outcome;
        gameState.turn += 1;
        
        // Clear and update scene
        actionInput.value = '';
        displayScene(data.scene);
        updateStats();
        
        // Check if game is over
        if (data.game_over) {
            showGameOver(data.outcome);
        } else {
            // Re-enable input
            actionInput.disabled = false;
            submitButton.disabled = false;
            actionInput.focus();
        }
        
        showLoading(false);
    } catch (error) {
        alert('Error processing action: ' + error.message);
        actionInput.disabled = false;
        submitButton.disabled = false;
        showLoading(false);
    }
}

async function restartGame() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/restart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Reset state
            gameState = {
                initialized: false,
                gameOver: false,
                outcome: null,
                turn: 0
            };
            
            // Update UI
            gameOverScreen.style.display = 'none';
            gameSection.style.display = 'none';
            briefingSection.style.display = 'flex';
            actionInput.value = '';
            actionInput.disabled = true;
            submitButton.disabled = true;
            
            startButton.focus();
        }
        
        showLoading(false);
    } catch (error) {
        alert('Error restarting game: ' + error.message);
        showLoading(false);
    }
}

function displayScene(sceneText) {
    // Sanitize and format the scene
    let formattedText = sceneText
        .replace(/\[GAME_OVER:.*?\]/gi, '') // Remove game over markers
        .trim();
    
    sceneContent.textContent = formattedText;
    
    // Scroll to bottom
    const scenePanel = document.querySelector('.scene-panel');
    scenePanel.scrollTop = scenePanel.scrollHeight;
}

function updateStats() {
    turnCounter.textContent = gameState.turn;
}

function showGameOver(outcome) {
    const outcomeTitle = document.getElementById('outcome-title');
    const outcomeMessage = document.getElementById('outcome-message');
    
    outcomeTitle.textContent = 'GAME OVER';
    outcomeTitle.style.color = outcomeColors[outcome] || '#ff6b6b';
    outcomeMessage.textContent = outcomeMessages[outcome] || 'The game has ended.';
    
    // Disable input
    actionInput.disabled = true;
    submitButton.disabled = true;
    
    // Show game over screen
    gameOverScreen.style.display = 'flex';
}

function showLoading(show) {
    loadingIndicator.style.display = show ? 'flex' : 'none';
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Page is ready
    startButton.focus();
});
