function fbMap() {
	var game = this;

	if(game == null) {
		return;
	}

	info = Object()

	info.startDate = matchCreation;

	for(frame : game.timeline.frames) {
		for(event : frame.events) {
			if(event.eventType == "CHAMPION_KILL") {
				info.x = event.position.x;
				info.y = event.position.y;
				info.timestamp = event.timestamp;
				info.killer = game.participants[event.killerId];
				info.victim = game.participants[event.victimId];
			}
		}

	}

	emit(game.matchId, info);

}