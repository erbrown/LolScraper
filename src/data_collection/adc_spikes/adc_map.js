function adcMap() {
	var game = this;

	var info = Object()

	info.startDate = game.matchCreation;
	info.patch = matchVersion;

	if(game.timeline == null) {
		return;
	}

	blue_adc = Object();
	red_adc = Object();

	// Find Ids for the ADCs
	for(var i in game.participants) {
		player = game.participants[i];
		if(player.timeline.role == "SOLO" && player.timeline.lane == "BOTTOM") {
			if(player.teamId == 100) {
				blue_adc.id = player.participantId;
				blue_adc.champion = player.championId;
			} else if(player.teamId == 200) {
				red_adc.id = player.participantId;
				red_adc.champion = player.championId;
			}

		}

	}

	blue_adc.frames = Object();
	red_adc.frames = Object();

	blue_adc.items = Object();
	red_adc.items = Object();


	for(var i in game.timeline.frames) {
		frame = game.timeline.frames[i];

		for(var j in frame.events) {
			lol_event = frame.events[j];

			// Track item purchases
			if(lol_event.eventType == "ITEM_PURCHASED") {
				if(lol_event.participantId == blue_adc.id) {
					blue_adc.items[lol_event.timestamp] = lol_event.itemId;
				} else if(lol_event.participantId == red_adc.id) {
					red_adc.items[lol_event.timestamp] = lol_event.itemId;
				}
			}

			// Track Champion Kills, Deaths, and Assists
			else if( lol_event == "CHAMPION_KILL") {
				if(victimId == blue_adc.id) {
					blue_adc.deaths
				}
			}


		}

		blue_stats = frame.participantFrames[blue_adc.id];
		blue_adc.frames[frame.timestamp] = blue_stats;
		red_stats = frame.participantFrames[blue_adc.id];
		red_adc.frames[frame.timestamp] = red_stats;




	}

	info.blue = blue_adc;
	info.red = red_adc;




}