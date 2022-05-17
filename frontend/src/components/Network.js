import React, {useState} from 'react'
import axios from 'axios'
import { Card,Grid,TextField,CardHeader,CardContent} from '@mui/material';
import IconButton from '@mui/material/IconButton';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import AddCircleIcon from '@mui/icons-material/AddCircle';

export const Network = () => {
	const [ssid, setSSID] = useState("");
	const [pw, setPW] = useState("");
	const configNetwork = async () => {
	let payload = {
		ssid:ssid,
		password:pw,
	}
    const response = await axios
      .get("/wifi",{params: payload})
      .catch((err) => {
        console.log("Err: ", err);
      });
       if(response === 200){
		   console.log(response.data)
       }
  };

 	return (
		<Grid container spacing={2}>
			<Grid item xs={12} sm={6} md={4}>
			<Card elevation={1}>
					<CardHeader
					action = {
						<HomeRoundedIcon/>
					}
					title="Create Your Environment"
					>
					</CardHeader>

					<CardContent>
					<form onSubmit={configNetwork}>
						<TextField style={{width: "80%"}} id="standard-basic" label="SSID" variant="standard" placeholder="SSID" onChange={e => setSSID(e.target.value)} />
						<TextField style={{width: "80%"}} id="standard-basic" label="Password" variant="standard" placeholder="Password" onChange={e => setPW(e.target.value)} />
						<IconButton variant="primary" type="submit"><AddCircleIcon/></IconButton>
					</form>
					</CardContent>
				</Card>
			</Grid>
		</Grid>
	);
}
