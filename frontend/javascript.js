class Player{
    constructor(name, id, time_when_added){
        this.name = name;
        this.id = id;
        this.time_when_added = time_when_added;
    }
    meto
}

function whenPressed(info){
    var date = new Date();
    var new_player = new Player(info.new_name.value, 1, date)
    console.log(new_player.name);
    console.log(new_player.id);
    console.log(new_player.time_when_added);
    output.innerHTML = el.value;
    return false;
}
