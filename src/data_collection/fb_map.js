function fbMap() {
	var game = this;

	var info = Object()
	info.startDate = game.matchCreation;

	if(game.timeline == null) {
		return;
	}
	for(var i in game.timeline.frames) {
		frame = game.timeline.frames[i];
		for(var j in frame.events) {
			lol_event = frame.events[j];
			if(lol_event.eventType == "CHAMPION_KILL") {
				info.x = lol_event.position.x;
				info.y = lol_event.position.y;
				info.timestamp = lol_event.timestamp;
				if(lol_event.killerId != null && lol_event.killerId >= 1 && lol_event.killerId <= 10) {
					info.killer = game.participants[lol_event.killerId-1].championId;
				}
				info.victim = game.participants[lol_event.victimId-1].championId;
				emit(game.matchId, info);
				return;
			}
		}

	}
}