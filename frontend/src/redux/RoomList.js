	const RoomList = () => {
		const fetchPosts = async () => {
			var rooms = [];
			axios.get("http://192.168.1.42:5000/rooms").then((response) => {
				response.data.forEach(element => {
					var roomObj = {};
					console.log(element)
					roomObj.room_name=element.name;
					roomObj.room_id=element.id;
					element.climate_schedule.forEach(climate_schedule => {
						console.log(climate_schedule)
						roomObj.schedule_start_time=climate_schedule.start_time;
						roomObj.schedule_end_time=climate_schedule.end_time;
						climate_schedule.IP.forEach(IP => {
							roomObj.schedule_ip_name=IP.name;
							roomObj.schedule_ip=IP.ip;
						});
					});
					element.climate_interval.forEach(climate_interval => {
						console.log(climate_interval)
						roomObj.interval_start_time=climate_interval.start_time;
						roomObj.interval_end_time=climate_interval.end_time;
						climate_interval.IP.forEach(IP => {
							roomObj.interval_ip_name=IP.name;
							roomObj.interval_ip=IP.ip;
						});
					});
					element.ip.forEach(ip => {
						console.log(ip)
						roomObj.ip = [{
							ip_name: ip.name,
							ip_state: ip.state,
							ip_address: ip.ip,
						}]
					});
					element.climate.forEach(climate => {
						roomObj.name=climate.name;
						roomObj.buffer_parameters=climate.buffer_parameters;
						roomObj.co2_buffer_parameters=climate.co2_buffer_parameters;
						roomObj.co2_parameters=climate.co2_parameters;
						roomObj.humidity_parameters=climate.humidity_parameters;
						roomObj.temperature_parameters=climate.temperature_parameters;
						climate.climate_day_night.forEach(climate_day_night => {
							roomObj.climate_start_time=climate_day_night.climate_start_time;
							roomObj.climate_end_time=climate_day_night.climate_end_time;
						});
					});
					rooms.push(roomObj)
				});
				setRooms(rooms)
			})
			.catch(error => setLoading(false))
		}
		fetchPosts();
	};
	const getIPS = () => {
		const fetchPosts = async () => {
			axios.get("http://192.168.1.42:5000/all_ips").then((response) => {
				console.log(response.data)
				setIPS(response.data)
				setLoading(false);
			})
			.catch(error => setLoading(false))
		}
		fetchPosts();
	};
