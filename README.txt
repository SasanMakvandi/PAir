Notes for me:
-These flights are not real time
-They do not need to be changed or cancled 
-And no passengers missing trips
Objects:
	1. Customer:
		-6 digit identifier -> int
		-frequent-flyer -> bool (once achieved never lost) basically loyalty stuff
		-miles: qaulifing miles -> int (sum of all flight segments multipied by their unique multiper)
		-all_flight_costs-> touple (tital cost of all flight segments)
	2. Airport:
		-id: three character identifier for each airport
		-map_location: the cordinates for this very speicific airport
	3. Flight Segments:
		-Tracks: .departure and arival airpot
			 .manifest
			 .seat avaliability
			 .bare cost
		-flight_id:
			.represents and alpha-numeric string distinguishig different flights
	4. Trip:
		-several or one flight segment
		-reservation id
		-customer_id
		-flights: every flight segment id
		-if a flight cannot be booked within the time frame, the whole trip gets canceled
	5. Filter:
		-criteration among all the trips and flights
	6. Visualizer and application don't really concern me

		


