let players = [];
let id = 1;
function creatPlayer(new_name){
    return{
        id: id++,
        name: new_name.trim(),
        createdAt: new Date().toISOString()
    };
}

function whenPressed(info){
    const nameValue = info.elements['name'].value;
    let new_player = creatPlayer(nameValue);
    players.push(new_player);
    console.log(new_player.name);
    console.log(new_player.id);
    console.log(new_player.createdAt);
    nameValue.value = '';
    updateTable();
    return false;
}

function deletePlayer(playerID){
    const playerIndex = players.findIndex(player => player.id === playerID);
    players.splice(playerIndex,1);
    updateTable();
}

function updateTable(){
    const tbody = document.getElementById('players-table');
    let tableHTML = '';
    players.forEach(player =>{
        const date = new Date(player.createdAt);
        const formattedDate = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
        tableHTML += `
        <tr>
            <td>${player.id}</td>
            <td>${player.name}</td>
            <td>${formattedDate}</td>
            <td><img src="../delet.png" onclick="deletePlayer(${player.id})" class = "delete_btn"></td>
        </tr>
        `;
    });
    tbody.innerHTML = tableHTML;
}